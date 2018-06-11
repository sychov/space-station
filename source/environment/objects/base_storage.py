# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""

import json

from base import BaseObject
from misc._pathes import OBJECT_TEXT_PATH_PATTERN
from misc._enums import *
from misc.events import events


class BaseStorage(BaseObject):
    """Base Storage class. Used for all game map objects in game,
    which have storage into.
    """
    def __init__(self, id_, description, storage_content, interface_class,
                                                      open_sound, close_sound):
        """Init.

            id_:                class ID in configuration files.
            description:        index of description string in locale
                                text files.
            storage_content:    StorageContent instance.
            interface_class:    Storage interface CLASS (not instance!)
            open_sound:         sound name for storage opening
            close_sound:        sound name for storage closing
        """
        super(BaseStorage, self).__init__(
            id_=id_,
            description=description)
        self._storage_content = storage_content
        self._interface_class = interface_class
        self.current_interface = None
        self.is_opened = False
        self._open_sound = open_sound
        self._close_sound = close_sound


    def open_interface(self, rect):
        """Show Storage interface on screen.
        """
        self.current_interface = self._interface_class(
                                                  rect, self._storage_content)
        self.current_interface.redraw_storage()
        events.show_interface_frame(frame=self.current_interface)
        events.disable_action_interface()
        self.is_opened = True
        if self._open_sound:
            self._sound_library.play(self._open_sound)
        events.put_message_to_players_log(self.actions_text['open'])


    def close_interface(self):
        """Hide Storage interface from screen.
        """
        events.hide_interface_frame(frame=self.current_interface)
        self.current_interface = None
        events.object_interface_close_reporting()
        self.is_opened = False
        if self._close_sound:
            self._sound_library.play(self._close_sound)
        events.put_message_to_players_log(self.actions_text['close'])


