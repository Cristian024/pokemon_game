"""
Módulo de modelos del juego Pokémon.
Contiene las clases base: Pokemon, Movimiento y Objeto.
"""

from .pokemon import Pokemon
from .movimiento import Movimiento
from .objeto import Objeto, Pocion, SuperPocion, Revivir

__all__ = ['Pokemon', 'Movimiento', 'Objeto', 'Pocion', 'SuperPocion', 'Revivir']
