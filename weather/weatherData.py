from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

# set the path of the execution of the Chrome Driver
chrome_driver_path = "C:\\Users\\User\\Documents\\Self_Practice\\Web_Crawler\\chromedriver.exe"
service = Service(chrome_driver_path)
options = Options()

driver = webdriver.Chrome(service=service, options=options)  # open the Chrome browser

driver.maximize_window() # maximize the browser window

driver.get("https://www.cwa.gov.tw/V8/C/W/County/index.html") # open the website

time.sleep(10)

data_list = []
root = driver.find_element(By.ID, "town")
infos = root.find_elements(By.TAG_NAME, "a")

for info in infos :
    data = {}

    city = info.find_element(By.CLASS_NAME, "city")
    data["city"] = city.text

    tems = info.find_elements(By.CLASS_NAME, "tem-C")

    temperature_values = []
    for tem in tems:
        tem_values = tem.find_elements(By.TAG_NAME, "i")
        temp_data = [tem_value.get_attribute("innerText") for tem_value in tem_values]

        temperature_values.extend(temp_data)

    data["temperature"] = temperature_values

    rain = info.find_element(By.CLASS_NAME, "rain")
    data["rain"] = rain.text

    data_list.append(data)

# put the result into a json file
with open("weatherData.json", "w", encoding="utf-8") as f:
    json.dump(data_list, f, ensure_ascii = False, indent = 2)

driver.close() # close the browser window