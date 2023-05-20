import pygame as pg

from camera import Camera
from numpy import array
from object_3d import Object3D
from projection import Projection


class SoftwareRender:
    def __init__(self) -> None:
        self.RESOLUTION = self.WIDTH, self.HEIGHT = 1400, 750
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(size=self.RESOLUTION)
        self.clock = pg.time.Clock()
        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [1.5, 1.5, -10])
        self.projection = Projection(self)
        vertexes_blue = array([
            (0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1),
            (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)
        ])
        vertexes_red = array([
            (0, 1.5, 0, 1), (0, 2.5, 0, 1), (1, 2.5, 0, 1), (1, 1.5, 0, 1),
            (0, 1.5, 1, 1), (0, 2.5, 1, 1), (1, 2.5, 1, 1), (1, 1.5, 1, 1)
        ])
        vertexes_green = array([
            (1.5, 1.5, 0, 1), (1.5, 2.5, 0, 1), (2.5, 2.5, 0, 1), (2.5, 1.5, 0, 1),
            (1.5, 1.5, 1, 1), (1.5, 2.5, 1, 1), (2.5, 2.5, 1, 1), (2.5, 1.5, 1, 1)
        ])
        vertexes_yellow = array([
            (1.5, 0, 0, 1), (1.5, 1, 0, 1), (2.5, 1, 0, 1), (2.5, 0, 0, 1),
            (1.5, 0, 1, 1), (1.5, 1, 1, 1), (2.5, 1, 1, 1), (2.5, 0, 1, 1)
        ])

        vertexes_orange = array([
            (0, 0, 1.5, 1), (0, 1, 1.5, 1), (1, 1, 1.5, 1), (1, 0, 1.5, 1),
            (0, 0, 2.5, 1), (0, 1, 2.5, 1), (1, 1, 2.5, 1), (1, 0, 2.5, 1)
        ])

        vertexes_pink = array([
            (0, 1.5, 1.5, 1), (0, 2.5, 1.5, 1), (1, 2.5, 1.5, 1), (1, 1.5, 1.5, 1),
            (0, 1.5, 2.5, 1), (0, 2.5, 2.5, 1), (1, 2.5, 2.5, 1), (1, 1.5, 2.5, 1)
        ])
        vertexes_brown = array([
            (1.5, 1.5, 1.5, 1), (1.5, 2.5, 1.5,
                                 1), (2.5, 2.5, 1.5, 1), (2.5, 1.5, 1.5, 1),
            (1.5, 1.5, 2.5, 1), (1.5, 2.5, 2.5,
                                 1), (2.5, 2.5, 2.5, 1), (2.5, 1.5, 2.5, 1)
        ])
        vertexes_violet = array([
            (1.5, 0, 1.5, 1), (1.5, 1, 1.5, 1), (2.5, 1, 1.5, 1), (2.5, 0, 1.5, 1),
            (1.5, 0, 2.5, 1), (1.5, 1, 2.5, 1), (2.5, 1, 2.5, 1), (2.5, 0, 2.5, 1)
        ])

        self.object_blue = Object3D(self, vertexes_blue, pg.Color('blue'))
        self.object_red = Object3D(self, vertexes_red, pg.Color('red'))
        self.object_green = Object3D(self, vertexes_green, pg.Color('green'))
        self.object_yellow = Object3D(
            self, vertexes_yellow, pg.Color('yellow'))
        self.object_orange = Object3D(
            self, vertexes_orange, pg.Color('orange'))
        self.object_pink = Object3D(
            self, vertexes_pink, pg.Color('pink'))
        self.object_brown = Object3D(
            self, vertexes_brown, pg.Color('brown'))
        self.object_violet = Object3D(
            self, vertexes_violet, pg.Color('violet'))

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.object_blue.draw()
        self.object_red.draw()
        self.object_green.draw()
        self.object_yellow.draw()
        self.object_orange.draw()
        self.object_pink.draw()
        self.object_brown.draw()
        self.object_violet.draw()

    def run(self):
        while True:
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()  # update full surface of the screen
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    SoftwareRender().run()
