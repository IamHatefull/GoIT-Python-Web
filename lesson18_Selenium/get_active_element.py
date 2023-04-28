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

# Navigate to url
driver.get("https://www.google.com")
driver.find_element(By.CSS_SELECTOR, '[name="q"]').send_keys("webElement")

# Get attribute of current active element
attr = driver.switch_to.active_element.get_attribute("title")
print(attr)
print(driver.current_url)

# Store 'SearchInput' element
SearchInput = driver.find_element(By.NAME, "q")
SearchInput.send_keys("selenium")

# Clears the entered text
SearchInput.clear()

# Returns true if element is enabled else returns false
value = driver.find_element(By.NAME, 'btnK').is_enabled()
print(value)

# Refresh the current page
driver.refresh()

