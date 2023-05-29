from test_case import TestCase
from selenium.webdriver.common.by import By

"""
    Ejemplo 2: Métodos para localización básica.

    - Cargar la url.
    - Localizar un elemento por id.
    - Localizar un elemento por name.
    - Localizar un elemento por xpath.
    - Localizar un elemento por css selector.
    - Localizar un elemento por class name.
    - Localizar un elemento por tag name.
    - Localizar un elemento por link text.
    - Localizar un elemento por partial link text.
"""


class TestMethod(TestCase):
    def __init__(self, headless, maximize, large_log, screenshots):
        super().__init__(headless, maximize, large_log, screenshots)

    def test_body(self):
        print("Testing locators")
        driver = self.page_controller.driver

        element_by_id = driver.find_element_by_id("background")
        element_by_id_2 = driver.find_element(By.ID, "background")

        assert element_by_id == element_by_id_2

        element_by_name = driver.find_element_by_name("input2build")
        element_by_name_2 = driver.find_element(By.NAME, "input2build")

        assert element_by_name == element_by_name_2

        element_by_xpath = driver.find_element_by_xpath("/html/body/nav/div/ul/li[1]/a")
        element_by_xpath_2 = driver.find_element(
            By.XPATH, "/html/body/nav/div/ul/li[1]/a"
        )

        assert element_by_xpath == element_by_xpath_2

        element_by_css_selector = driver.find_element_by_css_selector("h3")
        element_by_css_selector_2 = driver.find_element(By.CSS_SELECTOR, "h3")

        assert element_by_css_selector == element_by_css_selector_2

        element_by_class_name = driver.find_element_by_class_name("container-fluid")
        element_by_class_name_2 = driver.find_element(By.CLASS_NAME, "container-fluid")

        assert element_by_class_name == element_by_class_name_2

        element_by_tag_name = driver.find_element_by_tag_name("input")
        element_by_tag_name_2 = driver.find_element(By.TAG_NAME, "input")

        assert element_by_tag_name == element_by_tag_name_2
