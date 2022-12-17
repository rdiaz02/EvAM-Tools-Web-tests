from selenium_web_driver import selenium_driver
from tests import tester

if __name__ == '__main__':
    web_driver = selenium_driver()
    web_driver.connect()

    test_runner = tester(web_driver)
    test_runner.analyzing_BRCA_data_set()
    test_runner.analyzing_manually_constructed_synthetic_data()
