import pygame as pg

from math import pi
from matrix_transformations import rotate_x, rotate_y, rotate_z
from numpy import array


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
        self.fov_step = pi / 18

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

        if key[pg.K_UP]:
            self.camera_xax(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_xax(self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_yax(self.rotation_speed)
        if key[pg.K_LEFT]:
            self.camera_yax(-self.rotation_speed)
        if key[pg.K_p]:
            self.camera_zax(self.rotation_speed)
        if key[pg.K_l]:
            self.camera_zax(-self.rotation_speed)

    def camera_yax(self, angle):
        rotate = rotate_y(angle=angle)
        self.fix_ratation_matrix(rotate=rotate)

    def camera_xax(self, angle):
        rotate = rotate_x(angle=angle)
        self.fix_ratation_matrix(rotate=rotate)

    def camera_zax(self, angle):
        rotate = rotate_z(angle=angle)
        self.fix_ratation_matrix(rotate=rotate)

    def fix_ratation_matrix(self, rotate):
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def translate_matrix(self):
        x, y, z, w = self.position
        return array([
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])
    
    def rotate_matrix(self):
        rx, ry, rz = self.right[:3]
        fx, fy, fz = self.forward[:3]
        ux, uy, uz = self.up[:3]
        return array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
    
    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()