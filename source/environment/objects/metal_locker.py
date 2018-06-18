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
SND_HIT = 'metal_locker_hit.wav'
SND_BREAK = 'metal_locker_crack.wav'

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
            self._actions_list = [ACTION_BAD, ACTION_USE]
        elif kwargs['state'] == 'broken':
            self.state = BROKEN
            self._actions_list = [ACTION_BAD, ACTION_USE, ACTION_GOOD]
        elif kwargs['state'] == 'locked':
            self._actions_list = [ACTION_BAD, ACTION_USE]
            self.state = LOCKED


    def player_acts_good(self):
        """"Help" action of player.
        """
        if self.state == BROKEN:
            # temp TO DO: del later !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if randrange(5):
                self._outtext('repair_lock_fail', FAIL)
                self._sound_library.play(SND_OPEN)
            else:
                self._repair_lock()


    def player_acts_bad(self):
        """"Force" action of player.
        """
        if self.state == LOCKED:
            # temp TO DO: del later !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if randrange(5):
                self._outtext('break_lock_fail', FAIL)
                self._sound_library.play(SND_HIT)
            else:
                self._break_lock()
        else:
            if self.state == BROKEN:
                self._outtext('broken_hit')
            else:
                self._outtext('senseless_hit', once=True)
            self._sound_library.play(SND_HIT)


    def player_acts_use(self):
        """"Use" action of player.
        """
        if self.state != LOCKED:
            self.open_interface((600, 10, 0, 0))
        else:
            self._outtext('locked', once=True)


    def _break_lock(self):
        """Break locker's lock.
        """
        self.state = BROKEN
        tiles = {
            LAYER_OBJECTS: {(self.x, self.y): BROKEN_OBJ_TILE_NUM},
            LAYER_TOP: {(self.x, self.y - 1): BROKEN_TOP_TILE_NUM}
        }
        events.change_tiles_on_game_map(tiles=tiles)
        self._outtext('break_lock', SUCCESS)
        self._sound_library.play(SND_BREAK)
        self._change_description('broken')
        self._actions_list = [ACTION_BAD, ACTION_USE, ACTION_GOOD]
        events.update_action_interface()


    def _repair_lock(self):
        """Repair locker's lock.
        """
        self.state = NORMAL
        tiles = {
            LAYER_OBJECTS: {(self.x, self.y): NORMAL_OBJ_TILE_NUM},
            LAYER_TOP: {(self.x, self.y - 1): NORMAL_TOP_TILE_NUM}
        }
        events.change_tiles_on_game_map(tiles=tiles)
        self._outtext('repair_lock', SUCCESS)
        self._sound_library.play(SND_CLOSE)
        self._change_description('normal')
        self._actions_list = [ACTION_BAD, ACTION_USE]
        events.update_action_interface()

