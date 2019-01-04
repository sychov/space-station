# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     31-05-2018
 Description:
----------------------------------------------------------"""

import os

import pygame

from source.misc._pathes import SOUNDS_DIR


class SoundLibrary(object):
    """Singleton class for in-game sounds collection.
    """
    _instance = None


    def __new__(cls):
        """Create instance and initializing music lib.
        """
        if cls._instance:
            return cls._instance
        else:
            cls._instance = super(SoundLibrary, cls).__new__(cls)
            cls._instance._sounds = {}
            return cls._instance


    def get(self, sound_path):
        """Get Sound object by it's relative path from sound dir.

            sound_path:     relative path, like "ambient/noise.wav".

        Usualy it is better to play sounds directly, through
        "play()" method of SoundLibrary instance.
        """
        if sound_path not in self._sounds:
            path = os.path.join(SOUNDS_DIR, sound_path)
            self._sounds[sound_path] = pygame.mixer.Sound(path)
        return self._sounds[sound_path]


    def play(self, sound_path):
        """Play sound.

            sound_path:     relative path, like "ambient/noise.wav".
        """
        self.get(sound_path).play()




