import os
import requests
from bs4 import BeautifulSoup

directory = "/home/ssarrouf/Documents/webscrape/to_date_papers/wiley"

if not os.path.exists(directory):
    os.makedirs(directory)

with open("/home/ssarrouf/Documents/GitHub/WaterRemediationParser/wiley_doi_links_2.txt", "r") as f:
    urls = f.readlines()

for url in urls:
    url = url.strip()  
    url = url.replace("/doi/", "/doi/epdf/")
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    download_link = soup.select_one("#app-navbar > div.btn-group.navbar-right > div.grouped.right > a")["href"]
    
    if download_link is not None:
        download_url = f"https://onlinelibrary.wiley.com{download_link}"
        
        pdf_response = requests.get(download_url)
        
        doi = url.split("/")[-1]
        filename = f"{doi.replace('/', '_')}.pdf"
        filepath = os.path.join(directory, filename)
        
        with open(filepath, "wb") as f:
            f.write(pdf_response.content)
        
        print(f"Downloaded {filename}")
    
    else:
        print(f"Error downloading {url}: could not find download link")
        continue
