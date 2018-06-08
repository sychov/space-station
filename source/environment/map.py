# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     19-12-2017
 Description: Game map classes
----------------------------------------------------------"""

import json

import pygame
from pygame import Rect, Surface

from objects_manager import ObjectsManager
from map_cells import LayerCell, ObjectCell, FloorCell
from misc._enums import *


# ============================ MAP CLASS ================================= #


class Map(object):
    """ Main game map class.
    """
    # Order numbers of layers in map.json
    FLOOR_LAYER_NUM = 0
    DECOR_LAYER_NUM = 1
    OBJECTS_LAYER_NUM = 2
    TOP_LAYER_NUM = 3
    OBJ_MARKS_LAYER_NUM = 4

    # tiles indexies:
    STOPPABLES_FLOOR = (3, 2)
    WALKABLE_OBJ = 0

    # special object indexes offset (additional tileset starting index - 1)
    OBJECT_INDEXIES_OFFSET = 1280


    def __init__(self, map_path, tileset_path, display_size_tuple, scale=1):
        """ Init.

            map_path:               path to map (JSON) file
            tileset_path:           path to tileset (image) file
            display_size_tuple:     (<screen width>, <screen height>)
            scale:                  1 or 2 (for 1x or 2x)
        """
        # 1. Initialize basic attributes

        self.display_width, self.display_height = display_size_tuple
        self.scale = scale
        self.bottom_buffer = {
            CAMERA_COORDS: (0, 0),
            SURFACE: Surface((self.display_width * 3, self.display_height * 3))
        }

        self.objects_manager = ObjectsManager()

        # 2. Load map

        with open(map_path) as f:
            map_file_data = json.load(f)
        layers = map_file_data['layers']
        tile_size_origin = map_file_data['tileheight']

        self.tile_size = tile_size_origin * scale
        used_tiles = self._get_tiles_set_from_layers(layers)
        LayerCell.initialize(tileset_path, tile_size_origin, scale, used_tiles)

        self._objects_dict = self._get_objects_indexes_from_layer(
                                              layers[self.OBJ_MARKS_LAYER_NUM])

        self.layer_floor = self._get_map_from_layer(
                            layers[self.FLOOR_LAYER_NUM], LAYER_FLOOR)
        self.layer_floor_decor = self._get_map_from_layer(
                            layers[self.DECOR_LAYER_NUM], LAYER_FLOOR_DECOR)
        self.layer_objects = self._get_map_from_layer(
                            layers[self.OBJECTS_LAYER_NUM], LAYER_OBJECTS)
        self.layer_objects_top = self._get_map_from_layer(
                            layers[self.TOP_LAYER_NUM], LAYER_TOP)

        self.map_height_in_tiles = len(self.layer_floor)
        self.map_width_in_tiles = len(self.layer_floor[0])

        # 3. Form whole map rectangle borders (1 cell is border)

        min_x = min_y = self.tile_size
        width = self.tile_size * (self.map_width_in_tiles - 2)
        height = self.tile_size * (self.map_height_in_tiles - 2)
        self.rect = Rect(self.tile_size, self.tile_size, width, height)


    def make_bottom_buffer(self, camera_coords, direction=None, shift=0):
        """ For perfomance improvment, we are using special buffer for:
                - floor layer
                - floor decorations layer
                - bottom objects layer
        that is huge 3x3 screen size sprite of 9 display screens and used
        as a cache of bottom rendered map.

        Such buffer is partially redrawn (up to 3 screens) when user go out
        of it's borders.

        Current method makes whole buffer or it's part.

            camera_coords:   (<camera_x>, <camera_y>) for this moment

            direction:       None, if we have to redraw all, or
                             UP, DOWN, LEFT, RIGHT, if we have to redraw
                             some part of buffer (player crossed up, left,
                             etc. border of the buffer)

            shift:           If player overlapped the border, this is length
                             of such crossing in pixels (to correct redrawal)
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
            buffer_surface.scroll(dx=-self.display_width - shift, dy=0)
        else:
            left_cell = (left_x - self.display_width) / size
            start_cell_x = 0

        # LEFT scroll features
        if direction == LEFT:
            right_cell = left_x / size
            buffer_surface.scroll(dx=self.display_width - shift, dy=0)
        else:
            right_cell = (left_x + 2 * self.display_width) / size

        # DOWN scroll features
        if direction == DOWN:
            top_cell = (top_y + self.display_height) / size
            start_cell_y = self.display_height * 2 / size
            buffer_surface.scroll(dx=0, dy=-self.display_height - shift)
        else:
            top_cell = (top_y - self.display_height) / size
            start_cell_y = 0

        # UP scroll features
        if direction == UP:
            bottom_cell = top_y / size
            buffer_surface.scroll(dx=0, dy=self.display_height - shift)
        else:
            bottom_cell = (top_y + 2 * self.display_height) / size

        # draw background
        buffer_cell_y = start_cell_y
        for y_map in xrange(top_cell, bottom_cell + 1):
            buffer_cell_x = start_cell_x
            for x_map in xrange(left_cell, right_cell + 1):
                coords = (buffer_cell_x * size - dx,
                          buffer_cell_y * size - dy)

                floor_tile = self.layer_floor[y_map][x_map]
                buffer_surface.blit(floor_tile.image, coords)

                obj_tile = self.layer_objects[y_map][x_map]
                if obj_tile.tile_number:
                    buffer_surface.blit(obj_tile.image, coords)

                decor_tile = self.layer_floor_decor[y_map][x_map]
                if decor_tile.tile_number:
                    buffer_surface.blit(decor_tile.image, coords)
                buffer_cell_x += 1
            buffer_cell_y += 1

        self.bottom_buffer[CAMERA_COORDS] = camera_x, camera_y


    def draw_bottom_layers(self, screen, camera_coords):
        """ Draw screen part of buffered layers:
                - floor layer
                - floor decorations layer
                - bottom objects layer

            screen:             screen's Surface
            camera_coords:      current camera coords
        """
        camera_x, camera_y = camera_coords
        old_camera_x, old_camera_y = self.bottom_buffer[CAMERA_COORDS]

        # get difference between current camera position
        # and camera position on the moment when buffer created
        shift_x = camera_x - old_camera_x
        shift_y = camera_y - old_camera_y

        # if crossed RIGHT border of the buffer...
        if shift_x > self.display_width:
            outline = shift_x - self.display_width
            self.make_bottom_buffer(camera_coords, RIGHT, outline)
            return self.draw_bottom_layers(screen, camera_coords)
        # ...or crossed LEFT border of the buffer...
        elif shift_x < -self.display_width:
            outline = shift_x + self.display_width
            self.make_bottom_buffer(camera_coords, LEFT, outline)
            return self.draw_bottom_layers(screen, camera_coords)
        # ...or crossed BOTTOM border of the buffer...
        elif shift_y > self.display_height:
            outline = shift_y - self.display_height
            self.make_bottom_buffer(camera_coords, DOWN, outline)
            return self.draw_bottom_layers(screen, camera_coords)
        # ...or crossed TOP border of the buffer...
        elif shift_y < -self.display_height:
            outline = shift_y + self.display_height
            self.make_bottom_buffer(camera_coords, UP, outline)
            return self.draw_bottom_layers(screen, camera_coords)

        surface = self.bottom_buffer[SURFACE]
        rect = Rect(self.display_width + shift_x,
                    self.display_height + shift_y,
                    self.display_width,
                    self.display_height)
        screen.blit(surface.subsurface(rect), (0, 0))


    def draw_top_layer(self, screen, camera_coords):
        """ Draw top decorative layer on screen.
        Note, that this layer not buffered and redraw by tiles
        every frame.
        So, it is a good practice when number of such tiles is minimal.

            screen:             screen's Surface
            camera_coords:      current camera coords
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
                if self.layer_objects_top[y][x].tile_number:
                    tile = self.layer_objects_top[y][x].image
                    screen.blit(tile, (x*size - shift_x, y*size - shift_y))


    def get_first_walkable_cell_coords(self):
        """Return first cell on map, where player can spawn.
        Just for development purposes, will be changed later.
        """
        BOUNDS = 5
        for y in xrange(self.map_height_in_tiles):
            for x in xrange(self.map_width_in_tiles):
                 if self.layer_floor[y][x].is_walkable and \
                                          self.layer_objects[y][x].is_walkable:
                    return x * self.tile_size + BOUNDS, \
                           y * self.tile_size + BOUNDS


    def get_cells_to_verification(self, char_rect):
        """Return tuple of four cell's pairs around current char position.
        Every pair contains floor and object layer's cells.

            char_rect:      Rect instance with char's position
        """
        top = char_rect.y / self.tile_size
        left = char_rect.x / self.tile_size

        floor = self.layer_floor
        objects = self.layer_objects

        return ((floor[top][left],          objects[top][left]),
                (floor[top + 1][left],      objects[top + 1][left]),
                (floor[top][left + 1],      objects[top][left + 1]),
                (floor[top + 1][left + 1],  objects[top + 1][left + 1]))


    def _get_map_from_layer(self, layer, layer_type):
        """Scan layer for tiles numbers.

            layer:        dictionary of Tiled JSON map format with layer data
            layer_type:   enum of layer's type

        Return layer map in format:
            [
                [LayerCell, LayerCell, ....],
                [LayerCell, LayerCell, ....],
                ...
            ]
        """
        objects = self._objects_dict.keys()
        layer_map, row, x, y = [], [], 0, 0
        for tile_num in layer['data']:
            if layer_type == LAYER_FLOOR:
                is_walkable = tile_num not in self.STOPPABLES_FLOOR
                cell = FloorCell(x, y, tile_num, is_walkable)
            elif layer_type == LAYER_OBJECTS:
                is_walkable = tile_num == self.WALKABLE_OBJ
                is_usable = (x, y) in objects
                cell = ObjectCell(x, y, tile_num, is_walkable, is_usable)
            else:
                is_walkable = True
                cell = LayerCell(x, y, tile_num)
            row.append(cell)

            x += 1
            if x == layer['width']:
                layer_map.append(row)
                row, x = [], 0
                y += 1
        return layer_map


    def _get_tiles_set_from_layers(self, layers_list):
        """Scan layers for tiles numbers. Return set of this numbers.
        Used to identify actually used tiles and prevent to load
        useless ones.

            layers_list:     list of dictionaries in Tiled JSON map
                             format with layers data.
        """
        tiles = set()
        for layer in layers_list:
            tiles.update(set(layer['data']))
        return tiles


    def _get_objects_indexes_from_layer(self, layer):
        """Scan layer for tiles numbers.
        Those tile numbers actually are indexies to mark special objects.

            layer:        dictionary of Tiled JSON map format with layer data

        Return dictionary, where key is tuple of coords (X, Y), and
        value is index of the tile.
        """
        width = layer['width']
        objects = {}
        for q, tile_num in enumerate(layer['data']):
            if tile_num:
                y, x = divmod(q, width)
                objects[(x, y)] = tile_num - self.OBJECT_INDEXIES_OFFSET
        return objects

