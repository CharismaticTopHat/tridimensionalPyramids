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
        if x == 1 and y ==0 and z == 0:
            self.rotateX(theta)
        elif x == 0 and y == 1 and z == 0:
            self.rotateY(theta)
        elif x == 0 and y == 0 and z == 1:
            self.rotateZ(theta)
        else:
            radians = math.radians(theta)
            magnitude = math.sqrt(((x**2)+(y**2)+(z**2)))
            a = x/magnitude
            b = y/magnitude
            c = z/magnitude
            d = math.sqrt(((b**2)+(c**2)))
            
            cos_theta = math.cos(radians)
            sin_theta = math.sin(radians)

            a_2 = a*a
            b_2 = b*b
            c_2 = c*c
            d_2 = d*d
            
            self.M = [[((d_2*cos_theta)+a_2), (b*a*(-cos_theta+1)-(c*sin_theta)), (b*sin_theta+(c*a)*(-cos_theta+1)), 0],
                      [((c*sin_theta)-((b*a)*(cos_theta))+b*a), (((c_2*cos_theta)+(b_2*a_2*cos_theta)+a_2*b_2))/d_2, ((c*((d_2*b)-a*(c*sin_theta-b*a*cos_theta))-b*(c*cos_theta+b*a*sin_theta)))/d_2, 0],
                      [-b*sin_theta-c*a*cos_theta+c*a, (c*((c*a*sin_theta)-b*cos_theta)+b*(c*d_2-a*(-b*sin_theta-c*a*cos_theta)))/d_2, (b_2*cos_theta+c_2*a_2*cos_theta+c_2*d_2)/d_2, 0],
                      [0,0,0,1]
                      ]
            
            self.A = self.A @ self.M

        
    def mult_points(self, points):
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
