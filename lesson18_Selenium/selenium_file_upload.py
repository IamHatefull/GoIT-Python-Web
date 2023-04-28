from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)

#Get to the page
driver.get("https://the-internet.herokuapp.com/upload")

# find file upload element and send file by path.
driver.find_element(By.ID,"file-upload").send_keys("E:\Python\GitHub_Repositories\GitHub\GoIT-Python-Web\lesson18_Selenium\shotgun.jpg")
driver.implicitly_wait(10)

#After upload, find submit button and press it.
driver.find_element(By.ID,"file-submit").submit()


if(driver.page_source.find("File Uploaded!")):
    print("File upload success")
else:
    print("File upload failed")

driver.quit()