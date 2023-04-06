import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random

start_page = 0
end_page = 99

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--disable-web-security')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--log-level=3')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.3',
]

chromedriver_path = '/home/ssarrouf/Downloads/chromedriver'  

driver = uc.Chrome(executable_path=chromedriver_path, options=options)

with open('wiley_doi_links_2.txt', 'a') as f:
        url = f'https://onlinelibrary.wiley.com/action/doSearch?AfterYear=2000&AllField=water+remediation&BeforeYear=2023&content=articlesChapters&startPage=99&target=default&pageSize=20'

        user_agent = random.choice(user_agents)
        headers = {'User-Agent': user_agent}

        time.sleep(40)

        driver.get(url)
        time.sleep(random.uniform(0.5, 1.5))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = soup.find_all('a', class_='publication_title visitable')
        for link in links:
            f.write(f"https://onlinelibrary.wiley.com{link.get('href')}\n")

driver.quit()
