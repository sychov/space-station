# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     01-06-2018
 Description:
----------------------------------------------------------"""


from pygame import Rect, Color

from storage import Storage, StorageConfig
from frame import FrameConfig

from references._enums import *


FRAME_CONFIG = FrameConfig(
    tileset_path="../graphics/interface/brown_scifi_border.png",
    part_rects={
        TOP_LEFT:       Rect(0, 0, 60, 54),
        TOP_RIGHT:      Rect(140, 0, 85, 49),
        BOTTOM_LEFT:    Rect(0, 69, 50, 71),
        BOTTOM_RIGHT:   Rect(185, 67, 40, 73),
        UP:             Rect(62, 0, 51, 22),
        DOWN:           Rect(62, 124, 51, 16),
        LEFT:           Rect(0, 55, 19, 16),
        RIGHT:          Rect(204, 47, 21, 24),
    },
    padding=25
)

STORAGE_GONFIG = StorageConfig(
    frame_config=FRAME_CONFIG,
    grid_size=(3, 5),
    grid_top_left_corner=(24, 29),
    grid_line_color=Color(129, 132, 110),
    item_outline_color=Color(110, 110, 110),
    cell_avail_color=Color(70, 75, 62)
)


class WoodenShelfStorage(Storage):
    """Storage interface for wood locker
    """
    def __init__(self, rect):
        """Init.
        """
        super(WoodenShelfStorage, self).__init__(rect, STORAGE_GONFIG)


