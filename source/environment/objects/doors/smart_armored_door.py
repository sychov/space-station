# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     20-06-2018
 Description:
----------------------------------------------------------"""

from smart_door import SmartDoor
from misc.events import events
from misc._enums import *


# -------------------------------- Const ------------------------------- #

PHASE_4 = 421
PHASE_3 = 422
PHASE_2 = 423
PHASE_1 = 424
PHASE_0 = 0

DOOR_PHASES = [
    PHASE_4,
    PHASE_3,
    PHASE_2,
    PHASE_1,
    PHASE_0
]

DEFAULT_OPENED_DELAY = 1.5

# ----------------------------- Smart Door --------------------------- #


class SmartArmoredDoor(SmartDoor):
    """Door, opened from terminal. Armored version.
    """
    tiles_nums_checklist = DOOR_PHASES

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
        super(SmartArmoredDoor, self).__init__(
            id_=id_,
            description=description,
            opened_delay=opened_delay,
            terminal=terminal,
            automatics=automatics,
            **kwargs)

        self._opened_delay = kwargs.get('opened_delay', DEFAULT_OPENED_DELAY)
        self._door_animation_phases = DOOR_PHASES

