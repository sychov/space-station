# -*- coding: utf-8 -*-
"""----------------------------------------------------------
 Author:      alexey.sychov@gameloft.com
 Created:     08-06-2018
 Description: map_object_classes dictionary.
----------------------------------------------------------"""


from environment.objects.metal_locker import MetalLocker
from environment.objects.wooden_locker import WoodenLocker


# Simple table of links between map object class names in
# configuration files and those classes.

OBJECTS_CLASSES = {
    'blue_metal_locker': MetalLocker,
    'wooden_locker': WoodenLocker,
}