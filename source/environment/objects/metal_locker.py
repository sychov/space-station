# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""


from base import BaseObject
from environment.storage_container import StorageContent
from interface.storages.metal_locker import LockerStorage
from misc.events import events
from misc._enums import *


class MetalLocker(BaseObject):
    """
    """
    def __init__(self, id_, description, **kwargs):
        """
        """
        super(MetalLocker, self).__init__(
            id_=id_,
            description=description)
        self._storage_content = StorageContent(2, 4)


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
        interface = LockerStorage((500, 10, 0, 0), self._storage_content)
        interface.redraw_storage()
        events.show_interface_frame(frame=interface)




