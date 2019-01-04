# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     20-06-2018
 Description:
----------------------------------------------------------"""

from .smart_door import SmartDoor

# -------------------------------- Const ------------------------------- #

PHASE_5 = 410
PHASE_4 = 411
PHASE_3 = 412
PHASE_2 = 413
PHASE_1 = 414
PHASE_0 = 0

DOOR_PHASES = [
    PHASE_5,
    PHASE_4,
    PHASE_3,
    PHASE_2,
    PHASE_1,
    PHASE_0
]

DEFAULT_OPENED_DELAY = 3
ANIMATION_DELAY = 0.05

SND_OPEN = "gate_open_close.wav"
SND_CLOSE = "gate_open_close.wav"

# ----------------------------- Smart Door --------------------------- #


class GateDoor(SmartDoor):
    """Heavy gate door with terminal. Terminal linked with pair's one.
    """
    tiles_nums_checklist = DOOR_PHASES

    ANIMATION_DELAY = ANIMATION_DELAY

    SND_OPEN = SND_OPEN
    SND_CLOSE = SND_CLOSE


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
        super(GateDoor, self).__init__(
            id_=id_,
            description=description,
            opened_delay=opened_delay,
            terminal=terminal,
            automatics=automatics,
            **kwargs)

        self._opened_delay = kwargs.get('opened_delay', DEFAULT_OPENED_DELAY)
        self._door_animation_phases = DOOR_PHASES


    def _post_closing_actions(self):
        """Change state of linked terminal.
        """
        if not self._terminal:
            return
        terminal = self._object_manager.get_object_by_index(self._terminal)
        terminal.toggle_whole_pair_block(is_blocked=False)

