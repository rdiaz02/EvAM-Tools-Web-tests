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
        Initializes a new instance of the PageController class with the specified options.

        Args:
            driver (webdriver): The WebDriver instance to use.
            large_log (bool): Whether to enable large logging.
            screenshots (bool): Whether to take screenshots on errors.
        """
        # Set the driver, large_log, and screenshots options as instance variables
        self.driver = driver
        self.large_log = large_log
        self.screenshots = screenshots

        # Find the navbar element and get its session ID
        self.navbar = self.driver.find_element_by_id("navbar")
        self.session_id = self.navbar.get_attribute("data-tabsetid")

        # Find the tabs content elements and set the active tab to None
        self.tabs_content = self.driver.find_elements_by_xpath(
            "//div[@class='tab-content']/div")
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
                sleep(5)
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
        # If div is None, use the active tab
        if div == None:
            div = self.active_tab

        # Loop through the child elements of the div
        for elem in div.find_elements_by_xpath("./*"):
            # Wait for the element to become visible
            self.wait_visibility_by_xpath(elem, 10)

            # If the element is a div, recursively load its content
            if elem.tag_name == "div":
                self.load_content(elem)

    def wait_invisibility_by_xpath(self, xpath, timeout=10) -> bool:
        """
        Waits for an element to become invisible by its xpath.

        Args:
            xpath (str): The xpath of the element to wait for.
            timeout (int): The maximum amount of time to wait for the element to become invisible.

        Returns:
            bool: True if the element becomes invisible within the specified timeout, False otherwise.
        """
        try:
            # Wait for the element to become invisible using the specified xpath and timeout
            WebDriverWait(self.driver, timeout).until(
                ec.invisibility_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception:
            return False

    def wait_visibility_by_xpath(self, xpath, timeout=10) -> bool:
        """
        Waits for an element to become visible by its xpath.

        Args:
            xpath (str): The xpath of the element to wait for.
            timeout (int): The maximum amount of time to wait for the element to become visible.

        Returns:
            bool: True if the element becomes visible within the specified timeout, False otherwise.
        """
        try:
            # Wait for the element to become visible using the specified xpath and timeout
            WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception:
            return False

    def find_element_by_text(self, tag_name, text, ui_element=None) -> None:
        """
        Finds an element by its tag name and text.

        Args:
            tag_name (str): The tag name of the element to find.
            text (str): The text of the element to find.
            ui_element (WebElement): The UI element to search within. Defaults to the active tab.

        Returns:
            WebElement: The element with the specified tag name and text, or None if not found.
        """
        if ui_element == None:
            ui_element = self.active_tab

        # Find all elements with the specified tag name within the specified UI element
        for elem in ui_element.find_elements_by_tag_name(tag_name):
            # If the element's text matches the specified text, return the element
            if elem.text == text:
                return elem
        # If no element is found, return None
        return None

    def scroll_into_view(self, element):
        """
        Scrolls the specified element into view.

        Args:
            element (WebElement): The element to scroll into view.

        Returns:
            None
        """
        clickable = False
        while clickable == False:
            # Scroll the window by 300 pixels
            self.driver.execute_script("window.scrollBy(0,300)")
            try:
                # Try to click the element
                element.click()
                clickable = True
            except WebDriverException:
                # If the element is not clickable, continue scrolling
                pass

    def select_from_checklist(self, ui_element, check: list) -> None:
        """
        Selects the specified options from a checklist UI element.

        Args:
            ui_element (WebElement): The UI element to select options from.
            check (list): The list of options to select.

        Returns:
            None
        """
        # Scroll the UI element into view
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
                option_element.find_element_by_xpath("./input").click()
            # If the option is not in the list of options to select and is already selected, click on it to deselect it
            elif (
                option_element.text not in check
                and option_element.find_element_by_xpath("./input").is_selected()
                == True
            ):
                option_element.find_element_by_xpath("./input").click()

    def select_from_dropdown(self, ui_element, option) -> None:
        """
        Selects the specified option from a dropdown UI element.

        Args:
            ui_element (WebElement): The UI element to select the option from.
            option (str): The option to select.

        Returns:
            None
        """
        # Scroll the UI element into view
        self.scroll_into_view(ui_element)

        # Click on the dropdown input element to open the dropdown
        ui_element.find_element_by_class_name("selectize-input").click()

        # Loop through the options in the dropdown
        options = ui_element.find_elements_by_class_name("option")
        for opt in options:
            # If the option matches the specified option, click on it and break out of the loop
            if opt.text == option:
                opt.click()
                break

    def select_from_sliderbar(self, ui_element, value) -> None:
        """
        Selects the specified value from a slider bar UI element.

        Args:
            ui_element (WebElement): The UI element to select the value from.
            value (int): The value to select.

        Returns:
            None
        """
        # Scroll the UI element into view
        self.scroll_into_view(ui_element)

        # Get the minimum and maximum values of the slider bar
        slider_min_value = int(
            ui_element.find_element_by_class_name("irs-min").text)
        slider_max_value = int(
            ui_element.find_element_by_class_name("irs-max").text)

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
        direction = Keys.ARROW_RIGHT if value > int(
            slider_value) else Keys.ARROW_LEFT

        # Move the slider until the specified value is selected
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
        """
        Selects the specified option from a bullet list UI element.

        Args:
            ui_element (WebElement): The UI element to select the option from.
            option (str): The option to select.

        Returns:
            None
        """
        # Scroll the UI element into view
        self.scroll_into_view(ui_element)

        # Find the option element with the specified text and click on its input element
        option_element = ui_element.find_element_by_xpath(
            f".//span[text()='{option}']")
        option_element.find_element_by_xpath(
            "./preceding-sibling::input").click()

    def select_from_cross_sectional_data(self, tag_name: str) -> None:
        """
        Selects the specified tag from the cross-sectional data section.

        Args:
            tag_name (str): The tag to select.

        Returns:
            None
        """
        # Find the cross-sectional data section and the button with the specified tag
        cross_sectional_section = self.active_tab.find_element_by_xpath('//*[@id="tab-{}-2"]/div/div/div/div[1]'.format(
            self.session_id))
        cross_sectional_button = cross_sectional_section.find_element_by_xpath(
            f'.//span[text()="{tag_name}"]')

        # Click on the button and load the content
        cross_sectional_button.click()
        self.load_content()

    def run_evamtools(self, timeout=60) -> None:
        """
        Runs the EVAM Tools analysis and waits for the results to load.

        Args:
            timeout (int): The maximum amount of time to wait for the results to load.

        Returns:
            None
        """
        # Click on the "Analysis" button
        analysis_button = self.active_tab.find_element_by_xpath(
            '//*[@id="analysis"]')
        analysis_button.click()

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
        # Find the advanced options element and scroll it into view
        advanced_options = self.active_tab.find_element_by_xpath(
            '//*[@id="advanced_options"]')
        self.scroll_into_view(advanced_options)

        # If the all advanced options element is not displayed, click on the advanced options element
        # and wait for the all advanced options element to become visible
        if not self.active_tab.find_element_by_xpath('//*[@id="all_advanced_options"]'
                                                     ).is_displayed():
            self.active_tab.find_element_by_xpath(
                '//*[@id="advanced_options"]').click()
            self.wait_visibility_by_xpath('//*[@id="all_advanced_options"]')

    def toogle_advanced_options_off(self) -> None:
        """
        Toggles the advanced options off and waits for them to disappear.

        Returns:
            None
        """
        # Find the advanced options element and scroll it into view
        advanced_options = self.active_tab.find_element_by_xpath(
            '//*[@id="advanced_options"]')
        self.scroll_into_view(advanced_options)

        # If the all advanced options element is visible, click on the advanced options element
        # and wait for the all advanced options element to disappear
        if self.wait_visibility_by_xpath('//*[@id="all_advanced_options"]', 1):
            advanced_options.click()
            self.wait_invisibility_by_xpath(
                '//*[@id="all_advanced_options"]', 1)

    def set_advanced_options(self, option_name, option_value, timeout=10) -> None:
        """
        Sets the value of the specified advanced option.

        Args:
            option_name (str): The name of the option to set.
            option_value (str): The value to set the option to.
            timeout (int): The maximum amount of time to wait for the option to become visible.

        Returns:
            None
        """
        # Find the advanced options element and wait for it to become visible
        advanced_options = self.active_tab.find_element_by_id(
            "all_advanced_options")
        self.wait_visibility_by_id("all_advanced_options", timeout)

        # Loop through all the options in the advanced options element
        for option in advanced_options.find_elements_by_xpath("./div/div"):
            # If the option name does not match, continue to the next option
            if option.find_element_by_xpath("./label").text != option_name:
                continue

            # Determine the type of the option (input or div)
            try:
                option.find_element_by_xpath("./div")
                type = "div"
            except NoSuchElementException:
                type = "input"

            # Set the value of the option based on its type
            if type == "div":
                # If the option is a checklist, select the specified value
                if option.find_element_by_xpath("./div").get_attribute("class") == "shiny-options-group":
                    self.select_from_checklist(
                        option.find_element_by_xpath("./div"), option_value)
                # If the option is a dropdown, select the specified value
                else:
                    self.select_from_dropdown(
                        option.find_element_by_xpath("./div"), option_value)
            elif type == "input":
                # If the option is an input field, clear its current value and set the specified value
                option.find_element_by_xpath("./input").clear()
                option.find_element_by_xpath("./input").send_keys(option_value)

    def change_genotypes_count(self, index=[], counts=[]) -> None:
        """
        Changes the genotype counts for the specified indices.

        Args:
            index (list): A list of indices to change the counts for.
            counts (list): A list of counts to set for the specified indices.

        Returns:
            None
        """
        # Check that the index and counts lists have the same length
        if len(index) != len(counts):
            raise ValueError("Index, counts must have the same length")

        # Find the genotype table element and scroll it into view
        genotype_table = self.active_tab.find_element_by_id(
            "change_counts").find_element_by_tag_name("table")
        self.scroll_into_view(genotype_table)

        # Loop through each row in the genotype table
        for idx, row in enumerate(genotype_table.find_elements_by_xpath("./tbody/tr")):
            # If the index of the row matches one of the specified indices, change the count
            if int(row.find_element_by_xpath("./td[1]").text) == index[idx]:
                # Double-click on the count cell to activate the input field
                ActionChains(self.driver).double_click(
                    row.find_element_by_xpath("./td[3]")).perform()
                # Clear the current count and set the specified count
                row.find_element_by_xpath("./td[3]/input").clear()
                row.find_element_by_xpath(
                    "./td[3]/input").send_keys(counts[idx])

        # Press Ctrl+Enter to save the changes and wait for 1 second
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(
            Keys.ENTER).key_up(Keys.CONTROL).perform()
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
        # Scroll the cross-sectional data element into view and select the specified data
        self.scroll_into_view(self.active_tab.find_element_by_id("select_csd"))
        self.select_from_cross_sectional_data(data_to_rename)

        # Find the rename frame element and scroll it into view
        rename_frame = self.scroll_into_view(
            self.active_tab.find_element_by_id("dataset_name"))

        # Clear the current name and set the new name
        rename_frame.find_element_by_tag_name("input").clear()
        rename_frame.find_element_by_tag_name("input").send_keys(rename)

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
        # Find the file name element and set the name of the uploaded file
        file_name = self.driver.find_element_by_id("name_uploaded")
        file_name.clear()
        file_name.send_keys(name)

        # Find the upload file element and send the file path to it
        upload_file = self.driver.find_element_by_xpath('//*[@id="csd"]')
        upload_file.send_keys(file_path)

        # Wait for 0.5 seconds and load the content of the page
        self.driver.implicitly_wait(0.5)
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
        # Find the number of genes frame element and select the specified number of genes
        number_of_genes_frame = self.active_tab.find_element_by_id(
            "gene_number_slider")
        self.select_from_sliderbar(
            number_of_genes_frame.find_element_by_tag_name(
                "span"), number_of_genes
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
        # Find the add genotype frame element and scroll it into view
        add_genotype_frame = self.active_tab.find_element_by_id(
            "define_genotype")
        self.scroll_into_view(add_genotype_frame)

        # Select the specified mutations from the checklist
        self.select_from_checklist(add_genotype_frame.find_element_by_class_name(
            "shiny-options-group"), mutations)

        # Clear the genotype frequency input field and set the specified frequency
        add_genotype_frame.find_element_by_id("genotype_freq").clear()
        add_genotype_frame.find_element_by_id("genotype_freq").send_keys(count)

        # Wait for 1 second and click the Add button
        sleep(1)
        add_genotype_frame.find_element_by_tag_name("button").click()

    # DAG
    def define_DAG(self, model, parent_node, child_mode, action) -> None:
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
        # Find the DAG frame element and scroll it into view
        DAG_Frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(DAG_Frame)

        # Select the specified model, parent node, and child node from the bullet lists
        dag_model = DAG_Frame.find_element_by_id("dag_model")
        self.select_from_bullet_list(dag_model, model)

        dag_parent_node = DAG_Frame.find_element_by_id("dag_from")
        self.select_from_bullet_list(dag_parent_node, parent_node)

        dag_child_node = DAG_Frame.find_element_by_id("dag_to")
        self.select_from_bullet_list(dag_child_node, child_mode)

        # Perform the specified action on the DAG
        if action == "add":
            DAG_Frame.find_element_by_id("add_edge").click()
        elif action == "remove":
            DAG_Frame.find_element_by_id("remove_edge").click()

    def define_DAG_table(self, from_to, relation, lambdas) -> None:
        """
        Defines a directed acyclic graph (DAG) table for the analysis.

        Args:
            from_to (list): A list of tuples representing the parent-child node pairs in the DAG.
            relation (list): A list of strings representing the relations between the parent-child node pairs.
            lambdas (list): A list of strings representing the lambdas for the parent-child node pairs.

        Returns:
            None
        """
        # Check that the input lists have the same length
        if len(from_to) != len(relation) != len(lambdas):
            raise ValueError(
                "from_to, relation, lambdas must have the same length")

        # Find the DAG table element and scroll it into view
        DAG_table = self.active_tab.find_element_by_id(
            "dag_table").find_element_by_tag_name("table")
        self.scroll_into_view(DAG_table)

        # Iterate over the rows of the DAG table and update the specified parent-child node pairs
        for idx, row in enumerate(DAG_table.find_elements_by_xpath("./tbody/tr")):
            if (row.find_element_by_xpath("./td[1]").text, row.find_element_by_xpath("./td[2]").text) == from_to[idx]:
                # Double-click the relation cell to enable editing
                ActionChains(self.driver).double_click(
                    row.find_element_by_xpath("./td[3]")).perform()

                # Clear the current relation and lambda values and set the specified values
                row.find_element_by_xpath("./td[3]/input").clear()
                row.find_element_by_xpath(
                    "./td[3]/input").send_keys(relation[idx])
                row.find_element_by_xpath("./td[4]/input").clear()
                row.find_element_by_xpath(
                    "./td[4]/input").send_keys(lambdas[idx])

        # Press Ctrl+Enter to save the changes
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(
            Keys.ENTER).key_up(Keys.CONTROL).perform()
        sleep(1)

    def generate_data_from_DAG_model(
        self, epos, num_genotypes, observation_noise
    ) -> None:
        # Find the DAG frame element and scroll it into view
        DAG_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(DAG_frame)

        # Clear the epos, num_genotypes, and observation_noise input fields and set the specified values
        DAG_frame.find_element_by_id("epos").clear()
        DAG_frame.find_element_by_id("epos").send_keys(epos)

        DAG_frame.find_element_by_id("dag_num_samples").clear()
        DAG_frame.find_element_by_id(
            "dag_num_samples").send_keys(num_genotypes)

        DAG_frame.find_element_by_id("dag_obs_noise").clear()
        DAG_frame.find_element_by_id(
            "dag_obs_noise").send_keys(observation_noise)

    def define_MHN(self, values) -> None:
        """
        Defines a Markov hidden network (MHN) for the analysis.

        Args:
            values (list): A list of lists representing the values for the MHN.

        Returns:
            None
        """
        # Find the thetas table element and scroll it into view
        thetas_table = self.active_tab.find_element_by_id(
            "thetas_table").find_element_by_tag_name("table")
        self.scroll_into_view(thetas_table)

        # Iterate over the rows and columns of the thetas table and set the specified values
        for idx, row in enumerate(thetas_table.find_elements_by_xpath("./tbody/tr")):
            # Double-click the first cell of the row to enable editing
            ActionChains(self.driver).double_click(
                row.find_element_by_xpath("./td")).perform()

            for idx_2, col in enumerate(row.find_elements_by_xpath("./td")):
                try:
                    # Clear the current value and set the specified value
                    col.find_element_by_tag_name("input").clear()
                    col.find_element_by_tag_name(
                        "input").send_keys(values[idx][idx_2 - 1])
                except InvalidElementStateException:
                    continue

        # Press Ctrl+Enter to save the changes
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(
            Keys.ENTER).key_up(Keys.CONTROL).perform()
        sleep(1)

    def generate_data_from_MHN_model(self, num_genotypes, observation_noise) -> None:
        """
        Generates data from a Markov hidden network (MHN) model.

        Args:
            num_genotypes (int): The number of genotypes to generate data for.
            observation_noise (float): The observation noise to use for the data generation.

        Returns:
            None
        """
        # Find the MHN frame element and scroll it into view
        MHN_frame = self.active_tab.find_element_by_id("define_genotype")
        self.scroll_into_view(MHN_frame)

        # Clear the mhn_num_samples and mhn_obs_noise input fields and set the specified values
        MHN_frame.find_element_by_id("mhn_num_samples").clear()
        MHN_frame.find_element_by_id(
            "mhn_num_samples").send_keys(num_genotypes)

        MHN_frame.find_element_by_id("mhn_obs_noise").clear()
        MHN_frame.find_element_by_id(
            "mhn_obs_noise").send_keys(observation_noise)

        # Click the "Resample MHN" button to generate the data
        MHN_frame.find_element_by_id("resample_mhn").click()

    # Results tab functions
    def CPMs_to_show(self, check: list) -> None:
        """
        Selects the CPMs to show in the analysis.

        Args:
            check (list): A list of strings representing the CPMs to show.

        Returns:
            None
        """
        # Find the CPM options element and scroll it into view
        cpm_options = self.driver.find_element_by_xpath(
            '//*[@id="cpm2show"]/div')
        self.scroll_into_view(cpm_options)

        # Select the specified CPMs from the checklist
        self.select_from_checklist(cpm_options, check)

    def predictions_from_fitted_models(self, option) -> None:
        """
        Selects the predictions to show from the fitted models.

        Args:
            option (str): The option to select from the predictions.

        Returns:
            None
        """
        # Find the predictions element and scroll it into view
        predictions = self.driver.find_element_by_xpath('//*[@id="data2plot"]')
        self.scroll_into_view(predictions)

        # Click the specified option from the predictions
        predictions.find_element_by_xpath(f"//*[text()='{option}']").click()

    def type_of_label(self, option) -> None:
        """
        Selects the type of label to plot in the analysis.

        Args:
            option (str): The option to select from the labels.

        Returns:
            None
        """
        # Find the labels element and scroll it into view
        labels = self.driver.find_element_by_xpath('//*[@id="label2plot"]')
        self.scroll_into_view(labels)

        # Click the specified option from the labels
        labels.find_element_by_xpath(f"//*[text()='{option}']").click()

    def relevant_paths_to_show(self, value) -> None:
        """
        Selects the number of relevant paths to show in the analysis.

        Args:
            value (int): The number of relevant paths to show.

        Returns:
            None
        """
        # Find the slider box element and scroll it into view
        slider_box = self.active_tab.find_element_by_class_name("irs--shiny")
        self.scroll_into_view(slider_box)

        # Select the specified number of relevant paths from the slider bar
        self.select_from_sliderbar(slider_box, value)

    def download_results(self) -> None:
        """
        Downloads the results of the analysis.

        Returns:
            None
        """
        # Find the download button element and click it
        self.page_controller.xpath_click('//*[@id="download_cpm"]')
