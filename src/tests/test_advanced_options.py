from test_case import TestCase


class TestMethod(TestCase):
    def __init__(self, **config):
        super().__init__(**config)

    def test_body(self):
        self.evam_driver.navbar_to("User input", 10)
        self.evam_driver.toogle_advanced_options_on()
        self.evam_driver.set_advanced_options("OncoBN_model-label", "Conjunctive (CBN)")
        self.evam_driver.set_advanced_options("return_paths_max-label", "TRUE")
        self.evam_driver.set_advanced_options("MHN_lambda-label", "9")
        self.evam_driver.toogle_advanced_options_off()
