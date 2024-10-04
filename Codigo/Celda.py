"""
Clase que representa una celda 

Atributos:
    fila (int): Fila de la celda
    columna (int): Columna de la celda
    visitada (bool): Indica si la celda fue visitada
    activa (bool): Indica si la celda esta activa
    es_entrada_salida (bool): Indica si la celda es la entrada o la salida
    paredes (list): Un diccionario de los muros de la celda, llaves "top", "right", "bottom", "left"
    vecinos (list): Lista de celdas vecinas    
"""
class Celda(object):

    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.visitada = False
        self.activa = False
        self.es_entrada_salida = None
        self.paredes = {"top": True, "right": True, "bottom": True, "left": True}
        self.vecinos = []
        self.marcado = False
    
    """
    Funcion que verifica si hay paredes entre la celda y una celda vecina.
    Retorna True si hay paredes entre las celdas. De lo contrario, retorna False.

    Args:
        vecinos: La celda a verificar entre
    Return:
        True: Si hay paredes entre la celda y la celda vecina
        False: Si no hay paredes entre las celdas vecinas
    """
    def hay_pared_atras(self, vecinos):
        if self.fila - 1 == vecinos.fila:
            return self.paredes["top"] and vecinos.paredes["bottom"]
        if self.fila + 1 == vecinos.fila:
            return self.paredes["bottom"] and vecinos.paredes["top"]
        if self.columna - 1 == vecinos.columna:
            return self.paredes["left"] and vecinos.paredes["right"]
        if self.columna + 1 == vecinos.columna:
            return self.paredes["right"] and vecinos.paredes["left"]
        
    """
    Funcion que elimina los muros entre la celda y una celda vecina.
    Retorna True si los muros fueron eliminados. De lo contrario, retorna False.

    Args:
        fila_vecino: Fila de la celda vecina
        columna_vecino: Columna de la celda vecina

    Return:
        True: Si los muros fueron eliminados
        False: Si los muros no fueron eliminados
    """
    def remover_muros(self, fila_vecino, columna_vecino):
        if self.fila - 1 == fila_vecino:
            self.paredes["top"] = False
            return True, ""
        if self.fila + 1 == fila_vecino:
            self.paredes["bottom"] = False
            return True, ""
        if self.columna - 1 == columna_vecino:
            self.paredes["left"] = False
            return True, ""
        if self.columna + 1 == columna_vecino:
            self.paredes["right"] = False
            return True, ""
        return False

    """
    Funcion que establece la celda como una celda de entrada/salida deshabilitando el muro de la frontera exterior.
    Primero, verificamos si la entrada/salida esta en la fila superior. Luego, verificamos si deberia estar en la fila inferior.
    Finalmente, verificamos si esta en el muro izquierdo o en la fila inferior.

    Args:
        entrada_salida (bool): True para establecer esta celda como salida/entrada. False para eliminarla como una
        fila_limite (int): Limite de filas
        columna_limite (int): Limite de columnas
    """
    def establecer_entrada_salida(self, entrada_salida, fila_limite, columna_limite):
        if self.fila == 0:
            self.paredes["top"] = False
        if self.fila == fila_limite:
            self.paredes["bottom"] = False
        if self.columna == 0:
            self.paredes["left"] = False
        if self.columna == columna_limite:
            self.paredes["right"] = False
        self.es_entrada_salida = entrada_salida



    def to_dict(self):
        return {
            "fila": self.fila,
            "columna": self.columna,
            "visitada": self.visitada,
            "activa": self.activa,
            "es_entrada_salida": self.es_entrada_salida,
            "paredes": self.paredes,
            "vecinos": [vecino.to_dict() for vecino in self.vecinos]  # Serializa los vecinos
        }
