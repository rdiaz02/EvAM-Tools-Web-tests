from time import time, sleep

from selenium_core.selenium_wrapper import WrappedDriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
    InvalidElementStateException,
)


class EvAMToolsDriver(WrappedDriver):
    def __init__(self, **config):
        """
        Initializes a new instance of the PageController class with the specified options.

        Args:
            driver (webdriver): The WebDriver instance to use.
            large_log (bool): Whether to enable large logging.
        """
        super().__init__(**config)

        self.navbar = self.driver.find_element_by_id("navbar")
        self.session_id = self.navbar.get_attribute("data-tabsetid")

        self.tabs_content = self.driver.find_elements_by_xpath(
            "//div[@class='tab-content']/div"
        )
        self.active_tab = None

    def navbar_to(self, tab_name, timeout) -> None:
        """
        Navigates to the specified tab in the navbar.

        Args:
            tab_name (str): The name of the tab to navigate to.
            timeout (int): The maximum amount of time to wait for the tab to become active.

        Returns:
            None
        """
        start = time()

        # Loop through the tabs in the navbar
        for tab in self.navbar.find_elements_by_tag_name("li"):
            # If the tab name matches the specified tab name, click on it
            if tab.find_element_by_tag_name("a").text == tab_name:
                # Wait for the tab to become active
                while tab.get_attribute("class") != "active":
                    tab.click()
                    end = time()
                    if end - start > timeout:
                        # If the timeout has been exceeded, return "Failed"
                        return "Failed"

                # Set the active tab to the tab content element with the "active" class
                for tab_content in self.tabs_content:
                    if tab_content.get_attribute("class") == "tab-pane active":
                        self.active_tab = tab_content
                        break

                # Wait for the content to load
                self.load_content()
                break

        return "Success"

    def load_content(self, div=None) -> None:
        """
        Loads the content of the specified div element.

        Args:
            div (WebElement): The div element to load the content of. If None, the active tab is used.

        Returns:
            None
        """
        if div == None:
            div = self.active_tab

        # Loop through the child elements of the div
        for elem in div.find_elements_by_xpath("./*"):
            # Wait for the element to become visible
            self.wait_visibility_by_xpath(elem, 10)

            # If the element is a div, recursively load its content
            if elem.tag_name == "div":
                if self.headless and "plot" in elem.get_attribute("id"):
                    continue
                self.load_content(elem)

    def select_from_checklist(self, ui_element, check: list) -> None:
        """
        Selects the specified options from a checklist UI element.

        Args:
            ui_element (WebElement): The UI element to select options from.
            check (list): The list of options to select.

        Returns:
            None
        """
        self.scroll_into_view(ui_element)

        # Loop through the options in the UI element
        for option in ui_element.find_elements_by_xpath("./div"):
            option_element = option.find_element_by_xpath("./label")
            # If the option is in the list of options to select and is not already selected, click on it
            if (
                option_element.text in check
                and option_element.find_element_by_xpath("./input").is_selected()
                == False
            ):
                option_element.click()
            # If the option is not in the list of options to select and is already selected, click on it to deselect it
            elif (
                option_element.text not in check
                and option_element.find_element_by_xpath("./input").is_selected()
                == True
            ):
                option_element.click()

    def select_from_dropdown(self, ui_element, option) -> None:
        """
        Selects the specified option from a dropdown UI element.

        Args:
            ui_element (WebElement): The UI element to select the option from.
            option (str): The option to select.

        Returns:
            None
        """
        self.scroll_into_view(ui_element)

        # Click on the dropdown input element to open the dropdown
        ui_element.find_element_by_class_name("selectize-input").click()
        option_element = ui_element.find_element_by_xpath(
            f".//div[@class='option' and text()='{option}']"
        )
        option_element.click()

    def select_from_sliderbar(self, ui_element, value) -> None:
        """
        Selects the specified value from a slider bar UI element.

        Args:
            ui_element (WebElement): The UI element to select the value from.
            value (int): The value to select.

        Returns:
            None
        """
        self.scroll_into_view(ui_element)

        # Get the minimum and maximum values of the slider bar
        slider_min_value = int(ui_element.find_element_by_class_name("irs-min").text)
        slider_max_value = int(ui_element.find_element_by_class_name("irs-max").text)

        # Check if the specified value is within the range of the slider bar
        if value < slider_min_value or value > slider_max_value:
            raise ValueError(
                f"Value must be between {slider_min_value} and {slider_max_value}"
            )

        # Get the current value of the slider bar
        slider_value = int(
            ui_element.find_element_by_class_name("irs-single").get_attribute(
                "textContent"
            )
        )

        # Get the slider element
        slider = ui_element.find_element_by_class_name("irs-handle")

        # Determine the direction to move the slider
        direction = Keys.ARROW_RIGHT if value > int(slider_value) else Keys.ARROW_LEFT

        # Move the slider until the specified value is selected
        while slider_value != value:
            ActionChains(self.driver).click_and_hold(slider).send_keys(
                direction
            ).release().perform()
            sleep(0.5)
            slider_value = int(
                ui_element.find_element_by_class_name("irs-single").get_attribute(
                    "textContent"
                )
            )

    def select_from_bullet_list(self, ui_element, option) -> None:
        """
        Selects the specified option from a bullet list UI element.

        Args:
            ui_element (WebElement): The UI element to select the option from.
            option (str): The option to select.

        Returns:
            None
        """
        self.scroll_into_view(ui_element)

        # Find the option element with the specified text and click on its input element
        option_element = ui_element.find_element_by_xpath(f".//span[text()='{option}']")
        option_element.find_element_by_xpath("./preceding-sibling::input").click()

    def select_from_cross_sectional_data(self, tag_name: str) -> None:
        """
        Selects the specified tag from the cross-sectional data section.

        Args:
            tag_name (str): The tag to select.

        Returns:
            None
        """
        # Find the cross-sectional data section and the button with the specified tag
        cross_sectional_section = self.active_tab.find_element_by_xpath(
            f'//*[@id="tab-{self.session_id}-2"]/div/div/div/div[1]'
        )
        self.find_element_by_text("span", tag_name, cross_sectional_section).click()

        self.load_content()

    def run_evamtools(self, timeout=120) -> None:
        """
        Runs the EVAM Tools analysis and waits for the results to load.

        Args:
            timeout (int): The maximum amount of time to wait for the results to load.

        Returns:
            None
        """
        analysis_button = self.active_tab.find_element_by_xpath('//*[@id="analysis"]')
        self.scroll_into_view(analysis_button)
        analysis_button.click()

        try:
            sleep(0.5)
            self.wait_visibility_by_xpath("/html/body/div[12]/div/div", 1)
            warning = self.driver.find_element_by_xpath("/html/body/div[12]/div/div")
            warning.find_element_by_tag_name("button").click()
        except Exception:
            pass

        # Wait for the loading spinner to appear and disappear
        self.wait_visibility_by_xpath(
            "/html/body/div[12]/div/div[2]/div[1]/div/div[2]", timeout
        )
        self.wait_invisibility_by_xpath(
            "/html/body/div[12]/div/div[2]/div[1]/div/div[2]", timeout
        )

    def toogle_advanced_options_on(self) -> None:
        """
        Toggles the advanced options on and waits for them to load.

        Returns:
            None
        """
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
        """
        Toggles the advanced options off and waits for them to disappear.

        Returns:
            None
        """
        advanced_options = self.active_tab.find_element_by_xpath(
            '//*[@id="advanced_options"]'
        )
        self.scroll_into_view(advanced_options)

        if self.wait_visibility_by_xpath('//*[@id="all_advanced_options"]', 1):
            advanced_options.click()
            self.wait_invisibility_by_xpath('//*[@id="all_advanced_options"]', 1)

    def set_advanced_options(self, label_id, option_value, timeout=10) -> None:
        """
        Sets the value of the specified advanced option.

        Args:
            label_id (str): The ID of the label on the left of the option, obtained inspecting the element.
            option_value (str): The value to set the option to.
            timeout (int): The maximum amount of time to wait for the option to become visible.

        Returns:
            None
        """
        advanced_options = self.active_tab.find_element_by_id("all_advanced_options")
        self.wait_visibility_by_id("all_advanced_options", timeout)

        for option in advanced_options.find_elements_by_xpath("./div/div"):
            if option.find_element_by_xpath("./label").get_attribute("id") != label_id:
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

    def change_genotypes_count(self, counts={}) -> None:
        """
        Changes the genotype counts for the specified indices.

        Args:
            index (list): A list of indices to change the counts for.
            counts (list): A list of counts to set for the specified indices.

        Returns:
            None
        """
        if len(counts) == 0:
            return

        index = list(counts.keys())

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
                row.find_element_by_xpath("./td[3]/input").send_keys(counts[index[idx]])

        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(
            Keys.CONTROL
        ).perform()
        sleep(1)

    def rename_data(self, data_to_rename, rename) -> None:
        """
        Renames the specified cross-sectional data.

        Args:
            data_to_rename (str): The name of the data to rename.
            rename (str): The new name to give to the data.

        Returns:
            None
        """
        self.scroll_into_view(self.active_tab.find_element_by_id("select_csd"))
        self.select_from_cross_sectional_data(data_to_rename)

        rename_frame = self.active_tab.find_element_by_id("dataset_name")
        self.scroll_into_view(rename_frame)

        rename_frame.find_element_by_tag_name("input").clear()
        rename_frame.find_element_by_tag_name("input").send_keys(rename)
        rename_frame.find_element_by_tag_name("button").click()

    # Upload file params
    def upload_data_set(self, name, file_path: str) -> None:
        """
        Uploads a cross-sectional data set to the EVAM Tools page.

        Args:
            name (str): The name to give to the uploaded data set.
            file_path (str): The path to the file to upload.

        Returns:
            None
        """
        file_name = self.driver.find_element_by_id("name_uploaded")
        file_name.clear()
        file_name.send_keys(name)
        sleep(0.5)

        upload_file = self.driver.find_element_by_xpath('//*[@id="csd"]')
        upload_file.send_keys(file_path + name + ".csv")

        self.load_content()

    # Manually genotype frequencies
    def set_number_of_genes(self, number_of_genes: int) -> None:
        """
        Sets the number of genes to include in the analysis.

        Args:
            number_of_genes (int): The number of genes to include.

        Returns:
            None
        """
        number_of_genes_frame = self.active_tab.find_element_by_id("gene_number_slider")
        self.select_from_sliderbar(
            number_of_genes_frame.find_element_by_tag_name("span"), number_of_genes
        )

    def add_genotype(self, mutations: list, count: int) -> None:
        """
        Adds a new genotype to the analysis.

        Args:
            mutations (list): A list of mutations to include in the genotype.
            count (int): The frequency of the genotype.

        Returns:
            None
        """
        add_genotype_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(add_genotype_frame)

        if mutations != []:
            self.select_from_checklist(
                add_genotype_frame.find_element_by_class_name("shiny-options-group"),
                mutations,
            )

        add_genotype_frame.find_element_by_id("genotype_freq").clear()
        add_genotype_frame.find_element_by_id("genotype_freq").send_keys(count)

        sleep(1)
        add_genotype_frame.find_element_by_tag_name("button").click()

    # DAG
    def define_DAG_model(self, model) -> None:
        DAG_Frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(DAG_Frame)

        dag_model = DAG_Frame.find_element_by_id("dag_model")
        self.select_from_bullet_list(dag_model, model)
        sleep(1)

    def define_DAG_new_edge(self, parent_node, child_mode, action) -> None:
        """
        Defines a directed acyclic graph (DAG) for the analysis.

        Args:
            model (str): The name of the model to use for the DAG.
            parent_node (str): The name of the parent node in the DAG.
            child_mode (str): The name of the child node in the DAG.
            action (str): The action to perform on the DAG ("add" or "remove").

        Returns:
            None
        """
        DAG_Frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(DAG_Frame)

        dag_parent_node = DAG_Frame.find_element_by_id("dag_from")
        self.select_from_bullet_list(dag_parent_node, parent_node)

        dag_child_node = DAG_Frame.find_element_by_id("dag_to")
        self.select_from_bullet_list(dag_child_node, child_mode)

        if action == "add":
            DAG_Frame.find_element_by_id("add_edge").click()
        elif action == "remove":
            DAG_Frame.find_element_by_id("remove_edge").click()

    def define_DAG_table(self, values) -> None:
        """
        Defines a directed acyclic graph (DAG) table for the analysis.

        Args:
            from_to (list): A list of tuples representing the parent-child node pairs in the DAG.
            relation (list): A list of strings representing the relations between the parent-child node pairs.
            lambdas (list): A list of strings representing the lambdas for the parent-child node pairs.

        Returns:
            None
        """

        DAG_table = self.active_tab.find_element_by_id(
            "dag_table"
        ).find_element_by_tag_name("table")
        self.scroll_into_view(DAG_table)

        for idx, row in enumerate(DAG_table.find_elements_by_xpath("./tbody/tr")):
            for element in row.find_elements_by_xpath("./td"):
                ActionChains(self.driver).double_click(element).perform()
                element_input = element.find_element_by_xpath("./input")
                if element_input.get_attribute("readonly") == None:
                    element_input.clear()
                    element_input.send_keys(values[idx][0])
                    values[idx].pop(0)

        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(
            Keys.CONTROL
        ).perform()
        sleep(1)

    def define_DAG_epos(self, epos) -> None:
        DAG_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(DAG_frame)

        DAG_frame.find_element_by_id("epos").clear()
        DAG_frame.find_element_by_id("epos").send_keys(epos)

    def define_DAG_num_genotypes(self, num_genotypes) -> None:
        DAG_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(DAG_frame)

        DAG_frame.find_element_by_id("dag_num_samples").clear()
        DAG_frame.find_element_by_id("dag_num_samples").send_keys(num_genotypes)

    def define_DAG_observational_noise(self, observation_noise) -> None:
        DAG_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(DAG_frame)

        DAG_frame.find_element_by_id("dag_obs_noise").clear()
        DAG_frame.find_element_by_id("dag_obs_noise").send_keys(observation_noise)

    def generate_data_from_DAG(self) -> None:
        DAG_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(DAG_frame)

        DAG_frame.find_element_by_id("resample_dag").click()
        sleep(2)

    def reset_DAG(self) -> None:
        DAG_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(DAG_frame)

        DAG_frame.find_element_by_id("clear_dag").click()
        sleep(2)

    def define_MHN(self, values) -> None:
        """
        Defines a Markov hidden network (MHN) for the analysis.

        Args:
            values (list): A list of lists representing the values for the MHN.

        Returns:
            None
        """
        thetas_table = self.active_tab.find_element_by_id(
            "thetas_table"
        ).find_element_by_tag_name("table")
        self.scroll_into_view(thetas_table)

        for idx, row in enumerate(thetas_table.find_elements_by_xpath("./tbody/tr")):
            for element in row.find_elements_by_xpath("./td"):
                ActionChains(self.driver).double_click(element).perform()
                element_input = element.find_element_by_xpath("./input")
                if element_input.get_attribute("readonly") == None:
                    element_input.clear()
                    element_input.send_keys(values[idx][0])
                    values[idx].pop(0)

        # for idx, row in enumerate(thetas_table.find_elements_by_xpath("./tbody/tr")):
        #     ActionChains(self.driver).double_click(
        #         row.find_element_by_xpath("./td")
        #     ).perform()

        #     for idx_2, col in enumerate(row.find_elements_by_xpath("./td")):
        #         try:
        #             col.find_element_by_tag_name("input").clear()
        #             col.find_element_by_tag_name("input").send_keys(
        #                 values[idx][idx_2 - 1]
        #             )
        #         except InvalidElementStateException:
        #             continue

        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(
            Keys.CONTROL
        ).perform()
        sleep(1)

    def define_MHN_number_of_genotypes(self, num_genotypes) -> None:
        MHN_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(MHN_frame)

        MHN_frame.find_element_by_id("mhn_num_samples").clear()
        MHN_frame.find_element_by_id("mhn_num_samples").send_keys(num_genotypes)

    def define_MHN_observational_noise(self, observation_noise) -> None:
        MHN_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(MHN_frame)

        MHN_frame.find_element_by_id("mhn_obs_noise").clear()
        MHN_frame.find_element_by_id("mhn_obs_noise").send_keys(observation_noise)

    def generate_data_from_MHN(self) -> None:
        MHN_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(MHN_frame)

        MHN_frame.find_element_by_id("resample_mhn").click()
        sleep(2)

    def reset_MHN(self) -> None:
        MHN_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(MHN_frame)

        MHN_frame.find_element_by_id("clear_mhn").click()
        sleep(2)

    # Results tab functions
    def CPMs_to_show(self, check: list) -> None:
        """
        Selects the CPMs to show in the analysis.

        Args:
            check (list): A list of strings representing the CPMs to show.

        Returns:
            None
        """
        cpm_options = self.driver.find_element_by_xpath('//*[@id="cpm2show"]/div')
        self.scroll_into_view(cpm_options)

        self.select_from_checklist(cpm_options, check)

    def predictions_from_fitted_models(self, option) -> None:
        """
        Selects the predictions to show from the fitted models.

        Args:
            option (str): The option to select from the predictions.

        Returns:
            None
        """
        predictions = self.driver.find_element_by_xpath('//*[@id="data2plot"]')
        self.scroll_into_view(predictions)

        predictions.find_element_by_xpath(f"//*[text()='{option}']").click()

    def type_of_label(self, option) -> None:
        """
        Selects the type of label to plot in the analysis.

        Args:
            option (str): The option to select from the labels.

        Returns:
            None
        """
        labels = self.driver.find_element_by_xpath('//*[@id="label2plot"]')
        self.scroll_into_view(labels)

        labels.find_element_by_xpath(f"//*[text()='{option}']").click()

    def relevant_paths_to_show(self, value) -> None:
        """
        Selects the number of relevant paths to show in the analysis.

        Args:
            value (int): The number of relevant paths to show.

        Returns:
            None
        """
        slider_box = self.active_tab.find_element_by_class_name("irs--shiny")
        self.scroll_into_view(slider_box)

        self.select_from_sliderbar(slider_box, value)

    def download_results(self) -> None:
        """
        Downloads the results of the analysis.

        Returns:
            None
        """
        self.page_controller.xpath_click('//*[@id="download_cpm"]')
