from test_case import TestCase

"""
    Ejemplo 1: Métodos para obtención de datos básicos de la web.

    - Cargar la url.
    - Mostrar por pantalla la url actual.
    - Mostrar por pantalla el título de la página.
    - Mostrar por pantalla el código fuente de la página.
"""


class TestMethod(TestCase):
    def __init__(self, headless, maximize, large_log, screenshots):
        super().__init__(headless, maximize, large_log, screenshots)

    def test_body(self):
        print("Testing current url")
        driver = self.page_controller.driver

        print(driver.current_url)
        print(driver.title)
        print(driver.page_source)
