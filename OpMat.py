#Autor: Ivan Olmos Pineda

import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

#import random
import math
import numpy as np

class OpMat:
    
    def __init__(self):
        #Se inicializa las coordenadas de los vertices del cubo
        self.T = np.identity(4) #Traslación
        self.R = np.identity(4) #Rotación
        self.E = np.identity(4) #Escalado
        self.M = np.identity(4) #Matriz Acumulada
        self.stack = []
        
    def loadId(self):
        if self.stack:
            self.M = self.stack[-1].copy()  
        else:
            self.M = np.identity(4)

    def translate(self, tx, ty, tz):
        self.T = np.identity(4)
        self.T[0][3] = tx
        self.T[1][3] = ty
        self.T[2][3] = tz
        #print(self.T)
        self.M = np.matmul(self.M, self.T)
        
    def scale(self, sx, sy, sz):
        self.E=np.identity(4)
        self.E[0][0] = sx
        self.E[1][1] = sy
        self.E[2][2] = sz
        #print(self.E)
        self.M = np.matmul(self.M, self.E)
        
    def rotateZ(self, deg):
        radians = math.radians(deg)
        self.R = np.identity(4)
        self.R[0][0] = math.cos(radians)
        self.R[0][1] = -math.sin(radians)
        self.R[1][0] = math.sin(radians)
        self.R[1][1] = math.cos(radians)
        #print(self.R)
        self.M = np.matmul(self.M, self.R)
        
    def rotateX(self, deg):
        radians = math.radians(deg)
        self.R = np.identity(4)
        self.R[1][1] = math.cos(radians)
        self.R[1][2] = -math.sin(radians)
        self.R[2][1] = math.sin(radians)
        self.R[2][2] = math.cos(radians)
        #print(self.R)
        self.M = np.matmul(self.M, self.R)

    def rotateY(self, deg):
        radians = math.radians(deg)
        self.R[0][0] = math.cos(radians)
        self.R[0][2] = -math.sin(radians)
        self.R[2][0] = math.sin(radians)
        self.R[2][2] = math.cos(radians)
        #print(self.R)
        self.M = np.matmul(self.M, self.R)
        
    def print_T(self):
        print(self.T)
        
    def print_E(self):
        print(self.E)
        
    def print_R(self):
        print(self.R)
        
    def print_A(self):
        print(self.A)
        
    def rotate(self, theta, x, y, z):
        radians = np.radians(theta)
        c = np.cos(radians)
        s = np.sin(radians)
        t = 1 - c
        mag = np.sqrt(x**2 + y**2 + z**2)
        x /= mag
        y /= mag
        z /= mag

        # Rotation matrix around arbitrary axis (x, y, z)
        R = np.array([
            [t * x * x + c, t * x * y - s * z, t * x * z + s * y, 0],
            [t * x * y + s * z, t * y * y + c, t * y * z - s * x, 0],
            [t * x * z - s * y, t * y * z + s * x, t * z * z + c, 0],
            [0, 0, 0, 1]
        ])
        
        self.M = np.matmul(self.M, R)
        
    def mult_Points(self, points):
        vertexR = [np.matmul(self.M, vert) for vert in points]
        vertexR = [point[:-1] for point in vertexR]
        #print(vertexR)
        return vertexR

    def push(self):
        self.stack.append(self.M.copy())

        
    def pop(self):
        if self.stack:
            self.stack.pop(0)
            if self.stack:
                self.M = self.stack[-1]
            else:
                self.M = np.identity(4) 