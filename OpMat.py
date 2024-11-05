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


    def translate(self, tx, ty, tz):

        
    def scale(self, sx, sy, sz):

        
    def rotateZ(self, deg):

        
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

