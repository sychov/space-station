# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     25-05-2018
 Description:
----------------------------------------------------------"""


import pygame
from pygame import Rect, Surface, Color

from interface.frame import Frame, FrameConfig
from sounds.sound_library import SoundLibrary
from misc._enums import *


# ========================= Storage config class ========================== #


class StorageConfig(object):
    """Small class for Storage class configuration purposes.
    """
    def __init__(self, frame_config, grid_size, grid_top_left_corner,
                        grid_line_color, item_outline_color, cell_avail_color):
        """
        Creates simple config object for Storage class:

            frame_config:           FrameConfig instance
            grid_size:              (<cells count by X>, <cells count by Y>)
            grid_top_left_corner:   (x, y) shift from top-level corner,
                                    where cells grid begins
            grid_line_color:        Color inst, of cells grid lines
            item_outline_color:     Color inst, of item's outline
            cell_avail_color:       Color inst, of available cell's marking
        """
        self.frame_config = frame_config
        self.grid_size = grid_size
        self.grid_top_left_corner = grid_top_left_corner
        self.grid_line_color = grid_line_color
        self.outline_color = item_outline_color
        self.cell_avail_color = cell_avail_color


# ============================= Storage class ============================= #


class Storage(Frame):
    """Base Storage class.
    """
    _cell_size = None


    @classmethod
    def set_cell_size(cls, size):
        """
        """
        if cls._cell_size:
            raise RuntimeError('Cell size is already set!')
        if cls != Storage:
            raise RuntimeError('Cell size must be set through '
                               'Storage.set_cell_size() method!')
        cls._cell_size = size


    def __init__(self, rect, storage_config, storage_content):
        """
            rect:  x, y, width, height (on global screen)
            storage_config
            storage_content
        """
        if not self._cell_size:
            raise RuntimeError('Set Storage cell size first!')

        # ~ 1. Init base attributes ~

        self.content = storage_content
        if (self.content.width, self.content.height
                                                 ) != storage_config.grid_size:
            raise RuntimeError('Incorrect size of Storage content!')

        self._sound_library = SoundLibrary.get_instance()

        # metadata about item, currently dragged. None, if no item dragging
        self._dragged_item = None

        self._line_color = storage_config.grid_line_color
        self._item_outline_color = storage_config.outline_color
        self._available_cell_color = storage_config.cell_avail_color

        # ~ 2. Create Frame object ~

        padding = storage_config.frame_config.padding
        start_x, start_y = storage_config.grid_top_left_corner

        final_rect = Rect(rect)
        width_grid = self._cell_size * self.content.width
        if final_rect.width < width_grid + start_x + padding:
            final_rect.width = width_grid + start_x + padding
        height_grid = self._cell_size* self.content.height
        if final_rect.height < height_grid + start_y + padding:
            final_rect.height = height_grid + start_y + padding

        # rect of storage cells area
        self._storage_rect = Rect(start_x, start_y, width_grid, height_grid)

        # list of tuples (Rect, (x,y)) for every storage cell
        self._storage_cells_areas = self._get_storage_cells_areas()

        super(Storage, self).__init__(rect=final_rect,
                                      frame_config=storage_config.frame_config)

        # ~ 3. Draw grid ~

        self._draw_storage_grid()

        # ~ EVENTS ~

        self.add_event_handler(pygame.MOUSEBUTTONUP,
                               self._event_mousebutton_up)
        self.add_event_handler(pygame.MOUSEBUTTONDOWN,
                               self._event_mousebutton_down)


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


    def _draw_storage_items(self):
        """Draw items in storage.
        """
        for y in xrange(self.content.height):
            for x in xrange(self.content.width):
                cell = self.content.storage_cells[y][x]
                if not cell.is_empty() and not cell.is_dumb:
                    self._background.blit(
                        cell.inventory_item.image,
                        (self._storage_rect.x + x * self._cell_size,
                         self._storage_rect.y + y * self._cell_size))


    def _draw_storage_grid(self):
        """Draw storage items grid.
        """
        self._background.fill(self._background_color, self._storage_rect)
        pygame.draw.rect(self._background, self._line_color,
                                                         self._storage_rect, 1)

        _x = self._storage_rect.x + self._cell_size
        for x in xrange(self.content.width - 1):
            pygame.draw.line(
                self._background,
                self._line_color,
                (_x + x * self._cell_size, self._storage_rect.y),
                (_x + x * self._cell_size, self._storage_rect.y +
                                                    self._storage_rect.height),
            )

        _y = self._storage_rect.y + self._cell_size
        for y in xrange(self.content.height - 1):
            pygame.draw.line(
                self._background,
                self._line_color,
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
        for y in xrange(self.content.height):
            for x in xrange(self.content.width):
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
        self._sound_library.play('item_pick.wav')
        cell = self.content.storage_cells[y][x]

        if cell.is_dumb:
            cell, (x, y) = self.content.get_main_item_cell(cell)

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
        pygame.draw.lines(outlined_image, self._item_outline_color,
                                                         True, outline_list, 1)

        # draw cell borders
        if width > self._cell_size:
            pygame.draw.line(outlined_image, self._line_color,
                       (self._cell_size - 1, 0), (self._cell_size - 1, height))
        if height > self._cell_size:
            pygame.draw.line(outlined_image, self._line_color,
                        (0, self._cell_size - 1), (width, self._cell_size - 1))

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


    def _dragging_item_handled_off(self):
        """Tries to disable dragging item state.
        Return True, if state was enabled (disabling was successful).
        Move item, if it have to do this.
        """
        if self._dragged_item:
            self._sound_library.play('item_put.wav')
            cells = self._dragged_item[DI_TARGET_CELLS_LIST]
            storage = self._dragged_item[DI_TARGET_STORAGE]
            if cells and storage:
                item = self._dragged_item[DI_ITEM]
                if storage == self:
                    self.content.remove_item(item)
                    self.content.add_item_to_specific_cells(item, cells)
                else:
                    storage.content.add_item_to_specific_cells(item, cells)
                    storage.redraw_storage()
                    self.content.remove_item(item)
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
                cells_list = storage.content.get_cell_available_for(
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
                self._background.fill(self._available_cell_color, inner_rect)


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
                if not self.content.storage_cells[y][x].is_empty():
                    self._start_item_dragging(x, y, event.pos)

            return True
        else:
            return False

    # -------------------------------- #

    def __repr__(self):
        """Simple representation.
        """
        return 'Base Storage class instance.'

