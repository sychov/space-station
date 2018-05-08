# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     30-04-2018
 Description:
----------------------------------------------------------"""


from _enums import *


SPECIAL_COLLISIONS = {
    241: {X: 25, Y: 20, WIDTH: 50, HEIGHT: 40},    # short chair
    261: {X: 25, Y: 0,  WIDTH: 0,  HEIGHT: 0},     # table 1 left
    263: {X: 0,  Y: 0,  WIDTH: 25, HEIGHT: 0},     # table 1 right
    262: {X: 25, Y: 0,  WIDTH: 0,  HEIGHT: 0},     # table 2 left
    264: {X: 0,  Y: 0,  WIDTH: 25, HEIGHT: 0},     # table 2 right
    224: {X: 17, Y: 0,  WIDTH: 0,  HEIGHT: 0},     # shoverC left
    225: {X: 0,  Y: 0,  WIDTH: 17, HEIGHT: 0},     # shoverC right
    222: {X: 0,  Y: 0,  WIDTH: 0,  HEIGHT: 12},    # high locker
    223: {X: 0,  Y: 0,  WIDTH: 0,  HEIGHT: 12},    # low locker
    183: {X: 18, Y: 5,  WIDTH: 35, HEIGHT: 15},    # flower 1
    184: {X: 18, Y: 5,  WIDTH: 35, HEIGHT: 15},    # flower 2
    181: {X: 9,  Y: 0,  WIDTH: 18, HEIGHT: 12},    # cooler
}

# doors (all bounds are equal)
for q in (421, 422, 423, 424, 401, 402, 403, 404):
    SPECIAL_COLLISIONS[q] = {X: 0, Y: 15, WIDTH: 0, HEIGHT: 30}

# colored round puffics (all bounds are equal)
for q in (242, 243, 244, 245):
    SPECIAL_COLLISIONS[q] = {X: 15, Y: 10, WIDTH: 30, HEIGHT: 20}

# computer (all bounds are equal)
for q in (381, 382, 383):
    SPECIAL_COLLISIONS[q] = {X: 3, Y: 0, WIDTH: 6, HEIGHT: 10}

# checmical tubes (all bounds are equal)
for q in (341, 342, 343, 344):
    SPECIAL_COLLISIONS[q] = {X: 5, Y: 0, WIDTH: 10, HEIGHT: 12}

# mini-tubes (all bounds are equal)
for q in (273, 274, 275, 276, 277, 293, 294, 295, 296, 297, 313, 314, 315):
    SPECIAL_COLLISIONS[q] = {X: 20, Y: 10, WIDTH: 40, HEIGHT: 15}


