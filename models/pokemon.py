"""
Clase abstracta Pokemon - Clase base para todos los Pokémon
"""

from typing import List
import random
import time
from core.estrategia_evolucion import EstrategiaEvolucion
from models.movimiento import Movimiento

if __name__ == "__main__":
    from movimiento import Movimiento
else:
    from .movimiento import Movimiento


class Pokemon():
    """Clase base abstracta para todos los Pokémon"""
    
    def __init__(self, id_especie: int, nombre: str, nivel: int, tipo: str, 
                 vida_max: int, ataque: int, defensa: int, velocidad: int,
                 es_evolucion: bool, pokemon_evolucionado_id: int | None,
                 estrategia_evolucion: EstrategiaEvolucion, movimientos: List[Movimiento]):
        self._id_especie = id_especie
        self._nombre = nombre
        self._nivel = nivel
        self._tipo = tipo
        self._vida_max = vida_max
        self._vida_actual = vida_max
        self._ataque = ataque
        self._defensa = defensa
        self._velocidad = velocidad
        self._batallas_ganadas = 0
        self._experiencia = 0
        self._es_evolucion = es_evolucion
        self._pokemon_evolucionado_id = pokemon_evolucionado_id
        self._estrategia_evolucion = estrategia_evolucion
        self._movimientos = movimientos
    
    # --- Propiedades ---
    @property
    def id_especie(self) -> int:
        return self._id_especie
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def nivel(self) -> int:
        return self._nivel
    
    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def es_evolucion(self) -> bool:
        return self._es_evolucion
    
    @property
    def vida_actual(self) -> int:
        return self._vida_actual
    
    @property
    def vida_max(self) -> int:
        return self._vida_max
    
    @property
    def velocidad(self) -> int:
        return self._velocidad
    
    @property
    def ataque(self) -> int:
        return self._ataque
    
    @property
    def defensa(self) -> int:
        return self._defensa
    
    @property
    def batallas_ganadas(self) -> int:
        return self._batallas_ganadas
    
    @property
    def experiencia(self) -> int:
        return self._experiencia
    
    @property
    def experiencia_necesaria(self) -> int:
        return self._nivel * 100
    
    @property
    def esta_debilitado(self) -> bool:
        return self._vida_actual <= 0
    
    @property
    def movimientos(self) -> List[Movimiento]:
        return self._movimientos
    

    # --- Métodos principales ---#

    def atacar(self, objetivo: 'Pokemon', movimiento: Movimiento):
        """Realiza un ataque a otro Pokémon"""
        print(f"\n⚔️  {self._nombre} usa {movimiento.nombre}!")
        time.sleep(0.5)
        
        # Calcular daño con fórmula de Pokémon simplificada


        daño_base = ((2 * self._nivel / 5 + 2) * movimiento.poder * (self._ataque / objetivo._defensa)) / 50 + 2
        
        # Multiplicador de tipo
        multiplicador = self._calcular_efectividad(movimiento.tipo, objetivo._tipo)
        daño_final = int(daño_base * multiplicador)
        
        # Variación aleatoria (85% - 100%)
        daño_final = int(daño_final * random.uniform(0.85, 1.0))
        
        if daño_final < 1:
            daño_final = 1
        
        objetivo.recibir_dano(daño_final, multiplicador)
        return daño_final
    
    def recibir_dano(self, dano: int, multiplicador: float):
        """Recibe daño de un ataque"""
        self._vida_actual -= dano
        if self._vida_actual < 0:
            self._vida_actual = 0
        
        mensaje_efectividad = ""
        if multiplicador > 1:
            mensaje_efectividad = " ¡Es súper efectivo!"
        elif multiplicador < 1:
            mensaje_efectividad = " No es muy efectivo..."
        
        print(f" {self._nombre} recibe {dano} de daño!{mensaje_efectividad}")
        print(f"   Vida: {self._vida_actual}/{self._vida_max}")
        
        if self.esta_debilitado:
            print(f"  ¡{self._nombre} se ha debilitado!")
    
    def registrar_victoria(self):
        """Registra una victoria en batalla"""
        self._batallas_ganadas += 1
        self._experiencia += 50
        print(f"\n {self._nombre} gana 50 puntos de experiencia!")
        
        # Subir de nivel si acumula suficiente experiencia


        if self._experiencia >= self.experiencia_necesaria:
            self._subir_nivel()
    
    def _subir_nivel(self):
        """Sube de nivel al Pokémon"""
        self._nivel += 1
        self._experiencia = 0
        self._vida_max += 5
        self._ataque += 2
        self._defensa += 2
        self._velocidad += 1
        self._vida_actual = self._vida_max                              # Recupera vida al subir de nivel
        print(f"⬆️  ¡{self._nombre} ha subido al nivel {self._nivel}!")
    
    def evolucionar(self) -> 'Pokemon':
        """Intenta evolucionar el Pokémon usando su estrategia"""
        return self._estrategia_evolucion.evolucionar(self)
    
    def crear_evolucion(self) -> 'Pokemon':
        """Crea la evolución usando la factory"""
        if(self._pokemon_evolucionado_id):
            return PokemonFactory().crear_pokemon_por_id(self._pokemon_evolucionado_id)
        else:
            return self
    
    def curar(self, cantidad: int):
        """Cura al Pokémon"""
        self._vida_actual = min(self._vida_max, self._vida_actual + cantidad)
        print(f"💚 {self._nombre} recupera {cantidad} PS. Vida: {self._vida_actual}/{self._vida_max}")
    
    def revivir(self):
        """Revive al Pokémon"""
        self._vida_actual = self._vida_max // 2
        print(f"💚 {self._nombre} ha sido revivido con {self._vida_actual} PS!")
    
    def _calcular_efectividad(self, tipo_ataque: str, tipo_defensor: str) -> float:
        """Calcula la efectividad del ataque según los tipos"""
        tabla_tipos = {
            'Fuego': {'Planta': 2.0, 'Agua': 0.5, 'Fuego': 0.5},
            'Agua': {'Fuego': 2.0, 'Planta': 0.5, 'Agua': 0.5},
            'Planta': {'Agua': 2.0, 'Fuego': 0.5, 'Planta': 0.5},
            'Eléctrico': {'Agua': 2.0, 'Planta': 0.5},
            'Normal': {}
        }
        return tabla_tipos.get(tipo_ataque, {}).get(tipo_defensor, 1.0)
    
    def mostrar_estadisticas(self):
        """Muestra las estadísticas del Pokémon"""
        estado = "☠️ DEBILITADO" if self.esta_debilitado else "✅ ACTIVO"
        print(f"\n📊 {self._nombre} (Nv. {self._nivel}) - {self._tipo} - {estado}")
        print(f"   ❤️  Vida: {self._vida_actual}/{self._vida_max}")
        print(f"   ⚔️  Ataque: {self._ataque} | 🛡️  Defensa: {self._defensa} | 💨 Velocidad: {self._velocidad}")
        print(f"   🏅 Batallas ganadas: {self._batallas_ganadas} | ⭐ Experiencia: {self._experiencia}/{self.experiencia_necesaria}")
    
    def __str__(self) -> str:
        return f"{self._nombre} (Nv.{self._nivel} {self._tipo}) - {self._vida_actual}/{self._vida_max} PS"
    
    def mostrar_nombre(self) -> str:
        decorador = ""
        if self.tipo == "Fuego":
            decorador = "🔥"
        elif self.tipo == "Agua":
            decorador = "💧"
        elif self.tipo == "Planta":
            decorador = "🌿"
        elif self.tipo == "Eléctrico":
            decorador = "⚡"
        elif self.tipo == "Normal":
            decorador = "⭐"
        return f"{decorador} {self._nombre} (Nv.{self._nivel})"
