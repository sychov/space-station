# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""


from base import BaseObject


class MetalLocker(BaseObject):
    """
    """
    def __init__(self, id_, description, **kwargs):
        """
        """
        super(MetalLocker, self).__init__(
            id_=id_,
            description=description)