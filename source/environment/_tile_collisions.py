# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     30-04-2018
 Description: Collisions of some object tiles
----------------------------------------------------------"""


from misc._enums import *


# ---------------------------------------------------------------------------
#
# By default, all objects inner rectangle set according to whole tile size.
# Here we describe custom pixel indents of tile in format:
#
#      X:      <indent from the left>
#      Y:      <indent from the top>
#      WIDTH:  <object's width>
#                  (<tile width > = X + WIDTH + <indent from the right>)
#      HEIGHT:  <object's heigth>
#                  (<tile heigth > = X + HEIGTH + <indent from the bottom>)
#
# For scaled tiles this values would be auto-scaled
#
# ---------------------------------------------------------------------------

TILES_COLLISIONS = {
##    241: {X: 13, Y: 10, WIDTH: 27, HEIGHT: 21},    # short chair
    261: {X: 12, Y: 0,  WIDTH: 0,  HEIGHT: 0},     # table 1 left
    263: {X: 0,  Y: 0,  WIDTH: 12, HEIGHT: 0},     # table 1 right
    262: {X: 12, Y: 0,  WIDTH: 0,  HEIGHT: 0},     # table 2 left
    264: {X: 0,  Y: 0,  WIDTH: 12, HEIGHT: 0},     # table 2 right
    224: {X: 8,  Y: 0,  WIDTH: 0,  HEIGHT: 5},     # shoverC left
    225: {X: 0,  Y: 0,  WIDTH: 8,  HEIGHT: 5},     # shoverC right
    307: {X: 6,  Y: 2,  WIDTH: 0,  HEIGHT: 7},     # red bar left
    308: {X: 0,  Y: 2,  WIDTH: 6,  HEIGHT: 7},     # red bar right
    222: {X: 0,  Y: 0,  WIDTH: 0,  HEIGHT: 6},     # high locker
    223: {X: 0,  Y: 0,  WIDTH: 0,  HEIGHT: 6},     # low locker
##    183: {X: 9,  Y: 2,  WIDTH: 17, HEIGHT: 7},     # flower 1
##    184: {X: 9,  Y: 2,  WIDTH: 17, HEIGHT: 7},     # flower 2
    181: {X: 4,  Y: 0,  WIDTH: 9,  HEIGHT: 6},     # cooler
    367: {X: 2,  Y: 2,  WIDTH: 4,  HEIGHT: 7},     # yellow chair
    370: {X: 2,  Y: 2,  WIDTH: 4,  HEIGHT: 7},     # top sofa left
    371: {X: 2,  Y: 2,  WIDTH: 4,  HEIGHT: 7},     # top sofa right
    348: {X: 7,  Y: 2,  WIDTH: 7,  HEIGHT: 5},     # right sofa top
    368: {X: 7,  Y: 2,  WIDTH: 7,  HEIGHT: 5},     # right sofa bottom
    349: {X: 0,  Y: 2,  WIDTH: 7,  HEIGHT: 5},     # left sofa top
    369: {X: 0,  Y: 2,  WIDTH: 7,  HEIGHT: 5},     # left sofa bottom
}

# big lockers
for q in (301, 302, 461, 462, 463, 464, 465, 466,
                                                634, 635, 636, 637, 638, 639):
    TILES_COLLISIONS[q] = {X: 0,  Y: 0,  WIDTH: 0,  HEIGHT: 5}

# pult-left
for q in (481, 501):
    TILES_COLLISIONS[q] = {X: 0,  Y: 0,  WIDTH: 10,  HEIGHT: 0}

# pult-right
for q in (482, 502):
    TILES_COLLISIONS[q] = {X: 10,  Y: 0,  WIDTH: 10,  HEIGHT: 0}

# beds (all bounds are equal)
for q in (353, 354, 355, 356, 357, 358, 359, 360,
                                     373, 374, 375, 376, 377, 378, 379, 380):
    TILES_COLLISIONS[q] = {X: 5, Y: 2,  WIDTH: 10, HEIGHT: 5}

# doors (all bounds are equal)
for q in (421, 422, 423, 424, 401, 402, 403, 404):
    TILES_COLLISIONS[q] = {X: 0, Y: 7, WIDTH: 0, HEIGHT: 15}

# colored round puffics (all bounds are equal)
for q in (242, 243, 244, 245):
    TILES_COLLISIONS[q] = {X: 7, Y: 5, WIDTH: 15, HEIGHT: 10}

# colored small tables (all bounds are equal)
for q in (283, 284, 285, 303, 304, 305):
    TILES_COLLISIONS[q] = {X: 0, Y: 0, WIDTH: 0, HEIGHT: 6}

# computer (all bounds are equal)
for q in (381, 382, 383):
    TILES_COLLISIONS[q] = {X: 2, Y: 0, WIDTH: 4, HEIGHT: 5}

# checmical tubes (all bounds are equal)
for q in (341, 342, 343, 344):
    TILES_COLLISIONS[q] = {X: 2, Y: 0, WIDTH: 4, HEIGHT: 6}

# mini-tubes (all bounds are equal)
for q in (273, 274, 275, 276, 277, 293, 294, 295, 296, 297, 313, 314, 315,
          536, 537, 538, 539, 540, 576, 577, 578, 556, 557, 558, 559, 560):
    TILES_COLLISIONS[q] = {X: 10, Y: 5, WIDTH: 20, HEIGHT: 7}


