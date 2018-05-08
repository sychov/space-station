# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     19-12-2017
 Description: Game map classes
----------------------------------------------------------"""

import json

import pygame
from pygame import sprite, Rect, Surface

from _specials import SPECIAL_COLLISIONS
from objects_classes import Door
from _enums import *


# ========================== MAP CELL CLASS =============================== #

class Map_Cell(sprite.Sprite):
    """One cell of the map.
    Class must be initialized before using by initialize() method.
    This is because we will read tileset only once per class,
    but we dont want to hardcode its name.
    """
    # --------------------- ATTRS ------------------------ #

    _is_class_initialized = False
    SIZE = None
    tiles = []

    @classmethod
    def initialize(cls, filename, size, scale=1):
        """Load tileset for a map.
        Tileset must be single image. Tiles are read to be supported
        by Tiled editor, from left to right, and from up to down.
        """
        image = pygame.image.load(filename).convert_alpha()
        image_width, image_height = image.get_size()
        tiles = []
        for tile_y in range(0, image_height / size):
            for tile_x in range(0, image_width / size):
                rect = (tile_x * size, tile_y * size, size, size)
                tile = image.subsurface(rect).convert_alpha()
                if scale == 2:
                    tiles.append(pygame.transform.scale2x(tile))
                elif scale == 1:
                    tiles.append(tile)
                else:
                    raise RuntimeError('Sorry! only scale 1x and 2x is '
                                                              'supported now!')
        cls.tiles = tiles
        cls.SIZE = size * scale
        cls._is_class_initialized = True


    def __init__(self, x, y, tile_number):
        """
        """
        if not self._is_class_initialized:
            raise RuntimeError('Impossible to use insances before class '
                            'initializing! Use <class>.initialize(...) first!')
        self.rect = Rect(x * self.SIZE , y * self.SIZE, self.SIZE, self.SIZE)
        self.change_tile(tile_number)


    def set_walkable(self, flag):
        """ Set walkable flag of the secc.
        """
        self.is_walkable = flag


    def change_tile(self, tile_number, is_walkable=False):
        """ Set tile for this cell.
        """
        self.image = self.tiles[tile_number - 1]
        self.tile_number = tile_number
        self.is_walkable = is_walkable

        # correct collisions map for some sprites
        if tile_number in SPECIAL_COLLISIONS:
            special = SPECIAL_COLLISIONS[tile_number]
            self.rect.x += special[X]
            self.rect.y += special[Y]
            self.rect.width -= special[WIDTH]
            self.rect.height -= special[HEIGHT]


    def __repr__(self):
        """Simple representation.
        """
        return 'Game tile #%d :' % self.tile_number + str(self.is_walkable)


# ========================== MAP CELL CLASS =============================== #


class Map():
    """Main map class.
    """
    LAYER_NUM = 0
    DECOR_NUM = 1
    OBJECTS_NUM = 2
    TOP_NUM = 3

    # tiles indexies:
    STOPPABLES_FLOOR = (3, 2)
    WALKABLE_OBJ = 0
    DOORS = (94, 108)

    def __init__(self, map_path, tileset_path, display_size_tuple, scale=1):
        """
        """
        # 1. Initialize basic attributes

        self.debug_message = ''
        self.display_width, self.display_height = display_size_tuple
        self.scale = scale
        self.bottom_buffer = {
            CAMERA_COORDS: (0, 0),
            SURFACE: Surface((self.display_width * 3, self.display_height * 3))
        }

        # 2. Load map

        with open(map_path) as f:
            map_json = json.load(f)

        origin_tile_size = map_json['tileheight']
        Map_Cell.initialize(tileset_path, origin_tile_size, scale)
        self.tile_size = origin_tile_size * scale

        layers = map_json['layers']
        self.map = self._get_map_from_layer(
                                layers[self.LAYER_NUM], LAYER_FLOOR)
        self.decor = self._get_map_from_layer(
                                layers[self.DECOR_NUM], LAYER_FLOOR_DECOR)
        self.objects = self._get_map_from_layer(
                                layers[self.OBJECTS_NUM], LAYER_OBJECTS)
        self.top = self._get_map_from_layer(
                                layers[self.TOP_NUM], LAYER_TOP)

        self.tiles_height = len(self.map)
        self.tiles_width = len(self.map[0])

        # 3. Form whole map rectangle borders (1 cell is border)

        min_x = min_y = self.tile_size
        width = self.tile_size * (self.tiles_width - 2)
        height = self.tile_size * (self.tiles_height - 2)
        self.rect = Rect(self.tile_size, self.tile_size, width, height)


    def make_bottom_buffer(self, camera_coords, direction=None):
        """Draw part of map, screen + buffer zone (+ 1 screen in every
        direction). Bottom layers only (floor, floor decor and bottom object).
        This buffer will be used later as a cache of rendered map.
        """
        camera_x, camera_y = camera_coords
        old_camera_x, old_camera_y = self.bottom_buffer[CAMERA_COORDS]

        # if we partially redraw buffer, we have to remain another coord
        if direction == RIGHT or direction == LEFT:
            camera_y = old_camera_y
        elif direction == UP or direction == DOWN:
            camera_x = old_camera_x

        # get left and top borders of the screen (relative to buffer)
        left_x = camera_x - self.display_width / 2
        top_y = camera_y - self.display_height / 2

        size = self.tile_size
        dx = left_x % size
        dy = top_y % size

        buffer_surface = self.bottom_buffer[SURFACE]

        # RIGHT scroll features
        if direction == RIGHT:
            left_cell = (left_x + self.display_width) / size
            start_cell_x = self.display_width * 2 / size
            buffer_surface.scroll(dx=-self.display_width, dy=0)
        else:
            left_cell = (left_x - self.display_width) / size
            start_cell_x = 0

        # LEFT scroll features
        if direction == LEFT:
            right_cell = left_x / size
            buffer_surface.scroll(dx=self.display_width, dy=0)
        else:
            right_cell = (left_x + 2 * self.display_width) / size

        # DOWN scroll features
        if direction == DOWN:
            top_cell = (top_y + self.display_height) / size
            start_cell_y = self.display_height * 2 / size
            buffer_surface.scroll(dx=0, dy=-self.display_height)
        else:
            top_cell = (top_y - self.display_height) / size
            start_cell_y = 0

        # UP scroll features
        if direction == UP:
            bottom_cell = top_y / size
            buffer_surface.scroll(dx=0, dy=self.display_height)
        else:
            bottom_cell = (top_y + 2 * self.display_height) / size

        # draw background
        buffer_cell_y = start_cell_y
        for y_map in xrange(top_cell, bottom_cell + 1):
            buffer_cell_x = start_cell_x
            for x_map in xrange(left_cell, right_cell + 1):
                coords = (buffer_cell_x * size - dx,
                          buffer_cell_y * size - dy)

                floor_tile = self.map[y_map][x_map]
                buffer_surface.blit(floor_tile.image, coords)

                obj_tile = self.objects[y_map][x_map]
                if obj_tile.tile_number:
                    buffer_surface.blit(obj_tile.image, coords)

                decor_tile = self.decor[y_map][x_map]
                if decor_tile.tile_number:
                    buffer_surface.blit(decor_tile.image, coords)
                buffer_cell_x += 1
            buffer_cell_y += 1

        self.bottom_buffer[CAMERA_COORDS] = camera_x, camera_y


    def draw_bottom(self, screen, camera_coords):
        """Draw part of map (in a frame around camera_coords).
        """
        camera_x, camera_y = camera_coords
        old_camera_x, old_camera_y = self.bottom_buffer[CAMERA_COORDS]

        # get difference between current camera position
        # and camera position on the moment when buffer created
        shift_x = camera_x - old_camera_x
        shift_y = camera_y - old_camera_y

        if shift_x > self.display_width:
            self.make_bottom_buffer(camera_coords, direction=RIGHT)
            return self.draw_bottom(screen, camera_coords)
        elif shift_x < -self.display_width:
            self.make_bottom_buffer(camera_coords, direction=LEFT)
            return self.draw_bottom(screen, camera_coords)
        elif shift_y > self.display_height:
            self.make_bottom_buffer(camera_coords, direction=DOWN)
            return self.draw_bottom(screen, camera_coords)
        elif shift_y < -self.display_height:
            self.make_bottom_buffer(camera_coords, direction=UP)
            return self.draw_bottom(screen, camera_coords)

        surface = self.bottom_buffer[SURFACE]
        rect = Rect(self.display_width + shift_x,
                    self.display_height + shift_y,
                    self.display_width,
                    self.display_height)
        screen.blit(surface.subsurface(rect), (0, 0))


    def get_first_walkable_cell_coords(self):
        """Return first cell on map, where player can spawn.
        """
        BOUNDS = 5
        for y in xrange(self.tiles_height):
            for x in xrange(self.tiles_width):
                 if self.map[y][x].is_walkable and \
                                                self.objects[y][x].is_walkable:
                    return x * self.tile_size + BOUNDS, \
                           y * self.tile_size + BOUNDS


    def draw_top(self, screen, camera_coords):
        """Draw part of map (in a frame around camera_coords).
        """
        camera_x, camera_y = camera_coords

        shift_x = camera_x - self.display_width / 2
        shift_y = camera_y - self.display_height / 2
        size = self.tile_size

        left_cell = shift_x / self.tile_size
        top_cell = shift_y / self.tile_size
        right_cell = (shift_x + self.display_width) / self.tile_size
        bottom_cell = (shift_y + self.display_height) / self.tile_size

        for y in xrange(top_cell, bottom_cell + 1):
            for x in xrange(left_cell, right_cell + 1):
                if self.top[y][x].tile_number:
                    tile = self.top[y][x].image
                    screen.blit(tile, (x*size - shift_x, y*size - shift_y))


    def get_cells_to_verification(self, rect):
        """Return tuple of four cells around current char position.
        """
        top = rect.y / self.tile_size
        left = rect.x / self.tile_size
        return ((self.map[top][left], self.objects[top][left]),
                (self.map[top + 1][left], self.objects[top + 1][left]),
                (self.map[top][left + 1], self.objects[top][left + 1]),
                (self.map[top + 1][left + 1], self.objects[top + 1][left + 1]))


    def _get_map_from_layer(self, layer, layer_type):
        """Scan layer for tiles numbers.
        Return game map in format:
            [
                [Map_Cell, Map_Cell, ....],
                [Map_Cell, Map_Cell, ....],
                ...
            ]
        """
        layer_map, row, x, y = [], [], 0, 0
        for tile_num in layer['data']:
            cell = Map_Cell(x, y, tile_num)
            if layer_type == LAYER_FLOOR:
                cell.set_walkable(tile_num not in self.STOPPABLES_FLOOR)
            elif layer_type == LAYER_OBJECTS:
                cell.set_walkable(tile_num == self.WALKABLE_OBJ)
            row.append(cell)

            x += 1
            if x == layer['width']:
                layer_map.append(row)
                row, x = [], 0
                y += 1
        return layer_map


    def get_special_objects_list(self):
        """ Scan objects layer for special objects.
        Create them and return theirs list.
        """
        objects = []
        for y in xrange(self.tiles_height):
            for x in xrange(self.tiles_width):
                cell = self.objects[y][x]
                if cell.tile_number in self.DOORS:
                    objects.append(Door(cell))
        return objects

