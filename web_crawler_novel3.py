from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# set the path of the execution of the Chrome Driver
options =  Options()
options.chrome_executable_path = "C:\\Users\\User\\Documents\\Self Practice\\Web_Crawler\\chromedriver.exe"

driver = webdriver.Chrome(options = options) # open the Chrome browser

driver.get("https://czbooks.net/")

time.sleep(1)

search_bar = driver.find_element(By.CLASS_NAME, "search-bar")
search_bar.click()

search_input = driver.find_element(By.ID, "search-text")
search_input.clear() # clear the search bar
search_input.send_keys("偷偷藏不住")

time.sleep(1)

search_input.send_keys(Keys.ENTER)

novel_name = driver.find_element(By.CLASS_NAME, "novel-item-title")
novel_name.click()

time.sleep(1)

driver.back() # go back to last page
driver.back()

driver.forward() # go to next page

driver.close() # close the browser window