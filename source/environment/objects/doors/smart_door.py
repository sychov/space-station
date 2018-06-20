# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""

from simple_door import SimpleDoor
from misc.events import events
from misc._enums import *


# -------------------------------- Const ------------------------------- #

PHASE_4 = 401
PHASE_3 = 402
PHASE_2 = 403
PHASE_1 = 404
PHASE_0 = 0

DOOR_PHASES = [
    PHASE_4,
    PHASE_3,
    PHASE_2,
    PHASE_1,
    PHASE_0
]

ANIMATION_DELAY = 0.07
DEFAULT_OPENED_DELAY = 1.5

# ----------------------------- Smart Door --------------------------- #


class SmartDoor(SimpleDoor):
    """Door, opened from terminal.
    """
    tiles_nums_checklist = DOOR_PHASES

    ANIMATION_DELAY = ANIMATION_DELAY

    def __init__(self, id_, description, opened_delay=DEFAULT_OPENED_DELAY,
                                     terminal=None, automatics=None, **kwargs):
        """Init.

            id_:                Class ID in configuration files.
            description:        Index of description string in locale
                                text files.
            opened_delay:       How much time door will be opened after
                                it's opening.
            terminal:           Index of terminal object for this door.
            automatics:         Index for automatics obj for this doors.
            **kwargs:           All others parameters from config files.
        """
        super(SmartDoor, self).__init__(
            id_=id_,
            description=description,
            opened_delay=opened_delay,
            **kwargs)

        self._terminal = terminal
        self._automatics = automatics
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
            self._outtext('senseless_use', once=True)


    def _post_closing_actions(self):
        """Some actions, we have to do after door is actually closed.
        Virtual.
        """
        if self._terminal:
            terminal = self._object_manager.get_object_by_index(self._terminal)
            terminal.set_closed()

