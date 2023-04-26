from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

"""
WebDriver drives a browser natively, as a user would, either locally or on a remote machine using the Selenium server, marks a leap forward in terms of browser automation.
"""

#Solution to avoid error: "Couldn't read tbsCertificate as SEQUENCE"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#driver creating
#Path to chromedriver.exe -> 'E:\\Downloads\\chromedriver_win32\\chromedriver.exe'
driver = webdriver.Chrome(executable_path='E:\\Downloads\\chromedriver_win32\\chromedriver.exe', options=options)

#driver = webdriver.Chrome()
driver.get("http://www.python.org")

#Print the webpage title as a first step
print(f"The title of this website is: '{driver.title}'")

#Searchin for element of the webpage by its name
search = driver.find_element(By.NAME, 'q')
print(search)
time.sleep(2)
search.send_keys("business")
search.send_keys(Keys.RETURN)


main = driver.find_element(By.ID, "id-search-field")

driver.quit()
