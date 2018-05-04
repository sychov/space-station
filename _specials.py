# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     30-04-2018
 Description:
----------------------------------------------------------"""



SPECIAL_COLLISIONS = {
    241: {'dx': 25, 'dy': 20, 'd_width': 50, 'd_height': 40},  # short chair

    261: {'dx': 25, 'dy': 0, 'd_width': 0, 'd_height': 0},     # table 1 left
    263: {'dx': 0, 'dy': 0, 'd_width': 25, 'd_height': 0},     # table 1 right
    262: {'dx': 25, 'dy': 0, 'd_width': 0, 'd_height': 0},     # table 2 left
    264: {'dx': 0, 'dy': 0, 'd_width': 25, 'd_height': 0},     # table 2 right

    224: {'dx': 17, 'dy': 0, 'd_width': 0, 'd_height': 0},     # shoverC left
    225: {'dx': 0, 'dy': 0, 'd_width': 17, 'd_height': 0},     # shoverC right

    222: {'dx': 0, 'dy': 0, 'd_width': 0, 'd_height': 12},     # high locker
    223: {'dx': 0, 'dy': 0, 'd_width': 0, 'd_height': 12},     # low locker
    183: {'dx': 18, 'dy': 5, 'd_width': 35, 'd_height': 15},   # flower 1
    184: {'dx': 18, 'dy': 5, 'd_width': 35, 'd_height': 15},   # flower 2
    181: {'dx': 9, 'dy': 0, 'd_width': 18, 'd_height': 12},    # cooler
}

# doors (all bounds are equal)
for q in (421, 422, 423, 424, 401, 402, 403, 404):
    SPECIAL_COLLISIONS[q] = {'dx': 0, 'dy': 15, 'd_width': 0, 'd_height': 30}

# colored round puffics (all bounds are equal)
for q in (242, 243, 244, 245):
    SPECIAL_COLLISIONS[q] = {'dx': 15, 'dy': 10, 'd_width': 30, 'd_height': 20}

# computer (all bounds are equal)
for q in (381, 382, 383):
    SPECIAL_COLLISIONS[q] = {'dx': 3, 'dy': 0, 'd_width': 6, 'd_height': 10}

# checmical tubes (all bounds are equal)
for q in (341, 342, 343, 344):
    SPECIAL_COLLISIONS[q] = {'dx': 5, 'dy': 0, 'd_width': 10, 'd_height': 12}

# mini-tubes (all bounds are equal)
for q in (273, 274, 275, 276, 277, 293, 294, 295, 296, 297, 313, 314, 315):
    SPECIAL_COLLISIONS[q] = {'dx': 20, 'dy': 10, 'd_width': 40, 'd_height': 15}


