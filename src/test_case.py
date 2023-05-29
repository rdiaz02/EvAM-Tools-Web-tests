import traceback

from selenium_core.selenium_wrapper import WrappedDriver
from selenium_core.evam_tools_page_controller import EvAMToolsPage


class TestCase:
    def __init__(self, name, headless, maximize, large_log, screenshots):
        self.name = name
        self.headless = headless
        self.maximize = maximize
        self.large_log = large_log
        self.screenshots = screenshots
        self.wrapped_driver = None
        self.page_controller = None

    def test_body(self):
        # Override this method in the test case
        print("Default test body: Override this method in the test case")
        pass

    def run(self):
        self.set_up()

        try:
            method = getattr(self, "test_body")
            method()
        except Exception as e:
            print(f"Error while running test: {e}\n")

            if self.large_log:
                print(traceback.format_exc())

            if self.screenshots:
                self.wrapped_driver.save_screenshot(str(self.name) + "_error.png")

        self.tear_down()

    def set_up(self):
        self.wrapped_driver = WrappedDriver(self.headless, self.maximize)
        self.wrapped_driver.connect()
        self.page_controller = EvAMToolsPage(
            self.wrapped_driver.get_driver(), self.large_log, self.screenshots
        )

    def tear_down(self):
        self.driver.close()
