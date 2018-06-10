# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     07-06-2018
 Description:
----------------------------------------------------------"""


from pygame.locals import USEREVENT
from pygame.event import Event, post

from _enums import *


class CustomEvents(object):
    """Simple fabric for custom events.
    It's better to use standard single instance below.
    """
    # ----------------------- ActionInterface --------------------------- #

    def enable_action_interface(self, direction, object_):
        """Event for ActionInterface class.
        Enable action buttons near player's image.

            direction:      UP, DOWN, LEFT, RIGHT
            actions_list:   set (list) of ACTION_BAD, ACTION_GOOD, ACTION_USE
        """
        post(Event(
            USEREVENT,
            custom_type=EVENT_ENABLE_ACTION_INTERFACE,
            direction=direction,
            object_=object_
        ))


    def disable_action_interface(self):
        """Event for ActionInterface class.
        Disable action buttons near player's image.
        """
        post(Event(
            USEREVENT,
            custom_type=EVENT_DISABLE_ACTION_INTERFACE
        ))

    # ----------------------------- Log ------------------------------ #

    def put_message_to_players_log(self, message, message_type=None,
                                                                   once=False):
        """Event for ActionInterface class.
        Disable action buttons near player's image.
        """
        post(Event(
            USEREVENT,
            custom_type=EVENT_PLAYER_MESSAGE_TO_LOG,
            message=message,
            message_type=message_type,
            once=once
        ))

    # ----------------------- Frame Manager --------------------------- #

    def show_interface_frame(self, frame):
        """Event for FrameManager class.
        Disable action buttons near player's image.
        """
        post(Event(
            USEREVENT,
            custom_type=EVENT_SHOW_INTERFACE_FRAME,
            frame=frame,
        ))

    # ------------- #

    def __repr__(self):
        """
        """
        return "Custom events fabrique."

# -------------- instance for importing ------------------- #

events = CustomEvents()

