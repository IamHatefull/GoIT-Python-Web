from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

'''
#Solution to avoid error: "Couldn't read tbsCertificate as SEQUENCE"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#driver creating
#Path to chromedriver.exe -> 'E:\\Downloads\\chromedriver_win32\\chromedriver.exe'
driver = webdriver.Chrome(executable_path='E:\\Downloads\\chromedriver_win32\\chromedriver.exe', options=options)

#driver = webdriver.Chrome()
driver.get("https://www.selenium.dev/selenium/web/web-form.html")

#Print the webpage title as a first step
print(f"The title of this website is: '{driver.title}'")
driver.implicitly_wait(0.5)
print(f"The current url is: '{driver.current_url}'")

text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

text_box.send_keys("Selenium")
submit_button.click()

message = driver.find_element(by=By.ID, value="message")
value = message.text
print(value)
driver.quit()
'''

def test_eight_components():
    #Solution to avoid error: "Couldn't read tbsCertificate as SEQUENCE"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #driver creating
    #Path to chromedriver.exe -> 'E:\\Downloads\\chromedriver_win32\\chromedriver.exe'
    driver = webdriver.Chrome(executable_path='E:\\Downloads\\chromedriver_win32\\chromedriver.exe', options=options)

    #driver = webdriver.Chrome()
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    #Print the webpage title as a first step
    title = driver.title
    print(f"The title of this website is: '{title}'")
    driver.implicitly_wait(0.5)
    print(f"The current url is: '{driver.current_url}'")

    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    text_box.send_keys("Selenium")
    submit_button.click()

    message = driver.find_element(by=By.ID, value="message")
    value = message.text
    print(value)

    driver.quit()
