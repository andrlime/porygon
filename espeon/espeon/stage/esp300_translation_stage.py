"""
Interface for ESP-300 translation stage

TODO: Consider writing an abstract class for this
TODO: Might need to port to C++
"""

import atexit
import logging
import serial

import espeon.common as constants
import espeon.util as utilities

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


class ESP300TranslationStage:
    """
    Interface for an ESP-300 translation stage that connects to the device driver, writes bytes, and reads responses
    """

    def __init__(self, driver_path: str, axis: int = 1):
        logger.info("Initializing connection to device at %s, axis %s", driver_path, axis)
        self.device = serial.Serial(driver_path, baudrate=19200, timeout=1)
        self.axis = axis

        self.write(b"VER\r")
        self.get_name()

        logger.info("Connected to device %s (%s)", self.device_name, self.serial_number)
        atexit.register(self.close)

    def write(self, cmd: bytes):
        """
        Writes a byte command and returns the decoded string response
        """
        logger.info("Writing command %s", cmd)
        self.device.write(cmd)
        response = self.device.read(constants.MAX_RESPONSE_LEN).decode().strip()
        logger.info("Got response %s", response)
        return response

    def close(self):
        """
        Closes connection to the device
        """
        logger.info("Closing connection to %s", self.device_name)
        self.device.close()

    def get_name(self):
        """
        Returns device name and serial number as a tuple
        """
        cmd = utilities.encode_command(f"{self.axis}ID?")
        response = self.write(cmd)
        response_split = response.split(", ")
        device_name, serial_number = response_split[0], response_split[1]
        logger.debug("Fetched device name %s, serial number %s", device_name, serial_number)
        self.device_name = device_name
        self.serial_number = serial_number
        return device_name, serial_number
