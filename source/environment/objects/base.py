# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""

import json

from misc._pathes import OBJECT_TEXT_PATH_PATTERN
from misc._enums import *


class BaseObject(object):
    """
    """
    _locale = None
    _text = None
    description = '~ none ~'
    _actions_list = [ACTION_GOOD, ACTION_BAD, ACTION_USE]

    def __init__(self, id_, description):
        """
        """
        self.id = id_
        if not self._text:
            self._setup_localized_text()
        self.description = self._text[self.id]['descriptions'][description]


    @classmethod
    def set_locale(cls, locale):
        """
        """
        cls._locale = locale


    @classmethod
    def _setup_localized_text(cls):
        """
        """
        with open(OBJECT_TEXT_PATH_PATTERN % BaseObject._locale) as f:
                BaseObject._text = json.load(f)


    def get_actions_list(self):
        """
        """
        return self._actions_list


    def player_acts_good(self):
        """
        """
        pass


    def player_acts_bad(self):
        """
        """
        pass


    def player_acts_use(self):
        """
        """
        pass


