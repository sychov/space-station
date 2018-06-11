# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     07-06-2018
 Description:
----------------------------------------------------------"""


from pygame.locals import USEREVENT
from pygame.event import Event, post

from _enums import *


# ------------------------------ CONST --------------------------------- #

DEBUG = False

# ---------------------------------------------------------------------- #


class CustomEvents(object):
    """Simple fabric for custom events.
    It's better to use standard single instance below.
    """
    # --------------------------- Main -------------------------------- #

    def force_memory_free(self):
        """Event for Main app class.
        Force memory garbage collection.
        """
        if DEBUG:
            print '! force_memory_free'

        post(Event(
            USEREVENT,
            custom_type=EVENT_FORCE_MEMORY_FREE
        ))

    # ----------------------- ActionInterface --------------------------- #

    def enable_action_interface(self, direction, object_):
        """Event for ActionInterface class.
        Enable action buttons near player's image.

            direction:      UP, DOWN, LEFT, RIGHT
            object_:        selected game map object.
        """
        if DEBUG:
            print '+ enable_action_interface'

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
        if DEBUG:
            print '- disable_action_interface'

        post(Event(
            USEREVENT,
            custom_type=EVENT_DISABLE_ACTION_INTERFACE
        ))

    # ----------------------------- Log ------------------------------ #

    def put_message_to_players_log(self, message, message_type=None,
                                                                   once=False):
        """Event for ActionInterface class.
        Disable action buttons near player's image.

            message:                message text,
            message_type:           message tag (None for default)
            once:                   flag, True if need preventing spam
        """
        if DEBUG:
            print '   + put_message_to_players_log'

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
        Show interface frame.

            frame:       Frame instance, interface of game map's object.
        """
        if DEBUG:
            print '+ show_interface_frame'

        post(Event(
            USEREVENT,
            custom_type=EVENT_SHOW_INTERFACE_FRAME,
            frame=frame,
        ))


    def hide_interface_frame(self, frame):
        """Event for FrameManager class.
        Hide interface frame.

            frame:       Frame instance, interface of game map's object.
        """
        if DEBUG:
            print '- hide_interface_frame'

        post(Event(
            USEREVENT,
            custom_type=EVENT_HIDE_INTERFACE_FRAME,
            frame=frame,
        ))

    # ---------------------------- Player ----------------------------- #

    def actions_interface_close_reporting(self):
        """Event for Player class.
        Pure report about closing actions interface.
        """
        if DEBUG:
            print '   * actions_interface_close_reporting'

        post(Event(
            USEREVENT,
            custom_type=EVENT_ACTION_INTERFACE_CLOSED
        ))


    def object_interface_close_reporting(self):
        """Event for Player class.
        Pure report about closing object interface.
        """
        if DEBUG:
            print '   * object_interface_close_reporting'

        post(Event(
            USEREVENT,
            custom_type=EVENT_OBJECT_INTERFACE_CLOSED
        ))

    # ------------- #

    def __repr__(self):
        """
        """
        return "Custom events fabrique."


# -------------- instance for importing ------------------- #

events = CustomEvents()

