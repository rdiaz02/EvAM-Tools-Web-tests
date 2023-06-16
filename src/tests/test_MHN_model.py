from test_case import TestCase


class TestMethod(TestCase):
    def __init__(self, **config):
        super().__init__(**config)

    def test_body(self):
        self.evam_driver.navbar_to("User input", 10)
        self.evam_driver.select_from_cross_sectional_data("MHN\nlog-Θ\nmatrix")

        self.evam_driver.set_number_of_genes(3)
        self.evam_driver.define_MHN_number_of_genotypes(1000)
        self.evam_driver.generate_data_from_MHN()
        self.evam_driver.define_MHN([[0, 0, 0], [0, 3, 0], [0, 0, 0]])
        self.evam_driver.generate_data_from_MHN()
        self.evam_driver.define_MHN([[0, 0, 0], [0, 3, 4], [0, 0, 0]])
        self.evam_driver.generate_data_from_MHN()
        self.evam_driver.define_MHN([[0, 0, 0], [-2, 3, 4], [0, 0, 0]])
        self.evam_driver.generate_data_from_MHN()
