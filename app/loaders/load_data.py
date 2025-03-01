# app/loaders/load_data.py
import socket
import os
import pandas as pd
import logging
from datetime import datetime
from typing import Dict
from app.models.estructura_org import Unidad, Area, Puesto, Categoria
from app.models.persona import Persona
from app.models.persona_trabajador import PersonaTrabajador
from app.loaders.database import SessionLocal

def get_import_audit_data() -> dict:
    """Retorna los datos de auditoría para el proceso de importación."""
    return {
        'i_est_registro': 1,
        'v_usu_reg': 'system',
        'v_usu_mod': None,
        't_fec_reg': datetime.now(),
        't_fec_mod': None,
        'v_host_reg': socket.gethostname(),  # Obtiene el hostname real del servidor
        'v_host_mod': None,
        'v_ip_reg': socket.gethostbyname(socket.gethostname()),  # IP real del servidor
        'v_ip_mod': None
    }

def setup_logger():
    # Crear la ruta absoluta para el directorio de logs
    log_dir = os.path.join('C:\Griesgosapi\logs')
    log_file = os.path.join(log_dir, 'data_loader.log')
    
    # Asegurar que el directorio existe
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger('data_loader')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    handlers = [
        logging.FileHandler('data_loader.log'),
        logging.StreamHandler()
    ]
    
    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

logger = setup_logger()

def check_null_values(df: pd.DataFrame, required_cols: list) -> None:
    """Verifica valores nulos en columnas requeridas y los registra en el log."""
    for col in required_cols:
        null_rows = df[df[col].isna()]
        if not null_rows.empty:
            logger.warning(f"Columna {col} tiene {len(null_rows)} valores nulos:")
            for idx, row in null_rows.iterrows():
                logger.warning(f"----------> ID Persona: {row.get('ID de persona', 'No ID')} en fila {idx + 1}")

def get_or_create_master_data(db: SessionLocal, df: pd.DataFrame) -> Dict:
    """Crea o recupera datos maestros (unidades, áreas, puestos, categorías)."""
    master_data = {'unidad': {}, 'area': {}, 'puesto': {}, 'categoria': {}}
    model_map = {
        'unidad': (Unidad, 'Subdivisión de personal (Nombre de Subdivisión de personal)'),
        'categoria': (Categoria, 'Área de personal (Picklist Label)'),
        'puesto': (Puesto, 'Position Posición (Label)'),
        'area': (Area, 'Position Centro de costo (Código de centro de costos)')
    }
    
    audit_data = get_import_audit_data()
    
    # Primero procesamos las unidades
    try:
        unidad_model, unidad_column = model_map['unidad']
        unique_unidades = df[unidad_column].dropna().unique()
        
        for value in unique_unidades:
            name = str(value).strip()
            if not name:
                continue

            unidad = db.query(unidad_model).filter(unidad_model.v_des_nombre == name).first()
            if not unidad:
                unidad = unidad_model(
                    v_des_nombre=name,
                    **audit_data
                )
                db.add(unidad)
                db.flush()
            
            master_data['unidad'][name] = unidad.i_cod_unidad
        
        db.commit()
        logger.info(f"Procesadas unidades: {len(unique_unidades)} registros")
        
    except Exception as e:
        logger.error(f"Error procesando unidades: {str(e)}")
        db.rollback()
        return master_data

    # Luego procesamos el resto de entidades
    for data_type, (model, column) in model_map.items():
        if data_type == 'unidad':  # Ya procesado
            continue
            
        try:
            unique_values = df[column].dropna().unique()
            for value in unique_values:
                try:
                    name = str(value).strip()
                    if not name:
                        continue

                    item = db.query(model).filter(model.v_des_nombre == name).first()
                    if not item:
                        # Para áreas, necesitamos asignar una unidad
                        if data_type == 'area':
                            # Obtener la unidad correspondiente de la misma fila
                            unidad_name = df[df[column] == value][model_map['unidad'][1]].iloc[0]
                            unidad_id = master_data['unidad'].get(str(unidad_name).strip())
                            
                            item = model(
                                v_des_nombre=name,
                                i_cod_unidad=unidad_id,  # Asignar la unidad correspondiente
                                **audit_data
                            )
                        else:
                            item = model(
                                v_des_nombre=name,
                                **audit_data
                            )
                        
                        db.add(item)
                        db.flush()

                    id_field = f'i_cod_{data_type}'
                    master_data[data_type][name] = getattr(item, id_field)
                    
                except Exception as e:
                    logger.error(f"Error procesando {data_type} '{name}': {str(e)}")
            
            db.commit()
            logger.info(f"Procesados datos maestros de {data_type}: {len(unique_values)} registros")
            
        except Exception as e:
            logger.error(f"Error en procesamiento de {data_type}: {str(e)}")
            db.rollback()
            
    return master_data

