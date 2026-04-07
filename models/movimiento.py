"""
Clase Movimiento - Representa un ataque/movimiento de Pokémon
"""


class Movimiento:
    """Representa un movimiento/ataque de Pokémon"""
    
    def __init__(self, nombre: str, tipo: str, poder: int, pp: int):
        self._nombre = nombre
        self._tipo = tipo
        self._poder = poder
        self._pp_max = pp
        self._pp_actual = pp
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def tipo(self) -> str:
        return self._tipo
    
    @property
    def poder(self) -> int:
        return self._poder
    
    @property
    def pp_actual(self) -> int:
        return self._pp_actual
    
    @property
    def pp_max(self) -> int:
        return self._pp_max
    
    def usar(self) -> bool:
        """Usa el movimiento, retorna True si se pudo usar"""
        if self._pp_actual > 0:
            self._pp_actual -= 1
            return True
        return False
    
    def __str__(self) -> str:
        return f"{self._nombre} ({self._tipo}) - Poder: {self._poder} | PP: {self._pp_actual}/{self._pp_max}"
