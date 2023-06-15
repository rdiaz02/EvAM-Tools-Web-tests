from test_case import TestCase


class TestMethod(TestCase):
    def __init__(self, **config):
        super().__init__(**config)

    def test_body(self):
        self.evam_driver.navbar_to("User input", 10)
        self.evam_driver.select_from_cross_sectional_data("Upload file")
        self.evam_driver.select_from_cross_sectional_data(
            "Enter\ngenotype\nfrequencies\nmanually"
        )
        self.evam_driver.select_from_cross_sectional_data(
            "DAG and\nrates/cond.\nprobs."
        )
        self.evam_driver.select_from_cross_sectional_data("MHN\nlog-Θ\nmatrix")
