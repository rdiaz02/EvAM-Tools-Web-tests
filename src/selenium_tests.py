import test_case

class TestEvamToolsWebPage(test_case.TestCase):

    def __init__(self):
        active_tests_list = ['test_results_tab']
        super().__init__(active_tests_list)


    ############################# Basic functionality tests #############################
    def test_navbar(self) -> None:
        self.page_controller.navbar_to('User input', 10)
        self.page_controller.navbar_to('Results', 10)
        self.page_controller.navbar_to('About EvAM-Tools', 10)

    def test_user_input_tab(self) -> None:
        self.page_controller.navbar_to('User input', 10)

    def test_results_tab(self) -> None:
        self.page_controller.navbar_to('Results', 10)
        self.page_controller.CPMs_to_show(['CBN', 'OncoBN'])
        self.page_controller.predictions_from_fitted_models('Transition rates')
        self.page_controller.type_of_label('Last gene mutated')
        self.page_controller.type_of_label('Genotype')
        self.page_controller.relevant_paths_to_show(1)
        self.page_controller.relevant_paths_to_show(10)
        self.page_controller.relevant_paths_to_show(11)

    def test_advanced_options(self) -> None:
        self.page_controller.navbar_to('User input', 10)
        self.page_controller.toogle_advanced_options()
        self.page_controller.set_advanced_options('Return paths to maximum(a)', 'TRUE')
        self.page_controller.toogle_advanced_options()
    
    def test_user_input_tab(self) -> None:
        self.page_controller.navbar_to('User input', 10)
        slider_box = self.page_controller.active_tab.find_element_by_class_name('irs--shiny')
        self.page_controller.select_from_sliderbar(slider_box, 6)

    def analyzing_BRCA_data_set(self) -> None:

        self.page_controller.navbar_to('User input', 10)
        self.page_controller.click_cross_sectional_data('Upload file')

        self.page_controller.upload_data_set('BRCA_ba_s', '/home/lorenzo/Documentos/Universidad/TFG/EvAM-Tools-Web-tests/data/BRCA_ba_s.csv')

        # Boton de analisis
        self.page_controller.run_evamtools()

        # Descarga de los resultados
        self.page_controller.navbar_to('Results', 10)
        #self.page_controller.xpath_click('//*[@id="download_cpm"]')

