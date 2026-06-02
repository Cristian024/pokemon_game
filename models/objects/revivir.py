from ..objeto import Objeto
from ..pokemon import Pokemon

class Revivir(Objeto):
    """Revive a un Pokémon debilitado con la mitad de su PS"""
    
    def __init__(self, cantidad: int = 1):
        super().__init__("Revivir", "Revive a un Pokémon con 50% de PS", cantidad)
    
    def usar(self, pokemon: 'Pokemon') -> bool:
        if not super().usar(pokemon):
            return False
        if not pokemon.esta_debilitado:
            print(f"¡{pokemon.nombre} no está debilitado!")
            return False
        pokemon.revivir()
        return True