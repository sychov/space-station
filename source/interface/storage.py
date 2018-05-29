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
MIN_SIZE = (150, 130)
BACKGROUND_COLOR = Color(0, 0, 0)

PADDING = 25

STORAGE_TOP_LEFT = (24, 29)
CELL_SIZE = 64

LINE_COLOR = Color(0, 140, 140)
CELLS_MATRIX = (2, 4)

# =========================== Storage cell class =========================== #


class StorageCell(object):
    """Very simple class for cell content of Storage
    """
    def __init__(self):
        """
        """
        self.clear_cell()


    def is_empty(self):
        """
        """
        if self.inventory_item:
            return False
        else:
            return True


    def put_item(self, item, is_dumb=False):
        """
        """
        self.inventory_item = item
        self.is_dumb = is_dumb


    def clear_cell(self):
        """
        """
        self.inventory_item = None
        self.is_dumb = False


    def __repr__(self):
        """
        """
        if not self.inventory_item:
            return 'Empty cell'
        elif self.is_dumb:
            return 'Dumb cell of %s' % str(self.inventory_item)
        else:
            return 'Cell of %s' % str(self.inventory_item)


# ============================= Storage class ============================= #


class Storage(Frame):
    """Base Storage class.
    """
    def __init__(self, rect):
        """
        rect:  x, y, width, height (on global screen)
        """
        self._width, self._height = CELLS_MATRIX
        self._content = [
            [StorageCell() for x in xrange(self._width)]
                                                 for y in xrange(self._height)
        ]

        start_x, start_y = STORAGE_TOP_LEFT
        self._cell_size = CELL_SIZE
        self._padding = PADDING

        final_rect = Rect(rect)
        width_grid = self._cell_size * self._width
        if final_rect.width < width_grid + start_x + PADDING:
            final_rect.width = width_grid + start_x + PADDING
        height_grid = self._cell_size* self._height
        if final_rect.height < height_grid + start_y + PADDING:
            final_rect.height = height_grid + start_y + PADDING

        super(Storage, self).__init__(
            rect=final_rect,
            tileset_path=TILESET_PATH,
            parts_rects=PARTS_RECTS,
            max_size=MAX_SIZE,
            min_size=MIN_SIZE,
            bg_color=BACKGROUND_COLOR,
        )

        self._content_rect = Rect(start_x, start_y, width_grid, height_grid)
        self._draw_grid()

        # ~ EVENTS ~

        self.add_event_handler(pygame.MOUSEBUTTONUP,
                               self._event_mousebutton_up)
        self.add_event_handler(pygame.MOUSEBUTTONDOWN,
                               self._event_mousebutton_down)


    def update(self):
        """Update frame state (dragging and resizing handling).
        """
        self._update_dragging()


    def add_item(self, item):
        """
        """
        item_type = item.type
        for y in xrange(self._height):
            for x in xrange(self._width):
                if self._is_possible_to_put_item_to_cell(x, y, item_type):
                    # for 1x1 sprites:
                    if item_type == SPRITE_1x1:
                        self._content[y][x].put_item(item)
                        return True

                    # for 2x1 sprites:
                    elif item_type == SPRITE_2x1:
                        self._content[y][x].put_item(item)
                        self._content[y][x + 1].put_item(item, is_dumb=True)
                        return True

                    # for 1x2 sprites:
                    elif item_type == SPRITE_1x2:
                        self._content[y][x].put_item(item)
                        self._content[y + 1][x].put_item(item, is_dumb=True)
                        return True

                    # for 2x2 sprites:
                    elif item_type == SPRITE_2x2:
                        self._content[y][x].put_item(item)
                        self._content[y + 1][x].put_item(item, is_dumb=True)
                        self._content[y][x + 1].put_item(item, is_dumb=True)
                        self._content[y + 1][x + 1].put_item(item, is_dumb=True)
                        return True
        return False


    def _is_possible_to_put_item_to_cell(self, x, y, sprite_type):
        """
        """
        if not self._content[y][x].is_empty():
            return False

        # for 1x1 sprites:
        if sprite_type == SPRITE_1x1:
            return True

        # for 2x1 sprites:
        elif sprite_type == SPRITE_2x1 and x + 1 < self._width and \
                                            self._content[y][x + 1].is_empty():
            return True

        # for 1x2 sprites:
        elif sprite_type == SPRITE_1x2 and y + 1 < self._height and \
                                            self._content[y + 1][x].is_empty():
            return True

        # for 2x2 sprites:
        elif sprite_type == SPRITE_2x2 and \
                    y + 1 < self._height and x + 1 < self._width and \
                    self._content[y][x + 1].is_empty() and \
                    self._content[y + 1][x].is_empty() and \
                    self._content[y + 1][x + 1].is_empty():
            return True


    def _draw_items(self):
        """
        """
        for y in xrange(self._height):
            for x in xrange(self._width):
                cell = self._content[y][x]
                if not cell.is_empty() and not cell.is_dumb:
                    self._background.blit(
                        cell.inventory_item.image,
                        (self._content_rect.x + x * self._cell_size,
                         self._content_rect.y + y * self._cell_size))


    def _draw_grid(self):
        """Draw storage items grid.
        """
        pygame.draw.rect(self._background, LINE_COLOR, self._content_rect, 1)

        _x = self._content_rect.x + self._cell_size
        for x in xrange(self._width - 1):
            pygame.draw.line(
                self._background,
                LINE_COLOR,
                (_x + x * self._cell_size, self._content_rect.y),
                (_x + x * self._cell_size, self._content_rect.y +
                                                    self._content_rect.height),
            )

        _y = self._content_rect.y + self._cell_size
        for y in xrange(self._height - 1):
            pygame.draw.line(
                self._background,
                LINE_COLOR,
                (self._content_rect.x, _y + y * self._cell_size),
                (self._content_rect.x + self._content_rect.width,
                                                     _y + y * self._cell_size),
            )


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
            in_border_rect = Rect(
                self.rect.x + self._padding,
                self.rect.y + self._padding,
                self.rect.width - self._padding * 2,
                self.rect.height - self._padding * 2
            )
            if not in_border_rect.collidepoint(event.pos):
                self._enable_dragging_state(event.pos)
            else:
                pass


            return True
        else:
            return False

    # -------------------------------- #

    def __repr__(self):
        """Simple representation.
        """
        return 'Base Storage class instance.'

