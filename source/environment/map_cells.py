# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Description: Cell of game map's layer class.
----------------------------------------------------------"""

import pygame
from pygame import Rect

from source.misc._enums import *
from ._tile_collisions import TILES_COLLISIONS

# ------------------------------ CONST ------------------------------------- #

IGNORED_TILES_NUMS = [1980]

# ======================== BASE LAYER CELL CLASS ============================ #

class LayerCell(object):
    """ Single cell of the game map layer.
    Class must be initialized through

        LayerCell.initialize()

    method before using. This is because we don't want to read tileset
    every instance init, but we dont want to hardcode its name.
    """
    SIZE = None

    _is_class_initialized = False
    _scale = None
    _is_walkable = True
    _tileset = []


    @classmethod
    def initialize(cls, filename, size, scale, used_tiles):
        """ Load tileset for a game map.

            filename:       name of tileset image
            size:           size of 1 tile
            scale:          1 or 2 (for 2x size, every pixel doubles)
            used_tiles:     list of tiles numbers, used in game map

        Tileset must be single image. Tiles have to be supported
        by Tiled editor, order: from left to right, and from top to bottom.
        """
        image = pygame.image.load(filename).convert_alpha()
        image_width, image_height = image.get_size()
        _tileset = []

        count = 0
        for tile_y in range(0, image_height // size):
            for tile_x in range(0, image_width // size):

                # we don't need to load tiles images of not used tiles
                count += 1
                if count not in used_tiles:
                    _tileset.append(None)
                    continue

                rect = (tile_x * size, tile_y * size, size, size)
                tile = image.subsurface(rect).convert_alpha()
                if scale == 2:
                    _tileset.append(pygame.transform.scale2x(tile))
                elif scale == 1:
                    _tileset.append(tile)
                else:
                    raise RuntimeError('Sorry! only scale 1x and 2x is '
                                                              'supported now!')
        cls._tileset = _tileset
        cls.SIZE = size * scale
        cls._is_class_initialized = True
        cls._scale = scale
        del image


    def __init__(self, x, y, tile_number):
        """ Layer's cell creation.

            x, y:           tile coors on game map
            tile_number:    number of tile in _tileset list.
        """
        if not self._is_class_initialized:
            raise RuntimeError('Impossible to use insances before class '
                            'initializing! Use <class>.initialize(...) first!')
        self.rect = Rect(x * self.SIZE, y * self.SIZE, self.SIZE, self.SIZE)

        if tile_number not in IGNORED_TILES_NUMS:
            self.image = self._tileset[tile_number - 1]
        else:
            self.image = self._tileset[1]

        self.tile_number = tile_number
        self._tile_x = x
        self._tile_y = y

        # correction of collisions map for some sprites (bottom objects)
        if tile_number in TILES_COLLISIONS:
            special = TILES_COLLISIONS[tile_number]
            self.rect.x += special[X] * self._scale
            self.rect.y += special[Y] * self._scale
            self.rect.width -= special[WIDTH] * self._scale
            self.rect.height -= special[HEIGHT] * self._scale


    def set_tile(self, tile_num, walkable=None):
        """Change tile number to selected one.
        """
        self.tile_number = tile_num
        self.image = self._tileset[tile_num - 1]
        if walkable is not None:
            self.is_walkable = walkable


    def __repr__(self):
        """Simple representation.
        """
        return 'Cell #%d' % self.tile_number


# ======================== FLOOR CELL CLASS ============================ #


class FloorCell(LayerCell):
    """ Single cell of the game map floor layer.
    Remember, that base class must be initialized through

        LayerCell.initialize()

    """
    def __init__(self, x, y, tile_number, is_walkable=True):
        """ Layer's cell creation.

            x, y:           tile coors on game map
            tile_number:    number of tile in _tileset list.
            is_walkable:    boolean value, could this tile be walked
                            through, or not.
        """
        super(FloorCell, self).__init__(x, y, tile_number)
        self.is_walkable = is_walkable


    def __repr__(self):
        """Simple representation.
        """
        return 'Cell #%d, free: %s' % (self.tile_number, str(self.is_walkable))


# ======================== OBJECT CELL CLASS ============================ #


class ObjectCell(LayerCell):
    """ Single cell of the game map object layer.
    Remember, that base class must be initialized through

        LayerCell.initialize()

    """
    def __init__(self, x, y, tile_number, is_walkable=True):
        """ Layer's cell creation.

            x, y:           tile coors on game map
            tile_number:    number of tile in _tileset list.
            is_walkable:    boolean value, could this tile be walked
                            through, or not.
        """
        super(ObjectCell, self).__init__(x, y, tile_number)
        self.is_walkable = is_walkable
        self.object = None


    def link_to_object(self, object_):
        """Link map cell with map object by setting "object"
        attribute of cell.

            object_:        BaseObject instance.
        """
        self.object = object_
        if object_ is not None:
            object_.set_coords((self._tile_x, self._tile_y))


    def __repr__(self):
        """Simple representation.
        """
        return 'Cell #%d, free: %s' % (self.tile_number, str(self.is_walkable))

