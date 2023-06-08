import os
import time
import cloudscraper

def get_latest_file(path):
    files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    files.sort(key=lambda x: os.path.getmtime(x))

    # if the list is not empty, return the name of the most recent file
    if files:
        return files[-1]

# use a CloudScraper instance
scraper = cloudscraper.create_scraper()
scraper.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
})

download_directory = r"/home/ssarrouf/Documents/webscrape/to_date_papers/iop"

downloaded_files = os.listdir(download_directory)

with open('/home/ssarrouf/Documents/GitHub/WaterRemediationParser/scraped_doi_links/iop_href_links_2.txt', 'r') as f:
    for line in f:
        url = line.strip()
        # get the DOI part after 'pdfdirect/'
        doi = url.split('article/')[1]

        doi_renamed = doi.replace('/', '_')

        new_file_name = os.path.join(download_directory, doi_renamed + '.pdf')

        # check if the file already exists in the download directory
        if doi_renamed + '.pdf' in downloaded_files:
            print(f"File {new_file_name} already downloaded.")
            continue 

        response = scraper.get(url, stream=True)

        # check if the request was successful and the content is a PDF
        if response.status_code == 200 and response.headers['Content-Type'] == 'application/pdf':
            with open(new_file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
        else:
            print(f"Failed to download {url}")
        
        time.sleep(30) 

