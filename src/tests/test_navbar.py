from test_case import TestCase


class TestMethod(TestCase):
    def __init__(self, **config):
        super().__init__(**config)

    def test_body(self):
        self.evam_driver.navbar_to("User input", 10)
        self.evam_driver.navbar_to("Results", 10)
        self.evam_driver.navbar_to("About EvAM-Tools", 10)
