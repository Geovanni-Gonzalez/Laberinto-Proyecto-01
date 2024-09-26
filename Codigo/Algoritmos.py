import time
import random
import math


lista_algortimos = ["dfs_backtracking", "fuerza_bruta", "optimizacion"]

def dfs_backtracking(laberinto, coordenada_inicio):
    k_inicio, l_inicio = coordenada_inicio  # Coordenadas de inicio, donde empezara el laberinto
    camino = [(k_inicio, l_inicio)]  # Camino de la solucion
    laberinto.grid[k_inicio][l_inicio].visitada = True  # Marca la celda como visitada
    contador_visitas = 1  # Contador de visitas
    celdas_visitadas = []  # Lista de celdas visitadas

    print("DFS Backtracking")

    while contador_visitas< laberinto.tamanno_grid: # Mientras no se hayan visitado todas las celdas
        vecinos_indices = laberinto.encontrar_vecinos(k_inicio, l_inicio)   # Encuentra los vecinos de la celda actual
        vecinos_indices = laberinto.validar_vecino_generado(vecinos_indices)  # Valida si los vecinos han sido visitados

        if vecinos_indices is not None:
            celdas_visitadas.append((k_inicio, l_inicio))  # Agrega la celda actual a la lista de celdas visitadas
            k_siguiente, l_siguiente = random.choice(vecinos_indices)

            laberinto.grid[k_inicio][l_inicio].remover_muros(k_siguiente, l_siguiente)  # Remueve los muros entre la celda actual y la celda vecina
            laberinto.grid[k_siguiente][l_siguiente].remover_muros(k_inicio, l_inicio)  # Remueve los muros entre la celda vecina y la celda actual
            laberinto.grid[k_siguiente][l_siguiente].visitada = True

            k_inicio, l_inicio = k_siguiente, l_siguiente

            camino.append((k_inicio, l_inicio))  # Agrega la celda vecina al camino

            contador_visitas += 1  # Aumenta el contador de visitas 
        
        elif len(celdas_visitadas) > 0: # Si no hay vecinos no visitados, retrocede a la celda anterior
            k_inicio, l_inicio = celdas_visitadas.pop()  # Retrocede a la celda anterior
            camino.append((k_inicio, l_inicio))     # Agrega la celda al camino
        
    print("Numero de movimientos hechos: {}".format(len(camino)))  # Imprime el numero de movimientos hechos
    print("Numero de celdas visitadas: {}".format(contador_visitas))  # Imprime el numero de celdas visitadas

        
    laberinto.grid[laberinto.coord_entrada[0]][laberinto.coord_entrada[1]].establecer_entrada_salida("entrada",laberinto.num_filas-1, laberinto.num_columnas-1)  # Establece la celda de entrada
    laberinto.grid[laberinto.coord_salida[0]][laberinto.coord_salida[1]].establecer_entrada_salida("salida",laberinto.num_filas-1, laberinto.num_columnas-1)  # Establece la celda de salida

    for i in range(laberinto.num_filas):    # Reinicia las celdas visitadas
        for j in range(laberinto.num_columnas):     # Reinicia las celdas visitadas
            laberinto.grid[i][j].visitada = False   # Reinicia las celdas visitadas

    laberinto.camino_generacion=camino  # Guarda el camino de la generacion

    print ("Camino de generacion: ", camino)  # Imprime el camino de generacion

    



