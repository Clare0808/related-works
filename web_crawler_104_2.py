from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas

# set the path of the execution of the Chrome Driver
options =  Options()
options.chrome_executable_path = "C:\\Users\\User\\Documents\\Self Practice\\Web_Crawler\\chromedriver.exe"

driver = webdriver.Chrome(options = options) # open the Chrome browser

driver.maximize_window() # maximize the browser window

driver.get("https://www.104.com.tw/jobs/search/?jobcat=2007000000&jobsource=m_changejob") # open the website

time.sleep(10)

data_list = []

jobs = driver.find_elements(By.CLASS_NAME, "info-container")

for job in jobs :

    data = {}

    job_title = job.find_element(By.TAG_NAME, "h2")
    data["Title"] = job_title.text

    locations = job.find_elements(By.CSS_SELECTOR, "a[data-gtm-joblist]")
    for location in locations :
        if "地區" in location.get_attribute("data-gtm-joblist"):
            data["Place"] = location.text
           
    standards = job.find_elements(By.CSS_SELECTOR, "a[data-gtm-joblist]")
    for standard in standards :
        if "經歷" in standard.get_attribute("data-gtm-joblist"):
            data["Exprience"] = standard.text

    data_list.append(data)

print(data_list)

# store the data_list as a excel file
dataframe = pandas.DataFrame(data_list)
dataframe.to_excel("jobs.xlsx", index = False, engine = "openpyxl")

driver.close() # close the browser window