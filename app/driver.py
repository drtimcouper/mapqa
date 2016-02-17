from selenium import webdriver


class Driver:

    _driver = None

    def __init__(self, browser="Firefox"):
        self._driver = getattr(webdriver, browser)()

    def __del__(self):
        if self._driver:
            self._driver.close()

    def __getattr__(self, attr):
        return getattr(self._driver, attr)

