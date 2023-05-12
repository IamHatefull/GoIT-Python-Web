import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class ChromeSearch(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        #driver creating
        #Path to chromedriver.exe -> 'E:\\Downloads\\chromedriver_win32\\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path='E:\\Downloads\\chromedriver_win32\\chromedriver.exe', options=options)

        #self.driver = webdriver.Chrome('./chromedriver')

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("https://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element(by=By.NAME, value="q")
        elem.send_keys("getting started with python")
        elem.send_keys(Keys.RETURN)
        assert "https://www.python.org/search/?q=getting+started+with+python&submit=" == driver.current_url

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()