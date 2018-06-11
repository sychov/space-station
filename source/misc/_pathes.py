# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     04-06-2018
 Description: File pathes (global constants)
----------------------------------------------------------"""

import os
import sys


# ----------------------- get main directory path -------------------------- #

if sys.argv[0].rsplit('.', 1)[1] == 'exe':
    MAIN_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
else:
    MAIN_DIR = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))

# ------------------------------- PATH'es ---------------------------------- #


# ------ dirs ------- #

SOUNDS_DIR = os.path.join(MAIN_DIR, 'sounds')
INTERFACE_DIR = os.path.join(MAIN_DIR, 'graphics', 'interface')

# ------ variation patterns ------- #

OBJECT_TEXT_PATH_PATTERN = os.path.join(MAIN_DIR, 'gamedata', 'text',
                                                          'objects', '%s.json')

# ------ files ------- #

MAP_PATH = os.path.join(MAIN_DIR, 'gamedata', 'map', 'map.json')
MAP_TILES_PATH = os.path.join(MAIN_DIR, 'graphics', 'tilesets', 'TILES.png')
PLAYER_TILES_PATH = os.path.join(MAIN_DIR, 'graphics', 'chars', 'captain.png')
ACTIONS_TILES_PATH = os.path.join(MAIN_DIR, 'graphics', 'tilesets',
                                                            'action_icons.png')

MAP_OBJECTS_CONFIG = os.path.join(MAIN_DIR, 'gamedata', 'map_objects.json')


