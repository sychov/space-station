# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description:
----------------------------------------------------------"""


from base import BaseObject


class WoodenLocker(BaseObject):
    """
    """
    def __init__(self, id_, description, **kwargs):
        """
        """
        super(WoodenLocker, self).__init__(
            id_=id_,
            description=description)