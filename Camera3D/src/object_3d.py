import pygame as pg

from matrix_transformations import (
    rotate_x, 
    rotate_y, 
    rotate_z, 
    scale, 
    translate
)
from numpy import any, array


class Object3D:
    def __init__(self, render, vertexes, color):
        self.render = render
        self.vertexes = vertexes
        self.faces = array([
            (0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 7, 3), 
            (1, 5, 6, 2), (0, 1, 5, 4), (3, 2, 6, 7)
        ])
        self.color = color

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]

        for face in self.faces:
            polygon = vertexes[face]
            if not any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, self.color, polygon, 3)

        for vertex in vertexes:
            if not any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)):
                pg.draw.circle(self.render.screen, self.color, vertex, 6)

    def translate(self, pos):
        self.vertexes = self.vertexes @ translate(pos)

    def scale(self, scale_to):
        self.vertexes = self.vertexes @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertexes = self.vertexes @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertexes = self.vertexes @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertexes = self.vertexes @ rotate_z(angle)
