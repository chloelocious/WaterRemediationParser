import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os

# driver = webdriver.Chrome()

# for page in range(1, 11):

#     search_url = f"https://iopscience.iop.org/nsearch?terms=water+remediation&nextPage=2&previousPage=-1&currentPage={page}&orderBy=relevance&pageLength=50&searchDatePeriod=anytime&journals=1755-1315&journals=1757-899X&journals=2053-1591&journals=0957-4484&journals=1742-6596&journals=1945-7111&journals=2151-2043&journals=0022-3727&journals=1748-9326&journals=0952-4746&journals=2043-6262&journals=2162-8777&journals=0963-0252&journals=0953-8984&journals=1402-4896"
#     driver.get(search_url)

#     search_results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "art-list")))
#     hrefs = []
#     for element in search_results.find_elements_by_class_name("small.art-list-item-meta"):
#         link = element.find_element_by_tag_name("a").get_attribute("href")
#         hrefs.append(link)
#     with open(f"iop_href_links.txt", "a") as f:
#         for href in hrefs:
#             f.write(href + "\n")

# driver.quit()

# import os
# import requests

# with open("/home/ssarrouf/Documents/GitHub/WaterRemediationParser/iop_href_links.txt", "r+") as f:
#     lines = f.readlines()
#     f.seek(0)  # Move the file pointer to the beginning of the file
#     f.truncate()  # Clear the file contents
#     for line in lines:
#         line = line.strip()
#         pdf_link = line + "/pdf"
#         if os.path.isfile(pdf_link) or requests.get(pdf_link).status_code != 200:
#             f.write(line + "\n")
#         else:
#             f.write(pdf_link + "\n")

# from selenium import webdriver
# from selenium.webdriver.common.by import By

# driver = webdriver.Chrome()
# driver.get('https://pubs.acs.org/action/ssostart?redirectUri=%2Fdoi%2F10.1021%2Facsanm.8b01540')

# search_bar = driver.find_element(By.CSS_SELECTOR, 'input.ms-inv')

# search_bar.send_keys('northeastern university')
# search_bar.submit()

# username_field = driver.find_element(By.CSS_SELECTOR, 'input#username.form-element.form-field')
# username_field.send_keys('cowan.chl')
# password_field = driver.find_element(By.CSS_SELECTOR, 'input#password.form-element.form-field')
# password_field.send_keys('your_password')

# submit_button = driver.find_element(By.CSS_SELECTOR, 'button.form-element.form-button')
# submit_button.click()


import os
import requests
import urllib.request
import sys, os


# def override_where():
#     """ overrides certifi.core.where to return actual location of cacert.pem"""
#     # change this to match the location of cacert.pem
#     return os.path.abspath("cacert.pem")

# if hasattr(sys, "frozen"):
#     import certifi.core

#     os.environ["REQUESTS_CA_BUNDLE"] = override_where()
#     certifi.core.where = override_where

#     # delay importing until after where() has been replaced
#     import requests.utils
#     import requests.adapters
#     # replace these variables in case these modules were
#     # imported before we replaced certifi.core.where
#     requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
#     requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# driver = webdriver.Chrome()

# driver.get("https://myiopscience.iop.org/signin?origin=a0&return=https%3A%2F%2Fiopscience.iop.org%2F")

# #login_button = WebDriverWait(driver, 10).until(
# #    EC.element_to_be_clickable((By.XPATH, "//a[@class='c-nav--item'][contains(text(),'Login')]"))
# #)
# #login_button.click()

# username_field = driver.find_element(By.NAME, "username")
# password_field = driver.find_element(By.NAME, "password")

# username_field.send_keys("cowan_chl")
# password_field.send_keys("Ready220!!")

# login_button = driver.find_element(By.NAME, "submit")
# login_button.click()

# pdf_folder = '/home/ssarrouf/Documents/webscrape/to_date_papers/iop'
# os.makedirs(pdf_folder, exist_ok=True)

# # path to the links text file
# links_file = '/home/ssarrouf/Documents/GitHub/WaterRemediationParser/iop_href_links.txt'

# with open(links_file, 'r') as f:
#     links = f.read().splitlines()

# for link in links:
#     pdf_request = requests.get(link, stream=True)
#     if pdf_request.status_code == 200:
#         filename = os.path.join(pdf_folder, f'{link.split("/")[-2].replace("/", "_")}.pdf')
#         with open(filename, 'wb') as f:
#             f.write(pdf_request.content)
#             print(f"PDF file {filename} has been downloaded")
#     else:
#         print(f"Error downloading PDF file from {link}")
import os
import time
import requests
from selenium import webdriver

pdf_folder = "/home/ssarrouf/Documents/webscrape/to_date_papers/iop"
os.makedirs(pdf_folder, exist_ok=True)

# path to the links text file
links_file = '/home/ssarrouf/Documents/GitHub/WaterRemediationParser/scraped_doi_links/iop_href_links.txt'
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": pdf_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(60)

with open(links_file, 'r') as f:
    links = f.read().splitlines()

for link in links:
    driver.get(link)
    try:
        # wait for pdf viewer to load
        pdf_viewer = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "pdf-viewer")))

        # switch to pdf viewer iframe
        driver.switch_to.frame(pdf_viewer.find_element(By.TAG_NAME, "iframe"))

        # wait for download button to be clickable
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/pdf-viewer//viewer-toolbar//div/div[3]/viewer-download-controls//cr-icon-button"))
        )

        # click download button
        download_button.click()
        
        WebDriverWait(driver, 600).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.recaptcha-checkbox-spinner"))
        )
        
        filename = os.path.join(pdf_folder, f'{link.split("/")[-2].replace("/", "_")}.pdf')
        with open(filename, 'wb') as f:
            f.write(driver.find_element(By.TAG_NAME, "iframe").get_attribute("src").split("data:application/pdf;base64,")[1].encode())
            print(f"PDF file {filename} has been downloaded")
        
    except Exception as e:
        print(f"Error downloading PDF file from {link}: {str(e)}")

driver.quit()