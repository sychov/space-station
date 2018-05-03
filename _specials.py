# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     30-04-2018
 Description:
----------------------------------------------------------"""



SPECIAL_COLLISIONS = {
    168: {'dx': 25, 'dy': 20, 'd_width': 50, 'd_height': 40},  # short chair

    166: {'dx': 25, 'dy': 0, 'd_width': 0, 'd_height': 0},     # table 1 left
    167: {'dx': 0, 'dy': 0, 'd_width': 25, 'd_height': 0},     # table 1 right
    152: {'dx': 25, 'dy': 0, 'd_width': 0, 'd_height': 0},     # table 2 left
    153: {'dx': 0, 'dy': 0, 'd_width': 25, 'd_height': 0},     # table 2 right

    164: {'dx': 17, 'dy': 0, 'd_width': 0, 'd_height': 0},     # shoverC left
    165: {'dx': 0, 'dy': 0, 'd_width': 17, 'd_height': 0},     # shoverC right

    163: {'dx': 0, 'dy': 0, 'd_width': 0, 'd_height': 12},     # high locker
    162: {'dx': 0, 'dy': 0, 'd_width': 0, 'd_height': 12},     # low locker
    161: {'dx': 18, 'dy': 5, 'd_width': 35, 'd_height': 15},   # flower 1
    138: {'dx': 3, 'dy': 0, 'd_width': 6, 'd_height': 10},     # computer
    137: {'dx': 18, 'dy': 5, 'd_width': 35, 'd_height': 15},   # flower 2
    136: {'dx': 9, 'dy': 0, 'd_width': 18, 'd_height': 12},    # cooler

    135: {'dx': 5, 'dy': 0, 'd_width': 10, 'd_height': 12},    # big tube 1
    134: {'dx': 5, 'dy': 0, 'd_width': 10, 'd_height': 12},    # big tube 2
    133: {'dx': 5, 'dy': 0, 'd_width': 10, 'd_height': 12},    # big tube 3

    94:  {'dx': 0, 'dy': 15, 'd_width': 0, 'd_height': 30},    # red door
    108: {'dx': 0, 'dy': 15, 'd_width': 0, 'd_height': 30},    # blue door

}

# minitubes
for q in (127, 128, 155, 144, 145, 129, 141, 142, 156, 157, 130, 143):
    SPECIAL_COLLISIONS[q] = {'dx': 20, 'dy': 10, 'd_width': 40, 'd_height': 15}

