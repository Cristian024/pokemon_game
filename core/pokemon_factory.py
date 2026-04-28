"""
Interfaz PokemonFactory - Patrón Factory Method
"""

from models.pokemon import Pokemon
from models.movimiento import Movimiento
from database.repositories.pokemon_repository import PokemonRepository
from core.estrategia_evolucion import EvolucionPorBatallas, SinEvolucion, EstrategiaEvolucion
from typing import List

class PokemonFactory:
    def __init__(self):
        self.db = PokemonRepository()

    def crear_pokemon_por_id(self, id_especie: int) -> Pokemon:
        datos_base = self.db.obtener_especie(id_especie)

        return self.crear_pokemon_por_base(datos_base)

    def crear_pokemon_por_base(self, datos_base: dict) -> Pokemon:    
        return Pokemon(
            id_especie=datos_base['id_especie'],
            nombre=datos_base['nombre'],
            nivel=datos_base['nivel'],
            tipo=datos_base['tipo'],
            vida_max=datos_base['vida_max'],
            ataque=datos_base['ataque'],
            defensa=datos_base['defensa'],
            velocidad=datos_base['velocidad'],
            es_evolucion=datos_base['es_evolucion'],
            pokemon_evolucionado_id=datos_base['pokemon_evolucionado_id'] if 'pokemon_evolucionado_id' in datos_base else None,
            estrategia_evolucion=self.crear_estrategia_evolucion(datos_base['estrategia_evolucion']),
            movimientos=self.crear_movimientos(datos_base['movimientos'])
        )

    def crear_movimientos(self, movimientos: List[dict]) -> List[Movimiento]:
        lista_movimientos = []
        for movimiento in movimientos:
            lista_movimientos.append(Movimiento(
                nombre=movimiento['nombre'],
                tipo=movimiento['tipo'],
                poder=movimiento['poder'],
                pp=movimiento['pp']
            ))
        return lista_movimientos

    def crear_estrategia_evolucion(self, evolucion: str) -> EstrategiaEvolucion:
        tipo_evolucion = evolucion["tipo"]
        if tipo_evolucion == "EvolucionPorBatallas":
            return EvolucionPorBatallas(batallas_necesarias=evolucion["batallas_necesarias"])
        elif tipo_evolucion == "SinEvolucion":
            return SinEvolucion()
        else:
            raise ValueError(f"Estrategia de evolución no reconocida: {evolucion}")    
