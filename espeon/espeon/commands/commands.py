
from .command import Command

class AbortMotion(Command):
    """
    AB Abort Motion
    """
    def __init__(self):
        super().__init__("AB")

class ID(Command):
    """
    ID Get Name and Serial Number
    """
    def __init__(self, axis: int):
        super().__init__("ID", prefix=axis, postfix="?")

class Heartbeat(Command):
    """
    VER Ping the Device
    """
    def __init__(self):
        super().__init__("VER")
