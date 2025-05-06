"""
Runs scripts for an ESP-300 translation stage
"""

from espeon.stage import ESP300TranslationStage


def main(driver: str, axis: int = 1):
    stage = ESP300TranslationStage(driver_path=driver, axis=axis)

    stage.move_to_hardware_travel_limit("+")
    stage.sleep_ms(500)
    stage.abort_motion()


if __name__ == "__main__":
    main(driver="/dev/tty.usbserial-10", axis=1)
