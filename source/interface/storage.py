# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     25-05-2018
 Description:
----------------------------------------------------------"""


import pygame
from pygame import Rect, Surface, Color

from frame import Frame
from references._enums import *


# ------------------------------ CONST ------------------------------------- #

TILESET_PATH = "../graphics/interface/blue_scifi_border.png"

PARTS_RECTS = {
    TOP_LEFT:       Rect(0, 0, 60, 54),
    TOP_RIGHT:      Rect(140, 0, 85, 49),
    BOTTOM_LEFT:    Rect(0, 69, 50, 71),
    BOTTOM_RIGHT:   Rect(185, 67, 40, 73),
    UP:             Rect(62, 0, 51, 22),
    DOWN:           Rect(62, 124, 51, 16),
    LEFT:           Rect(0, 55, 19, 16),
    RIGHT:          Rect(204, 47, 21, 24),
}

MAX_SIZE = (700, 700)
MIN_SIZE = (300, 130)
BACKGROUND_COLOR = Color(10, 10, 10)

TEXT_COLOR = Color(250, 250, 0)
PADDING = 25
FONT = ('Comic Sans MS', 15)

# ============================= Storage class ============================= #

class Storage(Frame):
    """Base Storage class.
    """
    def __init__(self, rect):
        """
        rect:  x, y, width, height (on global screen)
        """
        super(Storage, self).__init__(
            rect=rect,
            tileset_path=TILESET_PATH,
            parts_rects=PARTS_RECTS,
            max_size=MAX_SIZE,
            min_size=MIN_SIZE,
            bg_color=BACKGROUND_COLOR,
            padding=PADDING
        )
        self.add_event_handler(pygame.MOUSEBUTTONUP,
                               self._event_mousebutton_up)
        self.add_event_handler(pygame.MOUSEBUTTONDOWN,
                               self._event_mousebutton_down)


    def update(self):
        """Update frame state (dragging and resizing handling).
        """
        self._update_dragging()

    # ---------------------- EVENTS ----------------------- #

    def _event_mousebutton_up(self, event):
        """Handle mouse button up event.
        """
        if self._dragging_handled_off():
            return True
        else:
            return False


    def _event_mousebutton_down(self, event):
        """Handle mouse button down event.
        """
        if self.rect.collidepoint(event.pos):
            self._enable_dragging_state(event.pos)
            return True
        else:
            return False

    # -------------------------------- #

    def __repr__(self):
        """Simple representation.
        """
        return 'Base Storage class instance.'

