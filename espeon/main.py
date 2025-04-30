"""
Runs scripts for an ESP-300 translation stage
"""

from espeon.stage import ESP300TranslationStage


def main(driver: str, axis: int = 1):
    stage = ESP300TranslationStage(driver_path=driver, axis=axis)

if __name__ == "__main__":
    main(driver="/dev/tty.usbserial-130", axis=1)
