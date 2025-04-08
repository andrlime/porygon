"""
Runs scripts for an ESP-300 translation stage
"""

from espeon.stage import ESP300TranslationStage

stage = ESP300TranslationStage(driver_path="/dev/tty.usbserial-130", axis=1)
