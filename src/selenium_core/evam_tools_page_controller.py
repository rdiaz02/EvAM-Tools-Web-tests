from time import time, sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
    InvalidElementStateException,
)


class EvAMToolsPage:
    def __init__(self, driver, large_log=False, screenshots=False):
        """
        principales elementos presentes en todos los tabs
        driver: webdriver
        navbar: elemento que contiene los tabs
        session_id: id de la sesion presente en varios ids de los elementos
        """
        self.driver = driver
        self.large_log = large_log
        self.screenshots = screenshots
        self.navbar = self.driver.find_element_by_id("navbar")
        self.session_id = self.navbar.get_attribute("data-tabsetid")
        self.tabs_content = self.driver.find_elements_by_xpath(
            "//div[@class='tab-content']/div"
        )
        self.active_tab = None

    # General function for navigating through tabs

    def navbar_to(self, tab_name, timeout) -> None:
        start = time()
        for tab in self.navbar.find_elements_by_tag_name("li"):
            if tab.find_element_by_tag_name("a").text == tab_name:
                while tab.get_attribute("class") != "active":
                    tab.click()
                    end = time()
                    if end - start > timeout:
                        return "Failed"

                for tab_content in self.tabs_content:
                    if tab_content.get_attribute("class") == "tab-pane active":
                        self.active_tab = tab_content
                        break

                sleep(5)
                self.load_content()
                break

        return "Success"

    def load_content(self, div=None) -> None:
        if div == None:
            div = self.active_tab
        for elem in div.find_elements_by_xpath("./*"):
            self.wait_visibility_by_xpath(elem, 10)
            if elem.tag_name == "div":
                self.load_content(elem)

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

    def find_element_by_text(
        self,
        tag_name,
        text,
        ui_element=None,
    ) -> None:
        if ui_element == None:
            ui_element = self.active_tab

        for elem in ui_element.find_elements_by_tag_name(tag_name):
            if elem.text == text:
                return elem
        return None

    def scroll_into_view(self, element):
        clickable = False
        while clickable == False:
            self.driver.execute_script("window.scrollBy(0,300)")
            try:
                element.click()
                clickable = True
            except WebDriverException:
                pass

    def select_from_checklist(self, ui_element, check: list) -> None:
        self.scroll_into_view(ui_element)
        for option in ui_element.find_elements_by_xpath("./div"):
            option_element = option.find_element_by_xpath("./label")
            if (
                option_element.text in check
                and option_element.find_element_by_xpath("./input").is_selected()
                == False
            ):
                option_element.find_element_by_xpath("./input").click()
            elif (
                option_element.text not in check
                and option_element.find_element_by_xpath("./input").is_selected()
                == True
            ):
                option_element.find_element_by_xpath("./input").click()

    def select_from_dropdown(self, ui_element, option) -> None:
        self.scroll_into_view(ui_element)
        ui_element.find_element_by_class_name("selectize-input").click()
        options = ui_element.find_elements_by_class_name("option")
        for opt in options:
            if opt.text == option:
                opt.click()
                break

    def select_from_sliderbar(self, ui_element, value) -> None:
        self.scroll_into_view(ui_element)
        slider_min_value = int(ui_element.find_element_by_class_name("irs-min").text)
        slider_max_value = int(ui_element.find_element_by_class_name("irs-max").text)

        if value < slider_min_value or value > slider_max_value:
            raise ValueError(
                f"Value must be between {slider_min_value} and {slider_max_value}"
            )

        slider_value = int(
            ui_element.find_element_by_class_name("irs-single").get_attribute(
                "textContent"
            )
        )

        slider = ui_element.find_element_by_class_name("irs-handle")

        direction = Keys.ARROW_RIGHT if value > int(slider_value) else Keys.ARROW_LEFT
        while slider_value != value:
            ActionChains(self.driver).click_and_hold(slider).send_keys(
                direction
            ).release().perform()
            slider_value = int(
                ui_element.find_element_by_class_name("irs-single").get_attribute(
                    "textContent"
                )
            )

    def select_from_bullet_list(self, ui_element, option) -> None:
        self.scroll_into_view(ui_element)
        for option in ui_element.find_elements_by_xpath("./label"):
            option_element = option.find_element_by_xpath("./span")
            if option_element.text == option:
                option.find_element_by_xpath("./input").click()
                break

    def select_from_cross_sectional_data(self, tag_name: str) -> None:
        cross_sectional_section = self.active_tab.find_element_by_xpath(
            f'//*[@id="tab-{self.session_id}-2"]/div/div/div/div[1]'
        )
        cross_sectional_button = self.find_element_by_text(
            "span", tag_name, cross_sectional_section
        )
        cross_sectional_button.click()
        self.load_content()

    def run_evamtools(self, timeout=60) -> None:
        self.active_tab.find_element_by_xpath('//*[@id="analysis"]').click()
        self.wait_visibility_by_xpath(
            "/html/body/div[12]/div/div[2]/div[1]/div/div[2]", timeout
        )
        self.wait_invisibility_by_xpath(
            "/html/body/div[12]/div/div[2]/div[1]/div/div[2]", timeout
        )

    def toogle_advanced_options_on(self) -> None:
        advanced_options = self.active_tab.find_element_by_xpath(
            '//*[@id="advanced_options"]'
        )
        self.scroll_into_view(advanced_options)
        if not self.active_tab.find_element_by_xpath(
            '//*[@id="all_advanced_options"]'
        ).is_displayed():
            self.active_tab.find_element_by_xpath('//*[@id="advanced_options"]').click()
            self.wait_visibility_by_xpath('//*[@id="all_advanced_options"]')

    def toogle_advanced_options_off(self) -> None:
        advanced_options = self.active_tab.find_element_by_xpath(
            '//*[@id="advanced_options"]'
        )
        self.scroll_into_view(advanced_options)
        if self.wait_visibility_by_xpath('//*[@id="all_advanced_options"]', 1):
            advanced_options.click()

    def set_advanced_options(self, option_name, option_value, timeout=10) -> None:
        advanced_options = self.active_tab.find_element_by_id("all_advanced_options")
        for option in advanced_options.find_elements_by_xpath("./div/div"):
            if option.find_element_by_xpath("./label").text != option_name:
                continue

            try:
                option.find_element_by_xpath("./div")
                type = "div"
            except NoSuchElementException:
                type = "input"

            if type == "div":
                if (
                    option.find_element_by_xpath("./div").get_attribute("class")
                    == "shiny-options-group"
                ):
                    self.select_from_checklist(
                        option.find_element_by_xpath("./div"), option_value
                    )
                else:
                    self.select_from_dropdown(
                        option.find_element_by_xpath("./div"), option_value
                    )
            elif type == "input":
                option.find_element_by_xpath("./input").clear()
                option.find_element_by_xpath("./input").send_keys(option_value)

    def change_genotypes_count(self, index=[], counts=[]) -> None:
        if len(index) != len(counts):
            raise ValueError("Index, counts must have the same length")

        genotype_table = self.active_tab.find_element_by_id(
            "change_counts"
        ).find_element_by_tag_name("table")
        self.scroll_into_view(genotype_table)

        for idx, row in enumerate(genotype_table.find_elements_by_xpath("./tbody/tr")):
            if int(row.find_element_by_xpath("./td[1]").text) == index[idx]:
                ActionChains(self.driver).double_click(
                    row.find_element_by_xpath("./td[3]")
                ).perform()
                row.find_element_by_xpath("./td[3]/input").clear()
                row.find_element_by_xpath("./td[3]/input").send_keys(counts[idx])
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(
            Keys.CONTROL
        ).perform()
        sleep(1)

    def rename_data(self, data_to_rename, rename) -> None:
        self.scroll_into_view(self.active_tab.find_element_by_id("select_csd"))
        self.select_from_cross_sectional_data(data_to_rename)

        rename_frame = self.scroll_into_view(
            self.active_tab.find_element_by_id("dataset_name")
        )
        rename_frame.find_element_by_tag_name("input").clear()
        rename_frame.find_element_by_tag_name("input").send_keys(rename)

    ## Upload file params
    def upload_data_set(self, name, file_path: str) -> None:
        file_name = self.driver.find_element_by_id("name_uploaded")
        file_name.clear()
        file_name.send_keys(name)

        upload_file = self.driver.find_element_by_xpath('//*[@id="csd"]')
        upload_file.send_keys(file_path)
        self.driver.implicitly_wait(0.5)
        self.load_content()

    ## Manually genotype frequencies
    def set_number_of_genes(self, number_of_genes: int) -> None:
        number_of_genes_frame = self.active_tab.find_element_by_id("gene_number_slider")
        self.select_from_sliderbar(
            number_of_genes_frame.find_element_by_tag_name("span"), number_of_genes
        )

    def add_genotype(self, mutations: list, count: int) -> None:
        add_genotype_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(add_genotype_frame)

        self.select_from_checklist(
            add_genotype_frame.find_element_by_class_name("shiny-options-group"),
            mutations,
        )
        add_genotype_frame.find_element_by_id("genotype_freq").clear()
        add_genotype_frame.find_element_by_id("genotype_freq").send_keys(count)
        sleep(1)
        add_genotype_frame.find_element_by_tag_name("button").click()

    ## DAG
    def define_DAG(self, model, parent_node, child_mode, action) -> None:
        DAG_Frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(DAG_Frame)

        dag_model = DAG_Frame.find_element_by_id("dag_model")
        self.select_from_bullet_list(dag_model, model)

        dag_parent_node = DAG_Frame.find_element_by_id("dag_from")
        self.select_from_bullet_list(dag_parent_node, parent_node)

        dag_child_node = DAG_Frame.find_element_by_id("dag_to")
        self.select_from_bullet_list(dag_child_node, child_mode)

        if action == "add":
            DAG_Frame.find_element_by_id("add_edge").click()
        elif action == "remove":
            DAG_Frame.find_element_by_id("remove_edge").click()

    def define_DAG_table(self, from_to, relation, lambdas) -> None:
        if len(from_to) != len(relation) != len(lambdas):
            raise ValueError("from_to, relation, lambdas must have the same length")

        DAG_table = self.active_tab.find_element_by_id(
            "dag_table"
        ).find_element_by_tag_name("table")
        self.scroll_into_view(DAG_table)

        for idx, row in enumerate(DAG_table.find_elements_by_xpath("./tbody/tr")):
            if (
                row.find_element_by_xpath("./td[1]").text,
                row.find_element_by_xpath("./td[2]").text,
            ) == from_to[idx]:
                ActionChains(self.driver).double_click(
                    row.find_element_by_xpath("./td[3]")
                ).perform()
                row.find_element_by_xpath("./td[3]/input").clear()
                row.find_element_by_xpath("./td[3]/input").send_keys(relation[idx])
                row.find_element_by_xpath("./td[4]/input").clear()
                row.find_element_by_xpath("./td[4]/input").send_keys(lambdas[idx])
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(
            Keys.CONTROL
        ).perform()
        sleep(1)

    def generate_data_from_DAG_model(
        self, epos, num_genotypes, observation_noise
    ) -> None:
        DAG_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(DAG_frame)

        DAG_frame.find_element_by_id("epos").clear()
        DAG_frame.find_element_by_id("epos").send_keys(epos)

        DAG_frame.find_element_by_id("dag_num_samples").clear()
        DAG_frame.find_element_by_id("dag_num_samples").send_keys(num_genotypes)

        DAG_frame.find_element_by_id("dag_obs_noise").clear()
        DAG_frame.find_element_by_id("dag_obs_noise").send_keys(observation_noise)

    def define_MHN(self, values) -> None:
        tethas_table = self.active_tab.find_element_by_id(
            "thetas_table"
        ).find_element_by_tag_name("table")
        self.scroll_into_view(tethas_table)

        for idx, row in enumerate(tethas_table.find_elements_by_xpath("./tbody/tr")):
            ActionChains(self.driver).double_click(
                row.find_element_by_xpath("./td")
            ).perform()
            for idx_2, col in enumerate(row.find_elements_by_xpath("./td")):
                try:
                    col.find_element_by_tag_name("input").clear()
                    col.find_element_by_tag_name("input").send_keys(
                        values[idx][idx_2 - 1]
                    )
                except InvalidElementStateException:
                    continue

        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(
            Keys.CONTROL
        ).perform()
        sleep(1)

    def generate_data_from_MHN_model(self, num_genotypes, observation_noise) -> None:
        MHN_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(MHN_frame)

        MHN_frame.find_element_by_id("mhn_num_samples").clear()
        MHN_frame.find_element_by_id("mhn_num_samples").send_keys(num_genotypes)

        MHN_frame.find_element_by_id("mhn_obs_noise").clear()
        MHN_frame.find_element_by_id("mhn_obs_noise").send_keys(observation_noise)

        MHN_frame.find_element_by_id("resample_mhn").click()

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
        slider_box = self.active_tab.find_element_by_class_name("irs--shiny")
        self.scroll_into_view(slider_box)
        self.select_from_sliderbar(slider_box, value)

    def download_results(self) -> None:
        self.page_controller.xpath_click('//*[@id="download_cpm"]')
