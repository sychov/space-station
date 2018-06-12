# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""

from base_storage import BaseStorage
from environment.storage_container import StorageContent
from interface.storages.wooden_locker import WoodenLockerInterface
from misc._enums import *


class WoodenLocker(BaseStorage):
    """Storage object - wooden shelf locker.
    """
    def __init__(self, id_, description, **kwargs):
        """Init.

            id_:                class ID in configuration files.
            description:        index of description string in locale
                                text files.
            **kwargs:           all others parameters from config files.
        """
        storage_content = StorageContent(2, 3)
        super(WoodenLocker, self).__init__(
            id_=id_,
            description=description,
            storage_content=storage_content,
            interface_class=WoodenLockerInterface,
            open_sound=kwargs.get('open_sound'),
            close_sound=kwargs.get('close_sound'))

        self._actions_list = [ACTION_BAD, ACTION_USE]


    def player_acts_good(self):
        """"Help" action of player.
        """
        pass


    def player_acts_bad(self):
        """"Force" action of player.
        """
        pass


    def player_acts_use(self):
        """"Use" action of player.
        """
        self.open_interface((600, 10, 0, 0))
