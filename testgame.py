import os
import os.path
import sys

import pygame
from pygame.locals import *

from astro import SCREEN_SIZE, GROUPS, MAX_FPS, COLLIDABLE_PAIRS, CONFIG_DIR, CONFIG_ORDER
import astro.keys
from astro.configurable import load_from_yaml
from astro.ship import PlayerShip
import astro.weapon
import astro.projectile

def check_collisions():
    # TODO: Use masks, at least some of the time
    for group1, group2 in COLLIDABLE_PAIRS:
        for sprite, colliders in pygame.sprite.groupcollide(group1, group2, False, False):
            for collider in colliders:
                sprite.collide_with(collider)

def load_all():
    for d in CONFIG_ORDER:
        dirpath = os.path.join(CONFIG_DIR, d)
        for fname in os.listdir(dirpath):
            if os.path.splitext(fname)[1].lower() == '.yaml':
                load_from_yaml(os.path.join(dirpath, fname))

def set_player_ship(ship):
    astro.keys.PLAYER_SHIP = ship

def handle_input_events():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            astro.keys.keydown(event.key, event.mod)
        elif event.type == KEYUP:
            astro.keys.keyup(event.key, event.mod)
        elif event.type == pygame.QUIT:
            sys.exit()

def init_game(player_ship):
    set_player_ship(player_ship)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Astro test')
    pygame.mouse.set_visible(False)

    background = pygame.Surface(screen.get_size()).convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    pygame.display.flip()

    load_all()
    ship = PlayerShip.instance('testship')
    init_game(ship)
    ship.place()
    clock = pygame.time.Clock()

    while True:
        clock.tick(MAX_FPS)

        handle_input_events()

        check_collisions()

        for group in GROUPS:
            group.update()

        # Draw
        screen.blit(background, (0, 0))
        for group in GROUPS:
            group.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()