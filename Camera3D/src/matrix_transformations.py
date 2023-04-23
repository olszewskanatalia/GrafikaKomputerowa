from math import cos, sin
from numpy import array


def translate(pos):
    tx, ty, tz = pos
    return array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1 ,0],
        [tx, ty, tz, 1]
    ])


def rotate_x(angle):
    return array([
        [1, 0, 0, 0],
        [0, cos(angle), sin(angle), 0],
        [0, -sin(angle), cos(angle), 0],
        [0, 0, 0, 1]
    ])


def rotate_y(angle):
    return array([
        [cos(angle), 0, -sin(angle), 0],
        [0, 1, 0, 0],
        [sin(angle), 0, cos(angle), 0],
        [0, 0, 0, 1]
    ])


def rotate_z(angle):
    return array([
        [cos(angle), sin(angle), 0, 0],
        [-sin(angle), cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def scale(n):
    return array([
        [n, 0, 0, 0],
        [0, n, 0, 0],
        [0, 0, n, 0],
        [0, 0, 0, 1]
    ])