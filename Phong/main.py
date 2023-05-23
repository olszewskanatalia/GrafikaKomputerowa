import json
import pygame
from pygame.locals import *

from phong_ball import PhongBall

WINDOW_X_SIZE = 400
WINDOW_Y_SIZE = 400

window = pygame.display.set_mode((WINDOW_X_SIZE, WINDOW_Y_SIZE))
active = True
ball = PhongBall()
table = None
refresh = True

# Mapowanie klawiszy na akcje
KEY_ACTIONS = {
    K_a: lambda: ball.move_light_pos(-1, 'x'),
    K_d: lambda: ball.move_light_pos(1, 'x'),
    K_w: lambda: ball.move_light_pos(-1, 'y'),
    K_s: lambda: ball.move_light_pos(1, 'y'),
    K_1: lambda: load_config("config.json"),
    K_2: lambda: load_config("config.json"),
    K_3: lambda: load_config("config.json"),
    K_4: lambda: load_config("config.json")
}


# Wczytaj dane konfiguracyjne z pliku config.json
def load_config(config_file):
    global table
    with open(config_file, "r") as r:
        table = json.loads(r.read())
    ball.update_colors(table)


# Obsługa zdarzeń
def handle_events():
    global active, refresh
    for event in pygame.event.get():
        if event.type == QUIT:
            active = False
        if event.type == KEYDOWN:
            if event.key in KEY_ACTIONS:
                KEY_ACTIONS[event.key]()
                refresh = True

# Odświeżanie ekranu
def refresh_screen():
    pygame.draw.rect(window, (0, 0, 0), (0, 0, WINDOW_X_SIZE, WINDOW_Y_SIZE))
    ball.create_image(window)
    pygame.display.update()

# Główna pętla programu
def main_loop():
    global active, refresh
    while active:
        handle_events()
        if refresh:
            refresh_screen()
            refresh = False

if __name__ == '__main__':
    load_config("config.json")
    main_loop()
