# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""


import json
from time import time

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
    def __init__(self, cell_size):
        """Init. Please, use only one instance of this class.
        """
        self._objects = {}
        self._timeouted_objects = {}
        self._timers_to_exec = []
        self.cell_size = cell_size

        BaseObject.initialize(LOCALE, self)

        try:
            with open(MAP_OBJECTS_CONFIG, 'r') as f:
                configuration = json.load(f)
        except:
            raise RuntimeError('Error reading JSON objects configuration '
                                                  '(%s)!' % MAP_OBJECTS_CONFIG)

        for key, value in configuration.items():
            index = int(key)
            id_ = value['class']
            class_ = OBJECTS_CLASSES[id_]
            kwargs = value['args']
            try:
                self._objects[index] = class_(id_=id_, **kwargs)
            except Exception as err:
                raise RuntimeError('Error creating object '
                                   '#%d (%s)!' % (index, value['class']) +
                                   '%s' % (str(type(err)) + str(err.args)))


    def get_object_by_index(self, index):
        """Return BaseObject instance of selected index.

            index:      game map "OBJ_MARKS_LAYER_NUM" index value.
        """
        if index in self._objects:
            return self._objects[index]
        else:
            return None


    def get_tiles_used_in_objects(self):
        """Return set of tile numbers, declared in objects.
        """
        tiles_check_list = set()
        for obj in self._objects.values():
            tiles_check_list.update(obj.tiles_nums_checklist)
        return tiles_check_list


    def update(self):
        """Check timer/callback table.
        Execute callbacks, time of which is coming.
        """
        need_to_update = False

        for nearest_timer in self._timers_to_exec:
            if nearest_timer > time():
                break

            self._timeouted_objects[nearest_timer]()
            del self._timeouted_objects[nearest_timer]
            need_to_update = True

        if need_to_update:
            self._timers_to_exec = self._timeouted_objects.keys()
            self._timers_to_exec.sort()


    def run_after_timeout(self, callback, timeout):
        """Add some callback, that will be ran after timeount expired.

            callback:       callback to execute (use lambdas for params)
            timeout:        it seconds (up to 3 sygn after point values
                            allowed, i.e. 0.025 sec)
        """
        callback_time = time() + timeout
        self._timeouted_objects[callback_time] = callback
        self._timers_to_exec = self._timeouted_objects.keys()
        self._timers_to_exec.sort()


    def __repr__(self):
        """Simple representation.
        """
        return 'Game map objects manager'
