
from typing import Optional
import random
import time

if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from models.pokemon import Pokemon
    from models.movimiento import Movimiento
    from models.entrenador import Entrenador
else:
    from models.pokemon import Pokemon
    from models.movimiento import Movimiento
    from models.entrenador import Entrenador


class SistemaDeBatalla:
    
    
    def __init__(self, entrenador: Entrenador):
        self._entrenador = entrenador
        self._oponente: Optional[Pokemon] = None
        self._turno = 1
        self._en_batalla = False
    
    def iniciar_batalla(self, oponente: Pokemon) -> bool:
        """Inicia una batalla contra un Pokémon salvaje"""
        self._oponente = oponente
        self._turno = 1
        self._en_batalla = True
        
        print("\n" + "=" * 50)
        print("⚔️  ¡HA APARECIDO UN POKÉMON SALVAJE! ⚔️")
        print("=" * 50)
        print(f"\n🐾 {oponente.nombre} (Nv.{oponente.nivel} {oponente.tipo})")
        print(f"   Vida: {oponente.vida_actual}/{oponente.vida_max}")
        
        pokemon_activo = self._entrenador.obtener_pokemon_activo()
        if pokemon_activo:
            print(f"\n👤 ¡Adelante, {pokemon_activo.nombre}!")
        else:
            print("\n❌ ¡No tienes Pokémon que puedan combatir!")
            return False
        
        return True
    
    def ejecutar_turno(self, accion: str, indice_movimiento: int = 0, indice_objeto: int = 0) -> str:
        
        """
        Ejecuta un turno de batalla
        Retorna: 'continuar', 'victoria', 'derrota', 'capturado', 'huir'
        """

        if not self._en_batalla or not self._oponente:
            return 'terminada'
        
        pokemon_jugador = self._entrenador.obtener_pokemon_activo()
        if not pokemon_jugador:
            return 'derrota'
        
        print(f"\n{'─' * 50}")
        print(f" TURNO {self._turno}")
        print(f"{'─' * 50}")
        
        # Determinar orden de ataque según velocidad 


        jugador_primero = pokemon_jugador.velocidad >= self._oponente.velocidad
        
        if accion == 'atacar':
            return self._ejecutar_ataque(pokemon_jugador, indice_movimiento, jugador_primero)
        
        elif accion == 'objeto':
            return self._usar_objeto(pokemon_jugador, indice_objeto, jugador_primero)
        
        elif accion == 'capturar':
            return self._intentar_captura(pokemon_jugador)
        
        elif accion == 'huir':
            print("\n🏃 ¡Has huido de la batalla!")
            self._en_batalla = False
            return 'huir'
        
        return 'continuar'
    
    def _ejecutar_ataque(self, pokemon_jugador: Pokemon, indice_movimiento: int, jugador_primero: bool) -> str:
        """Ejecuta un ataque de ambos Pokémon"""
        movimientos = pokemon_jugador.movimientos
        
        if indice_movimiento < 0 or indice_movimiento >= len(movimientos):
            print("Movimiento inválido.")
            return 'continuar'
        
        movimiento_jugador = movimientos[indice_movimiento]
        
        if movimiento_jugador.pp_actual <= 0:
            print(f"❌ ¡{movimiento_jugador.nombre} no tiene PP!")
            return 'continuar'
        


        # Turno del jugador o oponente según velocidad


        if jugador_primero:
            # Jugador ataca primero
            movimiento_jugador.usar()
            pokemon_jugador.atacar(self._oponente, movimiento_jugador)
            
            if self._oponente.esta_debilitado:
                return self._finalizar_victoria(pokemon_jugador)
            
            # Oponente contraataca
            self._oponente_ataca(pokemon_jugador)
        else:
            # Oponente ataca primero
            self._oponente_ataca(pokemon_jugador)
            
            if pokemon_jugador.esta_debilitado:
                if not self._entrenador.tiene_pokemon_activos():
                    return self._finalizar_derrota()
                return 'continuar'
            
            # Jugador contraataca
            movimiento_jugador.usar()
            pokemon_jugador.atacar(self._oponente, movimiento_jugador)
            
            if self._oponente.esta_debilitado:
                return self._finalizar_victoria(pokemon_jugador)
        
        self._turno += 1
        return 'continuar'
    
    def _oponente_ataca(self, pokemon_jugador: Pokemon):
        """El oponente realiza un ataque aleatorio"""
        movimientos_oponente = self._oponente.movimientos
        movimiento = random.choice(movimientos_oponente)
        
        # Verificar PP
        if movimiento.pp_actual <= 0:
            # Si no tiene PP, usa un ataque básico
            movimiento = Movimiento("Ataque Básico", "Normal", 20, 999)
        else:
            movimiento.usar()
        
        print(f"\n ¡El {self._oponente.nombre} salvaje te ataca!")
        self._oponente.atacar(pokemon_jugador, movimiento)
    
    def _usar_objeto(self, pokemon_jugador: Pokemon, indice_objeto: int, jugador_primero: bool) -> str:
        """Usa un objeto durante la batalla"""
        objetos_usables = self._entrenador.obtener_objetos_usables()
        
        if indice_objeto < 0 or indice_objeto >= len(objetos_usables):
            print(" Objeto inválido.")
            return 'continuar'
        
        # Usar objeto (no consume turno completo, pero el oponente puede atacar)

        indice_real = self._entrenador.inventario.index(objetos_usables[indice_objeto])
        self._entrenador.usar_objeto(indice_real, pokemon_jugador)
        
        # El oponente ataca después de usar objeto
        
        if not jugador_primero or random.random() > 0.5:
            self._oponente_ataca(pokemon_jugador)
            if pokemon_jugador.esta_debilitado:
                if not self._entrenador.tiene_pokemon_activos():
                    return self._finalizar_derrota()
        
        self._turno += 1
        return 'continuar'
    
    def _intentar_captura(self, pokemon_jugador: Pokemon) -> str:
        """Intenta capturar al Pokémon oponente"""
        # Fórmula de captura simplificada
        vida_restante = self._oponente.vida_actual / self._oponente.vida_max
        probabilidad = (1 - vida_restante) * 0.6  # Más débil = más fácil de capturar
        
        print(f"\n🎯 ¡Lanzaste una Pokéball!")
        time.sleep(0.5)
        print("   ¡Ding-ding-ding...!")
        time.sleep(0.5)
        
        if random.random() < probabilidad:
            print("   ¡...clic!")
            time.sleep(0.5)
            print(f"\n✅ ¡{self._oponente.nombre} ha sido capturado!")
            
            # Crear copia del oponente para el jugador
            pokemon_capturado = self._crear_copia_pokemon(self._oponente)
            self._entrenador.capturar_pokemon(pokemon_capturado)
            
            self._en_batalla = False
            return 'capturado'
        else:
            print("   ¡El Pokémon escapó!")
            # El oponente ataca
            self._oponente_ataca(pokemon_jugador)
            if pokemon_jugador.esta_debilitado:
                if not self._entrenador.tiene_pokemon_activos():
                    return self._finalizar_derrota()
            
            self._turno += 1
            return 'continuar'
    
    def _crear_copia_pokemon(self, original: Pokemon) -> Pokemon:
        """Crea una copia de un Pokémon para el jugador"""
        from core.pokemon_factory import PokemonFactory
        return PokemonFactory().crear_pokemon_por_id(original.id_especie)
    
    def _finalizar_victoria(self, pokemon_ganador: Pokemon) -> str:
        """Finaliza la batalla con victoria"""
        print("\n" + "=" * 50)
        print("🏆 ¡VICTORIA! 🏆")
        print("=" * 50)
        
        # Registrar victoria y experiencia (HU4)
        pokemon_ganador.registrar_victoria()
        
        # Intentar evolucionar (HU5, HU6)
        pokemon_evolucionado = pokemon_ganador.evolucionar()
        if pokemon_evolucionado != pokemon_ganador:
            # Reemplazar en el equipo
            idx = self._entrenador.equipo.index(pokemon_ganador)
            self._entrenador.equipo[idx] = pokemon_evolucionado
            # También en la pokedex
            if pokemon_ganador in self._entrenador.pokedex:
                pokedex_idx = self._entrenador.pokedex.index(pokemon_ganador)
                self._entrenador.pokedex[pokedex_idx] = pokemon_evolucionado
        
        self._en_batalla = False
        return 'victoria'
    
    def _finalizar_derrota(self) -> str:
        """Finaliza la batalla con derrota"""
        print("\n" + "=" * 50)
        print("💀 ¡DERROTA! 💀")
        print("=" * 50)
        print("Todos tus Pokémon han sido debilitados...")
        print("Te has quedado sin Pokémon que puedan combatir.")
        
        self._en_batalla = False
        return 'derrota'
    
    def mostrar_estado_batalla(self):
        """Muestra el estado actual de la batalla"""
        pokemon_jugador = self._entrenador.obtener_pokemon_activo()
        
        print(f"\n📊 ESTADO DE LA BATALLA:")
        print(f"   🐾 {self._oponente.nombre}: {self._oponente.vida_actual}/{self._oponente.vida_max} PS")
        if pokemon_jugador:
            print(f"   👤 {pokemon_jugador.nombre}: {pokemon_jugador.vida_actual}/{pokemon_jugador.vida_max} PS")
    
    def mostrar_opciones(self):
        """Muestra las opciones de batalla"""
        pokemon_jugador = self._entrenador.obtener_pokemon_activo()
        
        print(f"\n🎮 OPCIONES:")
        print(f"   1. ⚔️  Atacar")
        print(f"   2. 🎒 Usar Objeto")
        print(f"   3. 🎯 Capturar")
        print(f"   4. 🏃 Huir")
    
    @property
    def en_batalla(self) -> bool:
        return self._en_batalla
    
    @property
    def oponente(self) -> Optional[Pokemon]:
        return self._oponente
    
    @property
    def turno(self) -> int:
        return self._turno
