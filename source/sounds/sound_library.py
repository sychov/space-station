# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     31-05-2018
 Description:
----------------------------------------------------------"""

import os

import pygame


class SoundLibrary(object):
    """Class for in-game sounds collection.
    Works like singleton, but need to be initialized through first
    instance creating:

        SoundLibrary(<path to sounds dir>)

    Later, instances are got through:

        SoundLibrary.get_instance()
    """
    _instance = None

    @staticmethod
    def get_instance():
        """Returns instance of SoundLibrary class.
        Raise error, if it was not initialized yet.
        """
        if not SoundLibrary._instance:
            raise RuntimeError("SoundLibrary not initialized yet!")
        else:
            return SoundLibrary._instance


    def __init__(self, sounds_dir):
        """Create instance and initializing library.
        Could be called only once, raise error otherwise.

            sounds_dir:     path to sounds directory.

        """
        if SoundLibrary._instance:
            raise RuntimeError("SoundLibrary inst was already created!")

        self._sounds = {}
        self._sounds_path = sounds_dir
        SoundLibrary._instance = self


    def get(self, sound_path):
        """Get Sound object by it's relative path from sound dir.

            sound_path:     relative path, like "ambient/noise.wav".

        Usualy it is better to play sounds directly, through
        "play()" method of SoundLibrary instance.
        """
        if sound_path not in self._sounds:
            path = os.path.join(self._sounds_path, sound_path)
            self._sounds[sound_path] = pygame.mixer.Sound(path)
        return self._sounds[sound_path]


    def play(self, sound_path):
        """Play sound.

            sound_path:     relative path, like "ambient/noise.wav".
        """
        self.get(sound_path).play()




