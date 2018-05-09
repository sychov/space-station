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
    224: {X: 17, Y: 0,  WIDTH: 0,  HEIGHT: 10},    # shoverC left
    225: {X: 0,  Y: 0,  WIDTH: 17, HEIGHT: 10},    # shoverC right
    307: {X: 13, Y: 5,  WIDTH: 0,  HEIGHT: 15},    # red bar left
    308: {X: 0,  Y: 5,  WIDTH: 13, HEIGHT: 15},    # red bar right
    222: {X: 0,  Y: 0,  WIDTH: 0,  HEIGHT: 12},    # high locker
    223: {X: 0,  Y: 0,  WIDTH: 0,  HEIGHT: 12},    # low locker
    301: {X: 0,  Y: 0,  WIDTH: 0,  HEIGHT: 10},    # metal locker
    183: {X: 18, Y: 5,  WIDTH: 35, HEIGHT: 15},    # flower 1
    184: {X: 18, Y: 5,  WIDTH: 35, HEIGHT: 15},    # flower 2
    181: {X: 9,  Y: 0,  WIDTH: 18, HEIGHT: 12},    # cooler
    367: {X: 4,  Y: 5,  WIDTH: 8, HEIGHT: 15},     # yellow chair

    348: {X: 15,  Y: 5,  WIDTH: 15, HEIGHT: 10},   # right sofa top
    368: {X: 15,  Y: 5,  WIDTH: 15, HEIGHT: 10},   # right sofa bottom
    349: {X: 0,  Y: 5,  WIDTH: 15, HEIGHT: 10},    # left sofa top
    369: {X: 0,  Y: 5,  WIDTH: 15, HEIGHT: 10},    # left sofa bottom
}

# beds (all bounds are equal)
for q in (351, 352, 371, 372):
    SPECIAL_COLLISIONS[q] = {X: 10, Y: 5,  WIDTH: 20, HEIGHT: 10}

# doors (all bounds are equal)
for q in (421, 422, 423, 424, 401, 402, 403, 404):
    SPECIAL_COLLISIONS[q] = {X: 0, Y: 15, WIDTH: 0, HEIGHT: 30}

# colored round puffics (all bounds are equal)
for q in (242, 243, 244, 245):
    SPECIAL_COLLISIONS[q] = {X: 15, Y: 10, WIDTH: 30, HEIGHT: 20}

# colored small tables (all bounds are equal)
for q in (283, 284, 285, 303, 304, 305):
    SPECIAL_COLLISIONS[q] = {X: 0, Y: 0, WIDTH: 0, HEIGHT: 12}

# computer (all bounds are equal)
for q in (381, 382, 383):
    SPECIAL_COLLISIONS[q] = {X: 3, Y: 0, WIDTH: 6, HEIGHT: 10}

# checmical tubes (all bounds are equal)
for q in (341, 342, 343, 344):
    SPECIAL_COLLISIONS[q] = {X: 5, Y: 0, WIDTH: 10, HEIGHT: 12}

# mini-tubes (all bounds are equal)
for q in (273, 274, 275, 276, 277, 293, 294, 295, 296, 297, 313, 314, 315):
    SPECIAL_COLLISIONS[q] = {X: 20, Y: 10, WIDTH: 40, HEIGHT: 15}


