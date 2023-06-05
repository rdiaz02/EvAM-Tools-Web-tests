from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from os import getenv


class WrappedDriver:
    def __init__(self, headless, maximize) -> None:
        """
        Initializes a new instance of the WrappedDriver class.

        Args:
            headless (bool): Whether to run the browser in headless mode.
            maximize (bool): Whether to maximize the browser window.

        Returns:
            None
        """
        self.__driver = None
        self.__url = getenv("URL")
        self.__binary_loc = getenv("BINARY_LOC")
        self.headless = headless
        self.maximize = maximize

    def connect(self) -> None:
        """
        Connects to the specified URL using the Firefox browser.

        Returns:
            None
        """
        # Set up the Firefox options
        options = webdriver.FirefoxOptions()
        options.headless = self.headless

        # Set up the Firefox binary
        firefox_binary = FirefoxBinary(self.__binary_loc)
        firefox_binary.add_command_line_options("-private")

        # Create a new Firefox driver instance
        self.__driver = webdriver.Firefox(
            options=options, firefox_binary=firefox_binary
        )

        # Navigate to the specified URL
        self.__driver.get(self.__url)

        # Maximize the window if specified
        if self.maximize:
            self.__driver.maximize_window()

    def get_driver(self):
        """
        Returns the current instance of the Firefox driver.

        Returns:
            WebDriver: The current instance of the Firefox driver.
        """
        return self.__driver

    def get_url(self):
        """
        Returns the URL of the current web page.

        Returns:
            str: The URL of the current web page.
        """
        return self.__url

    def get_binary_loc(self):
        """
        Returns the location of the Firefox binary.

        Returns:
            str: The location of the Firefox binary.
        """
        return self.__binary_loc

    def close(self) -> None:
        """
        Closes the current window.

        Returns:
            None
        """
        if self.__driver != None:
            self.__driver.close()


def validate_browser(browser: str) -> bool:
    """
    Validates the configuration of the specified browser.

    Args:
        browser (str): The name of the browser to validate.

    Returns:
        bool: True if the browser configuration is valid, False otherwise.
    """
    if browser == "firefox":
        try:
            # Set up the Firefox options
            options = webdriver.FirefoxOptions()
            options.headless = True

            # Set up the Firefox binary
            firefox_binary = FirefoxBinary(getenv("BINARY_LOC"))

            # Create a new Firefox driver instance
            driver = webdriver.Firefox(options=options, firefox_binary=firefox_binary)

            # Navigate to the specified URL
            driver.get(getenv("URL"))

            # Close the window
            driver.close()

            # Print a success message and return True
            print("Firefox browser configuration is valid")
            return True
        except:
            # Print an error message and return False
            print(
                """Error in Firefox browser configuration:\n
            - Make sure you have the correct binary location in the .env file\n
            - make sure the Gecodriver is in your PATH or is in the /usr/bin directory\n
            - Make sure the URL is correct and the service is available\n"""
            )
            return False
