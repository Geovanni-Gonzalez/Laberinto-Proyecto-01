import matplotlib.pyplot as plt
from matplotlib import animation
import logging

logging.basicConfig(level=logging.DEBUG)

class Visualizador(object):
    """Clase que maneja todos los aspectos de la visualización.
    Atributos:
        laberinto: El laberinto que se visualizará
        tamaño_celda (int): Qué tan grandes serán las celdas en las gráficas
        altura (int): La altura del laberinto
        ancho (int): El ancho del laberinto
        ax: Los ejes para la gráfica
        lineas:
        cuadrados:
        nombre_archivo_media (string): El nombre de las animaciones e imágenes
    """
    def __init__(self, laberinto, tamaño_celda, nombre_archivo_media):
        self.laberinto = laberinto
        self.tamaño_celda = tamaño_celda
        self.altura = laberinto.num_filas * tamaño_celda
        self.ancho = laberinto.num_columnas * tamaño_celda
        self.ax = None
        self.lineas = dict()
        self.cuadrados = dict()
        self.nombre_archivo_media = nombre_archivo_media

    def establecer_nombre_archivo_media(self, nombre_archivo):
        """Establece el nombre del archivo de los medios
            Args:
                nombre_archivo (string): El nombre del medio
        """
        self.nombre_archivo_media = nombre_archivo

    def mostrar_laberinto(self):
        """Muestra una gráfica del laberinto sin la solución"""

        # Crear la figura de la gráfica y estilizar los ejes
        figura = self.configurar_grafica()

        # Graficar las paredes en la figura
        self.graficar_paredes()

        # Mostrar la gráfica al usuario
        plt.show()

        # Manejar cualquier posible guardado
        if self.nombre_archivo_media:
            figura.savefig("{}{}.png".format(self.nombre_archivo_media, "_generacion"), frameon=None)

    def graficar_paredes(self):
        """Grafica las paredes de un laberinto. Esto se utiliza al generar la imagen del laberinto"""
        for i in range(self.laberinto.num_filas):
            for j in range(self.laberinto.num_columnas):
                if self.laberinto.grid[i][j].es_entrada_salida == "entrada":
                    self.ax.text(j*self.tamaño_celda, i*self.tamaño_celda, "INICIO", fontsize=7, weight="bold")
                elif self.laberinto.grid[i][j].es_entrada_salida == "salida":
                    self.ax.text(j*self.tamaño_celda, i*self.tamaño_celda, "FIN", fontsize=7, weight="bold")
                if self.laberinto.grid[i][j].paredes["top"]:
                    self.ax.plot([j*self.tamaño_celda, (j+1)*self.tamaño_celda],
                                [i*self.tamaño_celda, i*self.tamaño_celda], color="k")
                if self.laberinto.grid[i][j].paredes["right"]:
                    self.ax.plot([(j+1)*self.tamaño_celda, (j+1)*self.tamaño_celda],
                                [i*self.tamaño_celda, (i+1)*self.tamaño_celda], color="k")
                if self.laberinto.grid[i][j].paredes["bottom"]:
                    self.ax.plot([(j+1)*self.tamaño_celda, j*self.tamaño_celda],
                                [(i+1)*self.tamaño_celda, (i+1)*self.tamaño_celda], color="k")
                if self.laberinto.grid[i][j].paredes["left"]:
                    self.ax.plot([j*self.tamaño_celda, j*self.tamaño_celda],
                                [(i+1)*self.tamaño_celda, i*self.tamaño_celda], color="k")

    def configurar_grafica(self):
        """Establece las propiedades iniciales de la gráfica del laberinto. También crea la gráfica y los ejes"""

        # Crear la figura de la gráfica
        figura = plt.figure(figsize=(7, 7*self.laberinto.num_filas/self.laberinto.num_columnas))

        # Crear los ejes
        self.ax = plt.axes()

        # Establecer una relación de aspecto igual
        self.ax.set_aspect("equal")

        # Remover los ejes de la figura
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

        caja_titulo = self.ax.text(0, self.laberinto.num_filas + self.tamaño_celda + 0.1,
                            r"{}$\times${}".format(self.laberinto.num_filas, self.laberinto.num_columnas),
                            bbox={"facecolor": "gray", "alpha": 0.5, "pad": 4}, fontname="serif", fontsize=15)

        return figura

    def mostrar_solucion_laberinto(self):
        """Función que grafica la solución al laberinto. También agrega indicaciones de los puntos de entrada y salida."""

        # Crear la figura y estilizar los ejes
        figura = self.configurar_grafica()

        # Graficar las paredes en la figura
        self.graficar_paredes()

        lista_de_retrocesos = [elemento_camino[0] for elemento_camino in self.laberinto.camino_solucion if elemento_camino[1]]

        # Mantiene un registro de cuántos círculos se han dibujado
        num_circulos = 0

        self.ax.add_patch(plt.Circle(((self.laberinto.camino_solucion[0][0][1] + 0.5)*self.tamaño_celda,
                                    (self.laberinto.camino_solucion[0][0][0] + 0.5)*self.tamaño_celda), 0.2*self.tamaño_celda,
                                    fc=(0, num_circulos/(len(self.laberinto.camino_solucion) - 2*len(lista_de_retrocesos)),
                                        0), alpha=0.4))

        for i in range(1, len(self.laberinto.camino_solucion)):
            if self.laberinto.camino_solucion[i][0] not in lista_de_retrocesos and\
                    self.laberinto.camino_solucion[i-1][0] not in lista_de_retrocesos:
                num_circulos += 1
                self.ax.add_patch(plt.Circle(((self.laberinto.camino_solucion[i][0][1] + 0.5)*self.tamaño_celda,
                    (self.laberinto.camino_solucion[i][0][0] + 0.5)*self.tamaño_celda), 0.2*self.tamaño_celda,
                    fc=(0, num_circulos/(len(self.laberinto.camino_solucion) - 2*len(lista_de_retrocesos)), 0), alpha=0.4))

        # Mostrar la gráfica al usuario
        plt.show()

        # Manejar cualquier guardado
        if self.nombre_archivo_media:
            figura.savefig("{}{}.png".format(self.nombre_archivo_media, "_solucion"), frameon=None)

    def mostrar_animacion_generacion(self):
        """Función que anima el proceso de generación de un laberinto donde el camino es una lista
        de coordenadas que indican el camino tomado para labrar (romper paredes) el laberinto."""

        # Crear la figura y estilizar los ejes
        figura = self.configurar_grafica()

        # El cuadrado que representa la cabeza del algoritmo
        indicador = plt.Rectangle((self.laberinto.camino_generacion[0][0]*self.tamaño_celda, self.laberinto.camino_generacion[0][1]*self.tamaño_celda),
            self.tamaño_celda, self.tamaño_celda, fc="purple", alpha=0.6)

        self.ax.add_patch(indicador)

        # Solo es necesario graficar la pared derecha e inferior para cada celda ya que las paredes se superponen.
        # También se añaden cuadrados para animar el camino tomado para labrar el laberinto.
        color_paredes = "k"
        for i in range(self.laberinto.num_filas):
            for j in range(self.laberinto.num_columnas):
                self.lineas["{},{}: derecha".format(i, j)] = self.ax.plot([(j+1)*self.tamaño_celda, (j+1)*self.tamaño_celda],
                        [i*self.tamaño_celda, (i+1)*self.tamaño_celda],
                    linewidth=2, color=color_paredes)[0]
                self.lineas["{},{}: abajo".format(i, j)] = self.ax.plot([(j+1)*self.tamaño_celda, j*self.tamaño_celda],
                        [(i+1)*self.tamaño_celda, (i+1)*self.tamaño_celda],
                    linewidth=2, color=color_paredes)[0]

                self.cuadrados["{},{}".format(i, j)] = plt.Rectangle((j*self.tamaño_celda,
                    i*self.tamaño_celda), self.tamaño_celda, self.tamaño_celda, fc="red", alpha=0.4)
                self.ax.add_patch(self.cuadrados["{},{}".format(i, j)])

        # Graficando los límites del laberinto.
        color_limite = "k"
        self.ax.plot([0, self.ancho], [self.altura, self.altura], color_limite)
        self.ax.plot([0, self.ancho], [0, 0], color_limite)
        self.ax.plot([0, 0], [0, self.altura], color_limite)
        self.ax.plot([self.ancho, self.ancho], [0, self.altura], color_limite)

        # Animación para graficar la generación del laberinto.
        def animate(frame):
            if frame < len(self.laberinto.camino_generacion):
                self.ax.set_title("Paso {}".format(frame))
                if frame > 0:
                    self.lineas["{},{}: derecha".format(self.laberinto.camino_generacion[frame-1][0],
                                                        self.laberinto.camino_generacion[frame-1][1])].set_color("red")
                    self.lineas["{},{}: abajo".format(self.laberinto.camino_generacion[frame-1][0],
                                                        self.laberinto.camino_generacion[frame-1][1])].set_color("red")
                if frame < len(self.laberinto.camino_generacion) - 1:
                    self.ax.add_patch(indicador)
                    indicador.set_xy((self.laberinto.camino_generacion[frame][0]*self.tamaño_celda,
                                    self.laberinto.camino_generacion[frame][1]*self.tamaño_celda))

        anim = animation.FuncAnimation(figura, animate, frames=len(self.laberinto.camino_generacion), repeat=False)

        # Mostrar la gráfica al usuario
        plt.show()

        # Manejar cualquier posible guardado
        if self.nombre_archivo_media:
            anim.save("{}.mp4".format(self.nombre_archivo_media), writer='ffmpeg', fps=60, dpi=100)

    def mostrar_animacion_solucion(self):
        """Función que anima el proceso de resolución del laberinto"""

        # Crear la figura y estilizar los ejes
        figura = self.configurar_grafica()

        # La cabeza del algoritmo
        indicador = plt.Rectangle((self.laberinto.camino_solucion[0][0][1]*self.tamaño_celda,
                                self.laberinto.camino_solucion[0][0][0]*self.tamaño_celda),
                                self.tamaño_celda, self.tamaño_celda, fc="green", alpha=0.6)
        self.ax.add_patch(indicador)

        # Animación para graficar la resolución del laberinto.
        def animate(frame):
            self.ax.set_title("Resolviendo el laberinto: Paso {}".format(frame))
            if frame > 0:
                self.ax.add_patch(plt.Circle(((self.laberinto.camino_solucion[frame-1][0][1] + 0.5)*self.tamaño_celda,
                                                (self.laberinto.camino_solucion[frame-1][0][0] + 0.5)*self.tamaño_celda), 
                                            0.2*self.tamaño_celda, fc=(0, 0, 1), alpha=0.4))
            if frame < len(self.laberinto.camino_solucion):
                indicador.set_xy((self.laberinto.camino_solucion[frame][0][1]*self.tamaño_celda,
                                self.laberinto.camino_solucion[frame][0][0]*self.tamaño_celda))

        anim = animation.FuncAnimation(figura, animate, frames=len(self.laberinto.camino_solucion), repeat=False)

        # Mostrar la gráfica al usuario
        plt.show()

        # Manejar cualquier posible guardado
        if self.nombre_archivo_media:
            anim.save("{}.mp4".format(self.nombre_archivo_media), writer='ffmpeg', fps=60, dpi=100)

