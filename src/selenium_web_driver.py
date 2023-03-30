from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from dotenv import load_dotenv
from pathlib import Path

import os
import time

# Geckodriver moved to /usr/bin/
dotenv_path = Path('path/to/.env')
load_dotenv(dotenv_path=dotenv_path)

class selenium_driver():
    driver = None
    actual_tab = None
    url = os.getenv('EVAM_URL')

    def connect(self) -> None:

        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True

        options = webdriver.FirefoxOptions()
        options.binary = os.getenv('BINARY_LOC')
        # options.headless = True
        firefox_binary=FirefoxBinary(os.getenv('BINARY_LOC'))
        firefox_binary.add_command_line_options("-private")

        self.driver = webdriver.Firefox(firefox_profile=profile, options=options, firefox_binary=firefox_binary)
        self.driver.get(self.url)

    # Miscelaneous functions

    def close(self) -> None:
        if self.driver != None:
            self.driver.close()

    def wait_invisibility_by_xpath(self, xpath, timeout) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                ec.invisibility_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception:
            return False

    def wait_visibility_by_xpath(self, xpath, timeout) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception:
            return False

    def find_and_click(self, xpath, timeout=10) -> None:
        if self.wait_visibility_by_xpath(xpath, timeout):
            elem = self.driver.find_element_by_xpath(xpath)
            elem.click()
        else:
            print('Element not found')

    # test oriented functions

    def test_navbar_load_page(self) -> None:
        self.navbar = self.driver.find_element_by_id('navbar')
        self.session_id = self.navbar.get_attribute('data-tabsetid')

        for idx, tab in enumerate(self.navbar.find_elements_by_tag_name('li')):
            nav_bar_button = tab.find_element_by_tag_name('a')
            if nav_bar_button.get_attribute('href') == f"{self.url}#tab-{self.session_id}-{str(idx+1)}":
                nav_bar_button.click()

    def navbar_to(self, tab_name, timeout) -> None:
        start = time.time()
        for tab in self.navbar.find_elements_by_tag_name('li'):
            if tab.find_element_by_tag_name('a').text == tab_name:
                while tab.get_attribute('class') != 'active':
                    tab.click()
                    end = time.time()
                    if end - start > timeout:
                        return 'Failed'
                break
        self.actual_tab = tab_name
        return 'Success'

    def loading_content(self) -> None:
        page_content = self.driver.find_element_by_class_name('container-fluid')
        for elem in page_content:
            try:
                content = elem.find_element_by_class_name('tab-content')
            except Exception as e:
                print(e)

        print('Loading finished')