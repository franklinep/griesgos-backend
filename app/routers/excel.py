# app/routers/excel.py
from fastapi import APIRouter, UploadFile, File
import os
from app.loaders.load_data import process_excel

router = APIRouter(prefix="/api/excel", tags=["excel"])

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    try:
        # Validar extensión
        if not file.filename.endswith(('.xlsx', '.xls')):
            return {
                "success": False,
                "message": "Formato no válido. Solo se permiten archivos Excel (.xlsx, .xls)"
            }

        # Crear directorio si no existe
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{file.filename}"

        # Guardar archivo
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Procesar Excel
        process_excel(file_path)

        return {
            "success": True,
            "message": "Archivo procesado correctamente",
            "filename": file.filename
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error al procesar archivo: {str(e)}"
        }