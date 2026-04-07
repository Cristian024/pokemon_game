```markdown
# 🎮 Pokémon Console Edition

Juego de Pokémon por consola implementado en Python.

## 📁 Estructura del Proyecto

```text
pokemon_game/
├── core/                        # Lógica central del juego
│   ├── estrategia_evolucion.py  # Patrón Strategy para evoluciones
│   ├── pokemon_factory.py       # Patrón Factory (Data-Driven)
│   └── sistema_batalla.py       # Gestión de combates por turnos
├── database/                    # Capa de persistencia (MongoDB)
│   ├── repositories/
│   │   └── pokemon_repository.py # Patrón Repository
│   └── conexion_mongo.py        # Patrón Singleton para la BD
├── models/                      # Entidades de dominio (Estado)
│   ├── entrenador.py            # Clase Entrenador (jugador)
│   ├── movimiento.py            # Clase Movimiento
│   ├── objeto.py                # Clases de objetos (Pociones, Revivir)
│   └── pokemon.py               # Modelo principal Pokemon
├── ui/                          # Interfaz de usuario
│   └── consola.py               # Menús interactivos
├── .env                         # Credenciales y URI de la base de datos
├── main.py                      # Punto de entrada del juego
└── README.md                    # Este archivo
```

## 🏗️ Patrones de Diseño Implementados

### 1. Data-Driven Factory (`PokemonFactory`)
Construye instancias de la clase `Pokemon` inyectando los *stats base* y tipos directamente desde los documentos almacenados en MongoDB.

### 2. Strategy (`EstrategiaEvolucion`)
Define algoritmos intercambiables sobre cómo evolucionan los Pokémon, aislando esta lógica de la clase `Pokemon`:
- `EvolucionPorBatallas` → Evoluciona tras N batallas ganadas.
- `SinEvolucion` → Bloquea la evolución.

### 3. Singleton (`ConexionMongo`)
Garantiza que toda la aplicación utilice una única instancia compartida para la conexión a la base de datos MongoDB, optimizando el consumo de recursos.

### 4. Repository (`PokemonRepository`)
Actúa como una capa de abstracción entre la lógica del juego (Core) y la base de datos (MongoDB). Permite buscar y obtener datos de las especies sin acoplar el código a consultas de `pymongo`.

## ✅ Historias de Usuario Implementadas

| ID | Historia | Implementación |
|---|---|---|
| HU1 | Capturar Pokémon | `Entrenador.capturar_pokemon()` |
| HU2 | Gestionar equipo | Equipo (máx 6) + PC (Pokédex) |
| HU3 | Batallas por turnos | `SistemaDeBatalla` |
| HU4 | Ganar experiencia | `registrar_victoria()` + `subir_nivel()` |
| HU5 | Evolución dinámica | Delegado a `EstrategiaEvolucion` a través de la DB |
| HU6 | Obtener datos DB | `PokemonRepository.obtener_especie()` |
| HU7 | Usar objetos | Poción, Súper Poción, Revivir |
| HU8 | Orden por velocidad | Lógica de cálculo de iniciativa |
| HU9 | Calcular daño | Fórmula con tipos y aleatoriedad |
| HU10 | Interfaz dinámica | Selección de iniciales por Tipo (`ui/consola.py`) |

## 🚀 Cómo Ejecutar

### Requisitos
- Python 3.7 o superior
- MongoDB local o cluster en MongoDB Atlas
- Librerías: `pymongo`, `python-dotenv`

### Instalación y Ejecución
```bash
# 1. Instalar dependencias
pip install pymongo python-dotenv

# 2. Configurar variables de entorno
# Asegúrate de crear el archivo .env con MONGO_URI y MONGO_DB_NAME

# 3. Ejecutar el juego
python main.py
```

## 🎮 Controles del Juego

### Menú Principal
1. 🐾 Buscar Pokémon salvaje
2. 👥 Ver mi equipo
3. 📱 Ver Pokédex
4. 🎒 Ver inventario
5. 📊 Ver estadísticas
6. 🚪 Salir

### En Batalla
1. ⚔️ Atacar → Selecciona un movimiento
2. 🎒 Usar Objeto → Selecciona objeto y Pokémon
3. 🎯 Capturar → Intenta capturar al Pokémon salvaje
4. 🏃 Huir → Escapa de la batalla

## 📊 Sistema de Tipos

| Atacante → Defensor | Fuego | Agua | Planta | Eléctrico |
|---|---|---|---|---|
| **Fuego** | 0.5x | 0.5x | 2.0x | 1.0x |
| **Agua** | 2.0x | 0.5x | 0.5x | 1.0x |
| **Planta** | 0.5x | 2.0x | 0.5x | 1.0x |
| **Eléctrico** | 1.0x | 2.0x | 0.5x | 0.5x |

## 🎒 Objetos

- **Poción**: Cura 20 PS
- **Súper Poción**: Cura 50 PS
- **Revivir**: Revive con 50% de PS

## 📄 Diagrama UML Base (Dominio)

El diseño del dominio respeta el siguiente contrato:

```text
┌─────────────────────────────────────────────────────────────┐
│                    <<abstract / model>>                     │
│                           Pokemon                           │
├─────────────────────────────────────────────────────────────┤
│ - id_especie: int                                           │
│ - nombre: String                                            │
│ - nivel: int                                                │
│ - tipo: List<String>                                        │
│ - evolucion: IEstrategiaEvolucion                           │
├─────────────────────────────────────────────────────────────┤
│ + atacar(): void                                            │
│ + recibir_dano(): void                                      │
│ + intentar_evolucionar(): int | None                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ tiene
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        <<interface>>                        │
│                    IEstrategiaEvolucion                     │
├─────────────────────────────────────────────────────────────┤
│ + verificar_evolucion(Pokemon p): int | None                │
└─────────────────────────────────────────────────────────────┘
         ▲                                            ▲
         │                                            │
         │ implementa                                 │ implementa
         │                                            │
┌──────────────────────┐                  ┌──────────────────────┐
│ EvolucionPorNivel    │                  │    SinEvolucion      │
├──────────────────────┤                  ├──────────────────────┤
│ - nivel_necesario    │                  │                      │
│ - id_siguiente       │                  │                      │
└──────────────────────┘                  └──────────────────────┘
```

## 👨‍💻 Autor

Proyecto educativo para demostrar el uso de Patrones de Diseño, Bases de Datos NoSQL (MongoDB) y Arquitecturas Limpias en Python.
```