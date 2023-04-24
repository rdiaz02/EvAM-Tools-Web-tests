import time
from time import time, sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

class EvAMToolsPage():

    def __init__(self, driver):
        """
            principales elementos presentes en todos los tabs
            driver: webdriver
            navbar: elemento que contiene los tabs
            session_id: id de la sesion presente en varios ids de los elementos
        """
        self.driver = driver
        self.navbar = self.driver.find_element_by_id('navbar')
        self.session_id = self.navbar.get_attribute('data-tabsetid')
        self.tabs_content = self.driver.find_elements_by_xpath("//div[@class='tab-content']/div")
        self.active_tab = None

    # General function for navigating through tabs

    def navbar_to(self, tab_name, timeout) -> None:
        start = time()
        for tab in self.navbar.find_elements_by_tag_name('li'):
            if tab.find_element_by_tag_name('a').text == tab_name:
                while tab.get_attribute('class') != 'active':
                    tab.click()
                    end = time()
                    if end - start > timeout:
                        return 'Failed'

                for tab_content in self.tabs_content:
                    if tab_content.get_attribute('class') == 'tab-pane active':
                        self.active_tab = tab_content
                        break

                sleep(5)
                start_load = time()
                self.load_content()
                end_load = time()
                print('Loading time: ' + str(end_load - start_load))
                break

        return 'Success'


    def load_content(self, div=None) -> None:
        # Mhe no me convence
        if div == None:
            div = self.active_tab
        for elem in div.find_elements_by_xpath('./*'):
            self.wait_visibility_by_xpath(elem, 10)
            if elem.tag_name == 'div':
                self.load_content(elem)

    # Misc functions

    def wait_invisibility_by_xpath(self, xpath, timeout=10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                ec.invisibility_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception:
            return False


    def wait_visibility_by_xpath(self, xpath, timeout=10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception:
            return False


    def scroll_into_view(self, element):
        clickable = False
        while clickable == False:
            self.driver.execute_script("window.scrollBy(0,200)")
            try:
                element.click()
                clickable = True
            except WebDriverException:
                pass


    def select_from_checklist(self, ui_element, check: list) -> None:

        self.scroll_into_view(ui_element)
        for option in ui_element.find_elements_by_xpath('./div'):
            option_element = option.find_element_by_xpath('./label')
            if option_element.text in check and option_element.find_element_by_xpath('./input').is_selected() == False:
                option_element.find_element_by_xpath('./input').click()
            elif option_element.text not in check and option_element.find_element_by_xpath('./input').is_selected() == True:
                option_element.find_element_by_xpath('./input').click()


    def select_from_dropdown(self, ui_element, option) -> None:

        self.scroll_into_view(ui_element)
        ui_element.find_element_by_class_name('selectize-input').click()
        options = ui_element.find_elements_by_class_name('option')
        for opt in options:
            if opt.text == option:
                opt.click()
                break


    def select_from_sliderbar(self, ui_element, value) -> None:

        slider_min_value = int(ui_element.find_element_by_class_name('irs-min').text)
        slider_max_value = int(ui_element.find_element_by_class_name('irs-max').text)

        if value < slider_min_value or value > slider_max_value:
            raise ValueError(f'Value must be between {slider_min_value} and {slider_max_value}')

        slider_value = int(ui_element.find_element_by_class_name('irs-single').get_attribute('textContent'))

        slider = ui_element.find_element_by_class_name('irs-handle')

        direction = Keys.ARROW_RIGHT if value > int(slider_value) else Keys.ARROW_LEFT
        while slider_value != value:
            ActionChains(self.driver).click_and_hold(slider).send_keys(direction).release().perform()
            slider_value = int(ui_element.find_element_by_class_name('irs-single').get_attribute('textContent'))


    # User input tab functions

    # # Left column buttons
    # Ejemplos de tag_name:
    #   'Upload file', 'Enter\ngenotype\nfrequencies\nmanually'
    #   'DAG and\nrates/cond.\nprobs.'
    #   'MHN\nlog-Θ\nmatrix'
    # Los saltos de linea tienen que quedar reflejados
    def click_cross_sectional_data(self, tag_name: str) -> None:
        cross_sectional_button = self.active_tab.find_element_by_text(tag_name)
        cross_sectional_button.click()
        self.load_content()

    def upload_data_set(self, name, file_path: str) -> None:
        file_name = self.driver.find_element_by_id('name_uploaded')
        file_name.clear()
        file_name.send_keys(name)

        upload_file = self.driver.find_element_by_xpath('//*[@id="csd"]')
        upload_file.send_keys(file_path)
        self.driver.implicitly_wait(0.5)
        self.load_content()

    def run_evamtools(self, timeout=10) -> None:
        self.active_tab.find_element_by_xpath('//*[@id="analysis"]').click()
        self.active_tab.wait_visibility_by_xpath('/html/body/div[12]/div/div[2]/div[1]/div/div[2]', 100)
        self.active_tab.wait_invisibility_by_xpath('/html/body/div[12]/div/div[2]/div[1]/div/div[2]', 100)

    def toogle_advanced_options(self) -> None:
        self.active_tab.find_element_by_xpath('//*[@id="advanced_options"]').click()
        self.wait_visibility_by_xpath('//*[@id="all_advanced_options"]')

    def set_advanced_options(self, option_name, option_value, timeout=10) -> None:
        advanced_options = self.active_tab.find_element_by_id('all_advanced_options')
        for option in advanced_options.find_elements_by_xpath('./div/div'):
            if option.find_element_by_xpath('./label').text != option_name:
                continue

            if option.find_element_by_xpath('./div'):
                if option.find_element_by_xpath('./div').get_attribute('class') == 'shiny-options-group':
                    self.select_from_checklist(option.find_element_by_xpath('./div'), option_value)
                else:
                    self.select_from_dropdown(option.find_element_by_xpath('./div'), option_value)
            elif option.find_element_by_xpath('./input'):
                option.find_element_by_xpath('./input').send_keys(option_value)

    # Results tab functions

    def CPMs_to_show(self, check: list) -> None:
        cpm_options = self.driver.find_element_by_xpath('//*[@id="cpm2show"]/div')
        self.select_from_checklist(cpm_options, check)

    def predictions_from_fitted_models(self, option) -> None:
        predicctions = self.driver.find_element_by_xpath('//*[@id="data2plot"]')
        predicctions.find_element_by_xpath(f"//*[text()='{option}']").click()

    def type_of_label(self, option) -> None:
        labels = self.driver.find_element_by_xpath('//*[@id="label2plot"]')
        labels.find_element_by_xpath(f"//*[text()='{option}']").click()

    def relevant_paths_to_show(self, value) -> None:
        slider_box = self.active_tab.find_element_by_class_name('irs--shiny')
        self.scroll_into_view(slider_box)
        self.select_from_sliderbar(slider_box, value)