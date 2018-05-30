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
OUTLINE_COLOR = Color(155, 83, 0)
CELLS_MATRIX = (2, 4)

# =========================== Storage cell class =========================== #


class StorageCell(object):
    """Very simple class for cell content of Storage
    """
    def __init__(self):
        """Create empty cell.
        """
        self.clear_cell()


    def is_empty(self):
        """Return True, if cell is empty, else False.
        """
        if self.inventory_item:
            return False
        else:
            return True


    def put_item(self, item, is_dumb=False):
        """Fill cell with item (main part or dumb one).

            item:          Inventory object
            is_dumb:       True, for upper-left corner, False for others
        """
        self.inventory_item = item
        self.is_dumb = is_dumb


    def clear_cell(self):
        """Make cell clear.
        """
        self.inventory_item = None
        self.is_dumb = False


    def __repr__(self):
        """Simple representation.
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
        # numbers of cells by horizontal and vertical coords
        self._width_in_cells, self._height_in_cells = CELLS_MATRIX

        # content of storage - 2x dimension array of StorageCell inst.
        self._storage_cells = [
            [StorageCell() for x in xrange(self._width_in_cells)]
                           for y in xrange(self._height_in_cells)]

        start_x, start_y = STORAGE_TOP_LEFT
        self._cell_size = CELL_SIZE
        self._padding = PADDING

        # metadata about item, currently dragged
        # None, if no item is being dragged
        self._dragged_item = None

        # ~ Create Frame object ~

        final_rect = Rect(rect)
        width_grid = self._cell_size * self._width_in_cells
        if final_rect.width < width_grid + start_x + PADDING:
            final_rect.width = width_grid + start_x + PADDING
        height_grid = self._cell_size* self._height_in_cells
        if final_rect.height < height_grid + start_y + PADDING:
            final_rect.height = height_grid + start_y + PADDING

        # rect of storage cells area
        self._storage_rect = Rect(start_x, start_y, width_grid, height_grid)

        # list of tuples (Rect, (x,y)) for every storage cell
        self._storage_cells_areas = self._get_storage_cells_areas()

        super(Storage, self).__init__(
            rect=final_rect,
            tileset_path=TILESET_PATH,
            parts_rects=PARTS_RECTS,
            max_size=MAX_SIZE,
            min_size=MIN_SIZE,
            bg_color=BACKGROUND_COLOR,
        )

        # ~ Draw grid ~

        self._draw_storage_grid()

        # ~ EVENTS ~

        self.add_event_handler(pygame.MOUSEBUTTONUP,
                               self._event_mousebutton_up)
        self.add_event_handler(pygame.MOUSEBUTTONDOWN,
                               self._event_mousebutton_down)


    def add_item(self, item):
        """Try to add item to storage with non-defined placement.
        Return True, if item was added and False
        """
        item_type = item.type
        for y in xrange(self._height_in_cells):
            for x in xrange(self._width_in_cells):
                if self._is_cell_available_for(x, y, item_type):
                    # for 1x1 sprites:
                    if item_type == SPRITE_1x1:
                        self._storage_cells[y][x].put_item(item)
                        return True

                    # for 2x1 sprites:
                    elif item_type == SPRITE_2x1:
                        self._storage_cells[y][x].put_item(item)
                        self._storage_cells[y][x + 1].put_item(
                                                            item, is_dumb=True)
                        return True

                    # for 1x2 sprites:
                    elif item_type == SPRITE_1x2:
                        self._storage_cells[y][x].put_item(item)
                        self._storage_cells[y + 1][x].put_item(
                                                            item, is_dumb=True)
                        return True

                    # for 2x2 sprites:
                    elif item_type == SPRITE_2x2:
                        self._storage_cells[y][x].put_item(item)
                        self._storage_cells[y + 1][x].put_item(
                                                            item, is_dumb=True)
                        self._storage_cells[y][x + 1].put_item(
                                                            item, is_dumb=True)
                        self._storage_cells[y + 1][x + 1].put_item(
                                                            item, is_dumb=True)
                        return True
        return False


    def draw(self, screen):
        """Draw frame on the screen.

            screen:     display screen Surface
        """
        super(Storage, self).draw(screen)
        if self._dragged_item:
            x, y = pygame.mouse.get_pos()
            x -= self._dragged_item['half_width']
            y -= self._dragged_item['half_height']
            screen.blit(self._dragged_item['image'], (x, y))


    def _is_cell_available_for(self, x, y, sprite_type):
        """Check, if item with "sprite_type" size can be put to cell
        with x, y coords.
        """
        if not self._storage_cells[y][x].is_empty():
            return False

        # for 1x1 sprites:
        if sprite_type == SPRITE_1x1:
            return True

        # for 2x1 sprites:
        elif sprite_type == SPRITE_2x1 and x + 1 < self._width_in_cells and \
                                            self._storage_cells[y][x + 1].is_empty():
            return True

        # for 1x2 sprites:
        elif sprite_type == SPRITE_1x2 and y + 1 < self._height_in_cells and \
                                            self._storage_cells[y + 1][x].is_empty():
            return True

        # for 2x2 sprites:
        elif sprite_type == SPRITE_2x2 and \
                    y + 1 < self._height_in_cells and x + 1 < self._width_in_cells and \
                    self._storage_cells[y][x + 1].is_empty() and \
                    self._storage_cells[y + 1][x].is_empty() and \
                    self._storage_cells[y + 1][x + 1].is_empty():
            return True


    def _draw_storage_items(self):
        """Draw items in storage.
        """
        for y in xrange(self._height_in_cells):
            for x in xrange(self._width_in_cells):
                cell = self._storage_cells[y][x]
                if not cell.is_empty() and not cell.is_dumb:
                    self._background.blit(
                        cell.inventory_item.image,
                        (self._storage_rect.x + x * self._cell_size,
                         self._storage_rect.y + y * self._cell_size))


    def _draw_storage_grid(self):
        """Draw storage items grid.
        """
        self._background.fill(BACKGROUND_COLOR, self._storage_rect)
        pygame.draw.rect(self._background, LINE_COLOR, self._storage_rect, 1)

        _x = self._storage_rect.x + self._cell_size
        for x in xrange(self._width_in_cells - 1):
            pygame.draw.line(
                self._background,
                LINE_COLOR,
                (_x + x * self._cell_size, self._storage_rect.y),
                (_x + x * self._cell_size, self._storage_rect.y +
                                                    self._storage_rect.height),
            )

        _y = self._storage_rect.y + self._cell_size
        for y in xrange(self._height_in_cells - 1):
            pygame.draw.line(
                self._background,
                LINE_COLOR,
                (self._storage_rect.x, _y + y * self._cell_size),
                (self._storage_rect.x + self._storage_rect.width,
                                                     _y + y * self._cell_size),
            )


    def _get_storage_cells_areas(self):
        """Form a dictionary, where keys are Rects instances, and
        values are (x, y) coords tuples of appropriate cells.
        Used for self._storage_cells_areas attr.
        """
        table = []
        cell_size = self._cell_size
        _x = self._storage_rect.x
        _y = self._storage_rect.y
        for y in xrange(self._height_in_cells):
            for x in xrange(self._width_in_cells):
                rect = Rect(_x + x * cell_size,
                            _y + y * cell_size,
                            cell_size,
                            cell_size)
                table.append((rect, (x, y)))
        return table


    def _get_cell_coords_by_click_pos(self, click_pos):
        """Return coords of cell, if was clicked to it.
        Else returns None.
        """
        for rect, coords in self._storage_cells_areas:
            if rect.collidepoint(click_pos):
                return coords
        else:
            return None


    def _start_item_dragging(self, x, y):
        """Mark cell's item by (x, y) coords as "dragged" one.
        Item is drawn as outlined, fill metadata for dragged item.
        """
        cell = self._storage_cells[y][x]

        if cell.is_dumb:
            cell, (x, y) = self._get_main_item_cell(cell)

        image = cell.inventory_item.image
        mask = pygame.mask.from_surface(image)
        outline_list = mask.outline()
        self._dragged_item = {
            'outline_image':  Surface(image.get_size()),
            'image': image,
            'x': x,
            'y': y,
            'half_width': image.get_width() / 2,
            'half_height': image.get_height() / 2,
        }
        pygame.draw.lines(self._dragged_item['outline_image'], OUTLINE_COLOR,
                                                        True, outline_list, 1)
        self._draw_dragged_item()


    def _draw_dragged_item(self):
        """Draw dragged item in storage.
        """
        x = self._dragged_item['x']
        y = self._dragged_item['y']
        image = self._dragged_item['outline_image']
        width, height = image.get_size()
        cell_rect = Rect(
            self._storage_rect.x + x * self._cell_size,
            self._storage_rect.y + y * self._cell_size,
            width - 1,
            height - 1
        )
        cell_place = self._background.subsurface(cell_rect)
        cell_place.blit(image, (1, 1))


    def _get_main_item_cell(self, cell):
        """Return "main" cell it's coords for chosen "dumb".
        """
        for y, row in enumerate(self._storage_cells):
            for x, some_cell in enumerate(row):
                if not some_cell.is_dumb and \
                               some_cell.inventory_item == cell.inventory_item:
                    return some_cell, (x, y)


    def _dragging_item_handled_off(self):
        """Tries to disable dragging item state.
        Return True, if state was enabled (disabling was successful)
        """
        if self._dragged_item:
            self._dragged_item = None
            self._draw_storage_grid()
            self._draw_storage_items()
            return True

    # ---------------------- EVENTS ----------------------- #

    def _event_mousebutton_up(self, event):
        """Handle mouse button up event.
        """
        if self._dragging_handled_off() or self._dragging_item_handled_off():
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
                x, y = event.pos
                relative_pos = x - self.rect.x, y - self.rect.y
                cell_coords = self._get_cell_coords_by_click_pos(relative_pos)
                if not cell_coords:
                    return True

                x, y = cell_coords
                if not self._storage_cells[y][x].is_empty():
                    self._start_item_dragging(x, y)

            return True
        else:
            return False

    # -------------------------------- #

    def __repr__(self):
        """Simple representation.
        """
        return 'Base Storage class instance.'

