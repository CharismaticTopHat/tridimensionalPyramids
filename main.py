import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys
import math
sys.path.append('..')
from OpMat import OpMat  # Clase para manejar operaciones matriciales
from Piramide import Piramide  # Clase que representa una pirámide 3D

# Inicialización de objetos para operaciones 3D y las pirámides
op3D = OpMat()
objeto1 = Piramide(op3D)
objeto2 = Piramide(op3D)

# Variables globales para animación
deg = 0.0  # Ángulo de rotación
pos = 0.0  # Posición en el eje Y
r = 0.0  # Radio de órbita
delta_deg = 1.0  # Incremento de rotación por frame

# Inicialización de pygame
pygame.init()

# Dimensiones de la ventana
screen_width = 900
screen_height = 600

# Parámetros de cámara
FOVY = 60.0
ZNEAR = 1.0
ZFAR = 500.0

# Posición y orientación del observador
EYE_X, EYE_Y, EYE_Z = 10.0, 10.0, 10.0  # Posición de la cámara
CENTER_X, CENTER_Y, CENTER_Z = 0, 0, 0  # Centro al que apunta
UP_X, UP_Y, UP_Z = 0, 1, 0  # Dirección "arriba" del sistema

# Límites de los ejes del sistema de coordenadas
X_MIN, X_MAX = -500, 500
Y_MIN, Y_MAX = -500, 500
Z_MIN, Z_MAX = -500, 500


def Axis():
    """
    Dibuja los ejes coordenados X, Y, Z en colores rojo, verde y azul respectivamente.
    """
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    
    # Eje X en rojo
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN, 0.0, 0.0)
    glVertex3f(X_MAX, 0.0, 0.0)
    glEnd()
    
    # Eje Y en verde
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, Y_MIN, 0.0)
    glVertex3f(0.0, Y_MAX, 0.0)
    glEnd()
    
    # Eje Z en azul
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, Z_MIN)
    glVertex3f(0.0, 0.0, Z_MAX)
    glEnd()

    glLineWidth(1.0)


def Init():
    """
    Inicializa OpenGL y configura la ventana de visualización.
    """
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Ejes 3D")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)  # Color de fondo negro
    glEnable(GL_DEPTH_TEST)  # Habilita pruebas de profundidad

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # Dibujo de polígonos en modo wireframe


# Llama a la función de inicialización
Init()

done = False


def display1():
    """
    Dibuja dos pirámides con transformaciones y animación.
    """
    global deg

    # Primera pirámide (con órbita y rotación)
    op3D.push()
    op3D.rotate(deg, 0.0, 1.0, 0.0)  # Rotación en órbita
    op3D.translate(5.0, 0.0, 0.0)   # Distancia desde el centro
    op3D.rotate(deg * 5, 0.0, 1.0, 0.0)
    op3D.scale(1.0, 1.0, 1.0)       # Escala de la pirámide
    objeto1.render()

    # Segunda pirámide pequeña como satélite
    op3D.push()
    op3D.rotateX(180)
    op3D.rotate(deg * 20, 0.0, 1.0, 0.0)
    op3D.translate(0.5, -3.0, 0.0)
    op3D.rotate(deg * -30, 0.0, 1.0, 0.0)
    op3D.scale(0.2, 0.2, 0.2)
    objeto2.render()
    op3D.pop()
    op3D.pop()


def display2():
    """
    Dibuja una pirámide con rotación y escalado en el espacio.
    """
    global deg
    glPushMatrix()
    glRotatef(deg, 1.0, 1.0, 1.0)  # Rotación combinada
    glTranslatef(2.0, 0.0, 0.0)

    glPushMatrix()
    glScalef(2.0, 2.0, 2.0)  # Escalado uniforme
    objeto1.draw()
    glPopMatrix()

    glTranslatef(3.0, 0.0, 0.0)
    glScalef(0.5, 0.5, 0.5)  # Escalado reducido
    objeto1.draw()
    glPopMatrix()


def display3():
    """
    Dibuja un objeto con movimiento hacia adelante y rotación.
    """
    global deg, pos, r

    op3D.push()
    op3D.rotateZ(270)
    op3D.rotate(deg * 10, 0.0, 1.0, 0.0)

    theta = deg * (math.pi / 180)  # Conversión a radianes
    x = r * math.cos(theta)
    z = r * math.sin(theta)

    op3D.translate(x, pos, z)
    op3D.rotate(deg * 50, 0.0, 1.0, 0.0)  # Rotación propia del objeto
    op3D.scale(0.8, 0.8, 0.8)            # Escalado menor
    objeto1.render()
    op3D.pop()

    # Actualización de posición y reinicio si se pasa de límites
    pos += 0.8
    r += 0.05
    if pos > 15.0:
        pos = -90.0
        r = 0.0


while not done:
    """
    Bucle principal de animación.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    display1()
    display2()
    display3()

    deg = deg + delta_deg if deg < 360.0 else 0.0

    pygame.display.flip()
    pygame.time.wait(100)

# Finaliza pygame
pygame.quit()