import traceback

from selenium_core.selenium_wrapper import WrappedDriver
from selenium_core.evam_tools_page_controller import EvAMToolsPage


class TestCase:
    def __init__(self, name, headless, maximize, large_log, screenshots):
        """
        Initializes a new instance of the TestCase class with the specified options.

        Args:
            name (str): The name of the test case.
            headless (bool): Whether to run the test in headless mode.
            maximize (bool): Whether to maximize the browser window.
            large_log (bool): Whether to enable large logging.
            screenshots (bool): Whether to take screenshots on errors.

        More arguments must be added to the constructor if they are needed in the test case.
        """
        self.name = name
        self.headless = headless
        self.maximize = maximize
        self.large_log = large_log
        self.screenshots = screenshots
        self.wrapped_driver = None
        self.page_controller = None

    def test_body(self) -> None:
        """
        Override this method in the test case.
        """
        # This is a default implementation of the test body that does nothing.
        # It should be overridden in the actual test case with the test steps.
        print("Default test body: Override this method in the test case")
        pass

    def run(self) -> None:
        """
        Runs the test case.
        """
        # Call the set_up method to prepare the test environment
        self.set_up()

        try:
            # Get the test_body method and call it
            method = getattr(self, "test_body")
            method()
        except Exception as e:
            # If an exception is raised, print the error message
            print(f"Error while running test: {e}\n")

            # If the large_log attribute is True, print the traceback
            if self.large_log:
                print(traceback.format_exc())

            # If the screenshots attribute is True, save a screenshot of the error
            if self.screenshots:
                self.wrapped_driver.save_screenshot(str(self.name) + "_error.png")

        # Call the tear_down method to clean up the test environment
        self.tear_down()

    def set_up(self) -> None:
        """
        Prepares the test environment.
        """
        # Create a WrappedDriver instance with the specified headless and maximize options
        self.wrapped_driver = WrappedDriver(self.headless, self.maximize)

        # Connect to the driver instance
        self.wrapped_driver.connect()

        # Create an EvAMToolsPage instance with the driver instance and specified options
        self.page_controller = EvAMToolsPage(
            self.wrapped_driver.get_driver(), self.large_log, self.screenshots
        )

    def tear_down(self) -> None:
        """
        Cleans up the test environment.
        """
        self.driver.close()
