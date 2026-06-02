from ..objeto import Objeto
from ..pokemon import Pokemon

class Pocion(Objeto):
    """Poción que cura 20 PS"""
    
    def __init__(self, cantidad: int = 1):
        super().__init__("Poción", "Restaura 20 PS", cantidad)
        self._curacion = 20
    
    def usar(self, pokemon: 'Pokemon') -> bool:
        if not super().usar(pokemon):
            return False
        if pokemon.esta_debilitado:
            print(f"¡{pokemon.nombre} está debilitado! No puede usar la poción.")
            return False
        pokemon.curar(self._curacion)
        return True