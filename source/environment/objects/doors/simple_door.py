# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""

from pygame import Rect

from source.environment.objects.base import BaseObject

from source.misc.events import events
from source.misc._enums import *


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
DEFAULT_OPENED_DELAY = 1

# ----------------------------- Simple Door --------------------------- #

class SimpleDoor(BaseObject):
    """Simple door, opened by players hands.
    """
    tiles_nums_checklist = DOOR_PHASES

    SND_OPEN = SND_OPEN
    SND_CLOSE = SND_CLOSE
    SND_HIT = SND_HIT
    SND_STOP = SND_STOP

    ANIMATION_DELAY = ANIMATION_DELAY

    def __init__(self, id_, description, opened_delay=DEFAULT_OPENED_DELAY,
                                                                     **kwargs):
        """Init.

            id_:                Class ID in configuration files.
            description:        Index of description string in locale
                                text files.
            opened_delay:       How much time door will be opened after
                                it's opening.
            **kwargs:           All others parameters from config files.
        """
        super(SimpleDoor, self).__init__(
            id_=id_,
            description=description)

        self._opened_delay = opened_delay
        self._actions_list = [ACTION_BAD, ACTION_USE]
        self.state = CLOSED
        self._door_animation_phases = DOOR_PHASES


    def player_acts_good(self):
        """"Help" action of player.
        """
        pass


    def player_acts_bad(self):
        """"Force" action of player.
        """
        if ACTION_BAD in self._actions_list:
            self._outtext('senseless_hit', once=True)
            self._sound_library.play(self.SND_HIT)


    def player_acts_use(self):
        """"Use" action of player.
        """
        if ACTION_USE in self._actions_list and self.state == CLOSED:
            self.open_door()


    def open_door(self):
        """Start door opening process.
        """
        self._outtext('opening', once=True)
        self._sound_library.play(self.SND_OPEN)
        self._actions_list = []
        events.update_action_interface()
        self.state = OPENED
        self._door_opening(0)


    def _door_opening(self, phase):
        """Continue process of door opening.
        """
        phase += 1
        if phase < len(self._door_animation_phases):
            tiles = {
                LAYER_OBJECTS: {
                    (self.x, self.y): self._door_animation_phases[phase]
                }
            }
            events.change_tiles_on_game_map(tiles=tiles)

            self._object_manager.run_after_timeout(
                     lambda : self._door_opening(phase), self.ANIMATION_DELAY)
        else:
            self._object_manager.run_after_timeout(
                     lambda : self._close_door(), self._opened_delay)


    def _close_door(self):
        """Start door closing process.
        """
        def open_door_callback():
            self._sound_library.play(self.SND_CLOSE)
            self._door_closing(len(self._door_animation_phases) - 1)

        def wait_a_bit_callback():
            self._sound_library.play(self.SND_STOP)
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
        """Continue process of door closing.
        """
        phase -= 1
        if phase >= 0:
            tiles = {
                LAYER_OBJECTS: {
                    (self.x, self.y): self._door_animation_phases[phase]
                }
            }
            events.change_tiles_on_game_map(tiles=tiles)
            self._object_manager.run_after_timeout(
                      lambda : self._door_closing(phase), self.ANIMATION_DELAY)
        else:
            self._actions_list = [ACTION_BAD, ACTION_USE]
            self.state = CLOSED
            events.update_action_interface()
            self._post_closing_actions()


    def _post_closing_actions(self):
        """Some actions, we have to do after door is actually closed.
        Virtual.
        """
        pass

