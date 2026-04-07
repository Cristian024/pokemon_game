# database/repositories/pokemon_repo.py
from database.conexion_mongo import ConexionMongo

class PokemonRepository:
    """Repositorio para interactuar con la colección de especies de Pokémon"""
    
    def __init__(self):
        conexion = ConexionMongo()
        self.db = conexion.obtener_db()
        self.coleccion = self.db["especies_pokemon"]

    def obtener_especies(self) -> list[dict]:
        """
        Obtiene todas las especies de Pokémon.
        Retorna una lista de diccionarios con los datos.
        """
        try:
            datos = self.coleccion.find({}, {"_id": 0})
            return list(datos)
        except Exception as e:
            print(f"Error al consultar las especies en la base de datos: {e}")
            return []

    def obtener_especie(self, id_especie: int) -> dict | None:
        """
        Busca los datos base de un Pokémon por su ID.
        Retorna un diccionario con los datos o None si no existe.
        """
        try:
            datos = self.coleccion.find_one({"id_especie": id_especie})
            
            if datos:
                return datos
            else:
                print(f"Advertencia: Pokémon con ID {id_especie} no encontrado en la base de datos.")
                return None
                
        except Exception as e:
            print(f"Error al consultar la especie en la base de datos: {e}")
            return None