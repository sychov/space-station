# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Description: Cell of game map's layer class.
----------------------------------------------------------"""

import pygame
from pygame import Rect

from _tile_collisions import TILES_COLLISIONS
from _enums import *


# ========================== LAYER CELL CLASS ============================== #

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
    _tileset = []


    @classmethod
    def initialize(cls, filename, size, scale, used_tiles):
        """ Load tileset for a game map.

            filename:   name of tileset image
            size:       size of 1 tile
            scale:      1 or 2 (for 2x size, every pixel doubles)

        Tileset must be single image. Tiles have to be supported
        by Tiled editor, order: from left to right, and from top to bottom.
        """
        image = pygame.image.load(filename).convert_alpha()
        image_width, image_height = image.get_size()
        _tileset = []

        count = 0
        for tile_y in xrange(0, image_height / size):
            for tile_x in xrange(0, image_width / size):

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


    def __init__(self, x, y, tile_number, is_walkable=True):
        """ Layer's cell creation.

            x, y:           tile coors on game map
            tile_number:    number of tile in _tileset list.
            is_walkable:    boolean value, could this tile be walked
                            through, or not.
        """
        if not self._is_class_initialized:
            raise RuntimeError('Impossible to use insances before class '
                            'initializing! Use <class>.initialize(...) first!')
        self.rect = Rect(x * self.SIZE, y * self.SIZE, self.SIZE, self.SIZE)
        self.image = self._tileset[tile_number - 1]
        self.tile_number = tile_number

        # correction of collisions map for some sprites (bottom objects)
        if tile_number in TILES_COLLISIONS:
            special = TILES_COLLISIONS[tile_number]
            self.rect.x += special[X] * self._scale
            self.rect.y += special[Y] * self._scale
            self.rect.width -= special[WIDTH] * self._scale
            self.rect.height -= special[HEIGHT] * self._scale
        self.is_walkable = is_walkable


    def __repr__(self):
        """Simple representation.
        """
        return 'Cell #%d, free: %s' % (self.tile_number, str(self.is_walkable))
