#Autor: Ivan Olmos Pineda

import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np

class Piramide:
    
    def __init__(self, op):
        #Se inicializa las coordenadas de los vertices del cubo
        self.points = np.array([[1.0,0.0,1.0,1.0], [1.0,0.0,-1.0,1.0], [-1.0,0.0,-1.0,1.0], [-1.0,0.0,1.0,1.0], [0.0,3.0,0.0,1.0]])
        self.op3D = op
        self.dir = []
        self.dir.append(0)
        self.dir.append(0)
        self.dir.append(0)
        
    def update(self):
        self.dir[0] = 0
    
    #funcion usada para verificar el dibujado con primitivas OpenGL    
    def draw(self):
        glBegin(GL_QUADS)
        glVertex3f(self.points[0][0],self.points[0][1],self.points[0][2])
        glVertex3f(self.points[1][0],self.points[1][1],self.points[1][2])
        glVertex3f(self.points[2][0],self.points[2][1],self.points[2][2])
        glVertex3f(self.points[3][0],self.points[3][1],self.points[3][2])        
        glEnd()
        
        glBegin(GL_LINES)
        glVertex3f(self.points[0][0],self.points[0][1],self.points[0][2])
        glVertex3f(self.points[4][0],self.points[4][1],self.points[4][2])
        glEnd() 
        glBegin(GL_LINES)
        glVertex3f(self.points[1][0],self.points[1][1],self.points[1][2])
        glVertex3f(self.points[4][0],self.points[4][1],self.points[4][2])
        glEnd()            
        glBegin(GL_LINES)
        glVertex3f(self.points[2][0],self.points[2][1],self.points[2][2])
        glVertex3f(self.points[4][0],self.points[4][1],self.points[4][2])
        glEnd()            
        glBegin(GL_LINES)
        glVertex3f(self.points[3][0],self.points[3][1],self.points[3][2])
        glVertex3f(self.points[4][0],self.points[4][1],self.points[4][2])
        glEnd()    
        
    def render(self):
        pointsR = self.points.copy()
        self.op3D.mult_Points(pointsR)
        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_QUADS)
        glVertex3f(pointsR[0][0],pointsR[0][1],pointsR[0][2])
        glVertex3f(pointsR[1][0],pointsR[1][1],pointsR[1][2])
        glVertex3f(pointsR[2][0],pointsR[2][1],pointsR[2][2])
        glVertex3f(pointsR[3][0],pointsR[3][1],pointsR[3][2])        
        glEnd()
        
        glBegin(GL_LINES)
        glVertex3f(pointsR[0][0],pointsR[0][1],pointsR[0][2])
        glVertex3f(pointsR[4][0],pointsR[4][1],pointsR[4][2])
        glEnd() 
        glBegin(GL_LINES)
        glVertex3f(pointsR[1][0],pointsR[1][1],pointsR[1][2])
        glVertex3f(pointsR[4][0],pointsR[4][1],pointsR[4][2])
        glEnd()            
        glBegin(GL_LINES)
        glVertex3f(pointsR[2][0],pointsR[2][1],pointsR[2][2])
        glVertex3f(pointsR[4][0],pointsR[4][1],pointsR[4][2])
        glEnd()            
        glBegin(GL_LINES)
        glVertex3f(pointsR[3][0],pointsR[3][1],pointsR[3][2])
        glVertex3f(pointsR[4][0],pointsR[4][1],pointsR[4][2])
        glEnd()    

    