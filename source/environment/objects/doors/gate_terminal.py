# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""

from source.misc.events import events
from source.misc._enums import *
from .door_terminal import DoorTerminal

# -------------------------------- Const ------------------------------- #

STATE_TILE_READY = 408
STATE_TILE_BUSY = 409

DEFAULT_DELAY_BEFORE_OPEN = 0.5

# ----------------------------- Door Terminal --------------------------- #


class GateTerminal(DoorTerminal):
    """Terminal for door management.
    """
    tiles_nums_checklist = [STATE_TILE_READY, STATE_TILE_BUSY]

    STATE_TILE_READY = STATE_TILE_READY
    STATE_TILE_BUSY = STATE_TILE_BUSY

    def __init__(self, id_, description, door=None, code=None,
                 free_access=True, delay=DEFAULT_DELAY_BEFORE_OPEN,
                 pair_terminal=None, **kwargs):
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
            pair_terminal:      Another terminal in pair. Only one
                                terminal could be opened in pair in
                                one moment of time.
            **kwargs:           All others parameters from config files.
        """
        super(GateTerminal, self).__init__(
            id_=id_,
            description=description,
            door=door,
            code=code,
            free_access=free_access,
            delay=delay,
            **kwargs)

        self._pair_terminal = pair_terminal


    def player_acts_use(self):
        """"Use" action of player.
        """
        if ACTION_USE not in self._actions_list:
            return

        if not self._check_access():
            self._outtext('access_denied', FAIL)
            self._sound_library.play(self.SND_USE_FAIL)

        elif self._status == BLOCKED:
            self._outtext('please_wait', FAIL)
            self._sound_library.play(self.SND_USE_FAIL)

        elif self._status == OPENED:
            self._sound_library.play(self.SND_USE_SUCCES)

        elif self._status == CLOSED:
            self._sound_library.play(self.SND_USE_SUCCES)
            door = self._object_manager.get_object_by_index(self._door)
            if door and door.state == CLOSED:

                self._outtext('successful_use', SUCCESS)
                self._status = OPENED

                self.toggle_whole_pair_block(is_blocked=True)

                if not self._delay_before_open:
                    door.open_door()
                else:
                    self._object_manager.run_after_timeout(
                                       door.open_door, self._delay_before_open)


    def toggle_block(self, is_blocked):
        """Block / unblock current terminal.

            is_blocked:       True, if you need to block terminal, or False
        """
        if is_blocked:
            self._status = BLOCKED
            tile = STATE_TILE_BUSY
        else:
            self._status = CLOSED
            tile = STATE_TILE_READY

        events.change_tiles_on_game_map(
            tiles={LAYER_OBJECTS: {(self.x, self.y): tile}})


    def toggle_whole_pair_block(self, is_blocked):
        """Block / unblock paired terminal.

            is_blocked:       True, if you need to block terminal, or False
        """
        self.toggle_block(is_blocked)
        if self._pair_terminal:
            pair = self._object_manager.get_object_by_index(self._pair_terminal)
            pair.toggle_block(is_blocked=is_blocked)

