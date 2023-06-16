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
        self.evam_driver.define_DAG_model("OncoBN")
        self.evam_driver.define_DAG_table(
            [["Single", "0.5"], ["Single", "0.7"], ["Single", "0.9"], ["Single", "0.3"]]
        )
        sleep(0.5)
        self.evam_driver.define_DAG_num_genotypes(10000)
        self.evam_driver.generate_data_from_DAG()

        self.evam_driver.define_DAG_epos("0.15")
        self.evam_driver.generate_data_from_DAG()
