"""
A file with a class for every command
"""

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


class MotorOn(Command):
    """
    MO Motor on

    xxMO or xxMO?
    """

    def __init__(self, axis: int):
        super().__init__("MO", str(axis))


class MoveHardwareTravelLimit(Command):
    """
    MT Move to hardware travel limit
    """

    def __init__(self, axis: int, direction: str):
        super().__init__("MT", str(axis), direction)


class MoveIndefinitely(Command):
    """
    MV Move indefinitely
    """

    def __init__(self, axis: int, direction: str):
        super().__init__("MV", str(axis), direction)
