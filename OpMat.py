# Autor: Ivan Olmos Pineda

import pygame
from pygame.locals import *

# Bibliotecas de OpenGL para manejar gráficos 3D
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import numpy as np

class OpMat:
    """
    Clase para manejar transformaciones matriciales en gráficos 3D.
    Permite realizar operaciones de traslación, rotación, y escalado, 
    así como mantener un estado acumulado de las transformaciones.
    """

    def __init__(self):
        """
        Inicializa las matrices de transformación y la pila de estados.
        - T: Matriz de traslación.
        - R: Matriz de rotación.
        - E: Matriz de escalado.
        - M: Matriz acumulada.
        - stack: Pila para guardar estados anteriores de la matriz acumulada.
        """
        self.T = np.identity(4)  # Matriz de traslación
        self.R = np.identity(4)  # Matriz de rotación
        self.E = np.identity(4)  # Matriz de escalado
        self.M = np.identity(4)  # Matriz acumulada
        self.stack = []  # Pila de estados

    def identity(self):
        """Restaura la matriz de OpenGL al estado de identidad."""
        glLoadIdentity()

    def loadId(self):
        """Restaura la matriz acumulada desde la pila o la reinicia."""
        if self.stack:
            self.M = self.stack[-1].copy()
        else:
            self.M = np.identity(4)

    def translate(self, tx, ty, tz):
        """
        Realiza una traslación en el espacio tridimensional.
        - tx, ty, tz: Desplazamientos en los ejes X, Y y Z respectivamente.
        """
        self.T = np.identity(4)  # Reinicia la matriz de traslación
        self.T[0][3] = tx  # Traslación en X
        self.T[1][3] = ty  # Traslación en Y
        self.T[2][3] = tz  # Traslación en Z
        self.M = np.matmul(self.M, self.T)  # Aplica la traslación acumulativa

    def scale(self, sx, sy, sz):
        """
        Realiza un escalado en el espacio tridimensional.
        - sx, sy, sz: Factores de escalado en los ejes X, Y y Z respectivamente.
        """
        self.E = np.identity(4)  # Reinicia la matriz de escalado
        self.E[0][0] = sx  # Escala en X
        self.E[1][1] = sy  # Escala en Y
        self.E[2][2] = sz  # Escala en Z
        self.M = np.matmul(self.M, self.E)  # Aplica el escalado acumulativo

    def rotateZ(self, deg):
        """
        Realiza una rotación alrededor del eje Z.
        - deg: Ángulo en grados.
        """
        radians = math.radians(deg)
        self.R = np.identity(4)  # Reinicia la matriz de rotación
        self.R[0][0] = math.cos(radians)
        self.R[0][1] = -math.sin(radians)
        self.R[1][0] = math.sin(radians)
        self.R[1][1] = math.cos(radians)
        self.M = np.matmul(self.M, self.R)  # Aplica la rotación acumulativa

    def rotateX(self, deg):
        """
        Realiza una rotación alrededor del eje X.
        - deg: Ángulo en grados.
        """
        radians = math.radians(deg)
        self.R = np.identity(4)
        self.R[1][1] = math.cos(radians)
        self.R[1][2] = -math.sin(radians)
        self.R[2][1] = math.sin(radians)
        self.R[2][2] = math.cos(radians)
        self.M = np.matmul(self.M, self.R)

    def rotateY(self, deg):
        """
        Realiza una rotación alrededor del eje Y.
        - deg: Ángulo en grados.
        """
        radians = math.radians(deg)
        self.R = np.identity(4)
        self.R[0][0] = math.cos(radians)
        self.R[0][2] = -math.sin(radians)
        self.R[2][0] = math.sin(radians)
        self.R[2][2] = math.cos(radians)
        self.M = np.matmul(self.M, self.R)

    def rotate(self, theta, x, y, z):
        """
        Realiza una rotación alrededor de un eje arbitrario.
        - theta: Ángulo en grados.
        - x, y, z: Coordenadas del eje de rotación.
        """
        radians = np.radians(theta)
        c = np.cos(radians)
        s = np.sin(radians)
        t = 1 - c
        mag = np.sqrt(x**2 + y**2 + z**2)  # Normalización del eje
        x /= mag
        y /= mag
        z /= mag

        # Matriz de rotación alrededor del eje (x, y, z)
        R = np.array([
            [t * x * x + c, t * x * y - s * z, t * x * z + s * y, 0],
            [t * x * y + s * z, t * y * y + c, t * y * z - s * x, 0],
            [t * x * z - s * y, t * y * z + s * x, t * z * z + c, 0],
            [0, 0, 0, 1]
        ])
        self.M = np.matmul(self.M, R)

    def mult_Points(self, points):
        """
        Multiplica un conjunto de puntos por la matriz acumulada.
        - points: Lista de puntos representados como matrices.
        """
        vertexR = [np.matmul(self.M, vert) for vert in points]  # Transformación
        vertexR = [point[:-1] for point in vertexR]  # Elimina la coordenada W
        return vertexR

    def push(self):
        """
        Guarda el estado actual de la matriz acumulada en la pila.
        """
        self.stack.append(self.M.copy())

    def pop(self):
        """
        Restaura el estado previo de la matriz acumulada desde la pila.
        """
        if self.stack:
            self.stack.pop()  # Elimina el estado más reciente
            if self.stack:
                self.M = self.stack[-1]  # Restaura el último estado
            else:
                self.M = np.identity(4)  # Reinicia si la pila está vacía