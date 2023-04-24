from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from dotenv import load_dotenv
from pathlib import Path

import os

# Geckodriver moved to /usr/bin/
dotenv_path = Path('path/to/.env')
load_dotenv(dotenv_path=dotenv_path)

class EvAMToolsDriver():

    def __init__(self) -> None:
        self.__driver = None
        self.__url = os.getenv('EVAM_URL')
        self.__binary_loc = os.getenv('BINARY_LOC')

    def connect(self, headless=False, maximize=False) -> None:

        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True

        options = webdriver.FirefoxOptions()
        options.headless = headless

        firefox_binary=FirefoxBinary(self.get_binary_loc())
        firefox_binary.add_command_line_options("-private")

        self.set_driver(webdriver.Firefox(firefox_profile=profile, options=options, firefox_binary=firefox_binary))
        self.__driver.get(self.get_url())
        if maximize: 
            self.__driver.maximize_window()

    def get_driver(self):
        return self.__driver

    def set_driver(self, driver):
        self.__driver = driver

    def get_url(self):
        return self.__url

    def get_binary_loc(self):
        return self.__binary_loc

    def close(self) -> None:
        if self.__driver != None:
            self.__driver.close()