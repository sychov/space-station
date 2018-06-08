# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""


import json

from misc._game_map_objects_types import map_obj_classes
from misc._pathes import MAP_OBJECTS_CONFIG


class MapObjectsManager(object):
    """
    """
    def __init__(self):
        """
        """
        self._objects = []


    def create_object(self, object_index):
        """
        """
        pass


    def _get_configuration(self):
        """
        """
        self._configuration = json.loads()