# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     19-12-2017
 Description:
----------------------------------------------------------"""


import pygame

from environment.game_map import Map
from persons.player import Player
from interface.log import Log
from interface.frame_manager import FrameManager
from interface.storage import Storage
from references._enums import *

# ------------------------------ CONST ------------------------------------- #

DISPLAY_SIZE = (1024, 768)
FPS = 200
DOUBLE = True
MAP_PATH = '../gamedata/map/map.json'
TILESET_PATH = "../graphics/tilesets/TILES.png"
CHARACTER_TILESET = '../graphics/chars/captain.png'

HUD_START_COORDS = (0, 633, 497, 135)

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

        self.frames_manager = FrameManager()
        self.log_frame = Log(HUD_START_COORDS)
        self.frames_manager.add_frame(self.log_frame)

        self.storage = Storage((300, 10, 300, 200))
        self.frames_manager.add_frame(self.storage)


    def mainloop(self):
        """Start game main loop.
        """
        while True:
            self.timer.tick(FPS)

            # ~ 1. Events handling ~

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.quit()

                if self.frames_manager.handle_event(event):
                    continue

                if self.player.handle_event(event):
                    continue

                # TO DO: to del !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_0:
                        self.log_frame.output('Hello! simple text test!')
                    elif event.key == pygame.K_9:
                        self.log_frame.output('Hello! danger test!', DANGER)
                    elif event.key == pygame.K_8:
                        self.log_frame.output('Hello! succes text!', SUCCESS)
                    elif event.key == pygame.K_7:
                        self.log_frame.output('Hello! fail text test!', FAIL)


            # ~ 2. Update ~

            self.frames_manager.update()
            self.player.update(self.game_map)

            # ~ 3. Draw ~

            camera_position = self.player.get_camera_pos()
            self.game_map.draw_bottom_layers(self.screen, camera_position)
            self.player.draw(self.screen)
            self.game_map.draw_top_layer(self.screen, camera_position)
            self.frames_manager.draw_frames(self.screen)

            # ~ 4. Display updating ~

            if DEBUG:
                debug_msg = '%s %s fps = %d' % (
                                self.player.debug_message,
                                self.game_map.debug_message,
                                self.timer.get_fps())
                self.debug_outtext(debug_msg, 0)

            pygame.display.update()


    def quit(self):
        """Exit from game.
        """
        pygame.quit()
        print "The end."
        raise SystemExit(0)


    def debug_outtext(self, msg, line=0):
        """Output line of text in a top left corner +20+20 with 25px interval.
        For debug purposes.
        """
        textsurface = self.debug_text.render(msg, False, DEBUG_COLOR)
        self.screen.blit(textsurface, (20, 20 + line * 25))


# --------------------------------- RUN ------------------------------------- #

if __name__ == '__main__':
    z = Main()
    z.mainloop()

