from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

#Solution to avoid error: "Couldn't read tbsCertificate as SEQUENCE"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#driver creating
#Path to chromedriver.exe -> 'E:\\Downloads\\chromedriver_win32\\chromedriver.exe'
driver = webdriver.Chrome(executable_path='E:\\Downloads\\chromedriver_win32\\chromedriver.exe', options=options)
#driver = webdriver.Chrome()

driver.get("https://www.selenium.dev/documentation/webdriver/interactions/alerts/")

# Click the link to activate the alert
driver.find_element(By.LINK_TEXT, "See an example alert").click()

# Wait for the alert to be displayed and store it in a variable
alert = WebDriverWait.until(expected_conditions.alert_is_present())

# Store the alert text in a variable
text = alert.text

# Press the OK button
alert.accept()