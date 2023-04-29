from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import alert_is_present


#Solution to avoid error: "Couldn't read tbsCertificate as SEQUENCE"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#driver creating
#Path to chromedriver.exe -> 'E:\\Downloads\\chromedriver_win32\\chromedriver.exe'
driver = webdriver.Chrome(executable_path='E:\\Downloads\\chromedriver_win32\\chromedriver.exe', options=options)
#driver = webdriver.Chrome()

driver.get("https://www.selenium.dev/documentation/webdriver/interactions/alerts")
print(driver.current_url)

# Click the link to activate the alert
driver.find_element(By.LINK_TEXT, "See an example alert").click()

wait = WebDriverWait(webdriver, 5)
# Wait for the alert to be displayed and store it in a variable
alert = driver.switch_to.alert

# Store the alert text in a variable
text = alert.text
print(text)

# Press the OK button
alert.accept()
# makes an end of alert code part more visible
print('Alert confirmed \n _____________')

# Click the link to activate the alert
driver.find_element(By.LINK_TEXT, "See a sample confirm").click()

# Wait for the alert to be displayed
#wait.until(expected_conditions.alert_is_present())

# Store the alert in a variable for reuse
alert = driver.switch_to.alert

# Store the alert text in a variable
text = alert.text
print(text)

# Press the Cancel button
alert.dismiss()
print('Confirm dismissed \n _____________')

# Click the link to activate the alert
driver.find_element(By.LINK_TEXT, "See a sample prompt").click()

# Wait for the alert to be displayed
#wait.until(expected_conditions.alert_is_present())

# Store the alert in a variable for reuse
alert = driver.switch_to.alert

# Type your message
alert.send_keys("Selenium")

# Press the OK button
alert.accept()
print('Text sended \n _____________')