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

# # Define the directory where the PDF files will be saved
# pdf_dir = '/home/ssarrouf/Documents/webscrape/to_date_papers/acs'

from undetected_chromedriver import Chrome, ChromeOptions
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# pdf folder to save acs files
download_dir = '/home/ssarrouf/Documents/webscrape/to_date_papers/acs'

options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
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
options.add_experimental_option("prefs", {"plugins.always_open_pdf_externally": True})
options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')
options.add_experimental_option('useAutomationExtension', False)
driver = Chrome(options=options)

# read the lines from the text file
with open('input_file.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    url = f"https://pubs.acs.org/doi/{line}"
    
    driver.get(url)
    time.sleep(5)

    try:
        pdf_button = driver.find_element(By.CSS_SELECTOR, 'div.article_header-links.pull-left > a.button_primary.pdf-button')
        pdf_button.click()
        time.sleep(5)

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