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
        self.A = np.identity(4) #Modelado
        self.M = np.identity(4) #Matriz Acumulada
        self.stack = []
        
    def loadId(self):
        if self.stack:
            self.A = self.stack[-1]
        else:
            self.A = np.identity(4)


    def translate(self, tx, ty, tz):
        self.T = np.identity(4)
        self.T[0][3] = tx
        self.T[1][3] = ty
        self.T[2][3] = tz
        self.M = np.matmul(self.M, self.T)
        
    def scale(self, sx, sy, sz):
        self.E = np.identity(4)
        self.E[0][0] = sx
        self.E[1][1] = sy
        self.E[2][2] = sz
        self.M = np.matmul(self.M, self.E)
        
    def rotateZ(self, deg):
        radians = math.radians(deg)
        self.R= [[math.cos(radians), -math.sin(radians), 0, 0],
                 [math.sin(radians), math.cos(radians), 0, 0],
                 [0,0,1,0],
                 [0,0,0,1]]
        self.M = np.matmul(self.M, self.R)
        
    def rotateX(self, deg):
        radians = math.radians(deg)
        self.R= [[1, 0, 0, 0],
                 [0, math.cos(radians), -math.sin(radians), 0],
                 [0, math.sin(radians), math.cos(radians),0],
                 [0,0,0,1]]
        self.M = np.matmul(self.M, self.R)

    def rotateY(self, deg):
        radians = math.radians(deg)
        self.R= [[math.cos(radians), 0, math.sin(radians), 0],
                 [0, 1, 0, 0],
                 [-math.sin(radians),0,math.cos(radians),0],
                 [0,0,0,1]]
        self.M = np.matmul(self.M, self.R)
        
    def rotate(self, theta, x, y, z):
        radians = math.radians(theta)
        P1 = self.points[0]
        P2 = self.points[2]
        V = [P2[0]-P1[0], P2[1]-P1[1], P2[2]-P1[2]]
        Vdelta = math.sqrt(pow(V[0],2)+pow(V[1],2)+pow(V[2],2))
        a = V[0]/Vdelta
        b = V[1]/Vdelta
        c = V[2]/Vdelta
        d = math.sqrt(pow(b,2)+pow(c,2))

        Rx = [
            [1, 0, 0, 0],
            [0, c / d, -b / d, 0],
            [0, b / d, c / d, 0],
            [0, 0, 0, 1]
        ]
        self.M = np.matmul(self.M, Rx)

        Ry = [
            [d, 0, -a, 0],
            [0, 1, 0, 0],
            [a, 0, d, 0],
            [0, 0, 0, 1]
        ]
        self.M = np.matmul(self.M, Ry)

        Rz = [
            [math.cos(radians), -math.sin(radians), 0, 0],
            [math.sin(radians), math.cos(radians), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        self.M = np.matmul(self.M, Rz)

        Ry_inv = [
            [d, 0, a, 0],
            [0, 1, 0, 0],
            [-a, 0, d, 0],
            [0, 0, 0, 1]
        ]
        self.M = np.matmul(self.M, Ry_inv)

        Rx_inv = [
            [1, 0, 0, 0],
            [0, c / d, b / d, 0],
            [0, -b / d, c / d, 0],
            [0, 0, 0, 1]
        ]
        self.M = np.matmul(self.M, Rx_inv)

        
    def mult_Points(self, points):
        pointsNew = [np.matmul(self.M, point) for point in points]
        pointsNew = [point[:-1] for point in pointsNew]
        return pointsNew

    def push(self):
        self.stack.append(self.M.copy())
        
    def pop(self):
        if self.stack:
            self.stack.pop()
            if self.stack:
                self.M = self.stack[-1]
            else:
                self.M = np.identity(4) 
        else:
            print("Stack está vacío.")
