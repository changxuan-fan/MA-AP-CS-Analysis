from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import time
import pandas as pd

# Set the download directory path
download_directory = os.path.expanduser("~/范昌轩/Boston University/CS 506/Dataset")

# Configure Chrome options for downloads
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": download_directory}
chrome_options.add_experimental_option("prefs", prefs)

# Launch Chrome with specified options
driver = webdriver.Chrome(options=chrome_options)

# URL of the website
url = "https://profiles.doe.mass.edu/statereport/ap.aspx"
driver.get(url)

# Select the years
years = ["2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008", "2007"]
subject_value = "COMSCA"

# Define student groups
student_groups = {
    'ALL': 'All Students',
    'LEP': 'English Learner',
    'ECODIS': 'Economically Disadvantaged',
    'LOWINC': 'Low Income',
    'SPED': 'Students with Disabilities',
    'HIGH': 'High Needs',
    'F': 'Female',
    'M': 'Male',
    'AI': 'Amer. Ind. or Alaska Nat.',
    'AS': 'Asian',
    'BL': 'Afr. Amer or Black',
    'HS': 'Hispanic or Latino',
    'MR': 'Multi-race, Non-Hisp. or Lat.',
    'HP': 'Nat. Haw. or Pacif. Isl.',
    'WH': 'White'
}

for year_option in years:
    # Select the year
    year_dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddYear")
    year_dropdown.send_keys(year_option)

    # Select the subject
    subject_dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddSubject")
    subject_dropdown.send_keys(subject_value)

    for group_abbr, group in student_groups.items():
        # Select the student group
        student_group_dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddStudentGroup")
        student_group_dropdown.send_keys(group_abbr)

        # Click the "View Report" button
        view_report_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnViewReport")
        view_report_button.click()

        # Click the "Export" button
        export_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_spExport")
        export_button.click()

        # Wait for the download to complete
        file_path = os.path.join(download_directory, 'ap_performance.xlsx')
        while not os.path.exists(file_path):
            time.sleep(1)

        # Create the year-specific folder if it doesn't exist
        os.makedirs(os.path.join(download_directory, year_option), exist_ok=True)

        # Define the paths
        excel_file = os.path.join(download_directory, "ap_performance.xlsx")
        csv_file = os.path.join(download_directory, year_option, f"{year_option[2:]}_AP_CS_Performance_{group}.csv")

        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(excel_file)

        # Save the DataFrame to a CSV file
        df.to_csv(csv_file, index=False)

        # Delete the file
        os.remove(excel_file)

        # Go back to the main page to start a new iteration
        driver.back()

# Close the webdriver
driver.quit()
