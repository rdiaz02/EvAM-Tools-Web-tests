from time import sleep
from selenium.webdriver.support.ui import WebDriverWait

class tester:

    def __init__(self, web_driver) -> None:
        self.driver = web_driver

    # Tests punto 2

    # Test 2.1
    def analyzing_BRCA_data_set(self) -> None:
        self.move_to_input()

        # upload button
        self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/label/input')

        self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[1]/label/span', 10)
        # Select the file name box
        file_name = self.driver.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/input')
        file_name.clear()
        file_name.send_keys('BRCA_ba')
        upload_file = self.driver.driver.find_element_by_xpath('//*[@id="csd"]')
        upload_file.send_keys('/home/lorenzo/Documentos/Universidad/TFG/EvAM-Tools-Web-tests/testing_files/BRCA_ba_s.csv')

        self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[4]/div/div/svg[1]/g[2]/g/rect[1]', 10)
        self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/button')
        self.driver.wait_invisibility_by_xpath('/html/body/div[12]/div/div[2]/div[1]/div/div[2]', 100)
        self.driver.find_and_click('//*[@id="download_cpm"]')


    def analyzing_manually_constructed_synthetic_data(self) -> None:
        self.move_to_input()

        self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div[2]/label/input')

        self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/input', 10)
        wt_count = self.driver.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/input')
        wt_count.clear()
        wt_count.send_keys('20')
        self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/button')
        self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[4]/div/div/svg[1]/g[2]', 10)

        self.driver.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/label/input')
        a_count = self.driver.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/input')
        a_count.clear()
        a_count.send_keys('15')
        self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/button')
        self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[4]/div/div/svg[1]/g[2]', 10)

        self.driver.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div/div[2]/label/input')
        self.driver.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div/div[3]/label/input')
        bc_count = self.driver.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/input')
        bc_count.clear()
        bc_count.send_keys('12')
        self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/button')
        self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[4]/div/div/svg[1]/g[2]', 10)

        self.driver.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/label/input')
        self.driver.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div/div[4]/label/input')
        ad_count = self.driver.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/input')
        ad_count.clear()
        ad_count.send_keys('20')
        self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/button')
        self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[4]/div/div/svg[1]/g[2]', 10)

        self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/button', 10)
        self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/button')

    def small_computational_experiments(self) -> None:
        self.move_to_input()

        self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/label/input')

        self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[1]/label/span', 10)
        file_name = self.driver.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/input')
        file_name.clear()
        file_name.send_keys('ov')
        upload_file = self.driver.driver.find_element_by_xpath('//*[@id="csd"]')
        upload_file.send_keys('/home/lorenzo/Documentos/Universidad/TFG/EvAM-Tools-Web-tests/testing_files/ov2.csv')

        file_name = self.driver.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[4]/div/div[2]/input')
        file_name.clear()
        file_name.send_keys('ov2')
        self.driver.find_and_click('//*[@id="save_csd_data"]')

        self.driver.find_and_click('//*[@id="advanced_options"]')
    
        return

    # Tests punto 3

    def analyzing_manually_constructed_data(self) -> None:
        self.move_to_input()

        self.driver.find_and_click('//html/body/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div[2]/label/input')

        genotype_count = self.driver.driver.find_element_by_xpath('//*[@id="genotype_freq"]')
        genotype_count.clear()
        genotype_count.send_keys('20')
        self.driver.find_and_click('//*[@id="add_genotype"]')

        self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/label/input')
        genotype_count = self.driver.driver.find_element_by_xpath('//*[@id="genotype_freq"]')
        genotype_count.clear()
        genotype_count.send_keys('15')
        self.driver.find_and_click('//*[@id="add_genotype"]')
