"""
Clases de Objetos - Items usables en batalla
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pokemon import Pokemon


class Objeto:
    """Representa un objeto usable en batalla"""
    
    def __init__(self, nombre: str, descripcion: str, cantidad: int = 1):
        self._nombre = nombre
        self._descripcion = descripcion
        self._cantidad = cantidad
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def cantidad(self) -> int:
        return self._cantidad
    
    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    def usar(self, pokemon: 'Pokemon') -> bool:
        """Usa el objeto en un Pokémon, retorna True si se usó correctamente"""
        if self._cantidad <= 0:
            print(f"¡No tienes más {self._nombre}!")
            return False
        
        self._cantidad -= 1
        print(f"\n🎒 Usaste {self._nombre} en {pokemon.nombre}")
        return True
    
    def agregar(self, cantidad: int):
        """Agrega más unidades del objeto"""
        self._cantidad += cantidad
    
    def __str__(self) -> str:
        return f"{self._nombre} x{self._cantidad} - {self._descripcion}"


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
