# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     23-05-2018
 Description:
----------------------------------------------------------"""


import pygame
from pygame import Rect, Surface, Color

from source.references._enums import *


# ========================== Frame class ============================== #

class Frame(object):
    """Parent frame class.
    Used as base to make any custom windows in-game.
    """
    def __init__(self, rect, tileset_path, parts_rects, max_size, min_size,
                                                            bg_color, padding):
        """ Load tileset for a game HUD.
        Create Hud instance with default settings of tileset and limits.

            rect:           x, y, width, height (position on global screen);
            tileset_path:   full path to tileset file
            parts_rects:    dictionary, where keys are directions and corners
                            enums (UP, BOTTOM_LEFT, etc), and values are
                            Rect instances
            max_size:       x, y
            min_size:       x, y
            bg_color:       Color instance
            padding:        int, in pixels, both for X and Y paddings
        """
        # 1. ~ Init variables ~

        self.parts_rects = parts_rects
        self.rect = Rect(rect)
        self.max_size = max_size
        self.min_size = min_size
        self.padding = padding
        self._background_color = bg_color

        # "_background_source" used as hidden canvas of maximum size, where
        # borders and background are drawn
        self._background_source = Surface(max_size)

        # "_background" used as a part of "_background_source", that is
        # actually drawn on screen
        self._background = None

        # 2. ~ Load tiles ~

        self._tileset = {}
        image = pygame.image.load(tileset_path)
        for q in (UP, DOWN, LEFT, RIGHT,
                  TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT):
            _rect = self.parts_rects[q]
            self._tileset[q] = image.subsurface(_rect).convert()

        # 3. ~ Make background ~

        min_x, min_y = self.min_size
        max_x, max_y = self.max_size
        self.rect.width = min(max(self.rect.width, min_x), max_x)
        self.rect.height = min(max(self.rect.height, min_y), max_y)
        self._redraw_background()


    def resize(self, dx, dy):
        """Change size of the frame relatevly on deltas of X and Y.
        """
        min_x, min_y = self.min_size
        max_x, max_y = self.max_size

        new_width = min(max(self.rect.width + dx, min_x), max_x)
        new_height = min(max(self.rect.height + dy, min_y), max_y)

        if (self.rect.width != new_width or self.rect.height != new_height):
            self.rect.width = new_width
            self.rect.height = new_height
            self._redraw_background()
            self._update_text()


    def move(self, dx, dy):
        """Move frame relatevly on deltas of X and Y.
        """
        self.rect.x += dx
        self.rect.y += dy


    def draw(self, screen):
        """Draw frame on the screen.
        """
        screen.blit(self._background, self.rect)


    def _redraw_background(self):
        """Draw background on "_background_source" surface.
        Set "_background" attribute to actual part of it.
        """
        width = self.rect.width
        height = self.rect.height
        surface = self._background_source

        surface.fill(self._background_color)

        # draw top side of the HUD
        hud_top_side_len = width - self.parts_rects[TOP_LEFT].width \
                                            - self.parts_rects[TOP_RIGHT].width
        plank_width, _ = self._tileset[UP].get_size()
        x = self.parts_rects[TOP_LEFT].width
        y = 0
        while hud_top_side_len > 0:
            surface.blit(self._tileset[UP], (x, y))
            x += plank_width
            hud_top_side_len -= plank_width

        # draw bottom side of the HUD
        hud_bottom_side_len = width - self.parts_rects[BOTTOM_LEFT].width \
                                         - self.parts_rects[BOTTOM_RIGHT].width
        plank_width, _ = self._tileset[DOWN].get_size()
        x = self.parts_rects[BOTTOM_LEFT].width
        y = height - self._tileset[DOWN].get_size()[1]
        while hud_bottom_side_len > 0:
            surface.blit(self._tileset[DOWN], (x, y))
            x += plank_width
            hud_bottom_side_len -= plank_width

        # draw left side of the HUD
        hud_left_side_len = height - self.parts_rects[TOP_LEFT].height \
                                         - self.parts_rects[BOTTOM_LEFT].height
        _, plank_height = self._tileset[LEFT].get_size()
        y = self.parts_rects[TOP_LEFT].height
        x = 0
        while hud_left_side_len > 0:
            surface.blit(self._tileset[LEFT], (x, y))
            y += plank_height
            hud_left_side_len -= plank_height

        # draw right side of the HUD
        hud_right_side_len = height - self.parts_rects[TOP_RIGHT].height \
                                        - self.parts_rects[BOTTOM_RIGHT].height
        _, plank_height = self._tileset[RIGHT].get_size()
        y = self.parts_rects[TOP_RIGHT].height
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
                            (0, height - self.parts_rects[BOTTOM_LEFT].height))
        surface.blit(self._tileset[BOTTOM_RIGHT],
                    (width - self._tileset[BOTTOM_RIGHT].get_size()[0],
                     height - self._tileset[BOTTOM_RIGHT].get_size()[1]))

        self._background = self._background_source.subsurface(
                                     (0, 0, self.rect.width, self.rect.height))


    def __repr__(self):
        """Simple representation.
        """
        return 'Frame class instance.'
