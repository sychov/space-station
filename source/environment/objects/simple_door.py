# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""

from pygame import Rect

from base import BaseObject
from misc.events import events
from misc._enums import *


# -------------------------------- Const ------------------------------- #

SND_OPEN = "door_open_close.wav"
SND_CLOSE = "door_open_close.wav"
SND_HIT = "door_hit.wav"
SND_STOP = "door_stop.wav"


PHASE_4 = 477
PHASE_3 = 478
PHASE_2 = 479
PHASE_1 = 480
PHASE_0 = 0

DOOR_PHASES = [
    PHASE_4,
    PHASE_3,
    PHASE_2,
    PHASE_1,
    PHASE_0
]

ANIMATION_DELAY = 0.07
OPENED_DELAY = 1

# ----------------------------- Metal Locker --------------------------- #

class SimpleDoor(BaseObject):
    """Storage object - metal locker.
    """
    tiles_nums_checklist = DOOR_PHASES

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

        self._opened_delay = kwargs.get('opened_delay', OPENED_DELAY)
        self._actions_list = [ACTION_BAD, ACTION_USE]
        self.state = CLOSED


    def player_acts_good(self):
        """"Help" action of player.
        """
        pass


    def player_acts_bad(self):
        """"Force" action of player.
        """
        if ACTION_BAD in self._actions_list:
            self._outtext('senseless_hit', once=True)
            self._sound_library.play(SND_HIT)


    def player_acts_use(self):
        """"Use" action of player.
        """
        if self.state == CLOSED:
            self._open_door()


    def _open_door(self):
        """Start door opening process.
        """
        self._outtext('opening', once=True)
        self._sound_library.play(SND_OPEN)
        self._actions_list = []
        events.update_action_interface()
        self.state = OPENED
        self._door_opening(0)


    def _door_opening(self, phase):
        """Draw phases of door opening.
        """
        phase += 1
        if phase < len(DOOR_PHASES):
            tiles = {
                LAYER_OBJECTS: {(self.x, self.y): DOOR_PHASES[phase]}
            }
            events.change_tiles_on_game_map(tiles=tiles)

            self._object_manager.run_after_timeout(
                          lambda : self._door_opening(phase), ANIMATION_DELAY)
        else:
            self._object_manager.run_after_timeout(
                          lambda : self._close_door(), self._opened_delay)


    def _close_door(self):
        """Start door closing process.
        """
        def open_door_callback():
            self._sound_library.play(SND_CLOSE)
            self._door_closing(len(DOOR_PHASES) - 1)

        def wait_a_bit_callback():
            self._sound_library.play(SND_STOP)
            self._object_manager.run_after_timeout(
                               lambda : self._close_door(), self._opened_delay)

        cell_rect = Rect(
            self.x * self._object_manager.cell_size,
            self.y * self._object_manager.cell_size,
            self._object_manager.cell_size,
            self._object_manager.cell_size
        )

        events.check_cell_free_of_chars(
            cell_rect=cell_rect,
            callback_no=open_door_callback,
            callback_yes=wait_a_bit_callback
        )
        self._sound_library.play(SND_CLOSE)


    def _door_closing(self, phase):
        """Draw phases of door closing.
        """
        phase -= 1
        if phase >= 0:
            tiles = {LAYER_OBJECTS: {(self.x, self.y): DOOR_PHASES[phase]}}
            events.change_tiles_on_game_map(tiles=tiles)
            self._object_manager.run_after_timeout(
                           lambda : self._door_closing(phase), ANIMATION_DELAY)
        else:
            self._actions_list = [ACTION_BAD, ACTION_USE]
            self.state = CLOSED
            events.update_action_interface()

