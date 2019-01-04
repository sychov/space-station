# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""

from source.environment.objects.base import BaseObject
from source.misc._enums import *


# -------------------------------- Const ------------------------------- #

SND_USE_SUCCES = "door_terminal_accessed.wav"
SND_USE_FAIL = "door_terminal_denied.wav"
SND_HIT = "metal_wall_hit.wav"

DEFAULT_DELAY_BEFORE_OPEN = 0.5

# ----------------------------- Door Terminal --------------------------- #


class DoorTerminal(BaseObject):
    """Terminal for door management.
    """
    SND_USE_SUCCES = SND_USE_SUCCES
    SND_USE_FAIL = SND_USE_FAIL
    SND_HIT = SND_HIT


    def __init__(self, id_, description, door=None, code=None,
                  free_access=True, delay=DEFAULT_DELAY_BEFORE_OPEN, **kwargs):
        """Init.

            id_:                Class ID in configuration files.
            description:        Index of description string in locale
                                text files.
            door:               Number of a door object, terminal connected
                                with (int).
            free_access:        Is free mode enabled (boolean). In free
                                mode terminal doesn't check access rights.
            code:               Code from players access scope for the
                                door. In free mode ignored.
            delay:              Time from activating terminal to opening
                                the door.
            **kwargs:           All others parameters from config files.
        """
        super(DoorTerminal, self).__init__(
            id_=id_,
            description=description)

        self._actions_list = [ACTION_BAD, ACTION_USE]
        self._door = door
        self._is_access_free = free_access
        self._code = code
        self._delay_before_open = delay

        self._status = CLOSED


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
        if ACTION_USE not in self._actions_list:
            return

        if self._check_access():
            self._sound_library.play(self.SND_USE_SUCCES)
            door = self._object_manager.get_object_by_index(self._door)
            if door and door.state == CLOSED and self._status == CLOSED:
                self._outtext('successful_use', SUCCESS)
                self._status = OPENED
                if not self._delay_before_open:
                    door.open_door()
                else:
                    self._object_manager.run_after_timeout(
                        door.open_door,
                        self._delay_before_open
                    )

        else:
            self._outtext('access_denied', FAIL)
            self._sound_library.play(self.SND_USE_FAIL)


    def set_closed(self):
        """Return terminal to state "door closed".
        Method for door object (to change status after closing).
        """
        self._status = CLOSED


    def _check_access(self):
        """Check, if access could be granted to player.
        Return True or False.
        """
        return self._is_access_free

