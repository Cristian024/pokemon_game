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

