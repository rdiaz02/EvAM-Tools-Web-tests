from test_case import TestCase

"""
    Test template:

    This template is used to create new tests. It is recommended to
    copy this file and rename it to something more descriptive.

    The name of the test class must be TestMethod, regardless of whether 
    the file name itself is more descriptive.

    The test we want to run must be defined within the test_body
    method of the class.

    Additional functions can be added to assist with additional logic.  
"""


class TestMethod(TestCase):
    def __init__(self, headless, maximize, large_log, screenshots):
        super().__init__(headless, maximize, large_log, screenshots)

    def test_body(self):
        print("Test template")
