from test_case import TestCase
from time import sleep

import os


class TestMethod(TestCase):
    def __init__(self, **config):
        super().__init__(**config)

    def test_body(self):
        self.evam_driver.navbar_to("User input", 10)
        self.evam_driver.select_from_cross_sectional_data("Upload file")

        self.evam_driver.upload_data_set("BRCA_ba_s", os.getenv("DATA_FILES_PATH"))

        self.evam_driver.toogle_advanced_options_on()
        self.evam_driver.set_advanced_options(
            "CPMs to use", ["CBN", "OT", "OncoBN", "MHN", "H-ESBCN"]
        )
        self.evam_driver.set_advanced_options("Number of MCMC iterations:", "500000")
        self.evam_driver.toogle_advanced_options_off()

        # Boton de analisis
        self.evam_driver.run_evamtools()

        # Descarga de los resultados
        self.evam_driver.navbar_to("Results", 10)
        self.evam_driver.CPMs_to_show(["CBN", "OT", "OncoBN"])
        sleep(10)
        self.evam_driver.CPMs_to_show(["MHN", "H-ESBCN"])
        sleep(10)

        # self.evam_driver.driver.find_element_by_xpath('//*[@id="download_cpm"]').click()
