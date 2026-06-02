from core.estrategia_evolucion import EstrategiaEvolucion
from models.pokemon import Pokemon

class SinEvolucion(EstrategiaEvolucion):
    """Estrategia para Pokémon que no evolucionan"""
    
    def evolucionar(self, pokemon: 'Pokemon') -> 'Pokemon':
        print(f"{pokemon.nombre} no puede evolucionar.")
        return pokemon