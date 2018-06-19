# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-05-2018
 Description: Dumb enum constants (like C-type enums)
----------------------------------------------------------"""


# enum: directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

IDLE = 5

IDLE_UP = 6
IDLE_DOWN = 7
IDLE_LEFT = 8
IDLE_RIGHT = 9

# enum: directions advanced
TOP_LEFT = 6
TOP_RIGHT = 7
BOTTOM_LEFT = 8
BOTTOM_RIGHT = 9

# enum: Rectangle
X = 11
Y = 12
WIDTH = 13
HEIGHT = 14

# enum: layers
LAYER_FLOOR = 21
LAYER_FLOOR_DECOR = 22
LAYER_OBJECTS = 23
LAYER_TOP = 24

# enum: buffer
SURFACE = 31
CAMERA_COORDS = 32

# enum: --------------------- free

# enum: text colors

DANGER = 51
SUCCESS = 52
FAIL = 53

# enum: sprite size type

SPRITE_1x1 = 61
SPRITE_2x1 = 62
SPRITE_1x2 = 63
SPRITE_2x2 = 64

# enum: dragged item

DI_OUTLINED_IMAGE = 71
DI_ITEM = 72
DI_CELL_X = 73
DI_CELL_Y = 74
DI_HALF_IMAGE_WIDTH = 75
DI_HALF_IMAGE_HEIGHT = 76
DI_LAST_MOUSE_POS = 77
DI_TARGET_CELLS_LIST = 78
DI_TARGET_STORAGE = 79

# enum: actions

ACTION_BAD = 81
ACTION_GOOD = 82
ACTION_USE = 83

# enum: events

EVENT_FORCE_MEMORY_FREE = 85
EVENT_UPDATE_ACTION_INTERFACE = 90
EVENT_ENABLE_ACTION_INTERFACE = 91
EVENT_DISABLE_ACTION_INTERFACE = 92
EVENT_PLAYER_MESSAGE_TO_LOG = 93
EVENT_SHOW_INTERFACE_FRAME = 94
EVENT_HIDE_INTERFACE_FRAME = 95
EVENT_ACTION_INTERFACE_CLOSED = 96
EVENT_OBJECT_INTERFACE_CLOSED = 97
EVENT_NEED_PLAY_NEXT_MUSIC_TRACK = 98
EVENT_GAME_MAP_CHANGE_TILE_NUM = 99
EVENT_DETECT_CHARS_ABSENCE_ON_CELL = 100

# enum: states

NORMAL = 120
BROKEN = 121
LOCKED = 122
CLOSED = 123
OPENED = 124



