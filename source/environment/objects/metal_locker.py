# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""

from random import randrange

from base_storage import BaseStorage
from environment.storage_container import StorageContent
from interface.storages.metal_locker import MetalLockerInterface
from misc.events import events
from misc._enums import *


# -------------------------------- Const ------------------------------- #

SND_OPEN = "metal_locker_open.wav"
SND_CLOSE = "metal_locker_close.wav"

NORMAL_OBJ_TILE_NUM = 301
NORMAL_TOP_TILE_NUM = 281
BROKEN_OBJ_TILE_NUM = 302
BROKEN_TOP_TILE_NUM = 282

# ----------------------------- Metal Locker --------------------------- #

class MetalLocker(BaseStorage):
    """Storage object - metal locker.
    """
    tiles_nums_checklist = [
        NORMAL_OBJ_TILE_NUM,
        NORMAL_TOP_TILE_NUM,
        BROKEN_OBJ_TILE_NUM,
        BROKEN_TOP_TILE_NUM,
    ]

    def __init__(self, id_, description, **kwargs):
        """Init.

            id_:                class ID in configuration files.
            description:        index of description string in locale
                                text files.
            **kwargs:           all others parameters from config files.
        """
        storage_content = StorageContent(2, 4)
        super(MetalLocker, self).__init__(
            id_=id_,
            description=description,
            storage_content=storage_content,
            interface_class=MetalLockerInterface,
            open_sound=SND_OPEN,
            close_sound=SND_CLOSE)

        if 'state' not in kwargs or kwargs['state'] == 'normal':
            self.state = NORMAL
        elif kwargs['state'] == 'broken':
            self.state = BROKEN


    def player_acts_good(self):
        """"Help" action of player.
        """
        if self.state == BROKEN:
            self._repair_lock()


    def player_acts_bad(self):
        """"Force" action of player.
        """
        if self.state == NORMAL:
            # temp TO DO: del later !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if randrange(5):
                self._outtext('break_lock_fail', FAIL)
                self._sound_library.play('metal_locker_hit.wav')
            else:
                self._break_lock()


    def player_acts_use(self):
        """"Use" action of player.
        """
        self.open_interface((600, 10, 0, 0))


    def _break_lock(self):
        """Break locker's lock.
        """
        self.state = BROKEN
        events.change_tile_num_on_game_map(
            tile_coords=(self.x, self.y),
            layer_type=LAYER_OBJECTS,
            tile_num=BROKEN_OBJ_TILE_NUM
        )
        events.change_tile_num_on_game_map(
            tile_coords=(self.x, self.y - 1),
            layer_type=LAYER_TOP,
            tile_num=BROKEN_TOP_TILE_NUM
        )
        self._outtext('break_lock', SUCCESS)
        self._sound_library.play('metal_locker_crack.wav')


    def _repair_lock(self):
        """Repair locker's lock.
        """
        self.state = NORMAL
        events.change_tile_num_on_game_map(
            tile_coords=(self.x, self.y),
            layer_type=LAYER_OBJECTS,
            tile_num=NORMAL_OBJ_TILE_NUM
        )
        events.change_tile_num_on_game_map(
            tile_coords=(self.x, self.y - 1),
            layer_type=LAYER_TOP,
            tile_num=NORMAL_TOP_TILE_NUM
        )
        self._outtext('repair_lock', SUCCESS)
        self._sound_library.play('metal_locker_close.wav')

