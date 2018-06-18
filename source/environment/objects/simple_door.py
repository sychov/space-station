# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""

from base import BaseObject
from misc.events import events
from misc._enums import *


# -------------------------------- Const ------------------------------- #

SND_OPEN = "door_open_close.wav"
SND_CLOSE = "door_open_close.wav"
SND_HIT = "door_hit.wav"

PHASE_4 = 477
PHASE_3 = 478
PHASE_2 = 479
PHASE_1 = 480
PHASE_0 = 0

# ----------------------------- Metal Locker --------------------------- #

class SimpleDoor(BaseObject):
    """Storage object - metal locker.
    """
    tiles_nums_checklist = [
        PHASE_4,
        PHASE_3,
        PHASE_2,
        PHASE_1,
        PHASE_0
    ]

    def __init__(self, id_, description, **kwargs):
        """Init.

            id_:                class ID in configuration files.
            description:        index of description string in locale
                                text files.
            **kwargs:           all others parameters from config files.
        """
        super(SimpleDoor, self).__init__(
            id_=id_,
            description=description)

        self._actions_list = [ACTION_BAD, ACTION_USE]
        self.state = CLOSED


    def player_acts_good(self):
        """"Help" action of player.
        """
        pass


    def player_acts_bad(self):
        """"Force" action of player.
        """
        self._outtext('senseless_hit', once=True)
        self._sound_library.play(SND_HIT)


    def player_acts_use(self):
        """"Use" action of player.
        """
        if self.state == CLOSED:
            self._outtext('opening', once=True)
            self._sound_library.play(SND_OPEN)


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

