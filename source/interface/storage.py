# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     25-05-2018
 Description:
----------------------------------------------------------"""


import pygame
from pygame import Rect, Surface, Color

from frame import Frame
from sounds.sound_library import SoundLibrary
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
OUTLINE_COLOR = Color(110, 110, 110)
CELLS_MATRIX = (2, 4)

AVAILABLE_COLOR = Color(0, 70, 70)

# =========================== Storage cell class =========================== #


class StorageCell(object):
    """Very simple class for cell content of Storage
    """
    def __init__(self):
        """Create empty cell.
        """
        self.clear()


    def is_empty(self, self_item=None):
        """Return True, if cell is empty, else False.
        """
        if self.inventory_item and self.inventory_item != self_item:
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


    def clear(self):
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
        self.sound_library = SoundLibrary.get_instance()

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
                if self._get_cell_available_for(x, y, item):
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


    def remove_item(self, item):
        """Remove item from storage cells.
        """
        for row in self._storage_cells:
            for cell in row:
                if cell.inventory_item == item:
                    cell.clear()


    def add_item_to_specific_cells(self, item, cells):
        """Try to add item to storage defined placement (specific cells).
        Return True, if item was added and False
        """
        upper_left_cell = min(cells)
        item_type = item.type

        # check, if all cells are ready to put item into
        for cell in cells:
            x, y = cell
            if not self._storage_cells[y][x].is_empty(self_item=item):
                return False

        # put item
        for cell in cells:
            x, y = cell
            is_dumb = cell != upper_left_cell
            self._storage_cells[y][x].put_item(item, is_dumb=is_dumb)

        return True


    def draw(self, screen):
        """Draw frame on the screen.

            screen:     display screen Surface
        """
        super(Storage, self).draw(screen)
        if self._dragged_item:
            x, y = pygame.mouse.get_pos()
            x -= self._dragged_item[DI_HALF_IMAGE_WIDTH]
            y -= self._dragged_item[DI_HALF_IMAGE_HEIGHT]
            screen.blit(self._dragged_item[DI_ITEM].image, (x, y))


    def update(self):
        """Update frame state (dragging and resizing handling).
        """
        self._update_dragging() or self._update_dragging_item()


    def bind_external_storage_search(self, external_method):
        """Bind external method "_get_target_storage()" to instance.
        """
        self._get_target_storage = external_method


    def redraw_storage(self):
        """Redraw storage content - grid and items.
        If item from storage is dragging, draw outline shape as well.
        """
        self._draw_storage_grid()
        self._draw_storage_items()
        if self._dragged_item:
            self._draw_dragged_item()


    def _get_target_storage(self):
        """External method.
        Must be binded through "bind_external_storage_search()" method
        before using.
        """
        raise RuntimeError('External method _get_target_storage() '
                           'not binded!')


    def _get_cell_available_for(self, x, y, item):
        """Check, if item with "sprite_type" size can be put to cell
        with x, y coords (counting around ones).
        """
        if not self._storage_cells[y][x].is_empty(self_item=item):
            return None

        sprite_type = item.type

        # for 1x1 sprites:
        if sprite_type == SPRITE_1x1:
            return [(x, y)]

        # for 2x1 sprites:
        elif sprite_type == SPRITE_2x1:
            if  x + 1 < self._width_in_cells and \
                        self._storage_cells[y][x + 1].is_empty(self_item=item):
                return [(x, y), (x + 1, y)]
            elif x - 1 >= 0 and \
                        self._storage_cells[y][x - 1].is_empty(self_item=item):
                return [(x - 1, y), (x, y)]

        # for 1x2 sprites:
        elif sprite_type == SPRITE_1x2:
            if y + 1 < self._height_in_cells and \
                        self._storage_cells[y + 1][x].is_empty(self_item=item):
                return [(x, y), (x, y + 1)]
            elif y - 1 >= 0 and \
                        self._storage_cells[y - 1][x].is_empty(self_item=item):
                return [(x, y - 1), (x, y)]

        # for 2x2 sprites:
        elif sprite_type == SPRITE_2x2:
            if y + 1 < self._height_in_cells:
                if x + 1 < self._width_in_cells and \
                   self._storage_cells[y][x + 1].is_empty(self_item=item) and \
                   self._storage_cells[y + 1][x].is_empty(self_item=item) and \
                   self._storage_cells[y + 1][x + 1].is_empty(self_item=item):
                    return [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
                elif x - 1 >= 0 and \
                   self._storage_cells[y][x - 1].is_empty(self_item=item) and \
                   self._storage_cells[y + 1][x].is_empty(self_item=item) and \
                   self._storage_cells[y + 1][x - 1].is_empty(self_item=item):
                    return [(x - 1, y), (x, y), (x - 1, y + 1), (x, y + 1)]
            if y - 1 >= 0:
                if x + 1 < self._width_in_cells and \
                   self._storage_cells[y][x + 1].is_empty(self_item=item) and \
                   self._storage_cells[y - 1][x].is_empty(self_item=item) and \
                   self._storage_cells[y - 1][x + 1].is_empty(self_item=item):
                    return [(x, y - 1), (x + 1, y - 1), (x, y), (x + 1, y)]
                elif x - 1 >= 0 and \
                   self._storage_cells[y][x - 1].is_empty(self_item=item) and \
                   self._storage_cells[y - 1][x].is_empty(self_item=item) and \
                   self._storage_cells[y - 1][x - 1].is_empty(self_item=item):
                    return [(x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)]
        return None


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
        x, y = click_pos
        relative_pos = x - self.rect.x, y - self.rect.y
        for rect, coords in self._storage_cells_areas:
            if rect.collidepoint(relative_pos):
                return coords
        else:
            return None


    def _start_item_dragging(self, x, y, mouse_pos):
        """Mark cell's item by (x, y) coords as "dragged" one.
        Item is drawn as outlined, fill metadata for dragged item.
        """
        self.sound_library.play('item_pick.wav')
        cell = self._storage_cells[y][x]

        if cell.is_dumb:
            cell, (x, y) = self._get_main_item_cell(cell)

        image = cell.inventory_item.image
        mask = pygame.mask.from_surface(image)
        outline_list = mask.outline()
        width, height = image.get_size()
        self._dragged_item = {
            DI_OUTLINED_IMAGE:  Surface((width, height)),
            DI_ITEM: cell.inventory_item,
            DI_CELL_X: x,
            DI_CELL_Y: y,
            DI_HALF_IMAGE_WIDTH: image.get_width() / 3,
            DI_HALF_IMAGE_HEIGHT: image.get_height() / 3,
            DI_LAST_MOUSE_POS: mouse_pos,
            DI_TARGET_CELLS_LIST: None,
            DI_TARGET_STORAGE: None,
        }
        outlined_image = self._dragged_item[DI_OUTLINED_IMAGE]
        pygame.draw.lines(outlined_image, OUTLINE_COLOR, True, outline_list, 1)

        # draw cell borders
        if width > CELL_SIZE:
            pygame.draw.line(outlined_image, LINE_COLOR,
                                   (CELL_SIZE - 1, 0), (CELL_SIZE - 1, height))
        if height > CELL_SIZE:
            pygame.draw.line(outlined_image, LINE_COLOR,
                                    (0, CELL_SIZE - 1), (width, CELL_SIZE - 1))

        self._draw_dragged_item()


    def _draw_dragged_item(self):
        """Draw dragged item in storage.
        """
        x = self._dragged_item[DI_CELL_X]
        y = self._dragged_item[DI_CELL_Y]
        image = self._dragged_item[DI_OUTLINED_IMAGE]
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
        Return True, if state was enabled (disabling was successful).
        Move item, if it have to do this.
        """
        if self._dragged_item:
            self.sound_library.play('item_put.wav')
            cells = self._dragged_item[DI_TARGET_CELLS_LIST]
            storage = self._dragged_item[DI_TARGET_STORAGE]
            if cells and storage:
                item = self._dragged_item[DI_ITEM]
                if storage == self:
                    self.remove_item(item)
                    self.add_item_to_specific_cells(item, cells)
                else:
                    storage.add_item_to_specific_cells(item, cells)
                    storage.redraw_storage()
                    self.remove_item(item)
                self.redraw_storage()

            self._dragged_item = None
            self.redraw_storage()
            return True


    def _update_dragging_item(self):
        """Handle process of dragging item from storage.
        If item could be put to mouse pointer location, mark
        target cells with special color filling.
        """
        # nothing to handle, if no item is dragging
        dragged_item = self._dragged_item
        if not dragged_item:
            return False

        # handled, if nothing was changed
        current_mouse_pos = pygame.mouse.get_pos()
        if current_mouse_pos == dragged_item[DI_LAST_MOUSE_POS]:
            return True
        else:
            dragged_item[DI_LAST_MOUSE_POS] = current_mouse_pos

        # ~ 1. Get last and current cells/storage pairs ~

        last_cells = dragged_item[DI_TARGET_CELLS_LIST]
        last_storage = dragged_item[DI_TARGET_STORAGE]

        current_cells = None
        current_storage = None

        storage = self._get_target_storage(current_mouse_pos)
        if storage:
            coords = storage._get_cell_coords_by_click_pos(current_mouse_pos)
            if coords:
                x, y = coords
                cells_list = storage._get_cell_available_for(
                                                   x, y, dragged_item[DI_ITEM])
                if cells_list:
                    current_cells = cells_list
                    current_storage = storage

        # ~ 2. Handle changes ~

        # handled, if all cells are the same ~
        if (current_cells == last_cells) and (current_storage == last_storage):
            return True

        # redraw last storage, if something was changed
        if last_cells:
            last_storage.redraw_storage()

        # mark cells, if we have new ones
        if current_cells:
            current_storage._mark_available_cells(cells_list)

        # update dragging item state
        dragged_item[DI_TARGET_CELLS_LIST] = current_cells
        dragged_item[DI_TARGET_STORAGE] = current_storage
        return True


    def _mark_available_cells(self, cell_list):
        """Fill by AVAILABLE_COLOR cells in "cell_list".
        """
        for rect, coords in self._storage_cells_areas:
            if coords in cell_list:
                inner_rect = (
                    rect.x + 1,
                    rect.y + 1,
                    rect.width - 1,
                    rect.height - 1,
                )
                self._background.fill(AVAILABLE_COLOR, inner_rect)


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
                cell_coords = self._get_cell_coords_by_click_pos(event.pos)
                if not cell_coords:
                    return True

                x, y = cell_coords
                if not self._storage_cells[y][x].is_empty():
                    self._start_item_dragging(x, y, event.pos)

            return True
        else:
            return False

    # -------------------------------- #

    def __repr__(self):
        """Simple representation.
        """
        return 'Base Storage class instance.'

