# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""


from base_storage import BaseStorage
from environment.storage_container import StorageContent
from interface.storages.metal_locker import MetalLockerInterface
from misc._enums import *


# ---------------------------------- Const ----------------------------- #

SND_OPEN = "metal_locker_open.wav"
SND_CLOSE = "metal_locker_close.wav"

# ----------------------------- MetalLocker ---------------------------- #

class MetalLocker(BaseStorage):
    """Storage object - metal locker.
    """
    def __init__(self, id_, description, **kwargs):
        """Init.

            id_:                class ID in configuration files.
            description:        index of description string in locale
                                text files.
            **kwargs:           all others parameters from config files.
        """
        storage_content = StorageContent(2, 4)
        super(MetalLocker, self).__init__(
            id_=id_,
            description=description,
            storage_content=storage_content,
            interface_class=MetalLockerInterface,
            open_sound=SND_OPEN,
            close_sound=SND_CLOSE)


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

