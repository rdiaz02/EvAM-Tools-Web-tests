from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from os import getenv


class WrappedDriver:
    def __init__(self, headless, maximize) -> None:
        self.__driver = None
        self.__url = getenv("URL")
        self.__binary_loc = getenv("BINARY_LOC")
        self.headless = headless
        self.maximize = maximize

    def connect(self) -> None:
        options = webdriver.FirefoxOptions()
        options.headless = self.headless

        firefox_binary = FirefoxBinary(self.__binary_loc)
        firefox_binary.add_command_line_options("-private")

        self.__driver = webdriver.Firefox(
            options=options, firefox_binary=firefox_binary
        )
        self.__driver.get(self.__url)

        if self.maximize:
            self.__driver.maximize_window()

    def get_driver(self):
        return self.__driver

    def get_url(self):
        return self.__url

    def get_binary_loc(self):
        return self.__binary_loc

    def close(self) -> None:
        if self.__driver != None:
            self.__driver.close()


def validate_browser(browser: str) -> bool:
    if browser == "firefox":
        try:
            options = webdriver.FirefoxOptions()
            options.headless = True
            firefox_binary = FirefoxBinary(getenv("BINARY_LOC"))
            driver = webdriver.Firefox(options=options, firefox_binary=firefox_binary)
            driver.get(getenv("URL"))
            driver.close()
            print("Firefox browser configuration is valid")
            return True
        except:
            print(
                """Error in Firefox browser configuration:\n
            - Make sure you have the correct binary location in the .env file\n
            - make sure the Gecodriver is in your PATH or is in the /usr/bin directory\n
            - Make sure the URL is correct and the service is available\n"""
            )
            return False
