"""
Interface for ESP-300 translation stage

TODO: Consider writing an abstract class for this
TODO: Might need to port to C++
"""

import atexit
import logging
import serial

import espeon.common as constants

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class ESP300TranslationStage:
    def __init__(self, driver_path: str, axis: int = 1):
        logger.info(f"Initializing connection to device at {driver_path}, axis {axis}")
        self.device = serial.Serial(
            driver_path,
            baudrate=19200,
            timeout=1
        )
        self.axis = axis

        self.write(b"VER\r")
        self.fetch_name()

        logger.info(f"Connected to device {self.device_name} ({self.serial_number})")        
        atexit.register(self.close)
    
    @staticmethod
    def encode_command(cmd_string: str):
        """
        Encodes a string command into bytes
        """
        logger.debug(f"Encoding command {cmd_string}")
        return f"{cmd_string}\r".encode()

    def fetch_name(self):
        """
        Sends (axis)ID?, e.g. 1ID?, to get the device name and serial number
        """
        cmd = ESP300TranslationStage.encode_command(
            cmd_string=f"{self.axis}ID?"
        )
        response = self.write(cmd)
        response_split = response.split(", ")
        device_name, serial_number = response_split[0], response_split[1]
        logger.debug(f"Fetched device name {device_name}, serial number {serial_number}")
        self.device_name = device_name
        self.serial_number = serial_number
    
    def get_name(self):
        """
        Returns device name and serial number as a tuple
        """
        return self.device_name, self.serial_number

    def write(self, cmd: bytes):
        """
        Writes a byte command and returns the decoded string response
        """
        logger.info(f"Writing command {cmd}")
        self.device.write(cmd)
        response = self.device.read(constants.MAX_RESPONSE_LEN).decode().strip()
        logger.info(f"Got response {response}")
        return response
    
    def close(self):
        """
        Closes connection to the device
        """
        logger.info(f"Closing connection to {self.device_name}")
        self.device.close()
