# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     19-12-2017
 Description:
----------------------------------------------------------"""


import pygame

from game_map import Map
from char_classes import Player
from hud import Hud
from _enums import *

# ------------------------------ CONST ------------------------------------- #

DISPLAY_SIZE = (1024, 768)
FPS = 183
DOUBLE = True
MAP_PATH = 'map.json'
TILESET_PATH = "tilesets/TILES.png"
CHARACTER_TILESET = 'chars/captain.png'

HUD_START_COORDS = (-13, 596, 497, 183)


DEBUG = True
DEBUG_COLOR = pygame.Color(0, 250, 0)

# ================================ MAIN ==================================== #


class Main(object):
    """ This is a game application.
    What could I say more?
    """
    def __init__(self):
        """ Init.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(DISPLAY_SIZE)

        if DEBUG:
            self.debug_text = pygame.font.SysFont('Comic Sans MS', 20)

        self.timer = pygame.time.Clock()

        self.game_map = Map(
            map_path=MAP_PATH,
            tileset_path=TILESET_PATH,
            display_size_tuple=DISPLAY_SIZE,
            scale=2 if DOUBLE else 1)

        x, y = self.game_map.get_first_walkable_cell_coords()
        self.player = Player(x, y, CHARACTER_TILESET,
                             scale=2 if DOUBLE else 1,
                             display_size=DISPLAY_SIZE)
        self.game_map.make_bottom_buffer(self.player.get_camera_pos())

        self.hud = Hud(HUD_START_COORDS)


    def mainloop(self):
        """Start game main loop.
        """
        key_right = key_left = key_top = key_bottom = False
        dragging = resizing = False
        mouse_pressed_pos = (0, 0)

        while True:
            self.timer.tick(FPS)

            # ~ 1. Events handling ~

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    print 'Exit'
                    return self

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.hud.rect.collidepoint(event.pos):
                        if self.hud.is_resize_button_pressed(event.pos):
                            # resize HUD
                            resizing = True
                        else:
                            # move HUD
                            dragging = True
                        mouse_pressed_pos = event.pos

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragging or resizing:
                        dragging = False
                        resizing = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        key_left = True
                    elif event.key == pygame.K_RIGHT:
                        key_right = True
                    elif event.key == pygame.K_UP:
                        key_top = True
                    elif event.key == pygame.K_DOWN:
                        key_bottom = True
                    elif event.key == pygame.K_d:
                        print self.hud.rect
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        print 'Exit'
                        return self

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        key_right = False
                    elif event.key == pygame.K_LEFT:
                        key_left = False
                    elif event.key == pygame.K_UP:
                        key_top = False
                    elif event.key == pygame.K_DOWN:
                        key_bottom = False

            # ~ 2. Keys handling ~

            if key_bottom:
                direction = DOWN
            elif key_top:
                direction = UP
            elif key_left:
                direction = LEFT
            elif key_right:
                direction = RIGHT
            else:
                direction = IDLE

            # ~ 3. HUD dragging handling ~

            if dragging or resizing:
                current_mouse_pos = pygame.mouse.get_pos()
                if current_mouse_pos != mouse_pressed_pos:
                    dx = current_mouse_pos[0] - mouse_pressed_pos[0]
                    dy = current_mouse_pos[1] - mouse_pressed_pos[1]
                    if dragging:
                        self.hud.move(dx, dy)
                    elif resizing:
                        self.hud.resize(dx, dy)
                    mouse_pressed_pos = current_mouse_pos


            # ~ 3. Game logics ~

            self.player.update(direction, self.game_map)
            camera_position = self.player.get_camera_pos()
            self.game_map.draw_bottom_layers(self.screen, camera_position)
            self.player.draw(self.screen)
            self.game_map.draw_top_layer(self.screen, camera_position)

            # ~ 4. Interface drawing ~

            self.hud.draw(self.screen)

            # ~ 5. Display updating ~

            if DEBUG:
                debug_msg = '%s %s fps = %d' % (
                                self.player.debug_message,
                                self.game_map.debug_message,
                                self.timer.get_fps())
                self.debug_outtext(debug_msg, 0)

            pygame.display.update()


    def debug_outtext(self, msg, line=0):
        """Output line of text in a top left corner +20+20 with 25px interval.
        For debug purposes.
        """
        textsurface = self.debug_text.render(msg, False, DEBUG_COLOR)
        self.screen.blit(textsurface, (20, 20 + line * 25))


# --------------------------------- RUN ------------------------------------- #

if __name__ == '__main__':
    z = Main().mainloop()

