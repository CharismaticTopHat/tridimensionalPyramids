import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys
sys.path.append('..')
from OpMat import OpMat
from Piramide import Piramide

op3D = OpMat()
objeto1 = Piramide(op3D)
objeto2 = Piramide(op3D)

deg = 0.0
delta_deg = 1.0

pygame.init()

screen_width = 900
screen_height = 600
#vc para el obser.
FOVY=60.0
ZNEAR=1.0
ZFAR=500.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=150.0
EYE_Y=150.0
EYE_Z=150.0
CENTER_X=0
CENTER_Y=0
CENTER_Z=0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500


def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)

def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Polar 3D movement")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

def InitObj():
    sc = [10, 10, 10]
    objeto1.setScale(sc)
    objeto1.setDeltaDir([1.0, 0.0, 0.0])
    objeto1.setDeltaDeg(1.0)

Init()
InitObj()

done = False

""" def display1():
    global deg
    op3D.push()
    op3D.rotate(deg,1.0,1.0,1.0)
    op3D.translate(2.0,0.0,0.0)
    op3D.push()
    op3D.scale(2.0, 2.0, 2.0)
    objeto1.update()
    objeto1.render()
    op3D.pop()
    op3D.translate(3.0, 0.0, 0.0)
    op3D.scale(0.5, 0.5, 0.5)
    objeto1.render()
    op3D.pop() """

def display2():
    global deg
    glPushMatrix()
    glTranslatef(objeto1.pos[0],0.0,objeto1.pos[2])
    glRotatef(deg, 1.0, 1.0, 1.0)
    glPushMatrix()
    glScalef(17,17,17)
    objeto1.draw()
    glPopMatrix()
    glTranslatef(objeto1.pos[0],0.0,objeto1.pos[2])
    glScalef(5,5,5)
    objeto1.draw()
    glPopMatrix()


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    
    #display1()
    display2()
    
    if (deg < 360.0):
        deg += delta_deg
    else:
        deg = 0.0
    
    pygame.display.flip()
    pygame.time.wait(100)

pygame.quit()