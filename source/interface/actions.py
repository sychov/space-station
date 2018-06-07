# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     06-06-2018
 Description:
----------------------------------------------------------"""

import pygame
from pygame import Surface, Rect

from references._enums import *
from references._pathes import ACTIONS_TILES_PATH


# ================================= CONST =================================== #


TILE_WIDTH = 25


# ===================== ACTION_INTERFACE CLASS ============================== #


class ActionInterface(pygame.sprite.Sprite):
    """Action buttons set, interface for player possible actions.
    """
    def __init__(self, display_size, scale):
        """ Init.
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
        self._iconset = []
        self._events = [pygame.USEREVENT]
        self._custom_events = [
            EVENT_DISABLE_ACTION_INTERFACE,
            EVENT_ENABLE_ACTION_INTERFACE]


    def _enable(self, direction, icon_set):
        """Enable action buttons.
        """
        self._iconset = icon_set
        self._direction = direction
        self._is_active = True


    def _disable(self):
        """Disable action buttons.
        """
        self._is_active = False


    def draw(self, screen):
        """Draw current player interface icons on screen.

            screen:     screen Surface
        """
        if self._is_active and self._iconset:
            positions = self._positions[len(self._iconset)]
            for icon, coords in zip(self._iconset, positions[self._direction]):
                screen.blit(self._tileset[icon], coords)


    def handle_event(self, event):
        """Returns True, if event handled. Else False.
        """
        if event.type not in self._events:
            return False

        if event.custom_type not in self._custom_events:
            return False

        if event.custom_type == EVENT_ENABLE_ACTION_INTERFACE:
            self._enable(event.direction, event.actions_list)
        elif event.custom_type == EVENT_DISABLE_ACTION_INTERFACE:
            self._disable()

        return True

