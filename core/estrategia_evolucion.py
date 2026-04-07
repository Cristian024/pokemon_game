
from abc import ABC, abstractmethod
import time

if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from models.pokemon import Pokemon
else:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from models.pokemon import Pokemon


class EstrategiaEvolucion(ABC):
    """Interfaz para las estrategias de evolución de Pokémon"""
    
    @abstractmethod
    def evolucionar(self, pokemon: 'Pokemon') -> 'Pokemon':
        """Método que define cómo evoluciona un Pokémon"""
        pass




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





class SinEvolucion(EstrategiaEvolucion):
    """Estrategia para Pokémon que no evolucionan"""
    
    def evolucionar(self, pokemon: 'Pokemon') -> 'Pokemon':
        print(f"{pokemon.nombre} no puede evolucionar.")
        return pokemon
