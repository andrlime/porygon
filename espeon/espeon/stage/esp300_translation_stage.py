"""
Interface for ESP-300 translation stage
"""

import atexit
import logging
import serial
import time

import espeon.common as constants
from espeon.commands import CommandList  # , CommandChain

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


class ESP300TranslationStage:
    """
    Interface for an ESP-300 translation stage that connects to the device driver, writes bytes, and reads responses

    TODO: Write an abstract RS232Device class
    """

    def __init__(self, driver_path: str, axis: int = 1):
        logger.info("Initializing connection to device at %s, axis %s", driver_path, axis)
        self.device = serial.Serial(driver_path, baudrate=19200, timeout=1)
        self.axis = axis

        self.ping()
        self.get_device_name_and_serial_number()
        self.motor_on()

        logger.info("Connected to device %s (%s)", self.device_name, self.serial_number)
        atexit.register(self.close)

    def sleep_ms(self, duration: int):
        """
        Pause for [duration] milliseconds
        """
        time.sleep(duration / 1000)

    def write(self, command: str):
        """
        Writes a byte command and returns the decoded string response

        args
        ----
        command: Command | CommandChain
            A string representation of a byte sequence which is encoded

        returns
        -------
        response: str
            The string response from the device with max length MAX_RESPONSE_LEN
        """
        logger.info("Writing command %s", command)

        self.device.write(command.encode())
        response = self.device.read(constants.MAX_RESPONSE_LEN).decode().strip()

        logger.info("Got response %s", response)
        return response

    def close(self):
        """
        Closes connection to the device
        """
        self.abort_motion()
        logger.info("Closing connection to %s", self.device_name)
        self.device.close()

    def abort_motion(self):
        """
        AB Stops motion of the translation stage
        """
        logger.info("Aborting motion of translation stage")
        return self.write(CommandList.AbortMotion())

    def motor_on(self):
        """
        MO Motor on
        """
        logger.info("Turning motor on")
        return self.write(CommandList.MotorOn(self.axis))

    def get_device_name_and_serial_number(self):
        """
        ID Returns device name and serial number as a tuple
        """
        response = self.write(CommandList.ID(axis=self.axis))

        response_split = response.split(", ")
        device_name, serial_number = response_split[0], response_split[1]
        logger.info("Fetched device name %s, serial number %s", device_name, serial_number)

        self.device_name = device_name
        self.serial_number = serial_number
        return device_name, serial_number

    def ping(self):
        """
        VER Does a healthcheck/heartbeat check on the device

        Expect to hear a ping / some other ack from the device
        """
        logger.info("Pinging device")
        return self.write(CommandList.Heartbeat())

    def move_to_hardware_travel_limit(self, direction: str):
        """
        MT Move to hardware travel limit

        Direction must equal + or -
        """
        if direction != "+" and direction != "-":
            raise ValueError("MT direction must be + or -")

        logger.info("Moving to hardware travel limit in direction %s", direction)

        return self.write(CommandList.MoveHardwareTravelLimit(self.axis, direction))

    def move_indefinitely(self, direction: str):
        """
        MV Move Indefinitely in one direction

        Direction must equal + or -
        """
        if direction != "+" and direction != "-":
            raise ValueError("MV direction must be + or -")

        logger.info("Moving indefinitely in direction %s", direction)

        return self.write(CommandList.MoveIndefinitely(self.axis, direction))
