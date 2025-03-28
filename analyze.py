import pandas as pd 
import re

df = pd.read_csv('jobData.csv')


# SALARY CONVERSION
def clean_salary(salary):
    if salary == "N/A":
        return None
    
    salary = str(salary)
    salary = salary.replace("$", "").strip()

    numbers = re.findall(r'\d+', salary)
    

    if not numbers:
        return None

    if "-" in salary:
        if "K" in salary:
            low, high = int(numbers[0]), int(numbers[1])
            return ((low + high) / 2) * 1000
        else:
            low, high = int(numbers[0]), int(numbers[2])
            return ((low + high) / 2) * 2080 # CONVERT HOURLY TO APPROXIMATE ANNUAL SALARY (ASSUMING 40 HOURS A WEEK, 52 WEEKS A YEAR)
        
    if "K" in salary:
        if numbers:
            return int(numbers[0]) * 1000
        
    if "Per hour" in salary or "hour" in salary:
        if numbers:
            return int(numbers[0]) * 2080
    
    return None

df["Cleaned Salary"] = df["Salary"].apply(clean_salary)


#ANALYSIS

# AVERAGE SALARY BY JOB TITLE
averageSalaryByJob = df.groupby('Job')['Cleaned Salary'].mean().sort_values(ascending=False).dropna()
print(averageSalaryByJob)

# TOP 5 AND LOWEST 5 PAYING BY JOB TITLE
highestTen = averageSalaryByJob.head(5)
lowestTen = averageSalaryByJob.dropna().tail(5)
print("\nTop 5: ")
print(highestTen)
print("\nBottom 5: ")
print(lowestTen)

# AVERAGE SALARY BY JOB TITLE
averageSalaryByLocation = df.groupby('Location')['Cleaned Salary'].mean().sort_values(ascending=False).dropna()
print(f"\n{averageSalaryByLocation}")

df.to_csv('JobDataWithCleanedSalary.csv', index=False)

import csv

csvFile = "AverageSalaryByJob.csv"
headers = ["Job", "Average Salary"]
with open(csvFile, 'w',newline='',encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    for job, averageSalary in averageSalaryByJob.items():
        writer.writerow({
            "Job" : job,
            "Average Salary" : averageSalary
        })

csvFile1 = "AverageSalaryByLocation.csv"
headers = ["Location", "Average Salary"]

with open(csvFile1, 'w',newline='',encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    for location, averageSalary in averageSalaryByLocation.items():
        writer.writerow({
            "Location" : location,
            "Average Salary" : averageSalary
        })

