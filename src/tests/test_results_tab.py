from test_case import TestCase


class TestMethod(TestCase):
    def __init__(self, **config):
        super().__init__(**config)

    def test_body(self):
        self.evam_driver.navbar_to("Results", 10)
        self.evam_driver.CPMs_to_show(["CBN", "OncoBN"])
        self.evam_driver.predictions_from_fitted_models("Transition rates")
        self.evam_driver.type_of_label("Last gene mutated")
        self.evam_driver.type_of_label("Genotype")
        self.evam_driver.relevant_paths_to_show(1)
        self.evam_driver.relevant_paths_to_show(10)
        self.evam_driver.relevant_paths_to_show(11)
