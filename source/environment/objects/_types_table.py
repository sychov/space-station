# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description: map_object_classes dictionary.
----------------------------------------------------------"""


from storages.metal_locker import MetalLocker
from storages.wooden_locker import WoodenLocker

from doors.simple_door import SimpleDoor
from doors.smart_door import SmartDoor
from doors.smart_armored_door import SmartArmoredDoor
from doors.gate_door import GateDoor

from doors.door_terminal import DoorTerminal
from doors.gate_terminal import GateTerminal

# Simple table of links between map object class names in
# configuration files and those classes.

OBJECTS_CLASSES = {
    'blue_metal_locker': MetalLocker,
    'wooden_locker': WoodenLocker,
    'simple_door': SimpleDoor,
    'smart_door': SmartDoor,
    'door_terminal': DoorTerminal,
    'smart_armored_door': SmartArmoredDoor,
    'gate_door': GateDoor,
    'gate_terminal': GateTerminal,

}