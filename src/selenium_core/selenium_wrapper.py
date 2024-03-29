from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException
from os import getenv
from time import sleep

BROWSER_TO_USE = "firefox"
CONFIG_ERROR_MSG = f"""Error in {BROWSER_TO_USE} browser configuration:\n
            - Make sure you have the correct binary location in the .env file in case of custom install\n
            - Make sure the driver is in your PATH or is in the /usr/bin directory\n
            - Make sure the URL is correct and the service is available\n"""


class WrappedDriver:
    def __init__(self, **config) -> None:
        self.driver = None
        self.url = getenv("URL")
        self.binary_loc = getenv(
            BROWSER_TO_USE.upper() + "_BINARY_LOC", "/usr/bin/" + BROWSER_TO_USE
        )
        self.config(**config)
        self.connect()

    def config(self, **config) -> None:
        self.headless = config.get("headless", False)
        self.maximize = config.get("maximize", False)
        self.large_log = config.get("large_log", False)
        self.save_screenshots = config.get("screenshots", False)

    def connect(self) -> None:
        if BROWSER_TO_USE == "firefox":
            self.connect_firefox()
        elif BROWSER_TO_USE == "google-chrome":
            self.connect_chrome()

    def connect_firefox(self) -> None:
        options = webdriver.FirefoxOptions()
        options.headless = self.headless

        firefox_binary = FirefoxBinary(self.binary_loc)
        firefox_binary.add_command_line_options("-private")

        self.driver = webdriver.Firefox(options=options, firefox_binary=firefox_binary)
        self.driver.get(self.url)

        if self.maximize:
            self.driver.maximize_window()

    def connect_chrome(self) -> None:
        options = webdriver.ChromeOptions()
        options.headless = self.headless

        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.url)

        if self.maximize:
            self.driver.maximize_window()

    def save_screenshot(self, name) -> None:
        if self.save_screenshots:
            self.driver.save_screenshot(name)

    def get_driver(self):
        return self.driver

    def get_url(self):
        return self.url

    def get_binary_loc(self):
        return self.binary_loc

    def close(self) -> None:
        if self.driver != None:
            if not self.headless:
                sleep(10)
            self.driver.quit()

    def wait_invisibility_by_xpath(self, xpath, timeout=10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                ec.invisibility_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception:
            return False

    def wait_visibility_by_xpath(self, xpath, timeout=10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception:
            return False

    def wait_visibility_by_id(self, id, timeout=10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located((By.ID, id))
            )
            return True
        except Exception:
            return False

    def find_element_by_text(
        self,
        tag_name,
        text,
        ui_element=None,
    ) -> None:
        if ui_element == None:
            ui_element = self.active_tab

        for elem in ui_element.find_elements_by_tag_name(tag_name):
            if elem.text == text:
                return elem
        return None

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.execute_script("window.scrollBy(0,-50)")
        sleep(1)
        return element


def validate_browser(browser: str) -> bool:
    global BROWSER_TO_USE
    if browser == "firefox":
        BROWSER_TO_USE = "firefox"
        try:
            options = webdriver.FirefoxOptions()
            options.headless = True
            firefox_binary = FirefoxBinary(
                getenv("FIREFOX_BINARY_LOC", "/usr/bin/" + BROWSER_TO_USE)
            )
            driver = webdriver.Firefox(options=options, firefox_binary=firefox_binary)
            driver.get(getenv("URL"))
            driver.close()
            print("Firefox browser configuration is valid")
            return True
        except Exception as e:
            print(f"Exception: {e}")
            print(CONFIG_ERROR_MSG)
            return False

    elif browser == "chrome":
        BROWSER_TO_USE = "google-chrome"
        try:
            options = webdriver.ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(options=options)
            driver.get(getenv("URL"))
            driver.close()
            print("Chrome browser configuration is valid")
            return True
        except Exception as e:
            print(f"Exception: {e}")
            print(CONFIG_ERROR_MSG)
            return False
    else:
        print(f"Browser {browser} not supported")
