import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sys

filename = "cow.obj"

def load_obj(filename):
    vertices = []
    faces = []
    with open(filename) as f:
        for line in f:
            if line.startswith("v "):
                vertex = list(map(float, line.split()[1:]))
                vertices.append(vertex)
            elif line.startswith("f "):
                face = [int(i.split("/")[0]) - 1 for i in line.split()[1:]]
                faces.append(face)
    return vertices, faces

def draw_obj(vertices, faces):
    white = (1.0, 1.0, 1.0)
    black = (0.0, 0.0, 0.0)
    is_white = True
    for face in faces:
        for vertex_id in face:
            glColor3fv(white if is_white else black)
            is_white = not is_white
            glBegin(GL_TRIANGLES)
            for vertex_id in face:
                glVertex3fv(vertices[vertex_id])
            glEnd()

def init(width_size, height_size):
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(100.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width_size) / float(height_size), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def display(vertices, faces, zoom, x_rotation, y_rotation, x_offset, y_offset):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(x_offset, y_offset, -zoom)
    glRotatef(x_rotation, 1.0, 0.0, 0.0)
    glRotatef(y_rotation, 0.0, 1.0, 0.0)
    draw_obj(vertices, faces)
    pygame.display.flip()

def main():
    pygame.init()
    width_size, height_size = 1200, 800
    screen = pygame.display.set_mode((width_size, height_size), pygame.OPENGL | pygame.DOUBLEBUF)
    init(width_size, height_size)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    vertices, faces = load_obj("cow.obj")
    zoom = 20.0
    x_rotation = 0.0
    y_rotation = 0.0
    x_offset = 0.0
    y_offset = 0.0
    is_arrow_key_pressed = False
    mouse_down = False
    prev_pos = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    zoom -= 1.0
                elif event.button == 5:  # Scroll down
                    zoom += 1.0
                elif event.button == 1:  # Left click
                    mouse_down = True
                    prev_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click
                    mouse_down = False
            elif event.type == pygame.MOUSEMOTION and mouse_down:
                curr_pos = pygame.mouse.get_pos()
                dx, dy = curr_pos[0] - prev_pos[0], curr_pos[1] - prev_pos[1]
                if pygame.mouse.get_pressed()[0]:
                    #x_rotation += dy * 0.1
                    #y_rotation += dx * 0.1
                    x_offset += dx * 0.01
                    y_offset -= dy * 0.01
                    prev_pos = curr_pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    is_arrow_key_pressed = True
                    x_rotation -= 15.0
                elif event.key == pygame.K_DOWN:
                    is_arrow_key_pressed = True
                    x_rotation += 15.0
                elif event.key == pygame.K_LEFT:
                    is_arrow_key_pressed = True
                    y_rotation -= 15.0
                elif event.key == pygame.K_RIGHT:
                    is_arrow_key_pressed = True
                    y_rotation += 15.0
            elif event.type == pygame.KEYUP:
                # Reset the boolean variable when an arrow key is released
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    is_arrow_key_pressed = False
        if is_arrow_key_pressed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                x_rotation -= 5.0
            elif keys[pygame.K_DOWN]:
                x_rotation += 5.0
            elif keys[pygame.K_LEFT]:
                y_rotation -= 5.0
            elif keys[pygame.K_RIGHT]:
                y_rotation += 5.0
        display(vertices, faces, zoom, x_rotation, y_rotation, x_offset, y_offset)

if __name__ == "__main__":
    main()
