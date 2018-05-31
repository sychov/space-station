# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     31-05-2018
 Description:
----------------------------------------------------------"""

import os

from pygame.mixer import Sound


class SoundLibrary(object):
    """
    """
    _instance = None


    @staticmethod
    def get_instance():
        """
        """
        if not SoundLibrary._instance:
            raise RuntimeError("SoundLibrary not initialized yet!")
        else:
            return SoundLibrary._instance


    def __init__(self, sounds_dir):
        """
        """
        if SoundLibrary._instance:
            raise RuntimeError("SoundLibrary inst was already created!")

        self._sounds = {}
        self._sounds_path = sounds_dir
        SoundLibrary._instance = self


    def get(self, sound_path):
        """
        """
        if sound_path not in self._sounds:
            path = os.path.join(self._sounds_path, sound_path)
            self._sounds[sound_path] = Sound(path)
        return self._sounds[sound_path]


    def play(self, sound_path):
        """
        """
        self.get(sound_path).play()




