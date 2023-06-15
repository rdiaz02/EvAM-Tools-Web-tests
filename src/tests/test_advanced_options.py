from test_case import TestCase


class TestMethod(TestCase):
    def __init__(self, **config):
        super().__init__(**config)

    def test_body(self):
        self.evam_driver.navbar_to("User input", 10)
        self.evam_driver.toogle_advanced_options_on()
        self.evam_driver.set_advanced_options("Return paths to maximum(a)", "TRUE")
        self.evam_driver.set_advanced_options("Lambda:", "9")
        self.evam_driver.toogle_advanced_options_off()
