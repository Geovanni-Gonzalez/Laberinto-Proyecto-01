from Laberinto import *
from Visualizador import *
from Solucionador import *


class Administrador:
    """
    Un administrador que abstrae la interacción con los componentes del laberinto.
    La creación de laberintos, las soluciones, y las visualizaciones son
    manejadas a través de este administrador.

    Atributos:
        laberintos (list): Es posible tener más de un laberinto. Se almacenan en esta variable.
        nombre_archivo (str): El nombre del archivo para guardar animaciones e imágenes.
        modo_silencioso (bool): Cuando está activado, la información no se muestra en la consola.
    """

    def __init__(self):
        self.laberintos = []
        self.nombre_archivo = ""
        self.modo_silencioso = False

    def agregar_laberinto(self, filas, columnas, id=0):
        """
        Agrega un laberinto al administrador. El laberinto recibe un índice basado en el
        total de laberintos en el administrador. El id será único mientras no se eliminen
        laberintos del administrador.

        Args:
            filas (int): La altura del laberinto.
            columnas (int): El ancho del laberinto.
            id (int):  El id único opcional del laberinto.

        Returns:
            Laberinto: El laberinto recién creado.
        """
        if id != 0:
            self.laberintos.append(Laberinto(filas, columnas, id))
        else:
            if len(self.laberintos) < 1:
                self.laberintos.append(Laberinto(filas, columnas, 0))
            else:
                self.laberintos.append(Laberinto(filas, columnas, len(self.laberintos) + 1))

        return self.laberintos[-1]

    def agregar_laberinto_existente(self, laberinto, sobrescribir=True):
        """
        Agrega un laberinto ya existente al administrador. Se asume que el laberinto
        ya tiene un id. Si el id ya existe, la función fallará a menos que
        se active la opción de sobrescribir.

        Args:
            laberinto (Laberinto): El laberinto a agregar.
            sobrescribir (bool): Permite reasignar un nuevo id único.

        Returns:
            Laberinto: El laberinto si fue agregado correctamente.
            False: Si no se pudo agregar debido a un conflicto de id.
        """
        if self.verificar_id_existente(laberinto.id) is None:
            if sobrescribir:
                if len(self.laberintos) < 1:
                    laberinto.id = 0
                else:
                    laberinto.id = len(self.laberintos) + 1
        else:
            return False
        self.laberintos.append(laberinto)
        return laberinto

    def obtener_laberinto(self, id):
        """Obtiene un laberinto por su id.

        Args:
            id (int): El id del laberinto.

        Returns:
            Laberinto: El laberinto si fue encontrado.
            None: Si no se encontró ningún laberinto con ese id.
        """
        for laberinto in self.laberintos:
            if laberinto.id == id:
                return laberinto
        print("Laberinto no encontrado.")
        return None

    def obtener_laberintos(self):
        """Obtiene todos los laberintos que el administrador maneja."""
        return self.laberintos

    def contar_laberintos(self):
        """Obtiene la cantidad de laberintos en el administrador."""
        return len(self.laberintos)

    def resolver_laberinto(self, id_laberinto, metodo, metodo_vecino="complejo"):
        """
        Resuelve un laberinto por un método específico.

        Args:
            id_laberinto (int): El id del laberinto a resolver.
            metodo (str): El nombre del método de solución (ej: 'dfs_backtracking', 'bi_directional', 'bfs').
            metodo_vecino (str): Método para encontrar vecinos (opcional).
        """
        laberinto = self.obtener_laberinto(id_laberinto)
        if laberinto is None:
            print("Laberinto no encontrado. Saliendo del solucionador.")
            return None

        if metodo == "fuerza_bruta":
            #solver = DFSBacktrackingSolver(laberinto, metodo_vecino, self.modo_silencioso)
            #laberinto.camino_solucion = solver.resolver()
            pass
        elif metodo == "optimizacion":
            pass

    def mostrar_laberinto(self, id, tamano_celda=1):
        """Muestra el laberinto sin solución."""
        vis = Visualizador(self.obtener_laberinto(id), tamano_celda, self.nombre_archivo)
        vis.mostrar_laberinto()

    def mostrar_animacion_generacion(self, id, tamano_celda=1):
        """Muestra la animación de la generación del laberinto."""
        vis = Visualizador(self.obtener_laberinto(id), tamano_celda, self.nombre_archivo)
        vis.mostrar_animacion_generacion()

    def mostrar_solucion(self, id, tamano_celda=1):
        """Muestra el laberinto con la solución."""
        vis = Visualizador(self.obtener_laberinto(id), tamano_celda, self.nombre_archivo)
        vis.mostrar_solucion_laberinto()

    def mostrar_animacion_solucion(self, id, tamano_celda=1):
        """Muestra la animación de la solución del laberinto."""
        vis = Visualizador(self.obtener_laberinto(id), tamano_celda, self.nombre_archivo)
        vis.animar_solucion_laberinto()

    def verificar_id_existente(self, id):
        """Verifica si el id ya pertenece a un laberinto existente."""
        return next((laberinto for laberinto in self.laberintos if laberinto.id == id), None)

    def establecer_nombre_archivo(self, nombre_archivo):
        """Establece el nombre del archivo para guardar animaciones o imágenes."""
        self.nombre_archivo = nombre_archivo

    def habilitar_modo_silencioso(self, habilitado):
        """Habilita o deshabilita el modo silencioso."""
        self.modo_silencioso = habilitado