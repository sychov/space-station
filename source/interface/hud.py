# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     04-06-2018
 Description:
----------------------------------------------------------"""


import pygame

from log import Log
from frame_manager import FrameManager
from storages.base import Storage
from frame import FrameConfig
from actions import ActionInterface
from misc._enums import *

# for test only:
from misc.events import events
from storages.pseudo_inventory import PseudoInventoryInterface


# ------------------------------ CONST ------------------------------------- #

CELL_SIZE = 32

LOG_START_COORDS = (0, 505, 497, 135)

DEBUG_FONT = ('Comic Sans MS', 20)
DEBUG_COLOR = pygame.Color(0, 250, 0)

# ================================ HUD ==================================== #


class Hud(object):
    """Main manager class for game HUD.
    Contains all frames, indicators and other in-game info in
    action phase.
    """
    def __init__(self, display_size, scale):
        """Init.

            display_size:       (width, height) of game screen window
            scale:              1 or 2
        """
        Storage.set_cell_size(CELL_SIZE * scale)

        self._frames_manager = FrameManager()
        self._debug_text = pygame.font.SysFont(*DEBUG_FONT)

        self.log_frame = Log(LOG_START_COORDS)
        self._frames_manager.add_frame(self.log_frame)

        self._action_interface = ActionInterface(display_size, scale)


        # ---------------- testing, del later ----------------------------- #
        self._pseudo_inventory_enabled = False      # TEST! DELETE LATER !!!!
        self._init_TEST_storages(scale)             # TEST! DELETE LATER !!!!


    def handle_event(self, event):
        """Returns True, if event handled. Else False.

            event:      pygame.event.Event instance
        """
        return self._frames_manager.handle_event(event) or \
               self._handle_TEST_pseudo_inventory_events(event) or \
               self._handle_TEST_log_events(event) or \
               self._action_interface.handle_event(event)


    def update(self, debug_text=None):
        """Update state of HUD components.

            debug_text:     debug text to be shown on screen.
        """
        self._frames_manager.update()
        if debug_text:
            self._debug_text_message = debug_text
        else:
            self._debug_text_message = None


    def draw(self, screen):
        """Draw HUD components.

            screen:     display screen Surface
        """
        self._action_interface.draw(screen)
        self._frames_manager.draw_frames(screen)
        self._debug_outtext(screen)


    def _debug_outtext(self, screen):
        """Output line of text in a top left corner +20+20 with 25px interval.
        For debug purposes.

            screen:     display screen Surface
        """
        textsurface = self._debug_text.render(
            self._debug_text_message,
            False,
            DEBUG_COLOR)
        screen.blit(textsurface, (20, 20))

    # -------------------------------- #

    def __repr__(self):
        """Simple representation.
        """
        return 'HUD class instance.'


    # ----------------------- PURE TESTING METHODS ---------------------- #
    # - ----------------- we will delete them later. -------------------- #

    def _handle_TEST_log_events(self, event):
        """ JUST FOR TESTING !!!!
        TO DO: DEL IT !!!!

            event:      pygame.event.Event instance
        """
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_0:
                self.log_frame.output('Hello! simple text test!')
                return True
            elif event.key == pygame.K_9:
                self.log_frame.output('Hello! danger test!', DANGER)
                return True
            elif event.key == pygame.K_8:
                self.log_frame.output('Hello! succes text!', SUCCESS)
                return True
            elif event.key == pygame.K_7:
                self.log_frame.output('Hello! fail text test!', FAIL)
                return True
            elif event.key == pygame.K_6:
                self.log_frame.output('Hello! ' * 20)
                return True
        return False


    def _handle_TEST_pseudo_inventory_events(self, event):
        """ JUST FOR TESTING !!!!
        TO DO: DEL IT !!!!

            event:      pygame.event.Event instance
        """
        if event.type == pygame.KEYUP and event.key == pygame.K_i:
            if self._pseudo_inventory_enabled:
                self._frames_manager.remove_frame(self.pseudo_inventory)
                self.pseudo_inventory = None
                self._pseudo_inventory_enabled = False
            else:
                self.pseudo_inventory = PseudoInventoryInterface(
                    (100, 100, 0, 0),
                    self.pseudo_inventory_content)
                self.pseudo_inventory.redraw_storage()
                self._frames_manager.add_frame(self.pseudo_inventory)
                self._pseudo_inventory_enabled = True


    def _init_TEST_storages(self, scale):
        """ JUST FOR TESTING !!!!
        TO DO: DEL IT !!!!

            scale:  1 or 2
        """
        from misc._pathes import MAIN_DIR
        from environment.items.base import InventoryObject
        from environment.storage_container import StorageContent

        InventoryObject.add_sprites(
            MAIN_DIR + '/graphics/tilesets/items_2x1.png',
            '2x1',
            SPRITE_2x1,
            scale
        )

        InventoryObject.add_sprites(
            MAIN_DIR + '/graphics/tilesets/items_2x2.png',
            '2x2',
            SPRITE_2x2,
            scale
        )

        big_item = InventoryObject('2x2', 3)
        medium_item = InventoryObject('2x1', 3)
        self.pseudo_inventory_content = StorageContent(4, 5)
        self.pseudo_inventory_content.add_item(medium_item)
        self.pseudo_inventory_content.add_item(big_item)

