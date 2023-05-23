import math
import threading

import pygame
from pygame import Surface


class PhongBall:
    def __init__(self, width=400, height=400):
        self.eye = [0, 0, 200]
        self.light_col = [0.27, 0.50, 0.70]
        self.light_pos = [200, 400, 500]

        self.width = width
        self.height = height

        self.radius = min(width, height) / 3
        self.center_x = width / 2
        self.center_y = height / 2
        self.center = [self.center_x, self.center_y, 0]

    def create_image(self, window: Surface):
        num_threads = 10
        step = self.width * 2 // num_threads

        threads = []
        for i in range(num_threads):
            start_x = -self.width + i * step
            end_x = -self.width + (i + 1) * step

            thread = threading.Thread(
                target=self.process_points, args=(window, start_x, end_x)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def process_points(self, window: Surface, start_x, end_x):
        for x in range(start_x, end_x):
            for y in range(-self.height, self.height):
                dist = math.sqrt(x ** 2 + y ** 2)
                if dist < self.radius:
                    z = math.sqrt(self.radius ** 2 - dist ** 2)
                    point = [x + self.center_x, y + self.center_y, z]

                    normal = self.__between_uv(self.center, point)
                    viewer = self.__between_uv(point, self.eye)
                    light = self.__between_uv(point, self.light_pos)

                    reflection = self.__uv(self.__reflect_vector(light, normal))

                    illumination = self.__arr_sum(
                        [
                            self.__ambient(),
                            self.__diffuse(light, normal),
                            self.__specular(reflection, viewer, self.spec_pow),
                        ]
                    )

                    color = list(int(self.__normalize(x) * 255) for x in illumination)
                    pygame.draw.rect(
                        window, color, (x + self.center_x, y + self.center_y, 1, 1)
                    )

    def move_light_pos(self, direction, axis):
        pos = 0 if axis == "x" else 1
        self.light_pos[pos] += direction * 50

    def update_colors(self, table):
        self.k_a = table["k_a"]
        self.k_d = table["k_d"]
        self.k_s = table["k_s"]
        self.spec_pow = table["spec_pow"]
        self.light_col = table["light_col"]

    def __ambient(self):
        return [ka * lc for ka, lc in zip(self.k_a, self.light_col)]

    def __diffuse(self, light_vector, normal_vector):
        diffuse = max(0.0, self.__multiply_vector(light_vector, normal_vector))
        return [kd * lc * diffuse for kd, lc in zip(self.k_d, self.light_col)]

    def __specular(self, reflect: list, vis: list, pow_elem: float):
        result = []
        for i in range(3):
            result.append(
                math.pow(max(0.0, self.__multiply_vector(reflect, vis)), pow_elem)
                * self.k_s[i]
                * self.light_col[i]
            )
        return result

    def __reflect_vector(self, light_vector, normal_vector):
        l_dot = self.__multiply_vector(light_vector, normal_vector)
        return [(2 * l_dot * normal_vector[i]) - light_vector[i] for i in range(3)]

    def __between_uv(self, vector_1, vector_2):
        result = []
        if len(vector_1) != len(vector_2) != 3:
            raise ValueError
        for i in range(3):
            result.append(vector_2[i] - vector_1[i])
        return self.__uv(result)

    @staticmethod
    def __arr_sum(array):
        return [sum(elements) for elements in zip(*array)]

    @staticmethod
    def __multiply_vector(vector_1, vector_2):
        return sum(v1 * v2 for v1, v2 in zip(vector_1, vector_2))

    @staticmethod
    def __normalize(value: float) -> float:
        return max(0, min(1, value))

    @staticmethod
    def __uv(vector):
        result = []
        if len(vector) != 3:
            raise ValueError
        vector_mag = math.sqrt(
            math.pow(vector[0], 2) + math.pow(vector[1], 2) + math.pow(vector[2], 2)
        )
        for i in range(3):
            result.append(vector[i] / vector_mag)
        return result
