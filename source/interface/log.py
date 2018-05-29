# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Description:
----------------------------------------------------------"""

from collections import deque
from itertools import islice

import pygame
from pygame import Rect, Surface, Color

from frame import Frame
from references._enums import *

# ------------------------------ CONST ------------------------------------- #

HUD_TILESET_PATH = "../graphics/interface/chat_border.png"

HUD_PARTS_RECTS = {
    TOP_LEFT:       Rect(0, 0, 78, 35),
    TOP_RIGHT:      Rect(219, 0, 45, 71),
    BOTTOM_LEFT:    Rect(0, 137, 61, 61),
    BOTTOM_RIGHT:   Rect(163, 134, 101, 64),
    UP:             Rect(77, 0, 142, 7),
    DOWN:           Rect(62, 192, 102, 6),
    LEFT:           Rect(0, 34, 5, 104),
    RIGHT:          Rect(258, 69, 6, 66),
}

HUD_MAX_SIZE = (700, 600)
HUD_MIN_SIZE = (300, 135)
HUD_DEQUE_MAX_LEN = 30
HUD_BACKGROUND_COLOR = Color(10, 10, 10)
HUD_TEXT_COLORS = {
    None: Color(200, 200, 200),
    DANGER: Color(230, 0, 0),
    SUCCESS: Color(0, 230, 0),
    FAIL: Color(230, 230, 0),
}
HUD_RESIZE_BUTTON_SIZE = 20

HUD_PADDING = 18
HUD_FONT = ('Lucida Console', 15)
HUD_LINE_SPACING = 2

# ========================== LOG frame class ============================== #

class Log(Frame):
    """HUD log class.
    It is made for logging in-game events in text form for player info.
    """
    def __init__(self, rect):
        """ Load tileset for a game HUD log.
        Create Log instance with default settings of tileset and limits.
            rect:  x, y, width, height (on global screen)
        """
        super(Log, self).__init__(
            rect=rect,
            tileset_path=HUD_TILESET_PATH,
            parts_rects=HUD_PARTS_RECTS,
            max_size=HUD_MAX_SIZE,
            min_size=HUD_MIN_SIZE,
            bg_color=HUD_BACKGROUND_COLOR,
        )
        self._padding = HUD_PADDING
        self._messages = deque(maxlen=HUD_DEQUE_MAX_LEN)
        self._font = pygame.font.SysFont(*HUD_FONT)
        self._current_message_index = None
        self._bottomed_message_index = None
        self._up_to_last_string = False
        self._update_text()

        # ~ EVENTS ~

        self.add_event_handler(pygame.MOUSEBUTTONUP,
                               self._event_mousebutton_up)
        self.add_event_handler(pygame.MOUSEBUTTONDOWN,
                               self._event_mousebutton_down)


    def output(self, msg, tag=None):
        """Output new message.
        """
        self._messages.append((msg, tag))
        self._update_text_bottomed()


    def update(self):
        """Update frame state (dragging and resizing handling).
        """
        self._update_dragging()
        if self._update_resizing():
            self._update_text(bottom_anchor=True)


    def _update_text(self, bottom_anchor=False):
        """Update text in box.
        If "bottom_anchor" == True, force to bottom align.
        """
        if bottom_anchor or self._current_message_index is None:
            self._update_text_bottomed()
        else:
            self._update_text_topped()


    def _update_text_topped(self):
        """Update text in the HUD log, redrawing them on log frame.
        This method will align text to the top of the log by current
        message index.
        """
        _width, _height = self._background.get_size()
        text_frame = self._background.subsurface(
                            (self._padding,
                             self._padding,
                             _width - self._padding * 2,
                             _height - self._padding * 2))

        text_frame.fill(HUD_BACKGROUND_COLOR)
        font_height = self._font.size("Tg")[1]
        text_width = text_frame.get_width()
        text_height = text_frame.get_height()

        position_y = 0
        max_position_y = text_height

        messages = islice(self._messages,
                          self._current_message_index,
                          len(self._messages))

        self._up_to_last_string = False
        for msg, tag in messages:
            for strings_surface in self._get_strings_surfaces_from_message(
                            msg=msg,
                            width=text_width,
                            color=HUD_TEXT_COLORS[tag]):
                if position_y > max_position_y:
                    return
                text_frame.blit(strings_surface, (0, position_y))
                position_y += font_height + HUD_LINE_SPACING
        self._up_to_last_string = True


    def _update_text_bottomed(self):
        """Update text in the HUD log, redrawing them on log frame.
        This method will align text to bottom of the log.
        """
        _width, _height = self._background.get_size()
        text_frame = self._background.subsurface(
                            (self._padding,
                             self._padding,
                             _width - self._padding * 2,
                             _height - self._padding * 2))

        text_frame.fill(HUD_BACKGROUND_COLOR)
        font_height = self._font.size("Tg")[1]
        text_width = text_frame.get_width()
        text_height = text_frame.get_height()

        position_y = text_height - font_height
        min_position_y = - font_height

        self._up_to_last_string = True

        message_index = len(self._messages) - 1
        for msg, tag in reversed(self._messages):
            for strings_surface in reversed(
                    self._get_strings_surfaces_from_message(
                            msg=msg,
                            width=text_width,
                            color=HUD_TEXT_COLORS[tag])):
                text_frame.blit(strings_surface, (0, position_y))
                position_y -= font_height + HUD_LINE_SPACING
                if position_y < min_position_y:
                    self._current_message_index = None
                    # update last shown message index
                    self._bottomed_message_index = message_index
                    return
            message_index -= 1


    def _get_strings_surfaces_from_message(self, msg, width, color):
        """Get list of surfaces, everyone is a fraphical string
        of message (according to frame width).

            msg:        string message
            width:      width of textbox in pixels
            color:      Color class instance
        """
        strings_surfaces = []
        while msg:
            q = 1
            # determine maximum width of line
            while self._font.size(msg[:q])[0] < width and q < len(msg):
                q += 1
            # if we've wrapped the msg, then adjust the wrap to the last word
            if q < len(msg):
                q = msg.rfind(" ", 0, q) + 1
            # render the line
            strings_surfaces.append(
               self._font.render( msg[:q], False, color, HUD_BACKGROUND_COLOR))
            # remove the msg we just blitted
            msg = msg[q:]
        return strings_surfaces


    def _is_resize_corner_selected(self, coords):
        """Check, if "coords" are in resize corner area.
        """
        x, y = coords
        if x > self.rect.x + self.rect.width - HUD_RESIZE_BUTTON_SIZE and \
           x < self.rect.x + self.rect.width and \
           y > self.rect.y + self.rect.height - HUD_RESIZE_BUTTON_SIZE and \
           y < self.rect.y + self.rect.height:
            return True
        else:
            return False

    # ---------------------- EVENTS ----------------------- #

    def _event_mousebutton_up(self, event):
        """Handle mouse button up event.
        """
        if self._dragging_handled_off() or self._resizing_handled_off():
            return True
        else:
            return False


    def _event_mousebutton_down(self, event):
        """Handle mouse button down event.
        """
        if self.rect.collidepoint(event.pos):

            # mouse scroll up
            if event.button == 4:
                self._scroll_up()

            # scroll down
            elif event.button == 5:
                self._scroll_down()

            elif self._is_resize_corner_selected(event.pos):
                # resize HUD
                self._enable_resizing_state(event.pos)

            else:
                # move HUD
                self._enable_dragging_state(event.pos)

            return True
        else:
            return False


    def _scroll_up(self):
        """Scroll text content up.
        """
        messages_count = len(self._messages)
        if not messages_count or \
           self._current_message_index == 0:
            return

        if self._current_message_index is None:
            self._current_message_index = self._bottomed_message_index
        else:
            self._current_message_index -= 1
        self._update_text()


    def _scroll_down(self):
        """Scroll text content down.
        """
        messages_count = len(self._messages)
        if not messages_count or \
           self._current_message_index is None or \
           self._up_to_last_string or \
           self._current_message_index == messages_count - 1:
            return

        self._current_message_index += 1
        self._update_text()

    # -------------------------------- #

    def __repr__(self):
        """Simple representation.
        """
        return 'HUD log class instance.'

