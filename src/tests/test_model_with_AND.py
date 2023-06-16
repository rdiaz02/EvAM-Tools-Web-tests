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
        self.evam_driver.define_DAG_new_edge("Root", "B", "remove")
        self.evam_driver.define_DAG_new_edge("A", "B", "add")
        self.evam_driver.define_DAG_new_edge("B", "D", "add")
        self.evam_driver.define_DAG_new_edge("C", "D", "add")
        sleep(1)
        self.evam_driver.define_DAG_table(
            [
                ["Single", "0.7"],
                ["Single", "0.6"],
                ["Single", "0.8"],
                ["Single", "0.9"],
                ["Single", "0.9"],
            ]
        )
        self.evam_driver.define_DAG_num_genotypes(1000)
        self.evam_driver.define_DAG_observational_noise("0.05")
        self.evam_driver.generate_data_from_DAG()

        self.evam_driver.run_evamtools()
        sleep(2)

        self.evam_driver.navbar_to("User input", 10)

        self.evam_driver.toogle_advanced_options_on()
        self.evam_driver.set_advanced_options("OncoBN_model-label", "Conjunctive (CBN)")
        self.evam_driver.toogle_advanced_options_off()

        self.evam_driver.run_evamtools()
        sleep(2)
