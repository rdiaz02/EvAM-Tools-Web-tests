from selenium_web_driver import selenium_driver
from tests import tester

if __name__ == '__main__':
    web_driver = selenium_driver()
    web_driver.connect()
    web_driver.test_navbar_load_page()
    print(web_driver.navbar_to('User input', 10))
    print(web_driver.navbar_to('Results', 10))
    print(web_driver.navbar_to('User input', 10))
    print(web_driver.navbar_to('About EvAM-Tools', 10))
    # ret = web_driver.move_to_user_input(10)
    # web_driver.loading_content()

    #test_runner = tester(web_driver)
    #test_runner.analyzing_BRCA_data_set()
    #test_runner.analyzing_manually_constructed_synthetic_data()
    #test_runner.small_computational_experiments()
    #test_runner.analyzing_manually_constructed_data()
