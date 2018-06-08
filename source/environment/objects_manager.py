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
    """
    """
    def __init__(self):
        """
        """
        self._objects = {}
        BaseObject.set_locale(LOCALE)

        try:
            configuration = self._get_configuration()
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


    def _get_configuration(self):
        """
        """
        with open(MAP_OBJECTS_CONFIG, 'r') as f:
            configuration = json.load(f)
        return configuration

