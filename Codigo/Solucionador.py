import time
import random
import logging
from Laberinto import *

logging.basicConfig(level=logging.DEBUG)


class Solucionador(object):
    """Clase base para métodos de solución.
    Cada nuevo método de solución debe sobrescribir el método resolver.

    Atributos:
        laberinto (list): El laberinto que se está resolviendo.
        método_vecino:
        modo_silencio: Cuando está habilitado, la información no se muestra en la consola.

    """

    def __init__(self, laberinto, modo_silencio, método_vecino):
        logging.debug("Constructor de la clase Solucionador llamado")

        self.laberinto = laberinto
        self.método_vecino = método_vecino
        self.nombre = ""
        self.modo_silencio = modo_silencio

    def resolver(self):
        logging.debug('Clase: Solucionador resolver llamado')
        raise NotImplementedError

    def obtener_nombre(self):
        logging.debug('Clase Solucionador obtener_nombre llamado')
        raise self.nombre

    def obtener_camino(self):
        logging.debug('Clase Solucionador obtener_camino llamado')
        return self.camino


