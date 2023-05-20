import math

# Właściwości materiału
material_color = (1.0, 0.0, 0.0)  # Kolor materiału (czerwony)
ambient_color = (0.2, 0.2, 0.2)  # Kolor światła otoczenia
diffuse_color = (1.0, 1.0, 1.0)  # Kolor oświetlenia rozproszonego
specular_color = (1.0, 1.0, 1.0)  # Kolor odbicia zwierciadlanego
specular_power = 50.0  # Moc odbicia zwierciadlanego

# Pozycja źródła światła
light_position = (1.0, 1.0, 1.0)

# Pozycja obserwatora
viewer_position = (0.0, 0.0, -1.0)

def phong_illumination(normal, position):
    # Obliczanie wektora światła
    light_vector = tuple(map(lambda x, y: x - y, light_position, position))
    light_distance = math.sqrt(sum([x ** 2 for x in light_vector]))
    light_vector = tuple(map(lambda x: x / light_distance, light_vector))

    # Obliczanie wektora widza
    viewer_vector = tuple(map(lambda x, y: x - y, viewer_position, position))
    viewer_distance = math.sqrt(sum([x ** 2 for x in viewer_vector]))
    viewer_vector = tuple(map(lambda x: x / viewer_distance, viewer_vector))

    # Obliczanie składnika ambientalnego
    ambient = tuple(map(lambda x, y: x * y, ambient_color, material_color))

    # Obliczanie składnika rozproszonego
    diffuse_factor = max(0.0, sum([x * y for x, y in zip(light_vector, normal)]))
    diffuse = tuple(map(lambda x, y: x * y * diffuse_factor, diffuse_color, material_color))

    # Obliczanie składnika zwierciadlanego
    reflection_vector = tuple(map(lambda x, y: 2 * y * x, normal, light_vector))
    reflection_factor = max(0.0, sum([x * y for x, y in zip(reflection_vector, viewer_vector)]))
    specular = tuple(map(lambda x, y: x * y * (reflection_factor ** specular_power), specular_color, material_color))

    # Sumowanie składników oświetlenia
    illumination = tuple(map(lambda x, y, z: x + y + z, ambient, diffuse, specular))

    return illumination

# Przykładowe obliczenie oświetlenia dla punktu na powierzchni
normal_vector = (0.0, 0.0, 1.0)  # Normalna do powierzchni
point_position = (0.0, 0.0, 0.0)  # Pozycja punktu na powierzchni

illumination = phong_illumination(normal_vector, point_position)
print("Oświetlenie dla punktu na powierzchni:")
print("R: {:.2f}, G: {:.2f}, B: {:.2f}".format(*illumination))
