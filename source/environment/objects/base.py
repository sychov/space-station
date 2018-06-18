# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""

import json

from sounds.sound_library import SoundLibrary
from misc._pathes import OBJECT_TEXT_PATH_PATTERN
from misc.events import events
from misc._enums import *


class BaseObject(object):
    """Base class for game map objects.
    All objects on game map, player can interact with, are
    based on this type.
    """
    _locale = None
    _text = None
    _actions_list = [ACTION_GOOD, ACTION_BAD, ACTION_USE]
    _sound_library = SoundLibrary()

    current_interface = None
    description = '~ none ~'

    # list of tiles for specific object (including all states).
    tiles_nums_checklist = []


    def __init__(self, id_, description):
        """Init.

            id_:                class ID in configuration files.
            description:        index of description string in locale
                                text files.
        """
        self.x = None
        self.y = None
        self.id = id_

        if not self._text:
            self._setup_localized_text()

        self.actions_text = self._text[self.id]['actions']
        self._change_description(description)


    @classmethod
    def set_locale(cls, locale):
        """Setup locale for all objects text strings.

            locale:         locale name (string)
        """
        cls._locale = locale


    @classmethod
    def _setup_localized_text(cls):
        """Get localized text from configuration file and setup it
        for all objects text strings.
        """
        with open(OBJECT_TEXT_PATH_PATTERN % BaseObject._locale) as f:
            BaseObject._text = json.load(f)


    def set_coords(self, coords):
        """Set tile coords for chosen object.
        If object consist of "obj" and "top" tiles, setting coords of
        the "obj" tile.
        If object consist of some "obj" tiles, setting coords of
        the upper left "obj" tile.
        In most cases this method is worth to be updated

            coords:     (X, Y) coords in tiles

        """
        self.x, self.y = coords


    def get_actions_list(self):
        """Return list of actions, player could act to this object.
        """
        return self._actions_list


    def player_acts_good(self):
        """Virtual method - "Help" action of player.
        """
        pass


    def player_acts_bad(self):
        """Virtual method - "Force" action of player.
        """
        pass


    def player_acts_use(self):
        """Virtual method - "Use" action of player.
        """
        pass


    def _outtext(self, text_key, tag=None, once=False):
        """If text string with this key exists in current locale,
        log it to console with chosen text tag.
        """
        msg = self.actions_text.get(text_key)
        if msg:
            events.put_message_to_players_log(msg, tag, once)


    def _change_description(self, description_key):
        """Change object description.
        """
        self.description = self._text[self.id]['descriptions'][description_key]


