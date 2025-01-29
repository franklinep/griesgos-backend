# app/test/test_connection.py
from sqlalchemy import create_engine, text
import urllib

def test_database_connection():
    try:
        params = urllib.parse.quote_plus(
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-7AMS20K;"
            "DATABASE=GRiesgosDB;"
            "Trusted_Connection=yes;"
        )

        SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        
        with engine.connect() as connection:
            print("¡Conexión exitosa! ✅")
            print(f"Conectado a: {connection.engine.url}")
            
            # Usar text() para las consultas SQL
            version = connection.execute(text("SELECT @@VERSION")).fetchone()
            print("\nVersión de SQL Server:")
            print(version[0])
            
            # Verificar la base de datos actual
            db_name = connection.execute(text("SELECT DB_NAME()")).fetchone()
            print(f"\nBase de datos actual: {db_name[0]}")
            
    except Exception as e:
        print("❌ Error de conexión:")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_database_connection()