# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     06-06-2018
 Description:
----------------------------------------------------------"""

import pygame
from pygame import Surface, Rect

from misc.events import events
from misc._enums import *
from misc._pathes import ACTIONS_TILES_PATH


# ================================= CONST =================================== #

TILE_WIDTH = 25

FORCE_KEY = pygame.K_c
USE_KEY = pygame.K_x
HELP_KEY = pygame.K_z

# ===================== ACTION_INTERFACE CLASS ============================== #


class ActionInterface(pygame.sprite.Sprite):
    """Action buttons set, interface for player possible actions.
    Consist of Force, Use and Help buttons (not obligatory).
    """
    def __init__(self, display_size, scale):
        """ Init.

        display_size:       (width, height) of game screen window
        scale:              1 or 2
        """
        pygame.sprite.Sprite.__init__(self)

        # ~ 1. Get images ~

        image = pygame.image.load(ACTIONS_TILES_PATH)
        image_width, image_height = image.get_size()
        self._tileset = {}

        offset = 0
        for icon in (ACTION_GOOD, ACTION_BAD, ACTION_USE):
            rect = Rect(offset, 0, TILE_WIDTH, image_height)
            self._tileset[icon] = image.subsurface(rect).convert_alpha()
            offset += TILE_WIDTH

        # ~ 2. Set positioning

        center_x = display_size[0] / 2
        center_y = display_size[1] / 2

        self._positions = {
            3: {
                UP: [
                    (center_x - 30 - TILE_WIDTH, center_y - 40 * scale),
                    (center_x - TILE_WIDTH / 2, center_y - 30 * scale - 40),
                    (center_x + 30, center_y - 40 * scale),
                ],
                DOWN: [
                    (center_x - 30 - TILE_WIDTH, center_y + 10),
                    (center_x - TILE_WIDTH / 2, center_y + 20),
                    (center_x + 30, center_y + 10),
                ],
                LEFT: [
                    (center_x - 35 * scale + 10,
                                center_y - 20 - image_height - 15 * scale),
                    (center_x - 25 * scale - 25,
                                center_y + 10 - image_height / 2 - 15 * scale),
                    (center_x - 35 * scale + 10,
                                center_y + 40 - 15 * scale),
                ],
                RIGHT: [
                    (center_x + 35 * scale - 35,
                                center_y - 20 - image_height - 15 * scale),
                    (center_x + 25 * scale,
                                center_y + 10 - image_height / 2 - 15 * scale),
                    (center_x + 35 * scale - 35,
                                center_y + 40 - 15 * scale),
                ],
            },

            2: {
                UP: [
                    (center_x - 20 - TILE_WIDTH, center_y - 30 * scale - 40),
                    (center_x + 20, center_y - 30 * scale - 40),
                ],
                DOWN: [
                    (center_x - 20 - TILE_WIDTH, center_y + 20),
                    (center_x + 20, center_y + 20),
                ],
                LEFT: [
                    (center_x - 25 * scale - 15,
                                center_y - 10 - image_height - 15 * scale),
                    (center_x - 25 * scale - 15,
                                center_y + 30 - 15 * scale),
                ],
                RIGHT: [
                    (center_x + 20 * scale - 5,
                                center_y - 10 - image_height - 15 * scale),
                    (center_x + 20 * scale - 5,
                                center_y + 30 - 15 * scale),
                ],
            },

            1: {
                UP: [(center_x - TILE_WIDTH / 2, center_y - 30 * scale - 40)],
                DOWN: [(center_x - TILE_WIDTH / 2, center_y + 20)],
                LEFT: [(center_x - 20 * scale - 25,
                            center_y + 10 - image_height / 2 - 15 * scale)],
                RIGHT: [(center_x + 20 * scale,
                                center_y + 10 - image_height / 2 - 15 * scale)]
            },
        }

        # ~ 3. Starting values

        self._direction = RIGHT
        self._is_active = False
        self._selected_object = None
        self._actions_list = []
        self._events = [pygame.USEREVENT, pygame.KEYDOWN]
        self._custom_events = [
            EVENT_DISABLE_ACTION_INTERFACE,
            EVENT_ENABLE_ACTION_INTERFACE,
            EVENT_UPDATE_ACTION_INTERFACE]


    def _enable(self, direction, object_):
        """Enable action buttons.

            direction:      direction of player char (UP, DOWN, LEFT, RIGHT)
            object_:        selected object to action's apply
        """
        self._selected_object = object_
        self._actions_list = object_.get_actions_list()
        self._direction = direction
        self._is_active = True


    def _update(self):
        """Update action buttons.
        """
        if self._selected_object:
            self._actions_list = self._selected_object.get_actions_list()


    def _disable(self):
        """Disable action buttons.
        """
        self._is_active = False


    def draw(self, screen):
        """Draw current player interface icons on screen.

            screen:     screen Surface
        """
        if self._is_active and self._actions_list:
            positions = self._positions[len(self._actions_list)]
            for icon, coords in zip(self._actions_list,
                                                   positions[self._direction]):
                screen.blit(self._tileset[icon], coords)


    def handle_event(self, event):
        """Returns True, if event handled. Else False.

            event:      pygame.event.Event instance
        """
        # proceed handled events only:
        if event.type not in self._events:
            return False

        # if keydown event, proceed action keys:
        elif event.type == pygame.KEYDOWN:

            if not self._is_active or \
                               event.key not in (FORCE_KEY, USE_KEY, HELP_KEY):
                return False

            elif event.key == FORCE_KEY:
                self._selected_object.player_acts_bad()
                return True

            elif event.key == USE_KEY:
                self._selected_object.player_acts_use()
                return True

            elif event.key == HELP_KEY:
                self._selected_object.player_acts_good()
                return True

        # if user event, proceed enabling/disableing interface:
        elif event.type == pygame.USEREVENT:

            if event.custom_type == EVENT_ENABLE_ACTION_INTERFACE:
                self._enable(event.direction, event.object_)
                return True

            elif event.custom_type == EVENT_DISABLE_ACTION_INTERFACE:
                self._disable()
                events.actions_interface_close_reporting()
                return True

            elif event.custom_type == EVENT_UPDATE_ACTION_INTERFACE:
                self._update()
                return True

            else:
                return False

        # don't proceed anything else.
        else:
            return False
