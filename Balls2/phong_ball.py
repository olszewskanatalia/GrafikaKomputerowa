import math
import random

import pygame
from pygame import Surface


class PhongBall:
    def __init__(self, width=400, height=400):
        self.__default()

        self.eye = [0, 0, 200]
        self.light_col = [0.27, 0.50, 0.70]
        self.light_pos = [200, 400, 500]

        self.width = width
        self.height = height

        self.radius = min(width, height) / 3
        self.center_x = width / 2
        self.center_y = height / 2

    def create_image(self, window: Surface):
        for x in range(-self.width, self.width):
            for y in range(-self.height, self.height):
                dist = math.sqrt(x ** 2 + y ** 2)
                if dist < self.radius:
                    z = math.sqrt(self.radius ** 2 - dist ** 2)

                    center = [self.center_x, self.center_y, 0]
                    point = [x + self.center_x, y + self.center_y, z]

                    normal = self.__between_uv(center, point)
                    viewer = self.__between_uv(point, self.eye)

                    light = self.__between_uv(point, self.light_pos)

                    reflection = self.__uv(self.__reflect_vector(light, normal))

                    amb_rgb = self.__ambient()
                    diff_rgb = self.__diffuse(light, normal)

                    spec_rgb = self.__specular(reflection, viewer, self.spec_pow)

                    illumination = self.__arr_sum([amb_rgb, diff_rgb, spec_rgb])

                    color = (
                        int(self.__normalize(illumination[0]) * 255),
                        int(self.__normalize(illumination[1]) * 255),
                        int(self.__normalize(illumination[2]) * 255)
                    )
                    pygame.draw.line(window, color, (x + self.center_x, y + self.center_y),
                                     (x + self.center_x, y + self.center_y))

    def __ambient(self) -> [float, float, float]:
        result = []
        for i in range(3):
            result.append(self.k_a[i] * self.light_col[i])
        return result

    def __diffuse(self, light_vector: list, normal_vector: list) -> [float, float, float]:
        result = []
        diffuse = max(0.0, self.__multiply_vector(light_vector, normal_vector))
        for i in range(3):
            result.append(self.k_d[i] * self.light_col[i] * diffuse)
        return result

    def __specular(self, reflect: list, vis: list, pow_elem: float):
        result = []
        for i in range(3):
            result.append(
                math.pow(max(0.0, self.__multiply_vector(reflect, vis)), pow_elem) * self.k_s[i] * self.light_col[i])
        return result

    def __reflect_vector(self, light_vector: list, normal_vector: list) -> [float, float, float]:
        result = []
        l_dot = self.__multiply_vector(light_vector, normal_vector)
        for i in range(3):
            result.append((2 * l_dot * normal_vector[i]) - light_vector[i])

        return result

    @staticmethod
    def __normalize(value: float) -> float:
        if value > 1:
            return 1
        if value < 0:
            return 0
        return value

    @staticmethod
    def __uv(vector: list) -> [float, float, float]:
        result = []
        if len(vector) != 3:
            raise ValueError
        vector_mag = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2) + math.pow(vector[2], 2))
        for i in range(3):
            result.append(vector[i] / vector_mag)
        return result

    def __between_uv(self, vector_1: list, vector_2: list) -> [float, float, float]:
        result = []
        if len(vector_1) != len(vector_2) != 3:
            raise ValueError
        for i in range(3):
            result.append(vector_2[i] - vector_1[i])
        return self.__uv(result)

    @staticmethod
    def __arr_sum(array: list) -> [float, float, float]:
        result = []
        for i in range(3):
            result.append(0.0)
            for j in range(len(array)):
                result[i] += array[j][i]
        return result

    @staticmethod
    def __multiply_vector(vector_1: list, vector_2: list) -> float:
        result = 0
        if len(vector_1) != len(vector_2) != 3:
            raise ValueError
        for i in range(len(vector_1)):
            result += vector_1[i] * vector_2[i]
        return result

    def move_light_pos_x(self, direction):
        self.light_pos[0] += direction * 50

    def move_light_pos_y(self, direction):
        self.light_pos[1] += direction * 50

    def change_material(self, option: int):
        if option == 0:
            self.__wood()
        elif option == 1:
            self.__default()
        elif option == 2:
            self.__random()

    def __wood(self):
        self.k_a = [1.000000, 1.000000, 1.000000]
        self.k_d = [0.640000, 0.640000, 0.640000]
        self.k_s = [0.500000, 0.500000, 0.500000]
        self.spec_pow = 100

    def __default(self):
        self.k_a = [0.49, 0.473, 0.422]
        self.k_d = [0.90, 0.97, 0.98]
        self.k_s = [0.956, 0.937, 0.986]
        self.spec_pow = 3

    def __random(self):
        self.k_a = [random.randint(1, 2000) / 2000, random.randint(1, 2000) / 2000, random.randint(1, 2000) / 2000]
        self.k_d = [random.randint(1, 2000) / 2000, random.randint(1, 2000) / 2000, random.randint(1, 2000) / 2000]
        self.k_s = [random.randint(1, 2000) / 2000, random.randint(1, 2000) / 2000, random.randint(1, 2000) / 2000]
        self.spec_pow = random.randint(1, 10)

        self.light_col = [random.randint(1, 2000) / 2000, random.randint(1, 2000) / 2000,
                          random.randint(1, 2000) / 2000]

    def update_colors(self, table):
        self.k_a = table["k_a"]
        self.k_d = table["k_d"]
        self.k_s = table["k_s"]
        self.spec_pow = table["spec_pow"]
        self.light_col = table["light_col"]