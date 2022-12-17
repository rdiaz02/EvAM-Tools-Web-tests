from time import sleep

class tester:

    def __init__(self, web_driver) -> None:
        self.driver = web_driver

    def move_to_input(self):
        if self.driver.wait_visibility_by_xpath('/html/body/nav/div/ul/li[2]/a', 10):
            self.driver.find_and_click('/html/body/nav/div/ul/li[2]/a')

    def analyzing_BRCA_data_set(self) -> None:
        self.move_to_input()

        if self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/label/input', 10):
            self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/label/input')

        sleep(5)
        self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[1]/label/span', 10)
        file_name = self.driver.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/input')
        file_name.clear()
        file_name.send_keys('BRCA_ba')
        upload_file = self.driver.driver.find_element_by_xpath('//*[@id="csd"]')
        upload_file.send_keys('/home/lorenzo/Documentos/Universidad/TFG/EvAM-Tools-Web-tests/testing_files/BRCA_ba_s.csv')
        sleep(5)

        if self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div[2]/label/input', 10):
            self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div[2]/label/input')
        sleep(5)
        if self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/label/input', 10):
            self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/label/input')

        self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/button', 10)
        self.driver.find_and_click('/html/body/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/button')


    def analyzing_manually_constructed_synthetic_data(self):
        self.move_to_input()

        if self.driver.wait_visibility_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div[2]/label/input', 10):
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