# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Description: Simple inventory object class
----------------------------------------------------------"""

import pygame
from pygame import Rect

from misc._enums import *


# ==================== Inventory object class ============================== #

class InventoryObject(object):
    """ Single sprite of the inventory object.
    Class must be initialized through:

        InventorySprite.add_sprites()

    method before actually using sprites.
    """
    _scale = None
    _tileset = {}


    @classmethod
    def add_sprites(cls, filename, alias, sprite_type, scale):
        """ Load tileset for inventory objects.

            filename:       name of tileset image
            alias:          alias for sprites set (user defined)
            sprite_type:    enum: sprite size (SPRITE_1x1, SPRITE_2x1,
                            SPRITE_1x2 or SPRITE_2x2)
            scale:          1 or 2 (for 2x size, every pixel doubles)

        All sprites consist of tiles 32x32.
        Order of tiles: from left to right, and from top to bottom.
        """
        image = pygame.image.load(filename).convert_alpha()
        image_width, image_height = image.get_size()
        _tileset = []

        size_x, size_y = cls._get_sizes_x_y(sprite_type)

        count = 0
        for tile_y in xrange(0, image_height / size_y):
            for tile_x in xrange(0, image_width / size_x):
                rect = (tile_x * size_x, tile_y * size_y, size_x, size_y)
                tile = image.subsurface(rect).convert_alpha()
                if scale == 2:
                    _tileset.append((pygame.transform.scale2x(tile),
                                     sprite_type))
                elif scale == 1:
                    _tileset.append((tile, sprite_type))
                else:
                    raise RuntimeError('Sorry! only scale 1x and 2x is '
                                                              'supported now!')
        if alias in cls._tileset:
            cls._tileset[alias].extend(_tileset)
        else:
            cls._tileset[alias] = _tileset

        if not cls._scale:
            cls._scale = scale

        del image


    def __init__(self, alias, tile_number):
        """ Layer's cell creation.

            alias:          alias for sprites set (user defined)
            tile_number:    number of tile in _tileset list.
        """
        self.image, self.type = self._tileset[alias][tile_number]


    @staticmethod
    def _get_sizes_x_y(enum_sprite_size):
        """Return tuple (size_x, size_y) for chosen sprite size
        enum type (SPRITE_1x1, SPRITE_2x1, SPRITE_1x2 or SPRITE_2x2)
        """
        if enum_sprite_size == SPRITE_1x1:
            size_x = 32
            size_y = 32
        elif enum_sprite_size == SPRITE_1x2:
            size_x = 32
            size_y = 64
        elif enum_sprite_size == SPRITE_2x1:
            size_x = 64
            size_y = 32
        elif enum_sprite_size == SPRITE_2x2:
            size_x = 64
            size_y = 64
        return size_x, size_y


    def __repr__(self):
        """Simple representation.
        """
        return 'Inventory object: type #%d' % self.type
