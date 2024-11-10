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
        self.pos = [0.0, 0.0, 0.0]
        self.delta_dir = [0.0, 0.0, 0.0]
        self.theta = 0.0
        self.delta_theta = 1.0
        self.rotAxis = [1.0, 0.0, 0.0]
        self.newDeg = lambda deg, inc_deg: (deg + inc_deg) % 360
        self.scale = [1.0,0.0,0.0]
        self.delta_scale = [0.0, 0.0, 0.0]
    
    def setPos(self, T):
        self.pos = T.copy()

    def setDeltaDir(self, deltaT):
        self.delta_dir = deltaT.copy()

    def setDeg(self, deg):
        self.theta = deg

    def setDeltaDeg(self, deltaDeg):
        self.delta_theta = deltaDeg

    def setScale(self, sc):
        self.scale = sc.copy()

    def setDeltaScale(self, deltaScale):
        self.delta_scale = deltaScale

    def update(self):
        newx = self.pos[0] + self.delta_dir[0]
        newz = self.pos[2] + self.delta_dir[2]

        if (np.abs(newx) < 150) and (np.abs(newz) < 150):
            self.pos[0] = newx
            self.pos[2] = newz
        else:
            self.pos[0] = 0.0
            self.pos[2] = 0.0
        #print("Posición X",self.pos[0], "Posición Z:",self.pos[2])
        self.theta = self.newDeg(self.theta, self.delta_theta)
    
    #funcion usada para verificar el dibujado con primitivas OpenGL    
    def draw(self):
        self.op3D.push()
        self.op3D.translate(self.pos[0], self.pos[1], self.pos[2])
        self.op3D.rotate(self.theta, 1.0, 1.0, 1.0)
        self.op3D.scale(self.scale[0], self.scale[1], self.scale[2])
        self.op3D.mult_points(self.points)
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
        self.op3D.pop()
        self.update()
        
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

    