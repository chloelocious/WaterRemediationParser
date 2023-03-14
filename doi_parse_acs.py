from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request
import re

# location of the Chrome driver
driver = webdriver.Chrome(executable_path='/home/ssarrouf/Downloads/chromedriver')
driver.get('https://pubs.acs.org/')

# submit login information
login_button = driver.find_element(By.CSS_SELECTOR, 'a[href="https://pubs.acs.org/action/ssoRequestForLoginPage"]')
login_button.click()

username_field = driver.find_element(By.CSS_SELECTOR, 'input#userid.input-user-name')
username_field.send_keys('cowan_chl')

password_field = driver.find_element(By.CSS_SELECTOR, 'input#password.input-password')
password_field.send_keys('q3BxdLpeygt-Z@6')

login_button = driver.find_element(By.CSS_SELECTOR, 'input.btn.btn-block.btn-yellow')
login_button.click()

# loop through pages
dois = []

for page_num in range(0, 21):
    search_page_url = 'https://pubs.acs.org/action/doSearch?field1=AllField&text1=water+remediation&field2=AllField&text2=&ConceptID=&ConceptID=&publication=&accessType=allContent&Earliest=&Earliest=&AfterMonth=1&AfterYear=2000&BeforeMonth=1&BeforeYear=2023&startPage={}&pageSize=100'.format(page_num)
    driver.get(search_page_url)

    # get the HTML content after login
    html_content = driver.page_source

    # find the abstracts and DOIs
    doi_matches = re.findall('<div class="issue-item_info">.*?<span>DOI: </span>(.*?)</div>', html_content, re.DOTALL)
    for doi_match in doi_matches:
        dois.append(doi_match.strip())


# write the DOIs to a file
with open('acs_dois.txt', 'w') as f:
    for doi in dois:
        f.write(doi + '\n')

# close the browser window
driver.quit()
