import pygame as pg
from matrix_transformations import *
from numpy import array
from math import pi

class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = array([*position, 1.0])
        self.forward = array([0, 0, 1, 1])
        self.up = array([0, 1, 0, 1])
        self.right = array([1, 0, 0, 1])
        self.h_fov = pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 0.02
        self.rotation_speed = 0.01

    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position += self.right * self.moving_speed
        if key[pg.K_d]:
            self.position -= self.right * self.moving_speed
        if key[pg.K_s]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_w]:
            self.position -= self.forward * self.moving_speed
        if key[pg.K_e]:
            self.position += self.up * self.moving_speed
        if key[pg.K_q]:
            self.position -= self.up * self.moving_speed

    def translate_matrix(self):
        x, y, z, w = self.position
        return array([
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])
    
    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return array([
            [rx, ux, fx, 0],
            [ry, uy, uz, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
    
    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()