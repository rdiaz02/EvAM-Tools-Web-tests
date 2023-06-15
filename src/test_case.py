import traceback

from selenium_core.evam_tools_page_controller import EvAMToolsDriver


class TestCase:
    def __init__(self, **config):
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
        self.name = config.get("name", "Test")
        self.large_log = config.get("large_log", False)
        self.set_up_config = config
        self.evam_driver = None

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

        self.set_up()

        try:
            method = getattr(self, "test_body")
            method()
        except Exception as e:
            print(f"Error while running test: {e}\n")
            self.evam_driver.save_screenshot(
                "./screenshots/" + str(self.name) + "_error.png"
            )

            if self.large_log:
                print(traceback.format_exc())

        self.tear_down()

    def set_up(self) -> None:
        """
        Prepares the test environment.
        """
        self.evam_driver = EvAMToolsDriver(**self.set_up_config)

    def tear_down(self) -> None:
        """
        Cleans up the test environment.
        """
        self.evam_driver.close()
