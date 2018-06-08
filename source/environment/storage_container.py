# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     01-06-2018
 Description:
----------------------------------------------------------"""


from misc._enums import *


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


# ========================= Storage content class ========================== #


class StorageContent(object):
    """Data model class for Storage class.
    """
    def __init__(self, width, height):
        """
        """
        self.width = width
        self.height = height
        self.storage_cells = [[StorageCell() for x in xrange(self.width)]
                                                 for y in xrange(self.height)]


    def add_item(self, item):
        """Try to add item to storage with non-defined placement.
        Return True, if item was added and False
        """
        item_type = item.type
        for y in xrange(self.height):
            for x in xrange(self.width):
                if self.get_cell_available_for(x, y, item):
                    # for 1x1 sprites:
                    if item_type == SPRITE_1x1:
                        self.storage_cells[y][x].put_item(item)
                        return True

                    # for 2x1 sprites:
                    elif item_type == SPRITE_2x1:
                        self.storage_cells[y][x].put_item(item)
                        self.storage_cells[y][x + 1].put_item(
                                                            item, is_dumb=True)
                        return True

                    # for 1x2 sprites:
                    elif item_type == SPRITE_1x2:
                        self.storage_cells[y][x].put_item(item)
                        self.storage_cells[y + 1][x].put_item(
                                                            item, is_dumb=True)
                        return True

                    # for 2x2 sprites:
                    elif item_type == SPRITE_2x2:
                        self.storage_cells[y][x].put_item(item)
                        self.storage_cells[y + 1][x].put_item(
                                                            item, is_dumb=True)
                        self.storage_cells[y][x + 1].put_item(
                                                            item, is_dumb=True)
                        self.storage_cells[y + 1][x + 1].put_item(
                                                            item, is_dumb=True)
                        return True
        return False


    def remove_item(self, item):
        """Remove item from storage cells.
        """
        for row in self.storage_cells:
            for cell in row:
                if cell.inventory_item == item:
                    cell.clear()


    def add_item_to_specific_cells(self, item, cells):
        """Try to add item to storage defined placement (specific cells).
        Return True, if item was added and False

            item:
            cells:

        """
        upper_left_cell = min(cells)
        item_type = item.type

        # check, if all cells are ready to put item into
        for cell in cells:
            x, y = cell
            if not self.storage_cells[y][x].is_empty(self_item=item):
                return False

        # put item
        for cell in cells:
            x, y = cell
            is_dumb = cell != upper_left_cell
            self.storage_cells[y][x].put_item(item, is_dumb=is_dumb)

        return True


    def get_cell_available_for(self, x, y, item):
        """Check, if item with "sprite_type" size can be put to cell
        with x, y coords (counting around ones).
        """
        if not self.storage_cells[y][x].is_empty(self_item=item):
            return None

        sprite_type = item.type

        # for 1x1 sprites:
        if sprite_type == SPRITE_1x1:
            return [(x, y)]

        # for 2x1 sprites:
        elif sprite_type == SPRITE_2x1:
            if  x + 1 < self.width and \
                        self.storage_cells[y][x + 1].is_empty(self_item=item):
                return [(x, y), (x + 1, y)]
            elif x - 1 >= 0 and \
                        self.storage_cells[y][x - 1].is_empty(self_item=item):
                return [(x - 1, y), (x, y)]

        # for 1x2 sprites:
        elif sprite_type == SPRITE_1x2:
            if y + 1 < self.height and \
                        self.storage_cells[y + 1][x].is_empty(self_item=item):
                return [(x, y), (x, y + 1)]
            elif y - 1 >= 0 and \
                        self.storage_cells[y - 1][x].is_empty(self_item=item):
                return [(x, y - 1), (x, y)]

        # for 2x2 sprites:
        elif sprite_type == SPRITE_2x2:
            if y + 1 < self.height:
                if x + 1 < self.width and \
                   self.storage_cells[y][x + 1].is_empty(self_item=item) and \
                   self.storage_cells[y + 1][x].is_empty(self_item=item) and \
                   self.storage_cells[y + 1][x + 1].is_empty(self_item=item):
                    return [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
                elif x - 1 >= 0 and \
                   self.storage_cells[y][x - 1].is_empty(self_item=item) and \
                   self.storage_cells[y + 1][x].is_empty(self_item=item) and \
                   self.storage_cells[y + 1][x - 1].is_empty(self_item=item):
                    return [(x - 1, y), (x, y), (x - 1, y + 1), (x, y + 1)]
            if y - 1 >= 0:
                if x + 1 < self.width and \
                   self.storage_cells[y][x + 1].is_empty(self_item=item) and \
                   self.storage_cells[y - 1][x].is_empty(self_item=item) and \
                   self.storage_cells[y - 1][x + 1].is_empty(self_item=item):
                    return [(x, y - 1), (x + 1, y - 1), (x, y), (x + 1, y)]
                elif x - 1 >= 0 and \
                   self.storage_cells[y][x - 1].is_empty(self_item=item) and \
                   self.storage_cells[y - 1][x].is_empty(self_item=item) and \
                   self.storage_cells[y - 1][x - 1].is_empty(self_item=item):
                    return [(x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)]
        return None


    def get_main_item_cell(self, cell):
        """Return "main" cell it's coords for chosen "dumb".
        """
        for y, row in enumerate(self.storage_cells):
            for x, some_cell in enumerate(row):
                if not some_cell.is_dumb and \
                               some_cell.inventory_item == cell.inventory_item:
                    return some_cell, (x, y)

