# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""

import json

from sounds.sound_library import SoundLibrary
from misc._pathes import OBJECT_TEXT_PATH_PATTERN
from misc._enums import *


class BaseObject(object):
    """Base class for game map objects.
    All objects on game map, player can interact with, are
    based on this type.
    """
    _locale = None
    _text = None
    description = '~ none ~'
    _actions_list = [ACTION_GOOD, ACTION_BAD, ACTION_USE]
    _sound_library = SoundLibrary.get_instance()


    def __init__(self, id_, description):
        """Init.

            id_:                class ID in configuration files.
            description:        index of description string in locale
                                text files.
        """
        self.id = id_
        if not self._text:
            self._setup_localized_text()
        self.description = self._text[self.id]['descriptions'][description]
        self.actions_text = self._text[self.id]['actions']


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


