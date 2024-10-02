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


class FuerzaBruta(Solucionador):

    def __init__(self, laberinto, modo_silencio=False, método_vecino="fuerza_bruta"):
        super().__init__(laberinto, modo_silencio, método_vecino)
        self.nombre = "Fuerza Bruta"
        self.camino = []  # Lista para almacenar el camino encontrado

    def resolver(self):
        # Iniciar desde las coordenadas seleccionadas
        entrada = self.laberinto.punto_inicio
        salida = self.laberinto.coord_salida
        self.camino = []
        visitados = set()  # Conjunto de celdas ya visitadas

        # Usamos una pila para almacenar los caminos posibles (simula DFS)
        stack = [(entrada, [entrada])]  # Cada elemento de la pila es (posición actual, camino recorrido hasta ahí)

        while stack:
            (actual, camino_actual) = stack.pop()  # Tomamos la celda actual y el camino recorrido hasta ahí
            if actual == salida:
                self.camino = camino_actual  # Si llegamos a la salida, guardamos el camino
                if not self.modo_silencio:
                    logging.info(f"Solución encontrada: {self.camino}")
                return self.camino

            if actual in visitados:
                continue

            # Marcamos la celda como visitada
            visitados.add(actual)

            # Obtener los vecinos de la celda actual
            vecinos = self.laberinto.encontrar_vecinos(*actual)
            vecinos_validos = self.laberinto.validar_vecino_generado(vecinos)

            # Añadir cada vecino no visitado a la pila con su respectivo camino
            for vecino in vecinos_validos:
                if vecino not in visitados:
                    stack.append((vecino, camino_actual + [vecino]))

        if not self.modo_silencio:
            logging.warning("No se encontró ninguna solución.")
        return None  # Si no se encuentra un camino
    
    def obtener_camino(self):
        return self.camino
    
        

class OptimizacionBacktracking(Solucionador):

    def __init__(self, laberinto, modo_silencio=False, método_vecino="optimizacion"):
        super().__init__(laberinto, modo_silencio, método_vecino)
        self.nombre = "Optimización Backtracking"
        self.camino = []  # Lista para almacenar el camino de la solución
    
    def resolver(self):
        # Iniciar desde la entrada del laberinto
        entrada = self.laberinto.punto_inicio
        k_actual, l_actual = entrada
        self.laberinto.grid[entrada[0]][entrada[1]].visitada = True
        salida = self.laberinto.coord_salida
        self.camino = []
        celdas_visitadas = []  # Lista de celdas visitadas

        while (entrada != salida):
            # Encontrar vecinos de la celda actual
            indices_vecinos = self.laberinto.encontrar_vecinos(k_actual, l_actual)

            # Validar si los vecinos han sido visitados
            indices_vecinos = self.laberinto.validar_vecino_solucion(indices_vecinos, k_actual, l_actual, salida[0], salida[1], self.método_vecino)

            # Si hay vecinos no visitados
            if indices_vecinos is not None:
                celdas_visitadas.append((k_actual, l_actual))  # Agregar la celda actual a la lista de celdas visitadas
                self.camino.append(((k_actual, l_actual),False)) # Agregar la celda actual al camino
            
                # Elegir un vecino aleatorio
                k_siguiente, l_siguiente = random.choice(indices_vecinos)
                
                #Se marca la celda actual como visitada
                self.laberinto.grid[k_siguiente][l_siguiente]. visitada = True
                
                #Se actualiza la celda actual
                k_actual, l_actual = k_siguiente, l_siguiente
                entrada = (k_actual, l_actual)

            
            # Si no hay vecinos no visitados
            elif len(celdas_visitadas) > 0:
                self.camino.append(((k_actual, l_actual),True)) # Agregar la celda actual al camino
                k_actual, l_actual = celdas_visitadas.pop()  # Retroceder a la celda anterior

        self.camino.append(((k_actual, l_actual),False)) # Agregar la celda actual al camino
        if not self.modo_silencio:
            logging.info(f"Solución encontrada: {self.camino}")

        return self.camino
        
        
        
                






