from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import random
import pdb
import pandas as pd




driver_path = r"C:\Users\jainprs\Downloads\amazon_review\chromedriver.exe"
service = Service(driver_path)

chrome_options = webdriver.ChromeOptions()

custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
chrome_options.add_argument(f"user-agent={custom_user_agent}")

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.indeed.com/jobs?q=mtss+coordinator&start=0")
driver.maximize_window()

sleep_time = random.uniform(9.4, 15.6)

soup_list = []

num_pages = 19

for page in range(num_pages):
    time.sleep(sleep_time)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    soup_list.append(soup)

    time.sleep(sleep_time)
    next_page_url = f"https://www.indeed.com/jobs?q=mtss+coordinator&start={page * 10}"
    driver.get(next_page_url)

company_names = [name.text for soup in soup_list for name in soup.find_all("span", class_="companyName")]
locations = [location.text.split("<!-- -->")[0].strip() for soup in soup_list for location in soup.find_all("div", class_="companyLocation")]

all_salary = []
description = []
post_date = []
job_titles_lis = []

for soup in soup_list:
    try:
        salaries = soup.find_all("div", class_="heading6 tapItem-gutter metadataContainer noJEMChips salaryOnly")
        for i in salaries:
            salary = i.text.strip()
            all_salary.append(salary)
    except:
        all_salary.append(None)

    try:
        data = soup.find_all("div", class_="heading6 tapItem-gutter result-footer")
        for i in data:
            desc = i.find("div", class_="job-snippet").text.strip()
            description.append(desc)
            
            posted = i.find("span", class_="date").text.strip()
            post_date.append(posted)
    except Exception as e:
        pass

    try:
        job_titles = soup.find_all("h2", class_="jobTitle css-1u6tfqq eu4oa1w0")
        for i in job_titles:
            job_titles_lis.append(i.text.strip())
    except Exception as e:
        pass


while len(all_salary) < len(company_names):
    all_salary.append(None)


data = {'Job Title': job_titles_lis, 'Company Name': company_names, 'Location': locations, 'Salary': all_salary, 'Description': description, 'Post Date': post_date}



pdb.set_trace()
