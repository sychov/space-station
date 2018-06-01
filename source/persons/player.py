# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     19-12-2017
 Description: Characters classes
----------------------------------------------------------"""

import pygame
from pygame import Rect

from char import Char
from references._enums import *


# ================================= CONST =================================== #


MOVE_SPEED = 2


# ============================ PLAYER CLASS ================================= #


class Player(Char):
    """Player character.
    """
    def __init__(self, start_x, start_y, tileset_path, scale, display_size):
        """ Init.

            start_x, start_y:       starting char's coords on global map
            tileset_path:           chars tileset file path
            scale:                  game tile's scale param (1 or 2)
            display_size:           (<screen width>, <screen height>)

        """
        super(Player, self).__init__(start_x, start_y, tileset_path,
                                                               scale, 'Player')
        self.camera_shift_x = self.rect.width / 2
        self.camera_shift_y = self.rect.height / 2

        x = (display_size[0] - self._inner_rect.width) / 2 - self._inner_rect.x
        y = (display_size[1] - self._inner_rect.height)/ 2 - self._inner_rect.y
        self.screen_coords = x, y

        self.key_left = self.key_right = self.key_top = self.key_bottom = False


    def get_camera_pos(self):
        """Get linked to our player camera coords (center of the screen).
        """
        x = self.rect.x + self.camera_shift_x
        y = self.rect.y + self.camera_shift_y
        return x, y


    def update(self, game_map):
        """Update player state.

            game_map:       Map class instance.
        """
        is_idle_state = False

        if self.key_bottom:
            self.rect.y += MOVE_SPEED
            self.direction = DOWN

        elif self.key_top:
            self.rect.y -= MOVE_SPEED
            self.direction = UP

        elif self.key_left:
            self.rect.x -= MOVE_SPEED
            self.direction = LEFT

        elif self.key_right:
            self.rect.x += MOVE_SPEED
            self.direction = RIGHT

        else:
            is_idle_state = True

        if is_idle_state or self._collide_map(game_map):
            if self.direction not in (IDLE, IDLE_UP, IDLE_DOWN, IDLE_LEFT,
                                                                   IDLE_RIGHT):
                self.direction = IDLE + self.direction

        self._redraw()


    def handle_event(self, event):
        """
        """
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                self.key_left = True
                return True

            elif event.key == pygame.K_RIGHT:
                self.key_right = True
                return True

            elif event.key == pygame.K_UP:
                self.key_top = True
                return True

            elif event.key == pygame.K_DOWN:
                self.key_bottom = True
                return True

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_RIGHT:
                self.key_right = False
                return True

            elif event.key == pygame.K_LEFT:
                self.key_left = False
                return True

            elif event.key == pygame.K_UP:
                self.key_top = False
                return True

            elif event.key == pygame.K_DOWN:
                self.key_bottom = False
                return True

        return False


    def _collide_map(self, game_map):
        """Check collision with other objects (game map, borders of it etc).
        Return True if collide, else False.

            game_map:       Map class instance.

        """
        # check borders of the map
        if not game_map.rect.contains(self.rect):
            if self.direction == RIGHT:
                self.rect.right = game_map.rect.right
            elif self.direction == LEFT:
                self.rect.left = game_map.rect.left
            elif self.direction == UP:
                self.rect.top = game_map.rect.top
            elif self.direction == DOWN:
                self.rect.bottom = game_map.rect.bottom
            return True

        # check nearest tiles
        for floor_c, object_c in game_map.get_cells_to_verification(self.rect):
            if not floor_c.is_walkable and self.rect.colliderect(floor_c):
                if self.direction == RIGHT:
                    self.rect.right = floor_c.rect.left
                elif self.direction == LEFT:
                    self.rect.left = floor_c.rect.right
                elif self.direction == UP:
                    self.rect.top = floor_c.rect.bottom
                elif self.direction == DOWN:
                    self.rect.bottom = floor_c.rect.top
                return True

            elif not object_c.is_walkable and self.rect.colliderect(object_c):
                if self.direction == RIGHT:
                    self.rect.right = object_c.rect.left
                elif self.direction == LEFT:
                    self.rect.left = object_c.rect.right
                elif self.direction == UP:
                    self.rect.top = object_c.rect.bottom
                elif self.direction == DOWN:
                    self.rect.bottom = object_c.rect.top
                return True

        return False
