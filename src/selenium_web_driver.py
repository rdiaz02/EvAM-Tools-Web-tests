from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from dotenv import load_dotenv
from pathlib import Path

import os

# Geckodriver moved to /usr/bin/
dotenv_path = Path('path/to/.env')
load_dotenv(dotenv_path=dotenv_path)

class selenium_driver():
    driver = None

    def connect(self) -> None:

        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True

        options = webdriver.FirefoxOptions()
        options.binary = os.getenv('BINARY_LOC')
        # options.headless = True
        firefox_binary=FirefoxBinary(os.getenv('BINARY_LOC'))
        firefox_binary.add_command_line_options("-private")

        self.driver = webdriver.Firefox(firefox_profile=profile, options=options, firefox_binary=firefox_binary)
        self.driver.get('https://www.iib.uam.es/evamtools/')
        self.driver.maximize_window()

    def close(self) -> None:
        if self.driver != None:
            self.driver.close()

    def wait_visibility_by_xpath(self, xpath, timeout=10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception:
            return False

    def find_and_click(self, xpath) -> None:
        elem = self.driver.find_element_by_xpath(xpath)
        elem.click()