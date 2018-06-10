# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""


from base import BaseObject
from misc._enums import *


class WoodenLocker(BaseObject):
    """
    """
    def __init__(self, id_, description, **kwargs):
        """
        """
        super(WoodenLocker, self).__init__(
            id_=id_,
            description=description)

        self._actions_list = [ACTION_BAD, ACTION_USE]


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

