"""
Render html into png using Selenium

Written by o3-mini 02/22/2025
"""

import logging
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from chimecho.config import AppConfig


def render_html_page(path: str) -> None:
    width, height = AppConfig().get_selenium_values()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--window-size={width},{height}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("file://" + os.path.abspath(path))

    _, _, _, screenshot_file = AppConfig().get_cli_values()
    driver.save_screenshot(f"{screenshot_file}.png")
    driver.quit()

    logging.info("Weekly schedule exported as %s.png", screenshot_file)