def process_excel(file_path: str) -> None:
    """Procesa el archivo Excel y carga los datos en la base de datos."""
    required_cols = [
        'ID de persona', 'Numero documento', 'Nombres', 'Primer apellido',
        'Fecha de ingreso', 'Subdivisión de personal (Nombre de Subdivisión de personal)',
        'Área de personal (Picklist Label)', 'Position Posición (Label)',
        'Position Centro de costo (Código de centro de costos)'
    ]
    
    stats = {
        'procesados': 0,
        'omitidos': 0,
        'errores': [],
    }
    
    try:
        logger.info(f"Iniciando procesamiento de {file_path}")
        
        # Leer Excel
        try:
            df = pd.read_excel(file_path)
            logger.info(f"Excel leído correctamente: {len(df)} filas encontradas")
        except Exception as e:
            logger.critical(f"Error al leer Excel: {str(e)}")
            return
            
        # Verificar columnas requeridas
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.critical(f"Columnas faltantes: {', '.join(missing_cols)}")
            return
            
        check_null_values(df, required_cols)
        
        db = SessionLocal()
        audit_data = get_import_audit_data()
        
        try:
            # Procesar datos maestros
            master_data = get_or_create_master_data(db, df)
            
            # Procesar cada fila del Excel
            for idx, row in df.iterrows():
                try:
                    # Validar documento
                    if pd.isna(row['Numero documento']):
                        raise ValueError("Número de documento es nulo")
                    
                    documento = str(row['Numero documento']).strip()
                    
                    # Verificar si la persona ya existe
                    existing_persona = db.query(Persona).filter(
                        Persona.v_num_documento == documento
                    ).first()
                    
                    if existing_persona:
                        logger.warning(f"Persona con documento {documento} ya existe - Omitiendo")
                        stats['omitidos'] += 1
                        continue
                    
                    # Crear nueva persona
                    new_persona = Persona(
                        v_num_documento=documento,
                        v_des_nombres=str(row['Nombres']).strip(),
                        v_des_apellidos=str(row['Primer apellido']).strip(),
                        v_cod_empresa=str(row['ID de persona']).zfill(8),
                        **audit_data
                    )
                    
                    db.add(new_persona)
                    db.flush()
                    
                    # Procesar fecha de ingreso
                    fecha_ingreso = None
                    if pd.notna(row['Fecha de ingreso']):
                        try:
                            fecha_ingreso = pd.to_datetime(row['Fecha de ingreso'])
                        except Exception as e:
                            logger.warning(f"Error en fecha para documento {documento}: {str(e)}")
                    
                    # Crear registro de trabajador
                    new_trabajador = PersonaTrabajador(
                        i_cod_persona=new_persona.i_cod_persona,
                        i_cod_unidad=master_data['unidad'].get(
                            str(row['Subdivisión de personal (Nombre de Subdivisión de personal)']).strip()
                        ),
                        i_cod_categoria=master_data['categoria'].get(
                            str(row['Área de personal (Picklist Label)']).strip()
                        ),
                        i_cod_puesto=master_data['puesto'].get(
                            str(row['Position Posición (Label)']).strip()
                        ),
                        i_cod_area=master_data['area'].get(
                            str(row['Position Centro de costo (Código de centro de costos)']).strip()
                        ),
                        t_fec_ingreso=fecha_ingreso or datetime.now(),
                        **audit_data
                    )
                    
                    db.add(new_trabajador)
                    stats['procesados'] += 1
                    
                    # Commit cada 100 registros
                    if stats['procesados'] % 100 == 0:
                        db.commit()
                        logger.info(f"Procesados {stats['procesados']} registros")
                    
                except Exception as e:
                    stats['errores'].append(f"Error en fila {idx + 1}: {str(e)}")
                    logger.error(f"Error procesando fila {idx + 1}: {str(e)}")
                    db.rollback()
                    continue
            
            # Commit final
            db.commit()
            logger.info("Procesamiento completado exitosamente")
            
        except Exception as e:
            logger.critical(f"Error en el procesamiento: {str(e)}")
            db.rollback()
        
        finally:
            # Registrar estadísticas finales
            logger.info(f"""
Resumen de importación:
- Registros procesados exitosamente: {stats['procesados']}
- Registros omitidos: {stats['omitidos']}
- Errores encontrados: {len(stats['errores'])}
            """)
            
            if stats['errores']:
                logger.warning("Primeros 10 errores encontrados:")
                for error in stats['errores'][:10]:
                    logger.error(error)
                if len(stats['errores']) > 10:
                    logger.warning(f"...y {len(stats['errores']) - 10} errores más")
            
            db.close()
            
    except Exception as e:
        logger.critical(f"Error fatal en el proceso: {str(e)}")