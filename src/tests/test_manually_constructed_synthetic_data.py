from test_case import TestCase


class TestMethod(TestCase):
    def __init__(self, **config):
        super().__init__(**config)

    def test_body(self):
        self.evam_driver.navbar_to("User input", 10)
        self.evam_driver.select_from_cross_sectional_data(
            "Enter\ngenotype\nfrequencies\nmanually"
        )
        self.evam_driver.add_genotype([], "20")
        self.evam_driver.add_genotype(["A"], "15")
        self.evam_driver.add_genotype(["B", "C"], "12")
        self.evam_driver.add_genotype(["A", "D"], "20")

        self.evam_driver.rename_data("Empty", "Aliassed_1")

        self.evam_driver.run_evamtools()
