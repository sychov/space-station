# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     19-12-2017
 Description: Characters classes
----------------------------------------------------------"""

import pygame
from pygame import Rect

from base import BaseChar
from misc._enums import *
from misc.events import events

# ================================= CONST =================================== #


MOVE_SPEED = 2


# ============================ PLAYER CLASS ================================= #


class Player(BaseChar):
    """Player character.
    """
    def __init__(self, coords, tileset_path, scale, display_size):
        """ Init.

            coords:                 starting coords (X, Y) on global map
            tileset_path:           chars tileset file path
            scale:                  game tile's scale param (1 or 2)
            display_size:           (<screen width>, <screen height>)

        """
        super(Player, self).__init__(coords, tileset_path, scale, 'Player')
        self.camera_shift_x = self.rect.width / 2
        self.camera_shift_y = self.rect.height / 2

        x = (display_size[0] - self._inner_rect.width) / 2 - self._inner_rect.x
        y = (display_size[1] - self._inner_rect.height)/ 2 - self._inner_rect.y
        self.screen_coords = x, y

        self.key_left = self.key_right = self.key_top = self.key_bottom = False

        self._current_object_selected = None
        self._is_object_action_interface_on = False


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
        """Handle event.
        If event is handled, return True, else False.
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
        """Check collision with other objects (game map borders,
        non-walkable floor cells and object cells).
        If collide with non-walkable, return to last possible position.
        If collide with usable object, show actions interface.
        Return True if collide, else False.

            game_map:       Map class instance.
        """
        # 1. Check borders of the map.

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

        # 2. Check nearest tiles

        is_usable_found = False
        is_player_stopped = False
        stop_border = None

        for floor_c, object_c in game_map.get_cells_to_verification(self.rect):

            # - check floor tiles walkability:
            if not floor_c.is_walkable and self.rect.colliderect(floor_c):
                if self.direction == RIGHT:
                    stop_border = floor_c.rect.left
                elif self.direction == LEFT:
                    stop_border = floor_c.rect.right
                elif self.direction == UP:
                    stop_border = floor_c.rect.bottom
                elif self.direction == DOWN:
                    stop_border = floor_c.rect.top
                is_player_stopped = True

            # - if ok, check object walkability:
            elif not object_c.is_walkable and self.rect.colliderect(object_c):
                if self.direction == RIGHT:
                    stop_border = object_c.rect.left
                elif self.direction == LEFT:
                    stop_border = object_c.rect.right
                elif self.direction == UP:
                    stop_border = object_c.rect.bottom
                elif self.direction == DOWN:
                    stop_border = object_c.rect.top
                is_player_stopped = True

                # - check object usability, if non-walkable:
                if object_c.is_usable and not is_usable_found:
                    point = self._get_sensitive_point(self.direction)
                    if object_c.rect.collidepoint(point):
                        if self._is_object_action_interface_on and \
                                     self._current_object_selected == object_c:
                            # don't need to re-enable action interface
                            # alredy opened for the same object
                            continue
                        else:
                            self._enable_actions_interface(object_c)
                            is_usable_found = True

        if is_player_stopped:
            # stop to border value:
            if self.direction == RIGHT:
                self.rect.right = stop_border
            elif self.direction == LEFT:
                self.rect.left = stop_border
            elif self.direction == UP:
                self.rect.top = stop_border
            elif self.direction == DOWN:
                self.rect.bottom = stop_border
            return True
        else:
            # we don't need action interface, when moving
            if self._is_object_action_interface_on:
                self._disable_actions_interface()
            return False


    def _enable_actions_interface(self, obj):
        """Enable interface of player's action buttons.
        """
        events.enable_action_interface(
            direction=self.direction,
            actions_list=[ACTION_GOOD, ACTION_BAD, ACTION_USE])

        self._is_object_action_interface_on = True
        self._current_object_selected = obj



    def _disable_actions_interface(self):
        """Disable interface of player's action buttons.
        """
        events.disable_action_interface()

        self._is_object_action_interface_on = False
        self._current_object_selected == None


    def _get_sensitive_point(self, direction):
        """Get point in the middle of collision box side, to
        check, if player could use map object.
        """
        x, y, width, height = self.rect
        half_width = width / 2
        half_height = height / 2
        if direction == LEFT:
            return (x, y + half_height)
        elif direction == RIGHT:
            return (x + width, y + half_height)
        elif direction == UP:
            return (x + half_width, y)
        elif direction == DOWN:
            return (x + half_width, y + height)


