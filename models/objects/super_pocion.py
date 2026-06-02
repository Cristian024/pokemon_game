from ..objeto import Objeto
from ..pokemon import Pokemon

class SuperPocion(Objeto):
    """Súper Poción que cura 50 PS"""
    
    def __init__(self, cantidad: int = 1):
        super().__init__("Súper Poción", "Restaura 50 PS", cantidad)
        self._curacion = 50
    
    def usar(self, pokemon: 'Pokemon') -> bool:
        if not super().usar(pokemon):
            return False
        if pokemon.esta_debilitado:
            print(f"¡{pokemon.nombre} está debilitado! No puede usar la súper poción.")
            return False
        pokemon.curar(self._curacion)
        return True