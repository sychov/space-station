# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     12-06-2018
 Description: Music box module. Just for music.
----------------------------------------------------------"""

import os
import fnmatch
from random import shuffle

import pygame

from misc._pathes import MUSIC_DIR
from misc.events import EVENT_SONG_END


class MusicBox(object):
    """Singleton class for in-game music collection.
    """
    _instance = None

    def __new__(cls):
        """Create instance and initializing music lib.
        """
        if cls._instance:
            return cls._instance
        else:
            cls._instance = super(MusicBox, cls).__new__(cls)
            return cls._instance


    def start(self):
        """Start music playing.
        """
        tracks = fnmatch.filter(os.listdir(MUSIC_DIR), '*.ogg')
        shuffle(tracks)
        self._compositions_list = [os.path.join(MUSIC_DIR, track)
                                                           for track in tracks]
        self._playlist = self._compositions_list[:]
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.set_endevent(EVENT_SONG_END)
        if self._compositions_list:
            self.play_next()


    def play_next(self):
        """Play next track.
        """
        if self._playlist:
            pygame.mixer.music.load(self._playlist.pop())
            pygame.mixer.music.play()
        else:
            self._playlist = self._compositions_list[:]
            self.play_next()

