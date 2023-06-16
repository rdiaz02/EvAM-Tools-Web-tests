from test_case import TestCase
from time import sleep

import os


class TestMethod(TestCase):
    def __init__(self, **config):
        super().__init__(**config)

    def test_body(self):
        self.evam_driver.navbar_to("User input", 10)
        self.evam_driver.select_from_cross_sectional_data("Upload file")

        self.evam_driver.upload_data_set("ov2", os.getenv("DATA_FILES_PATH"))

        self.evam_driver.rename_data("ov2", "ov_500K_s14")

        self.evam_driver.toogle_advanced_options_on()
        self.evam_driver.set_advanced_options("cpm_methods-label", ["H-ESBCN"])
        self.evam_driver.set_advanced_options("HESBCN_seed-label", "14")
        self.evam_driver.set_advanced_options("HESBCN_MCMC_iter-label", "500000")
        self.evam_driver.toogle_advanced_options_off()

        self.evam_driver.run_evamtools()
