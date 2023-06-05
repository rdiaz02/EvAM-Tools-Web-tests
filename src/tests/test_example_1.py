from test_case import TestCase


class TestMethod(TestCase):
    def __init__(self, headless, maximize, large_log, screenshots):
        super().__init__(headless, maximize, large_log, screenshots)

    def test_body(self):
        """
        Tests the methods for obtaining basic web page data.

        Returns:
            None
        """
        print("Testing current url")
        driver = self.page_controller.driver

        # Print the current URL, title, and page source
        print(driver.current_url)
        print(driver.title)
        print(driver.page_source)
