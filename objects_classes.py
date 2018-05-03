# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     02-05-2018
 Description:
----------------------------------------------------------"""



class Door(object):
    """ Simple door class.
    """
    TICKS = 10

    def __init__(self, map_cell):
        """ Note, that tiles must be set next way:
            closed_tile_number - closed
            closed_tile_number + [1-3] - partial opened
            0 - opened
        """
        # linked to door cell of the map
        self.map_cell = map_cell

        # linked to door cell of the map
        self.closed_tile_number = map_cell.tile_number

        # list of objects, activates this door
        self.activators_list = []

        # range in pixels, door is activated by obj from activators_list
        self.activation_range = None

        # could it change it's state or not
        self.locked = False

        # is some action (opening or closing) now provided
        self.active = False

        # if opening = False and active = True, it means door is closing
        self.opening = False

        # current image phase (0 - closed, 4 - opened)
        self.current_phase = 0

        # counter of frames to phase change
        self.counter = self.TICKS


    def add_activator(self, activators_list, activation_range):
        """
        """
        # list of objects, activates this door
        self.activators_list = activators_list
        # range in pixels, door is activated by obj from activators_list
        self.activation_range = activation_range


    def update(self):
        """
        """
        if self.active:
            # continue started action and return
            return

        need_to_activate = False
        for activator in self.activators_list:
            pass
            #if activator.rect.x -
            # self.activation_range

        if need_to_activate:
            # start opening
            pass
        elif self.current_phase == 4 and not need_to_activate:
            # start closing
            pass




