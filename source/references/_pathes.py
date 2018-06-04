# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     04-06-2018
 Description: Global constants
----------------------------------------------------------"""



import os
import sys

if sys.argv[0].rsplit('.', 1)[1] == 'exe':
    MAIN_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
else:
    MAIN_DIR = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))

SOUNDS_DIR = os.path.join(MAIN_DIR, 'sounds')
INTERFACE_DIR = os.path.join(MAIN_DIR, 'graphics', 'interface')

MAP_PATH = os.path.join(MAIN_DIR, 'gamedata', 'map', 'map.json')
MAP_TILES_PATH = os.path.join(MAIN_DIR, 'graphics', 'tilesets', 'TILES.png')
PLAYER_TILES_PATH = os.path.join(MAIN_DIR, 'graphics', 'chars', 'captain.png')