"""
CODE FOR ACS LOGIN CREDENTIALS 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from selenium import webdriver
from selenium.webdriver.common.by import By

launch website
driver = webdriver.Chrome()
driver.get('https://pubs.acs.org/action/ssostart?redirectUri=%2Fdoi%2F10.1021%2Facsanm.8b01540')

search_bar = driver.find_element(By.CSS_SELECTOR, 'input.ms-inv')

login form information
search_bar.send_keys('northeastern university')
search_bar.submit()

wait for the page to load and find the username and password fields
username_field = driver.find_element(By.CSS_SELECTOR, 'input#username.form-element.form-field')
username_field.send_keys('cowan.chl')
password_field = driver.find_element(By.CSS_SELECTOR, 'input#password.form-element.form-field')
password_field.send_keys('your_password')

submit_button = driver.find_element(By.CSS_SELECTOR, 'button.form-element.form-button')
submit_button.click()
"""



"""
CODE FOR WRITING DOI NUMBERS TO TEXT FILE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wget -U "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36" -i acs_dois.txt -P /home/ssarrouf/Documents/webscrape/to_date_papers/acs
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

driver = webdriver.Chrome()  # or your preferred webdriver

with open('/home/ssarrouf/Documents/GitHub/WaterRemediationParser/acs_new_doi_links.txt', 'w') as f:
    for start_page in range(21):
        url = f'https://pubs.acs.org/action/doSearch?AllField=water+remediation&startPage={start_page}&pageSize=100'
        driver.get(url)

        # find all the DOI elements on the page
        doi_elements = driver.find_elements(By.CSS_SELECTOR, 'div.issue-item_metadata > div.issue-item_info > span.issue-item_doi')
        for doi_element in doi_elements:
            doi_match = re.search(r'10\.1021\/[^\s]*', doi_element.text)
            if doi_match:
                doi_value = doi_match.group(0)
                print(doi_value)
                f.write(doi_value + '\n')  # write to file
driver.quit() 
"""


"""
CODE FOR DOWNLOADING PDFS FROM DOI LINKS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pdf folder to save acs files
pdf_folder = '/home/ssarrouf/Documents/webscrape/to_date_papers/acs'
os.makedirs(pdf_folder, exist_ok=True)

DOI links text file
doi_links_file = '/home/ssarrouf/Documents/GitHub/WaterRemediationParser/acs_new_doi_links.txt'

numbers=[]
with open(doi_links_file, 'r') as f:
    doi_links = f.read().splitlines()
    for link in doi_links:
        number = link
        numbers.append(number)

for number in numbers:
    pdf_url = f'https://pubs.acs.org/doi/pdf/{number}'
    pdf_request = requests.get(pdf_url, stream=True, verify='/home/ssarrouf/.local/lib/python3.8/site-packages/certifi/cacert.pem')
    filename = os.path.join(pdf_folder, f'{number.replace("/", "_")}.pdf')
    with open(filename, 'wb') as f:
        f.write(pdf_request.content)
"""

# pdf_dir = '/home/ssarrouf/Documents/webscrape/to_date_papers/acs'
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions
import undetected_chromedriver as uc
uc.TARGET_VERSION = 110

download_dir = '/home/ssarrouf/Documents/webscrape/to_date_papers/acs'
actual_download_dir = '/home/ssarrouf/Documents/webscrape/to_date_papers/new_acs_2'
second_dir = '/home/ssarrouf/Documents/train_data'
third_dir = '/home/ssarrouf/Documents/test_data'

options = ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--disable-audio-output")
options.add_argument("--disable-background-networking")
options.add_argument("--disable-default-apps")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-logging")
options.add_argument("--disable-sync")
options.add_argument("--disable-translate")
options.add_argument("--hide-scrollbars")
options.add_argument("--mute-audio")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")
options.add_argument("--safebrowsing-disable-auto-update")
options.add_argument("--ignore-certificate-errors")
prefs = {"plugins.always_open_pdf_externally": True, "download.default_directory": actual_download_dir}
options.add_experimental_option("prefs", prefs)
options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')

driver = Chrome(options=options)

with open('/home/ssarrouf/Documents/GitHub/WaterRemediationParser/new_dois_missed.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    url = f"https://pubs.acs.org/doi/{line}"
    filename = line.strip().split('/')[-1] + ".pdf"
    file_path = os.path.join(download_dir, filename)
    file_path_2 = os.path.join(second_dir, filename)
    file_path_3 = os.path.join(third_dir, filename)

    if os.path.isfile(file_path) or os.path.isfile(file_path_2) or os.path.isfile(file_path_3):
        print(f"Skipping {line.strip()} since {filename} already exists in {download_dir}")
        continue

    driver.get(url)
    time.sleep(10)

    try:
        # switch to the reCAPTCHA iframe
        #frame = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[starts-with(@name, 'a-') and starts-with(@src, 'https://www.google.com/recaptcha')]")))

        # click the reCAPTCHA checkbox
       #checkbox = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-checkmark")))
        #checkbox.click()
        #pdf_button_1 = driver.find_element(By.CSS_SELECTOR, "a.seamless-access-btn.state-inst-did-not-provide-access")
        #pdf_button_1.click()

        pdf_button = driver.find_element(By.CSS_SELECTOR, "a.button_primary.pdf-button")
        print(pdf_button)
        pdf_button.click()

        time.sleep(10)

        # PDF viewer window
        driver.switch_to.window(driver.window_handles[-1])

        # download the PDF
        download_button = driver.find_element(By.ID, 'download')
        download_button.click()

        time.sleep(10)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        print(f"No PDF button found for {line}")

driver.quit()




