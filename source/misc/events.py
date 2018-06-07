# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     07-06-2018
 Description:
----------------------------------------------------------"""


from pygame.locals import USEREVENT
from pygame.event import Event

from references._enums import *


def enable_action_interface(direction, actions_list):
    """
    """
    return Event(
        USEREVENT,
        custom_type=EVENT_ENABLE_ACTION_INTERFACE,
        direction=direction,
        actions_list=actions_list)


def disable_action_interface():
    """
    """
    return Event(
        USEREVENT,
        custom_type=EVENT_DISABLE_ACTION_INTERFACE)

