import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("DATABASE_URL")

try:
    engine = create_engine(url)
    connection = engine.connect()
    print("✅ ¡Conexión exitosa a Supabase!")
    connection.close()
except Exception as e:
    print(f"❌ Error de conexión: {e}")