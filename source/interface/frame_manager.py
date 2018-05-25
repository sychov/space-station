# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     24-05-2018
 Description:
----------------------------------------------------------"""


from references._enums import *


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
        """
        if on_top:
            self._frames.append(frame)
        else:
            self._frames.insert(0, frame)
        self._update_events()


    def delete_frame(self, frame):
        """Delete frame from manager's list.
        """
        self._frames.remove(frame)
        self._update_events()


    def move_frame_to_top(self, frame):
        """Focus on selected frame.
        """
        self._frames.remove(frame)
        self._frames.append(frame)


    def draw_frames(self, screen):
        """Draw all frames in manager.
        """
        for frame in self._frames:
            frame.draw(screen)


    def handle_event(self, event):
        """Returns True, if event handled. Else False.
        """
        if event.type not in self.events:
            return False

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
        """update set of events, handled by frames in manager.
        """
        events = set()
        for frame in self._frames:
            registered_events = set(frame._events.keys())
            events.update(registered_events)
        self.events = events

