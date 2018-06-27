# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     19-12-2017
 Description:
----------------------------------------------------------"""

import gc

import pygame

from environment.map import Map
from chars.player import Player
from chars.chars_manager import CharsManager
from interface.hud import Hud
from sounds.music_box import MusicBox

from misc._pathes import MAP_PATH, MAP_TILES_PATH, PLAYER_TILES_PATH
from misc._enums import *
from misc.events import EVENT_SONG_END


# ------------------------------ CONST ------------------------------------- #

DISPLAY_SIZE = (1024, 640)
FPS_LIMIT = 180
DOUBLE = True
DEBUG = True

# ================================ MAIN ==================================== #


class Main(object):
    """ This is a game application.
    What could I say more?
    """
    def __init__(self):
        """ Init.
        """
        scale = 2 if DOUBLE else 1

        # ~ 1. Pygame init ~

        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.mixer.init()
        pygame.init()

        # ~ 2. Set attr components ~

        self.screen = pygame.display.set_mode(DISPLAY_SIZE)
        self.hud = Hud(display_size=DISPLAY_SIZE, scale=scale)

        self.timer = pygame.time.Clock()

        self.game_map = Map(
            map_path=MAP_PATH,
            tileset_path=MAP_TILES_PATH,
            display_size_tuple=DISPLAY_SIZE,
            scale=scale)

        self.player = Player(
            coords=self.game_map.get_first_walkable_cell_coords(),
            tileset_path=PLAYER_TILES_PATH,
            scale=scale,
            display_size=DISPLAY_SIZE)

        self.chars_manager = CharsManager(self.player)

        # init map buffer first time
        self.game_map.make_bottom_buffer(self.player.get_camera_pos())

        # start music playing
        self.music_box = MusicBox()
        self.music_box.start()


    def mainloop(self):
        """Start game main loop.
        """
        while True:
            milliseconds_spent = self.timer.tick(FPS_LIMIT)

            # ~ 1. Events handling ~

            for event in pygame.event.get():

                # main event: exit from game
                if event.type == pygame.QUIT:
                    self.quit()

                # main event: need to play next song
                if event.type == EVENT_SONG_END:
                    self.music_box.play_next()
                    continue

                # main event: need to force garbage collector
                if event.type == pygame.USEREVENT and \
                                  event.custom_type == EVENT_FORCE_MEMORY_FREE:
                    gc.collect()
                    continue

                # HUD events:
                if self.hud.handle_event(event):
                    continue

                # Player events:
                if self.player.handle_event(event):
                    continue

                # Game Map events:
                if self.game_map.handle_event(event):
                    continue

                # Char Manager events:
                if self.chars_manager.handle_event(event):
                    continue

            # ~ 2. Update ~

            self.hud.update(debug_text=self._get_debug_message())
            self.player.update(self.game_map, milliseconds_spent)
            self.game_map.objects_manager.update()

            # ~ 3. Draw ~

            camera_position = self.player.get_camera_pos()
            self.game_map.draw_bottom_layers(self.screen, camera_position)
            self.player.draw(self.screen)
            self.game_map.draw_top_layer(self.screen, camera_position)

            self.hud.draw(self.screen)

            # ~ 4. Display updating ~

            pygame.display.update()


    def quit(self):
        """Exit from game.
        """
        pygame.quit()
        print "The end."
        raise SystemExit(0)


    def _get_debug_message(self):
        """Form debug message.
        For test purposes only.
        """
        if DEBUG:
            return 'fps = %d' % self.timer.get_fps()


# --------------------------------- RUN ------------------------------------- #

if __name__ == '__main__':
    z = Main()
    z.mainloop()

