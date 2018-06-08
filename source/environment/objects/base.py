# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""

import json

from misc._pathes import OBJECT_TEXT_PATH_PATTERN


class BaseObject(object):
    """
    """
    _locale = None
    _text = None
    description = '~ none ~'

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

