# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     19-06-2018
 Description:
----------------------------------------------------------"""

import pygame

from source.misc._enums import *

# ----------------------------- Chars manager ------------------------- #


class CharsManager(object):
    """Agregation class for chars.
    """
    def __init__(self, player):
        """Init. Please, use only one instance of this class.
        """
        self._chars = {player}


    def add_char(self, char):
        """Add character to list for further managing.

            char:      Char class character.
        """
        if char not in self._chars:
            self._chars.append(char)


    def handle_event(self, event):
        """Handle event.
        If event is handled, return True, else False.

            event:      pygame.event.Event instance
        """
        if event.type == pygame.USEREVENT:

            if event.custom_type == EVENT_DETECT_CHARS_ABSENCE_ON_CELL:
                for char in self._chars:
                    result = char.rect.colliderect(event.cell_rect)
                    if result and event.callback_yes:
                        event.callback_yes()
                    elif not result and event.callback_no:
                        event.callback_no()
                return True

        return False


    def __repr__(self):
        """Simple representation.
        """
        return 'Chars manager.'
