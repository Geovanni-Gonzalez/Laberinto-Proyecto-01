import random
import math
import time
from Celda import *
from Algoritmos import *
import json

class Laberinto(object):
    """
    Clase que representa un laberinto
    Contiene funciones para generar aleatoriamente el laberinto, asi como para resolver el laberinto.

    Atributos:

        num_filas (int): El alto del laberinto, en celdas
        num_columnas (int): El ancho del laberinto, en celdas
        id (int): Un identificador unico para el laberinto
        tamanno_grid (int): El area del laberinto, tambien el numero total de celdas en el laberinto
        entrada (tuple): Coordenadas de la celda de entrada
        salida (tuple): Coordenadas de la celda de salida
        camino_generacion (list): El camino que se tomo al generar el laberinto
        camino_solucion (list): El camino que se tomo por un solucionador al resolver el laberinto
        grid_inicial (list): Una copia de la cuadricula inicial
        grid (list): Una copia de grid_inicial (posiblemente esto no sea necesario

    """

    def __init__(self, numero_filas, numero_columnas, id=0, algoritmo="dfs_backtracking"):
        self.num_filas = numero_filas
        self.num_columnas = numero_columnas
        self.id = id
        self.tamanno_grid = numero_filas * numero_columnas
        self.entrada = None
        self.coord_entrada = self.seleccionar_entrada_salida_random(None)
        self.coord_salida = self.seleccionar_entrada_salida_random(self.coord_entrada)
        self.camino_generacion = []
        self.camino_solucion = None
        self.grid_inicial = self.generaar_grid()
        self.grid = self.grid_inicial
        self.generar_laberinto(algoritmo, self.coord_entrada)
        self.algoritmo = algoritmo
        self.punto_inicio = None

    def establecer_punto_inicio(self, punto_inicio):
        self.punto_inicio = punto_inicio
    
    def obtener_punto_inicio(self):
        return self.punto_inicio

    """
    Funcion que crea una cuadricula 2D de objetos Celda. Esto puede ser pensado como un laberinto sin caminos tallados.

    Return: 
        Una lista con objetos Celda en cada posicion
    """

    def generaar_grid(self):
        grid = []
        for i in range(self.num_filas):
            grid.append([])
            for j in range(self.num_columnas):
                grid[i].append(Celda(i, j))
        return grid
    """
    Funcion que encuentra todos los vecinos existentes y no visitados de una celda en la cuadricula.
    Retorna una lista de tuplas que contienen indices para los vecinos no visitados.

    Args:
        fila_celda (int): Fila de la celda
        columna_celda (int): Columna de la celda

    Return:
        None: Si no hay vecinos no visitados
        list: Una lista de vecinos que no han sido visitados
    """

    def encontrar_vecinos(self, fila, columna):
        vecinos = []

        def verificar_vecino(fila, columna):
            if fila >= 0 and fila < self.num_filas and columna >= 0 and columna < self.num_columnas:
                vecinos.append((fila, columna))

        verificar_vecino(fila - 1, columna)
        verificar_vecino(fila + 1, columna)
        verificar_vecino(fila, columna - 1)
        verificar_vecino(fila, columna + 1)

        if len(vecinos)> 0:
            return vecinos
        else:
            return None
        
    
    """
    Funcion que valida si un vecino es no visitado o no. Cuando se genera el laberinto, solo queremos movernos a celdas no visitadas (a menos que estemos retrocediendo).

    Args:
        vecino_indices: Indices de la celda vecina

    Return:
        True: Si el vecino ha sido visitado
        False: Si el vecino no ha sido visitado
    """
    def validar_vecino_generado(self, vecino_indices):
        
        lista_vecinos = [n for n in vecino_indices if not self.grid[n[0]][n[1]].visitada] # Lista de vecinos no visitados

        if len(lista_vecinos) > 0:
            return lista_vecinos
        else:
            return None
    """
    Funcion que valida si un vecino es una solucion o no. Cuando se resuelve el laberinto, solo queremos movernos a celdas que no sean paredes.

    Args:
        vecino_indices: Indices de la celda vecina
        k: Fila de la celda actual
        l: Columna de la celda actual
        k_fin: Fila de la celda de salida
        l_fin: Columna de la celda de salida
        metodo: Metodo de resolucion del laberinto  

    Return:
        True: Si el vecino es una solucion
        False: Si el vecino no es una solucion
    """        

    def validar_vecino_solucion(self, vecino_indices, k, l, k_fin, l_fin, metodo):
        if metodo == '1':# Fuerza bruta
            return self.fuerza_bruta(k, l, k_fin, l_fin, set(), [])      
        
        elif metodo=='2':# Optimizacion backtracking
            lista_vecinos=[]    # Lista de vecinos no visitados
            distancia_min_target= 100000    # Distancia minima al target

            # Encuentra el vecino mas cercano al target
            for k_n, l_n in vecino_indices:
                # Si el vecino no ha sido visitado y no hay paredes entre la celda actual y la celda vecina
                if (not self.grid[k_n][l_n].visitada and not self.grid[k][l].hay_pared_atras(self.grid[k_n][l_n])):
                    distancia_target= math.sqrt((k_n- k_fin)**2 + (l_n-l_fin)**2)
                    # Si la distancia al target es menor que la distancia minima al target
                    if distancia_target < distancia_min_target:
                        # Actualiza la distancia minima al target
                        distancia_min_target=distancia_target
                        # Actualiza el vecino mas cercano al target
                        min_vecino=(k_n, l_n)
            
            # Si no hay vecinos no visitados
            if "min_vecino" in locals():        
                lista_vecinos.append(min_vecino)
                

        if len(lista_vecinos) > 0:    
            return lista_vecinos
        else:
            return None

    """
    Funcion que selecciona aleatoriamente las coordenadas de entrada y salida del laberinto.
    Args:
        entrada_salida_usada: Coordenadas de entrada y salida
    Return:
        rng_entrada_salida: Coordenadas de entrada y salida
    """
    def seleccionar_entrada_salida_random(self, entrada_salida_usada):

        rng_entrada_salida=entrada_salida_usada # Coordenadas de entrada y salida

        while rng_entrada_salida == entrada_salida_usada:
            rng_lado = random.randint(0, 3) # Selecciona aleatoriamente las coordenadas de entrada y salida

            if rng_lado == 0:
                rng_entrada_salida = (0, random.randint(0, self.num_columnas - 1)) # Arriba

            elif rng_lado == 2:
                rng_entrada_salida = (self.num_filas - 1, random.randint(0, self.num_columnas - 1)) # Derecha
            
            elif rng_lado == 1:
                rng_entrada_salida = (random.randint(0, self.num_filas - 1), self.num_columnas - 1) # Abajo

            elif rng_lado == 3:
                rng_entrada_salida = (random.randint(0, self.num_filas - 1), 0) # Izquierda

        return rng_entrada_salida
    
    def generar_laberinto(self, metodo, coordenadas_inicio=(0,0)):
        if metodo == "dfs_backtracking":
            dfs_backtracking(self, coordenadas_inicio)


    def to_dict(self):
        return {
            "id": self.id,
            "num_filas": self.num_filas,
            "num_columnas": self.num_columnas,
            "tamanno_grid": self.tamanno_grid,
            "entrada": self.coord_entrada,
            "salida": self.coord_salida,
            "camino_generacion": self.camino_generacion,
            "camino_solucion": self.camino_solucion,
            "grid": [[celda.to_dict() for celda in fila] for fila in self.grid],
            "punto_inicio": self.punto_inicio
        }

    def marcar_camino(self, coordenada):
            """ Método para marcar una celda en el camino como parte de la solución """
            x, y = coordenada
            self.grid[x][y].visitada = True  # O actualiza la representación visual 
    
    def puede_moverse(self, actual, vecino):
            k_actual, l_actual = actual
            k_vecino, l_vecino = vecino
            
            # Verificar si el vecino está a la derecha
            if l_vecino == l_actual + 1 and self.grid[k_actual][l_actual].paredes['right']:
                return False
            # Verificar si el vecino está a la izquierda
            if l_vecino == l_actual - 1 and self.grid[k_actual][l_actual].paredes['left']:
                return False
            # Verificar si el vecino está arriba
            if k_vecino == k_actual - 1 and self.grid[k_actual][l_actual].paredes['top']:
                return False
            # Verificar si el vecino está abajo
            if k_vecino == k_actual + 1 and self.grid[k_actual][l_actual].paredes['bottom']:
                return False
    
            return True
    
