from test_case import TestCase


class TestMethod(TestCase):
    def __init__(self, **config):
        super().__init__(**config)

    def test_body(self):
        """
        Tests the methods for obtaining basic web page data.

        Returns:
            None
        """
        print("Testing current url")
        driver = self.evam_driver.driver

        print(driver.current_url)
        print(driver.title)
        print(driver.page_source)
