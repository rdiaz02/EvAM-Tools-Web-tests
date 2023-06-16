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
        self.evam_driver.set_number_of_genes(5)
        self.evam_driver.define_DAG_model("CBN/H-ESBCN")
        self.evam_driver.define_DAG_new_edge("A", "D", "add")
        self.evam_driver.define_DAG_new_edge("B", "C", "add")
        self.evam_driver.define_DAG_new_edge("A", "E", "add")
        self.evam_driver.define_DAG_new_edge("F", "E", "add")
        sleep(1)
        self.evam_driver.define_DAG_table(
            [
                ["Single", "3.2"],
                ["Single", "1.5"],
                ["Single", "0.9"],
                ["Single", "0.9"],
                ["Single", "2"],
                ["Single", "2"],
                ["Single", "1"],
                ["Single", "1"],
            ]
        )
        self.evam_driver.define_DAG_num_genotypes(1000)
        self.evam_driver.define_DAG_observational_noise("0.01")
        self.evam_driver.generate_data_from_DAG()

        self.evam_driver.run_evamtools()
