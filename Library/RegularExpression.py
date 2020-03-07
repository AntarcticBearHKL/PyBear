import re

from BearPY.GlobalBear import *

def ReContain(String, Pattern):
    if not re.search(Pattern, String):
        return False
    return True