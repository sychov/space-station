# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     24-05-2018
 Description:
----------------------------------------------------------"""

import pygame

from storages.base import Storage
from misc.events import events
from misc._enums import *


class FrameManager(object):
    """Simple class of frames aggregation.
    """
    def __init__(self):
        """Init.
        """
        self._frames = []
        self.events = []


    def add_frame(self, frame, on_top=True):
        """Add frame to manager's list.

            frame:      Frame instance
            on_top:     True, if frame must be on top layer (default)
        """
        if on_top:
            self._frames.append(frame)
        else:
            self._frames.insert(0, frame)
        self._update_events()

        if isinstance(frame, Storage):
            frame.bind_external_storage_search(self._get_storage_in_position)


    def remove_frame(self, frame):
        """Delete frame from manager's list.

            frame:      Frame instance
        """
        self._frames.remove(frame)
        self._update_events()
        events.force_memory_free()


    def move_frame_to_top(self, frame):
        """Focus on selected frame.

            frame:      Frame instance
        """
        self._frames.remove(frame)
        self._frames.append(frame)


    def draw_frames(self, screen):
        """Draw all frames in manager.

            screen:     display screen Surface
        """
        for frame in self._frames:
            frame.draw(screen)


    def handle_event(self, event):
        """Returns True, if event handled. Else False.

            event:      pygame.event.Event instance
        """
        if event.type not in self.events:
            return False

        # handle Frame Manager events:
        if event.type == pygame.USEREVENT:

            if event.custom_type == EVENT_SHOW_INTERFACE_FRAME:
                self.add_frame(event.frame)
                return True

            elif event.custom_type == EVENT_HIDE_INTERFACE_FRAME:
                self.remove_frame(event.frame)
                return True

        # handle frames events:
        for frame in reversed(self._frames):
            if frame.handle_event(event):
                self.move_frame_to_top(frame)
                return True
        else:
            return False


    def update(self):
        """Update state of every frame in manager.
        """
        for frame in reversed(self._frames):
            frame.update()


    def _update_events(self):
        """Update set of events, handled by frames in manager.
        """
        events = set()
        for frame in self._frames:
            registered_events = set(frame._events.keys())
            events.update(registered_events)
        self.events = events


    def _get_storage_in_position(self, coords):
        """Scan for first frame collided given mouse position.
        If this frame is Storage, return it.

            coords:        (X, Y) - game screen coords

        Return Storage instance, or None.
        """
        for frame in reversed(self._frames):
            if frame.rect.collidepoint(coords):
                break
        else:
            return None

        if isinstance(frame, Storage):
            return frame
        else:
            return None

