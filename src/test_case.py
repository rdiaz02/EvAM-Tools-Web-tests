import unittest
from evam_tools_driver import EvAMToolsDriver
from evam_tools_page_tests import EvAMToolsPage

class TestCase(unittest.TestCase):
    
    def __init__(self, tests_list):
        self.tests_list = tests_list
        self.drive = None
        self.page_controller = None

    def run(self):
        print('Running tests: ' + str(self.tests_list))
        for test in self.tests_list:
            self.setUp()
            try:
                method = getattr(self, test)
                method()
            except Exception as e:
                print('Error running test ' + test + ': ' + str(e))
            self.tearDown()

    def setUp(self):
        self.driver = EvAMToolsDriver()
        self.driver.connect(headless=False, maximize=True)
        self.page_controller = EvAMToolsPage(self.driver.get_driver())

    def tearDown(self):
        self.driver.close()

    def test_default(self):
        print('test_default')
