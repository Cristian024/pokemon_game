
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

