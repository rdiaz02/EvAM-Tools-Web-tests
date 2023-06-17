from test_case import TestCase
from time import sleep


class TestMethod(TestCase):
    def __init__(self, **config):
        super().__init__(**config)

    def test_body(self):
        self.evam_driver.navbar_to("User input", 10)
        self.evam_driver.select_from_cross_sectional_data(
            "DAG and\nrates/cond.\nprobs."
        )
        self.evam_driver.set_number_of_genes(4)
        self.evam_driver.define_DAG_model("CBN/H-ESBCN")
        self.evam_driver.define_DAG_table(
            [
                ["Single", "2"],
                ["Single", "2.5"],
                ["Single", "1"],
                ["Single", "1.5"],
            ]
        )
        sleep(1)
        self.evam_driver.define_DAG_observational_noise("0.01")
        self.evam_driver.define_DAG_num_genotypes(5000)
        self.evam_driver.generate_data_from_DAG()

        self.evam_driver.toogle_advanced_options_on()
        self.evam_driver.set_advanced_options(
            "cpm_methods-label", ["CBN", "OT", "OncoBN", "MHN", "H-ESBCN"]
        )
        self.evam_driver.toogle_advanced_options_off()

        self.evam_driver.run_evamtools()
        sleep(2)
