from core.estrategia_evolucion import EstrategiaEvolucion
from models.pokemon import Pokemon
import time

class EvolucionPorBatallas(EstrategiaEvolucion):
    """Estrategia de evolución basada en batallas ganadas"""
    
    def __init__(self, batallas_necesarias: int = 3):
        self._batallas_necesarias = batallas_necesarias
    
    def evolucionar(self, pokemon: 'Pokemon') -> 'Pokemon':
        if pokemon.batallas_ganadas >= self._batallas_necesarias:
            print(f"\n ¡{pokemon.nombre} está evolucionando! ")
            time.sleep(1)
            pokemon_evolucionado = pokemon.crear_evolucion()
            print(f" ¡{pokemon.nombre} ha evolucionado a {pokemon_evolucionado.nombre}! \n")
            return pokemon_evolucionado
        else:
            batallas_faltantes = self._batallas_necesarias - pokemon.batallas_ganadas
            print(f"{pokemon.nombre} necesita {batallas_faltantes} batallas más para evolucionar.")
            return pokemon
    
    @property
    def batallas_necesarias(self) -> int:
        return self._batallas_necesarias