# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""


import json

from objects._types_table import OBJECTS_CLASSES
from objects.base import BaseObject
from misc._pathes import MAP_OBJECTS_CONFIG


# ---------------------------------- Const ----------------------------- #

LOCALE = 'rus'

# ----------------------------- ObjectsManager ------------------------- #


class ObjectsManager(object):
    """Agregation class for game map objects.
    Forms objects list using game map data and configuration files.
    """
    def __init__(self):
        """Init. Please, use only one instance of this class.
        """
        self._objects = {}
        BaseObject.set_locale(LOCALE)

        try:
            with open(MAP_OBJECTS_CONFIG, 'r') as f:
                configuration = json.load(f)
        except:
            raise RuntimeError('Error reading JSON objects configuration (%s)!'
                                                          % MAP_OBJECTS_CONFIG)

        for key, value in configuration.items():
            index = int(key)
            id_ = value['class']
            class_ = OBJECTS_CLASSES[id_]
            kwargs = value['args']
            try:
                self._objects[index] = class_(id_=id_, **kwargs)
            except:
                raise RuntimeError('Error creating object '
                                         '#%d (%s)!' % (index, value['class']))


    def get_object_by_index(self, index):
        """Return BaseObject instance of selected index.

            index:      game map "OBJ_MARKS_LAYER_NUM" index value.
        """
        if index in self._objects:
            return self._objects[index]
        else:
            return None


    def __repr__(self):
        """Simple representation.
        """
        return 'Game map objects manager'
