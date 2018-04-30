# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     19-12-2017
 Description:
----------------------------------------------------------"""


import pygame

from game_map_classes import Map
from char_classes import Player, NPC


# ------------------------------ CONST ------------------------------------- #

DISPLAY_SIZE = (1024, 768)
FPS = 90
DOUBLE = True
BG_COLOR = pygame.Color(31, 29, 44)

DEBUG = False
DEBUG_COLOR = pygame.Color(0, 250, 0)

# ================================ MAIN ==================================== #


class Main(object):
    """Main app class
    """
    def __init__(self):
        """
        """
        pygame.init()
        self.screen = pygame.display.set_mode(DISPLAY_SIZE)
        self.screen.fill(BG_COLOR)

        pygame.font.init()
        self.debug_text = pygame.font.SysFont('Comic Sans MS', 20)

        self.timer = pygame.time.Clock()

        self.game_map = Map(
            map_path='map.json',
            tileset_path="tilesets/TILES.png",
            display_size_tuple=DISPLAY_SIZE,
            scale=2 if DOUBLE else 1)

        x, y = self.game_map.get_first_walkable_cell_coords()
        self.player = Player(x,
                             y,
                             'chars/captain.png',
                             scale=2 if DOUBLE else 1)
        self.player_coords = self.player.get_player_coords_on_screen(
                                                                  DISPLAY_SIZE)


    def debug_outtext(self, msg, line=0):
        """Output line of text in a top left corner +20+20 with 25px interval.
        For debug purposes.
        """
        textsurface = self.debug_text.render(msg, False, DEBUG_COLOR)
        self.screen.blit(textsurface, (20, 20 + line * 25))


    def mainloop(self):
        """Start game main loop.
        """
        key_right = key_left = key_top = key_bottom = False

        while True:
            self.timer.tick_busy_loop(FPS)

            # events handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    print 'Exit'
                    return self

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        key_left = True
                    elif event.key == pygame.K_RIGHT:
                        key_right = True
                    elif event.key == pygame.K_UP:
                        key_top = True
                    elif event.key == pygame.K_DOWN:
                        key_bottom = True
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        print 'Exit'
                        return self

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        key_right = False
                    elif event.key == pygame.K_LEFT:
                        key_left = False
                    elif event.key == pygame.K_UP:
                        key_top = False
                    elif event.key == pygame.K_DOWN:
                        key_bottom = False

            # keys handling
            if key_bottom:
                direction = 'bottom'
            elif key_top:
                direction = 'top'
            elif key_left:
                direction = 'left'
            elif key_right:
                direction = 'right'
            else:
                direction = 'idle'

            self.player.update(direction, self.game_map)
            camera_x, camera_y = self.player.get_camera_pos()
            self.screen.fill(BG_COLOR)
            self.game_map.draw_bottom(self.screen, (camera_x, camera_y))
            self.screen.blit(self.player.image, self.player_coords)
            self.game_map.draw_top(self.screen, (camera_x, camera_y))

            if DEBUG:
                debug_msg = self.game_map.debug + ', fps = %d' % \
                                                           self.timer.get_fps()
                self.debug_outtext(debug_msg, 0)

            pygame.display.update()


# --------------------------------- RUN ------------------------------------- #

if __name__ == '__main__':
    z = Main().mainloop()

