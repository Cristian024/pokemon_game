"""
Clase Entrenador - Representa al jugador/entrenador Pokémon
"""

from typing import List, Optional

if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from models.pokemon import Pokemon
    from models.objeto import Pocion, SuperPocion, Revivir, Objeto
else:
    from models.pokemon import Pokemon
    from models.objeto import Pocion, SuperPocion, Revivir, Objeto


class Entrenador:
    """Representa al jugador/entrenador Pokémon"""
    
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._pokedex: List[Pokemon] = []  # Colección completa (HU1)
        self._equipo: List[Pokemon] = []   # Equipo activo (HU2)
        self._inventario: List[Objeto] = []  # Objetos (HU7)
        self._inicializar_objetos()
    
    def _inicializar_objetos(self):
        """Inicializa el inventario con objetos básicos"""
        self._inventario.append(Pocion(5))
        self._inventario.append(SuperPocion(2))
        self._inventario.append(Revivir(1))
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def equipo(self) -> List[Pokemon]:
        return self._equipo
    
    @property
    def pokedex(self) -> List[Pokemon]:
        return self._pokedex
    
    @property
    def inventario(self) -> List[Objeto]:
        return self._inventario
    
    # --- Gestión de Pokémon (HU1, HU2) ---
    def capturar_pokemon(self, pokemon: Pokemon):
        """Captura un Pokémon y lo agrega a la colección"""
        self._pokedex.append(pokemon)
        print(f"\n ¡{pokemon.nombre} ha sido capturado!")
        
        # Agregar al equipo si hay espacio (máximo 6)
        if len(self._equipo) < 6:
            self._equipo.append(pokemon)
            print(f"   {pokemon.nombre} se ha unido a tu equipo.")
        else:
            print(f"   {pokemon.nombre} fue enviado al PC.")
    
    def agregar_a_equipo(self, pokemon: Pokemon):
        """Agrega un Pokémon del PC al equipo"""
        if pokemon in self._pokedex and pokemon not in self._equipo:
            if len(self._equipo) < 6:
                self._equipo.append(pokemon)
                print(f"\n {pokemon.nombre} ha sido agregado al equipo.")
            else:
                print("\n Tu equipo está completo (6/6).")
        else:
            print("\n El Pokémon no está en tu colección o ya está en el equipo.")
    
    def remover_de_equipo(self, pokemon: Pokemon):
        """Remueve un Pokémon del equipo (lo envía al PC)"""
        if pokemon in self._equipo:
            self._equipo.remove(pokemon)
            print(f"\n {pokemon.nombre} ha sido enviado al PC.")
        else:
            print("\n El Pokémon no está en tu equipo.")
    
    def tiene_pokemon_activos(self) -> bool:
        """Verifica si tiene Pokémon que puedan combatir"""
        return any(not p.esta_debilitado for p in self._equipo)
    
    def obtener_pokemon_activo(self) -> Optional[Pokemon]:
        """Obtiene el primer Pokémon no debilitado del equipo"""
        for pokemon in self._equipo:
            if not pokemon.esta_debilitado:
                return pokemon
        return None
    
    # --- Gestión de objetos (HU7) ---
    def mostrar_inventario(self):
        """Muestra el inventario de objetos"""
        print(f"\n🎒 Inventario de {self._nombre}:")
        for i, objeto in enumerate(self._inventario, 1):
            print(f"   {i}. {objeto}")
    
    def usar_objeto(self, indice: int, pokemon: Pokemon) -> bool:
        """Usa un objeto del inventario en un Pokémon"""
        if 0 <= indice < len(self._inventario):
            return self._inventario[indice].usar(pokemon)
        print(" Objeto inválido.")
        return False
    
    def obtener_objetos_usables(self) -> List[Objeto]:
        """Obtiene los objetos que tienen cantidad > 0"""
        return [obj for obj in self._inventario if obj.cantidad > 0]
    
    # --- Información ---
    def mostrar_equipo(self):
        """Muestra el equipo actual"""
        print(f"\n👥 Equipo de {self._nombre}:")
        for i, pokemon in enumerate(self._equipo, 1):
            estado = "💀" if pokemon.esta_debilitado else "✅"
            print(f"   {i}. {estado} {pokemon}")
    
    def mostrar_pokedex(self):
        """Muestra la colección completa"""
        print(f"\n📱 Pokédex de {self._nombre} ({len(self._pokedex)} Pokémon):")
        for i, pokemon in enumerate(self._pokedex, 1):
            en_equipo = "👥" if pokemon in self._equipo else "💻"
            print(f"   {i}. {en_equipo} {pokemon.nombre} ({pokemon.tipo}) - Nv.{pokemon.nivel}")
