from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


# COLLECTING JOB DATA
options = webdriver.ChromeOptions()
options.headless = False  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.glassdoor.ca/Job/canada-software-developer-jobs-SRCH_IL.0,6_IN3_KO7,25.htm")

# move to bottom of page to refresh jobs
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

input("\nReveal to collect jobs. Enter to continue with scrape...")


jobTitles = driver.find_elements(By.CLASS_NAME, "JobCard_jobTitle__GLyJ1")
companies = driver.find_elements(By.CLASS_NAME, "EmployerProfile_compactEmployerName__9MGcV")
locations = driver.find_elements(By.CLASS_NAME, "JobCard_location__Ds1fM")

print(f"\nProgram found {len(jobTitles)} jobs.")

jobData = []
for i in range(len(jobTitles)):
    try:
        salary = driver.find_elements(By.CLASS_NAME, "JobCard_salaryEstimate__QpbTW")[i].text.strip()
    except:
        salary = "N/A"

    jobTitle = jobTitles[i].text.strip() if jobTitles[i].text.strip() else "N/A"
    company = companies[i].text.strip() if companies[i].text.strip() else "N/A"
    location = locations[i].text.strip() if locations[i].text.strip() else "N/A"
    
    jobData.append({
        "Job": jobTitle,
        "Company": company,
        "Location": location,
        "Salary": salary
    })

# DATA CLEANUP
for job in jobData:
    job["Job"] = job["Job"].replace("\n", " ")  
    job["Company"] = job["Company"].replace("\n", " ")  
    job["Location"] = job["Location"].replace("\n", " ")  
    job["Salary"] = job["Salary"].replace("\n", " ")  

input("\nEnter to add data to csv file and complete...")


# JOB DATA TO CSV
import csv

csvFile = "jobData.csv"
headers = ["Job", "Company", "Location", "Salary"]

with open(csvFile, 'w',newline='',encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)

    writer.writeheader()

    for job in jobData:
        writer.writerow(job)

print(f"Job data has been written into {csvFile}")