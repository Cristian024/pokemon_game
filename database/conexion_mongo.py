# database/conexion.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()

class ConexionMongo:
    """Implementación del patrón Singleton para la conexión a MongoDB usando .env"""
    
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexionMongo, cls).__new__(cls)
            
            uri = os.getenv("MONGO_URI")
            nombre_db = os.getenv("MONGO_DB_NAME")
            
            try:
                cls._instancia.cliente = MongoClient(uri)
                cls._instancia.db = cls._instancia.cliente[nombre_db]
            except ConnectionFailure as e:
                print(f"Error crítico conectando a MongoDB: {e}")
                
        return cls._instancia

    def obtener_db(self):
        """Retorna el objeto de la base de datos"""
        return self.db