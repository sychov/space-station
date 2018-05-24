# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     19-12-2017
 Description: Characters classes
----------------------------------------------------------"""

import pyganim
import pygame
from pygame import Surface, Rect, Color

from references._enums import *

# ================================= CONST =================================== #


CHAR_SIZE = 42
DELAY = 100
CHAR_INNER_COLLISION = {
    X: 10,
    Y: 30,
    WIDTH: 22,
    HEIGHT: 10
}
BG_COLOR = Color("#888822")


# ============================== CHAR CLASS ================================ #


class Char(pygame.sprite.Sprite):
    """ Char main class.
    Used for a player and for others "humanoids" in game.
    """
    DIRECTIONS = (UP, RIGHT, DOWN, LEFT)

    def __init__(self, start_x, start_y, tileset_path, scale, id_):
        """ Init.

            start_x, start_y:       starting char's coords
            tileset_path:           chars tileset file path
            scale:                  game tile's scale param (1 or 2)
            id_:                    string identificator.

        """
        pygame.sprite.Sprite.__init__(self)

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


    def update(self, direction, game_map):
        """Update character state. Abstract :)
        I know about `abc` lib, but it is too complex for this case.
        Ok... Be honest - it is too complex for most of cases! :)
        """
        raise RuntimeError('Need to define update nethod!')


    def draw(self, screen):
        """Draw current player animation phase on screen.

            screen:     screen Surface
        """
        screen.blit(self.image, self.screen_coords)


    def _get_animation_set(self, tileset_path, delay, scale):
        """ Form and return standard animation set with chosen delay.

            tileset_path:           chars tileset file path
            scale:                  game tile's scale param (1 or 2)
            delay:                  animation delay (in milliseconds).

        """
        image = pygame.image.load(tileset_path).convert_alpha()
        if image.get_size() != (CHAR_SIZE * 4, CHAR_SIZE * 4):
            raise RuntimeError('Sorry! only scale 4x4 tilesets with size '
                                            'of %d supported now!' % CHAR_SIZE)
        animations = {}
        for tile_y, phase_name in zip(xrange(4), self.DIRECTIONS):
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

                # First frames of every direction used for IDLE directions.
                # This directions has no animation and have index:
                #       IDLE + <direction const>
                # in animations list.
                if tile_x == 0:
                    animations[IDLE + phase_name] = pyganim.PygAnimation(
                                                               [(tile, DELAY)])
            animations[phase_name] = pyganim.PygAnimation(tiles)
        return animations


    def _redraw(self):
        """ Update character sprite according to current animation phase
        and direction.
        """
        if self.direction in self.animations:
            self.image.fill(BG_COLOR)
            self.animations[self.direction].blit(self.image, (0, 0))
        else:
            raise RuntimeError('ERROR: incorrect animation state!')


    def __repr__(self):
        """Simple representation.
        """
        return 'Char sprite set: %s' % self.id_


