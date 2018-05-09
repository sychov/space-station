# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     19-12-2017
 Description: Characters classes
----------------------------------------------------------"""

import pyganim
import pygame
from pygame import sprite, draw
from pygame import Surface, Rect, Color

from _enums import *

# ================================= CONST =================================== #

# ------------------------ TILESET ------------------------ #

CHAR_SIZE = 42
DELAY = 100
CHAR_INNER_COLLISION = {
    X: 10,
    Y: 30,
    WIDTH: 22,
    HEIGHT: 10
}
BG_COLOR = Color("#888822")

# ------------------------ OTHER -------------------------- #

MOVE_SPEED = 2
DIRECTIONS = (UP, RIGHT, DOWN, LEFT)

# ============================== CHAR CLASS ================================ #


class Char(sprite.Sprite):
    """Char abstract class.
    Used for a player and for others humanoids in game.
    """
    def __init__(self, start_x, start_y, tileset_path, scale, id_):
        """
        """
        sprite.Sprite.__init__(self)

        self.startX = start_x
        self.startY = start_y
        self.size = CHAR_SIZE * scale
        self.direction = DOWN
        self.id_ = id_

        # rect of character inside sprite. Is left for debug purposes.
        self._inner_rect = Rect(
            CHAR_INNER_COLLISION[X] * scale,
            CHAR_INNER_COLLISION[Y] * scale,
            CHAR_INNER_COLLISION[WIDTH] * scale,
            CHAR_INNER_COLLISION[HEIGHT] * scale)

        # real rect of character
        self.rect = Rect(self.startX,
                         self.startY,
                         self._inner_rect.width,
                         self._inner_rect.height)

        # ~ image & animation ~

        self.image = Surface((self.size, self.size))
        self.image.fill(BG_COLOR)
        self.image.set_colorkey(BG_COLOR)

        self.animations = self._get_animation_set(tileset_path, DELAY, scale)
        for q in self.animations:
            self.animations[q].play()
        self._redraw()


    def _get_animation_set(self, tileset_path, delay, scale):
        """Form standard animation set with chosen delay (in milliseconds).
        """
        image = pygame.image.load(tileset_path).convert_alpha()
        if image.get_size() != (CHAR_SIZE * 4,CHAR_SIZE * 4):
            raise RuntimeError('Sorry! only scale 4x4 tilesets with size '
                                            'of %d supported now!' % CHAR_SIZE)
        animations = {}
        for tile_y, phase_name in zip(xrange(4), DIRECTIONS):
            tiles = []
            for tile_x in xrange(4):
                rect = (tile_x * CHAR_SIZE,
                        tile_y * CHAR_SIZE,
                        CHAR_SIZE,
                        CHAR_SIZE)
                tile = image.subsurface(rect).convert_alpha()
                if scale == 2:
                    tile = pygame.transform.scale2x(tile)
                tiles.append((tile, DELAY))

                if tile_x == 0:
                    animations[IDLE + phase_name] = pyganim.PygAnimation(
                                                               [(tile, DELAY)])
            animations[phase_name] = pyganim.PygAnimation(tiles)
        return animations


    def _redraw(self):
        """Draw character sprite according to animation phase and direction.
        """
        if self.direction in self.animations:
            self.image.fill(BG_COLOR)
            self.animations[self.direction].blit(self.image, (0, 0))

##            # FOR DEBUG
##            draw.rect(self.image, (0, 250, 0), self._inner_rect, 1)
##            draw.rect(self.image, (250, 250, 0), (0, 0, self.size, self.size), 1)
        else:
            raise RuntimeError('ERROR: incorrect animation state!')


    def update(self, direction, game_map):
        """Update character state. Abstract :)
        I know about `abc` lib, but it is too complex for this case.
        """
        raise RuntimeError('Need to define update nethod!')


    def _stop_moving(self):
        """Change moving animation to idle in the same direction.
        """
        self.direction = IDLE + self.direction


    def _collide_map(self, game_map):
        """Check collision with other objects (game map, borders of it etc).
        Return True if collide, else False.
        Authomatically stop moving if collide.
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
            self._stop_moving()
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
                self._stop_moving()
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
                self._stop_moving()
                return True

        return False


    def __repr__(self):
        """Simple representation.
        """
        return 'Char sprite set: %s' % self.id_


# ============================ PLAYER CLASS ================================= #


class Player(Char):
    """Player character.
    """
    def __init__(self, start_x, start_y, tileset_path, scale, display_size):
        """
        """
        super(Player, self).__init__(
                               start_x, start_y, tileset_path, scale, 'Player')
        self.camera_shift_x = self.rect.width / 2
        self.camera_shift_y = self.rect.height / 2
        self.debug_message = ''

        x = (display_size[0] - self._inner_rect.width) / 2 - self._inner_rect.x
        y = (display_size[1] - self._inner_rect.height)/ 2 - self._inner_rect.y
        self.screen_coords = x, y


    def get_camera_pos(self):
        """Get linked to player camera coords (center of the screen).
        """
        x = self.rect.x + self.camera_shift_x
        y = self.rect.y + self.camera_shift_y
        return x, y


    def update(self, direction, game_map):
        """Update player state.
        """
        if direction in DIRECTIONS:
            self.direction = direction
            if direction == LEFT:
                self.rect.x -= MOVE_SPEED
            elif direction == RIGHT:
                self.rect.x += MOVE_SPEED
            if direction == UP:
                self.rect.y -= MOVE_SPEED
            elif direction == DOWN:
                self.rect.y += MOVE_SPEED

        elif direction == IDLE:
            if self.direction in DIRECTIONS:
                self._stop_moving()

        self._collide_map(game_map)
        self._redraw()

    def draw(self, screen):
        """Draw current player animation phase on screen
        """
        screen.blit(self.image, self.screen_coords)


# ============================ NPC CLASS ================================= #


class NPC(Char):
    """NPC character.
    """
    def __init__(self, start_x, start_y, tileset_path, scale, npc_id):
        """
        """
        super(NPC, self).__init__(
                               start_x, start_y, tileset_path, scale, npc_id)


    def update(self, direction, game_map):
        """Update npc state.
        """
        pass


