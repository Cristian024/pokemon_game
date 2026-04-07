"""
Consola - Juego principal de Pokémon por consola
"""

from typing import Optional
import random
import time

if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from models.entrenador import Entrenador
    from core.sistema_batalla import SistemaDeBatalla
    from core.pokemon_factory import PokemonFactory
    from database.repositories.pokemon_repository import PokemonRepository
else:
    from models.entrenador import Entrenador
    from core.sistema_batalla import SistemaDeBatalla
    from core.pokemon_factory import PokemonFactory
    from database.repositories.pokemon_repository import PokemonRepository


class Consola:
    """Juego principal de Pokémon por consola"""
    
    def __init__(self):
        self._pokemon_repository = PokemonRepository()
        self._pokemones: list[dict] = []
        for pokemonbase in self._pokemon_repository.obtener_especies():
            self._pokemones.append(PokemonFactory().crear_pokemon_por_base(datos_base=pokemonbase))
        self._entrenador: Optional[Entrenador] = None
        self._batalla: Optional[SistemaDeBatalla] = None
        self._ejecutando = False
    
    def iniciar(self):
        """Inicia el juego"""
        self._mostrar_titulo()
        self._crear_entrenador()
        self._elegir_pokemon_inicial()
        self._ejecutando = True
        self._bucle_principal()
    
    def _mostrar_titulo(self):
        """Muestra el título del juego"""
        print("\n" + "=" * 60)
        print("  ⚡ 🌿 🔥  POKÉMON - CONSOLE EDITION  🔥 🌿 ⚡")
        print("=" * 60)
       
    
    def _crear_entrenador(self):
        """Crea al entrenador jugador"""
        print("\n👤 ¡Bienvenido al mundo Pokémon!")
        
        nombre = input("\n¿Cuál es tu nombre, entrenador? ").strip()
        if not nombre:
            nombre = "Ash"
        self._entrenador = Entrenador(nombre)
        print(f"\n✅ ¡Bienvenido, {nombre}! ¡Tu aventura Pokémon comienza ahora!")
    
    def _elegir_pokemon_inicial(self):
        """Permite elegir el Pokémon inicial"""

        pokemones_por_tipo = {}
        for p in self._pokemones:
            tipo_principal = p.tipo
            es_evolucion = p.es_evolucion
            
            if tipo_principal not in pokemones_por_tipo:
                pokemones_por_tipo[tipo_principal] = []
            
            if not es_evolucion:
                pokemones_por_tipo[tipo_principal].append(p)
            
        tipos_disponibles = list(pokemones_por_tipo.keys())

        tipo_elegido = None
        while True:
            print("\n🌟 Selecciona el TIPO de tu Pokémon inicial:")
            for i, tipo in enumerate(tipos_disponibles, 1):
                print(f"   {i}. {tipo}")
                
            opcion_tipo = input(f"\nElige un tipo (1-{len(tipos_disponibles)}): ").strip()
            
            if opcion_tipo.isdigit() and 1 <= int(opcion_tipo) <= len(tipos_disponibles):
                tipo_elegido = tipos_disponibles[int(opcion_tipo) - 1]
                break
            else:
                print("❌ Opción inválida. Intenta de nuevo.")

        pokemones_filtrados = pokemones_por_tipo[tipo_elegido]
        
        while True:
            print(f"\n🎁 Pokémon disponibles de tipo {tipo_elegido}:")
            for i, p in enumerate(pokemones_filtrados, 1):
                print(f"   {i}. {p.mostrar_nombre()}")
                
            opcion_poke = input(f"\nElige tu compañero (1-{len(pokemones_filtrados)}): ").strip()
            
            if opcion_poke.isdigit() and 1 <= int(opcion_poke) <= len(pokemones_filtrados):
                pokemon = pokemones_filtrados[int(opcion_poke) - 1]
                
                self._entrenador.capturar_pokemon(pokemon)
                break
            else:
                print("❌ Opción inválida. Intenta de nuevo.")
    
    def _bucle_principal(self):
        """Bucle principal del juego"""
        while self._ejecutando:
            self._mostrar_menu_principal()
            opcion = input("\nElige una opción: ").strip()
            self._procesar_opcion(opcion)
    
    def _mostrar_menu_principal(self):
        """Muestra el menú principal"""
        print("\n" + "=" * 50)
        print("  📋 MENÚ PRINCIPAL")
        print("=" * 50)
        print("   1. Buscar Pokémon salvaje")
        print("   2. Ver mi equipo")
        print("   3. Ver Pokédex")
        print("   4. Ver inventario")
        print("   5. Ver estadísticas")
        print("   6. Salir")
    
    def _procesar_opcion(self, opcion: str):
        """Procesa la opción del menú"""
        if opcion == "1":
            self._buscar_pokemon_salvaje()
        elif opcion == "2":
            self._entrenador.mostrar_equipo()
        elif opcion == "3":
            self._entrenador.mostrar_pokedex()
        elif opcion == "4":
            self._entrenador.mostrar_inventario()
        elif opcion == "5":
            self._mostrar_estadisticas_detalladas()
        elif opcion == "6":
            self._salir()
        else:
            print(" Opción inválida. Intenta de nuevo.")
    
    def _buscar_pokemon_salvaje(self):
        """Busca un Pokémon salvaje para combatir"""
        if not self._entrenador.tiene_pokemon_activos():
            print("\n ¡No tienes Pokémon que puedan combatir! Ve a curarlos primero.")
            return
        
        print("\n🔍 Buscando Pokémon salvaje...")
        time.sleep(1)
        
        # Generar Pokémon salvaje aleatorio
        pokemones = []
        for pokemonbase in self._pokemon_repository.obtener_especies():
            pokemones.append(PokemonFactory().crear_pokemon_por_base(datos_base=pokemonbase))
        pokemon_salvaje = random.choice(pokemones)
        pokemon_salvaje._nivel = random.randint(3, 10)  # Nivel aleatorio
        
        # Iniciar batalla
        self._batalla = SistemaDeBatalla(self._entrenador)
        if self._batalla.iniciar_batalla(pokemon_salvaje):
            self._bucle_batalla()
    
    def _bucle_batalla(self):

        """Bucle de la batalla"""

        while self._batalla and self._batalla.en_batalla:
            self._batalla.mostrar_estado_batalla()
            self._batalla.mostrar_opciones()
            
            accion = input("\n¿Qué harás? (1-4): ").strip()
            
            if accion == "1":                          # Atacar
                self._seleccionar_ataque()
            elif accion == "2":                        # Usar objeto
                self._seleccionar_objeto()
            elif accion == "3":                          # Capturar
                resultado = self._batalla.ejecutar_turno('capturar')
                if resultado != 'continuar':
                    break
            elif accion == "4":                             # Huir
                self._batalla.ejecutar_turno('huir')
                break
            else:
                print(" Opción inválida.")
    
    def _seleccionar_ataque(self):
        """Permite seleccionar un ataque"""
        pokemon_activo = self._entrenador.obtener_pokemon_activo()
        if not pokemon_activo:
            return
        
        print(f"\n  Selecciona un movimiento:")
        for i, mov in enumerate(pokemon_activo.movimientos, 1):
            print(f"   {i}. {mov}")
        
        try:
            opcion = int(input("\nMovimiento (número): ")) - 1
            resultado = self._batalla.ejecutar_turno('atacar', indice_movimiento=opcion)
            
            if resultado == 'victoria':
                print("\n ¡Ganaste la batalla!")
            elif resultado == 'derrota':
                print("\n Has perdido la batalla...")
                self._ofrecer_curacion()
        except ValueError:
            print(" Opción inválida.")
    
    def _seleccionar_objeto(self):

        """Permite seleccionar un objeto"""

        objetos = self._entrenador.obtener_objetos_usables()
        
        if not objetos:
            print(" ¡No tienes objetos!")
            return
        
        print(f"\n Selecciona un objeto:")
        for i, obj in enumerate(objetos, 1):
            print(f"   {i}. {obj}")
        
        try:
            opcion_objeto = int(input("\nObjeto (número): ")) - 1
            
            # Mostrar Pokémon del equipo

            print(f"\n👥 ¿En qué Pokémon?")
            self._entrenador.mostrar_equipo()
            
            opcion_pokemon = int(input("\nPokémon (número): ")) - 1
            
            if 0 <= opcion_pokemon < len(self._entrenador.equipo):
                pokemon = self._entrenador.equipo[opcion_pokemon]
                
                # Encontrar el índice real en el inventario

                objeto = objetos[opcion_objeto]
                indice_real = self._entrenador.inventario.index(objeto)
                
                resultado = self._batalla.ejecutar_turno('objeto', indice_objeto=indice_real)
                
                if resultado == 'derrota':
                    print("\n💀 Has perdido la batalla...")
                    self._ofrecer_curacion()
        except (ValueError, IndexError):
            print(" Opción inválida.")
    
    def _ofrecer_curacion(self):
        """Ofrece curar al equipo después de una derrota"""
        print("\n ¿Deseas curar a tu equipo?")
        opcion = input("(s/n): ").strip().lower()
        
        if opcion == 's':
            for pokemon in self._entrenador.equipo:
                pokemon._vida_actual = pokemon.vida_max
            print(" ¡Tu equipo ha sido curado!")
    
    def _mostrar_estadisticas_detalladas(self):
        """Muestra estadísticas detalladas de un Pokémon"""
        self._entrenador.mostrar_equipo()
        
        try:
            opcion = int(input("\nVer estadísticas de (número): ")) - 1
            if 0 <= opcion < len(self._entrenador.equipo):
                self._entrenador.equipo[opcion].mostrar_estadisticas()
        except ValueError:
            print(" Opción inválida.")
    
    def _salir(self):
        """Sale del juego"""
        print(f"\n ¡Hasta luego, {self._entrenador.nombre}!")
        print("¡Gracias por jugar POKÉMON CONSOLE EDITION!")
        self._ejecutando = False
