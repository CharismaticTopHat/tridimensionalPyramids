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
            self.A = self.stack[-1].copy()  
        else:
            self.A = np.identity(4)


    def translate(self, tx, ty, tz):
        self.T[0][3] = tx
        self.T[1][3] = ty
        self.T[2][3] = tz
        self.M = np.matmul(self.M, self.T)
        
        
    def scale(self, sx, sy, sz):
        self.E[0][3] = sx
        self.E[1][3] = sy
        self.E[2][3] = sz
        self.M = np.matmul(self.M, self.E)
        
    def rotateZ(self, deg):
        radians = math.radians(deg)
        self.R[0][0] =  math.cos(radians)
        
        
    def rotateX(self, deg):


    def rotateY(self, deg):

        
    def print_T(self):
        print(self.T)
        
    def print_E(self):
        print(self.E)
        
    def print_R(self):
        print(self.R)
        
    def print_A(self):
        print(self.A)
        
    def rotate(self, theta, x, y, z): 

        
    def mult_Points(self, points):


    def push(self):

        
    def pop(self):

