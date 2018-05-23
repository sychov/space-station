# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     23-05-2018
 Description:
----------------------------------------------------------"""


from collections import deque

import pygame
from pygame import Rect, Surface, Color

from _enums import *


# ------------------------------ CONST ------------------------------------- #

##HUD_TILESET_PATH = "interface/chat3.png"
##
##HUD_PARTS_RECTS = {
##    TOP_LEFT:       Rect(0, 0, 60, 54),
##    TOP_RIGHT:      Rect(140, 0, 85, 49),
##    BOTTOM_LEFT:    Rect(0, 69, 50, 71),
##    BOTTOM_RIGHT:   Rect(185, 67, 40, 73),
##    UP:             Rect(62, 0, 51, 22),
##    DOWN:           Rect(62, 124, 51, 16),
##    LEFT:           Rect(0, 55, 19, 16),
##    RIGHT:          Rect(204, 47, 21, 24),
##}
##
##HUD_MAX_SIZE = (700, 700)
##HUD_MIN_SIZE = (300, 130)
##HUD_DEQUE_MAX_LEN = 10
##HUD_BACKGROUND_COLOR = Color(0, 0, 0)
##HUD_TEXT_COLORS = {}
##HUD_RESIZE_BUTTON_SIZE = 20
##
##HUD_PADDING = 25
##HUD_FONT = ('Comic Sans MS', 15)

HUD_TILESET_PATH = "interface/chat_border.png"

HUD_PARTS_RECTS = {
    TOP_LEFT:       Rect(0, 0, 78, 35),
    TOP_RIGHT:      Rect(219, 0, 45, 71),
    BOTTOM_LEFT:    Rect(0, 137, 61, 61),
    BOTTOM_RIGHT:   Rect(163, 134, 101, 64),
    UP:             Rect(77, 0, 142, 7),
    DOWN:           Rect(62, 192, 102, 6),
    LEFT:           Rect(0, 34, 5, 104),
    RIGHT:          Rect(258, 69, 6, 66),
}

HUD_MAX_SIZE = (700, 600)
HUD_MIN_SIZE = (300, 135)
HUD_DEQUE_MAX_LEN = 10
HUD_BACKGROUND_COLOR = Color(10, 10, 10)
HUD_TEXT_COLORS = {}
HUD_RESIZE_BUTTON_SIZE = 20

HUD_PADDING = 18
HUD_FONT = ('Lucida Console', 15)

# ========================== HUD monitor class ============================== #

class InterfaceFrame(object):
    """
    """
    def __init__(self, rect):
        """ Load tileset for a game HUD.
        Create Hud instance with default settings of tileset and limits.

            rect:  x, y, width, height (on global screen)
        """
        image = pygame.image.load(HUD_TILESET_PATH)
        image_width, image_height = image.get_size()

        self._tileset = {}
        for q in (TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT, UP,
                                                            DOWN, LEFT, RIGHT):
            _rect = HUD_PARTS_RECTS[q]
            self._tileset[q] = image.subsurface(_rect).convert()

        self._background_source = Surface(HUD_MAX_SIZE)

        self._background = None
        self._messages = deque()
        self._background_color = HUD_BACKGROUND_COLOR

        self.rect = Rect(rect)
        min_x, min_y = HUD_MIN_SIZE
        max_x, max_y = HUD_MAX_SIZE
        self.rect.width = min(max(self.rect.width, min_x), max_x)
        self.rect.height = min(max(self.rect.height, min_y), max_y)


        self._redraw_background()

        self._font = pygame.font.SysFont(*HUD_FONT)
        self._update_text()


    def resize(self, dx, dy):
        """
        """
        min_x, min_y = HUD_MIN_SIZE
        max_x, max_y = HUD_MAX_SIZE

        new_width = min(max(self.rect.width + dx, min_x), max_x)
        new_height = min(max(self.rect.height + dy, min_y), max_y)

        if (self.rect.width != new_width or self.rect.height != new_height):
            self.rect.width = new_width
            self.rect.height = new_height
            self._redraw_background()
            self._update_text()


    def move(self, dx, dy):
        """
        """
        self.rect.x += dx
        self.rect.y += dy


    def output(self, msg):
        """
        """
        pass


    def draw(self, screen):
        """
        """
        screen.blit(self._background, self.rect)


    def is_resize_corner_selected(self, coords):
        """
        """
        x, y = coords
        if x > self.rect.x + self.rect.width - HUD_RESIZE_BUTTON_SIZE and \
           x < self.rect.x + self.rect.width and \
           y > self.rect.y + self.rect.height - HUD_RESIZE_BUTTON_SIZE and \
           y < self.rect.y + self.rect.height:
            return True
        else:
            return False


    def _redraw_background(self):
        """
        """
        width = self.rect.width
        height = self.rect.height
        surface = self._background_source

        surface.fill(self._background_color)

        # draw top side of the HUD
        hud_top_side_len = width - HUD_PARTS_RECTS[TOP_LEFT].width \
                                             - HUD_PARTS_RECTS[TOP_RIGHT].width
        plank_width, _ = self._tileset[UP].get_size()
        x = HUD_PARTS_RECTS[TOP_LEFT].width
        y = 0
        while hud_top_side_len > 0:
            surface.blit(self._tileset[UP], (x, y))
            x += plank_width
            hud_top_side_len -= plank_width

        # draw bottom side of the HUD
        hud_bottom_side_len = width - HUD_PARTS_RECTS[BOTTOM_LEFT].width \
                                          - HUD_PARTS_RECTS[BOTTOM_RIGHT].width
        plank_width, _ = self._tileset[DOWN].get_size()
        x = HUD_PARTS_RECTS[BOTTOM_LEFT].width
        y = height - self._tileset[DOWN].get_size()[1]
        while hud_bottom_side_len > 0:
            surface.blit(self._tileset[DOWN], (x, y))
            x += plank_width
            hud_bottom_side_len -= plank_width

        # draw left side of the HUD
        hud_left_side_len = height - HUD_PARTS_RECTS[TOP_LEFT].height \
                                          - HUD_PARTS_RECTS[BOTTOM_LEFT].height
        _, plank_height = self._tileset[LEFT].get_size()
        y = HUD_PARTS_RECTS[TOP_LEFT].height
        x = 0
        while hud_left_side_len > 0:
            surface.blit(self._tileset[LEFT], (x, y))
            y += plank_height
            hud_left_side_len -= plank_height

        # draw right side of the HUD
        hud_right_side_len = height - HUD_PARTS_RECTS[TOP_RIGHT].height \
                                         - HUD_PARTS_RECTS[BOTTOM_RIGHT].height
        _, plank_height = self._tileset[RIGHT].get_size()
        y = HUD_PARTS_RECTS[TOP_RIGHT].height
        x = width - self._tileset[RIGHT].get_size()[0]
        while hud_right_side_len > 0:
            surface.blit(self._tileset[RIGHT], (x, y))
            y += plank_height
            hud_right_side_len -= plank_height

        # draw corners
        surface.blit(self._tileset[TOP_LEFT], (0, 0))
        surface.blit(self._tileset[TOP_RIGHT],
                           (width - self._tileset[TOP_RIGHT].get_size()[0], 0))
        surface.blit(self._tileset[BOTTOM_LEFT],
                            (0, height - HUD_PARTS_RECTS[BOTTOM_LEFT].height))
        surface.blit(self._tileset[BOTTOM_RIGHT],
                    (width - self._tileset[BOTTOM_RIGHT].get_size()[0],
                     height - self._tileset[BOTTOM_RIGHT].get_size()[1]))

        self._background = self._background_source.subsurface(
                                     (0, 0, self.rect.width, self.rect.height))


    def _update_text(self):
        """
        """
        width, height = self._background.get_size()
        background = self._background.subsurface(
                            (HUD_PADDING,
                             HUD_PADDING,
                             width - HUD_PADDING,
                             height - HUD_PADDING))
        textsurface = self._font.render('Hello world!',
                                        False,
                                        Color(250, 250, 0),
                                        HUD_BACKGROUND_COLOR)
        background.blit(textsurface, (0, 0))


    def __repr__(self):
        """Simple representation.
        """
        return 'Chat HUD class instance.'