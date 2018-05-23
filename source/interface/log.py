# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Description:
----------------------------------------------------------"""

from collections import deque

import pygame
from pygame import Rect, Surface, Color

from references._enums import *

from frame import Frame

# ------------------------------ CONST ------------------------------------- #

##HUD_TILESET_PATH = "interface/chat3.png"
##
##HUD_PARTS_RECTS = {
##    TOP_LEFT:       Rect(0, 0, 60, 54),
##    TOP_RIGHT:      Rect(140, 0, 85, 49),
##    BOTTOM_LEFT:    Rect(0, 69, 50, 71),
##    BOTTOM_RIGHT:   Rect(185, 67, 40, 73),
##    UP:             Rect(62, 0, 51, 22),
##    DOWN:           Rect(62, 124, 51, 16),
##    LEFT:           Rect(0, 55, 19, 16),
##    RIGHT:          Rect(204, 47, 21, 24),
##}
##
##HUD_MAX_SIZE = (700, 700)
##HUD_MIN_SIZE = (300, 130)
##HUD_DEQUE_MAX_LEN = 10
##HUD_BACKGROUND_COLOR = Color(0, 0, 0)
##HUD_TEXT_COLORS = {}
##HUD_RESIZE_BUTTON_SIZE = 20
##
##HUD_PADDING = 25
##HUD_FONT = ('Comic Sans MS', 15)

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
HUD_DEQUE_MAX_LEN = 10
HUD_BACKGROUND_COLOR = Color(10, 10, 10)
HUD_TEXT_COLOR = Color(230, 230, 0)
HUD_RESIZE_BUTTON_SIZE = 20

HUD_PADDING = 18
HUD_FONT = ('Lucida Console', 15)
HUD_LINE_SPACING = 2

# ========================== HUD monitor class ============================== #

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
            padding=HUD_PADDING
        )
        self._messages = deque(maxlen=HUD_DEQUE_MAX_LEN)
        self._font = pygame.font.SysFont(*HUD_FONT)

        # TO DO: DEL
        self._messages.extend(
            q.strip() for q in
            u'''Welcome to the printables page!
            Here you’ll find various printouts that I’ve made for games.
            For the non-word-list printables down below.
            If you click the image, it will take you to the printable.
            If you click the words under the image, it will take you to.
            Post with instructions on how to use the printable.
            Hopefully this page can help you find the game you’re looking for.
            Happy playing!'''.splitlines()
        )
        # /TO DO: DEL

        self._update_text_bottomed()


    def output(self, msg, tag=None):
        """Output new message.
        """
        self._messages.appendleft((msg, tag))
        self._update_text_bottomed()


    def is_resize_corner_selected(self, coords):
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


    def _update_text_bottomed(self):
        """Update text in the HUD log, redrawing them on log frame.
        This method will align text to bottom of the log.
        """
        _width, _height = self._background.get_size()
        text_frame = self._background.subsurface(
                            (self.padding,
                             self.padding,
                             _width - self.padding * 2,
                             _height - self.padding * 2))


        font_height = self._font.size("Tg")[1]
        text_width = text_frame.get_width()
        text_height = text_frame.get_height()

        position_y = text_height - font_height
        min_position_y = - text_height

        break_flag = False
        for msg in self._messages:
            print msg
            for strings_surface in self._get_strings_surfaces_from_message(
                            msg=msg, width=text_width, color=HUD_TEXT_COLOR):
                text_frame.blit(strings_surface, (0, position_y))
                position_y -= font_height + HUD_LINE_SPACING
                if position_y < min_position_y:
                    break_flag = True
                    break
            if break_flag:
                break


    def _get_strings_surfaces_from_message(self, msg, width, color):
        """
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
        strings_surfaces.reverse()
        return strings_surfaces


    def __repr__(self):
        """Simple representation.
        """
        return 'HUD log class instance.'

