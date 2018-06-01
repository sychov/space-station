# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     23-05-2018
 Description:
----------------------------------------------------------"""


import pygame
from pygame import Rect, Surface, Color

from references._enums import *


# ======================== Frame config class ========================= #


class FrameConfig(object):
    """Small class for Frame class configuration purposes.
    """
    def __init__(self, tileset_path, part_rects, padding=1, max_size=None,
                                       min_size=None, bg_color=Color(0, 0, 0)):
        """
        Creates simple config object for Frame class:

            tileset_path:   full path to tileset file
            part_rects:     dictionary, where keys are directions and corners
                            enums (UP, BOTTOM_LEFT, etc), and values are
                            Rect instances
            padding:        padding from all border's sides in pixels
            max_size:       (x, y), maximum frame size
            min_size:       (x, y), minimum frame size
            bg_color:       Color instance, for background re-filling
        """
        self.tileset_path = tileset_path
        self.part_rects = part_rects
        self.padding = padding
        self.max_size = max_size
        self.min_size = min_size
        self.bg_color = bg_color


# ========================== Frame class ============================== #


class Frame(object):
    """Parent frame class.
    Used as base to make any custom windows in-game.
    """
    _cached_tilesets = {}

    def __init__(self, rect, frame_config):
        """ Load tileset for a game HUD.
        Create Hud instance with default settings of tileset and limits.

            rect:           x, y, width, height (position on global screen);

        """
        # 1. ~ Init variables ~

        self.rect = Rect(rect)

        self._parts_rects = frame_config.part_rects
        self._background_color = frame_config.bg_color

        if frame_config.max_size:
            self._max_size = frame_config.max_size
        else:
            self._max_size = (self.rect.width, self.rect.height)

        if frame_config.min_size:
            self._min_size = frame_config.min_size
        else:
            self._min_size = (self.rect.width, self.rect.height)

        self._padding = frame_config.padding

        self._events = {}

        # "_background_source" used as hidden canvas of maximum size, where
        # borders and background are drawn
        self._background_source = Surface(self._max_size)

        # "_background" used as a part of "_background_source", that is
        # actually drawn on screen
        self._background = None

        self._dragging = False
        self._resizing = False
        self._mouse_pressed_pos = None

        # 2. ~ Load tiles ~

        if frame_config.tileset_path in Frame._cached_tilesets:
            self._tileset = Frame._cached_tilesets[frame_config.tileset_path]
        else:
            self._tileset = {}
            image = pygame.image.load(frame_config.tileset_path)
            for q in (UP, DOWN, LEFT, RIGHT,
                      TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT):
                _rect = self._parts_rects[q]
                self._tileset[q] = image.subsurface(_rect).convert()
            Frame._cached_tilesets[frame_config.tileset_path] = self._tileset

        # 3. ~ Make background ~

        min_x, min_y = self._min_size
        max_x, max_y = self._max_size
        self.rect.width = min(max(self.rect.width, min_x), max_x)
        self.rect.height = min(max(self.rect.height, min_y), max_y)
        self._redraw_background()


    def resize(self, dx, dy):
        """Change size of the frame relatevly on deltas of X and Y.

            dx:     delta on X
            dy:     delta on Y
        """
        min_x, min_y = self._min_size
        max_x, max_y = self._max_size

        new_width = min(max(self.rect.width + dx, min_x), max_x)
        new_height = min(max(self.rect.height + dy, min_y), max_y)

        if (self.rect.width != new_width or self.rect.height != new_height):
            self.rect.width = new_width
            self.rect.height = new_height
            self._redraw_background()


    def move(self, dx, dy):
        """Move frame relatevly on deltas of X and Y.

            dx:     delta on X
            dy:     delta on Y
        """
        self.rect.x += dx
        self.rect.y += dy


    def draw(self, screen):
        """Draw frame on the screen.

            screen:     display screen Surface
        """
        screen.blit(self._background, self.rect)


    def add_event_handler(self, event_type, callback):
        """Add event to be handled

            event_type:     pygame event type (e.g. ygame.MOUSEBUTTONUP)
            callback:       callback to execute
        """
        self._events[event_type] = callback


    def handle_event(self, event):
        """Main events handler.
        To listen specific event by this method, add it to table through
        add_event_handler() method.

            event:      element got from pygame.event

        Return True, if event was handled, else False.
        """
        if event.type in self._events:
            return self._events[event.type](event)
        else:
            return False


    def update(self):
        """Update frame state. Purely virtual method :)
        """
        pass


    def _update_dragging(self):
        """Method for using in classes, descendants of Frame.
        If dragging state was enabled, update frame's coords on screen.
        """
        if self._dragging:
            current_mouse_pos = pygame.mouse.get_pos()
            if current_mouse_pos != self._mouse_pressed_pos:
                dx = current_mouse_pos[0] - self._mouse_pressed_pos[0]
                dy = current_mouse_pos[1] - self._mouse_pressed_pos[1]
                self.move(dx, dy)
                self._mouse_pressed_pos = current_mouse_pos
                return True
        return False


    def _update_resizing(self):
        """Method for using in classes, descendants of Frame.
        If resizing state was enabled, update frame's size.
        """
        if self._resizing:
            current_mouse_pos = pygame.mouse.get_pos()
            if current_mouse_pos != self._mouse_pressed_pos:
                dx = current_mouse_pos[0] - self._mouse_pressed_pos[0]
                dy = current_mouse_pos[1] - self._mouse_pressed_pos[1]
                self.resize(dx, dy)
                self._mouse_pressed_pos = current_mouse_pos
                return True
        return False


    def _dragging_handled_off(self):
        """Tries to disable dragging state.
        Return True, if state was enabled (disabling was successful)
        """
        if self._dragging:
            self._dragging = False
            return True


    def _resizing_handled_off(self):
        """Tries to disable resizing state.
        Return True, if state was enabled (disabling was successful)
        """
        if self._resizing:
            self._resizing = False
            return True


    def _enable_dragging_state(self, mouse_pressed_pos):
        """Enable dragging state.
        """
        self._dragging = True
        self._mouse_pressed_pos = mouse_pressed_pos


    def _enable_resizing_state(self, mouse_pressed_pos):
        """Enable resizing state.
        """
        self._resizing = True
        self._mouse_pressed_pos = mouse_pressed_pos


    def _redraw_background(self):
        """Draw background on "_background_source" surface.
        Set "_background" attribute to actual part of it.
        """
        width = self.rect.width
        height = self.rect.height
        surface = self._background_source

        surface.fill(self._background_color)

        # draw top side of the HUD
        hud_top_side_len = width - self._parts_rects[TOP_LEFT].width \
                                           - self._parts_rects[TOP_RIGHT].width
        plank_width, _ = self._tileset[UP].get_size()
        x = self._parts_rects[TOP_LEFT].width
        y = 0
        while hud_top_side_len > 0:
            surface.blit(self._tileset[UP], (x, y))
            x += plank_width
            hud_top_side_len -= plank_width

        # draw bottom side of the HUD
        hud_bottom_side_len = width - self._parts_rects[BOTTOM_LEFT].width \
                                        - self._parts_rects[BOTTOM_RIGHT].width
        plank_width, _ = self._tileset[DOWN].get_size()
        x = self._parts_rects[BOTTOM_LEFT].width
        y = height - self._tileset[DOWN].get_size()[1]
        while hud_bottom_side_len > 0:
            surface.blit(self._tileset[DOWN], (x, y))
            x += plank_width
            hud_bottom_side_len -= plank_width

        # draw left side of the HUD
        hud_left_side_len = height - self._parts_rects[TOP_LEFT].height \
                                        - self._parts_rects[BOTTOM_LEFT].height
        _, plank_height = self._tileset[LEFT].get_size()
        y = self._parts_rects[TOP_LEFT].height
        x = 0
        while hud_left_side_len > 0:
            surface.blit(self._tileset[LEFT], (x, y))
            y += plank_height
            hud_left_side_len -= plank_height

        # draw right side of the HUD
        hud_right_side_len = height - self._parts_rects[TOP_RIGHT].height \
                                       - self._parts_rects[BOTTOM_RIGHT].height
        _, plank_height = self._tileset[RIGHT].get_size()
        y = self._parts_rects[TOP_RIGHT].height
        x = width - self._tileset[RIGHT].get_size()[0]
        while hud_right_side_len > 0:
            surface.blit(self._tileset[RIGHT], (x, y))
            y += plank_height
            hud_right_side_len -= plank_height

        # draw corners
        surface.blit(self._tileset[TOP_LEFT], (0, 0))
        surface.blit(self._tileset[TOP_RIGHT],
                           (width - self._tileset[TOP_RIGHT].get_size()[0], 0))
        surface.blit(self._tileset[BOTTOM_LEFT],
                           (0, height - self._parts_rects[BOTTOM_LEFT].height))
        surface.blit(self._tileset[BOTTOM_RIGHT],
                    (width - self._tileset[BOTTOM_RIGHT].get_size()[0],
                     height - self._tileset[BOTTOM_RIGHT].get_size()[1]))

        self._background = self._background_source.subsurface(
                                     (0, 0, self.rect.width, self.rect.height))

    # -------------------------------- #

    def __repr__(self):
        """Simple representation.
        """
        return 'Frame class instance.'
