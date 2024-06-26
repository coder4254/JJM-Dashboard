import numpy as np
import pandas as pd
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def open_driver():
    driver=webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(20)
    return driver

def open_url(driver):
    url = "https://ejalshakti.gov.in/JJM/Login.aspx?"
    url2 = "https://ejalshakti.gov.in/JJM/JJMReports/Physical/JJMRep_HouseholdTapWaterConnection_D.aspx?StateId=LmYh8%2bZGmQs%3d&StateN=%2fiAQE24FHFC1GvKTiMxE1w%3d%3d&Fin=joOf9Wxy6nf0qdH7vFm42w%3d%3d&DistrictId=gMqMutIC0u0%3d"
    driver.get(url)
    time.sleep(2)
    driver.get(url2)

def scrap_data(driver):
    # Locate the table using XPath
    table = driver.find_element(By.XPATH, '//*[@id="tableReportTable"]')

    # Extract table rows
    rows = []
    for row in table.find_elements(By.XPATH, './/tr')[1:]:  # Skip header row
        cells = row.find_elements(By.XPATH, './/td')
        row_data = [cell.text.strip() for cell in cells]
        rows.append(row_data)

    driver.close()
    return rows

# create a DataFrame
def clean_data(rows):
    df = pd.DataFrame(columns=['District', 'Household', 'PWS_HH', 'HH_Connections', 'New_Connections', 'Private_Connections', 'Total_HH_Connection', 'PWS Connection (%)'])
    for i in range(33):
        dist = rows[2:][i][1]
        HH = rows[2:][i][2]
        pws_HH = rows[2:][i][3]
        conn = rows[2:][i][16]
        new_conn = rows[2:][i][17]
        private = rows[2:][i][18]
        tot_HH = rows[2:][i][19]
        percent = rows[2:][i][20]

        # append to dataframe
        df.loc[i] = [dist, HH, pws_HH, conn, new_conn, private, tot_HH, percent]
    
    # remove useless rows
    df = df[~df['District'].isin(['State Average', 'National Average'])]
    return df

def final_data(df):
    df['Household'] = df['Household'].apply(lambda x: x.replace(',', ''))
    df['Total_HH_Connection'] = df['Total_HH_Connection'].apply(lambda x: x.replace(',', ''))

    df['Household'] = df['Household'].astype(int)
    df['Total_HH_Connection'] = df['Total_HH_Connection'].astype(int)

    df['Connection Coverage (%)'] = round(df['Total_HH_Connection'] / df['Household'] * 100, 2)
    
    df.to_csv('Karnataka_FHTC.csv')
    print("Successfully Saved - Karnataka_FHTC.csv")

# calling all functions linearly
driver = open_driver()
open_url(driver=driver)
rows = scrap_data(driver=driver)
df = clean_data(rows=rows)
final_data(df)