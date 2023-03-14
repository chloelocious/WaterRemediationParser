from batterydataextractor.scrape.acs import ACSWebScraper
from crossref.restful import Works


if __name__ == "__main__":
    query = "water remediation"
    file_location = r"/home/ssarrouf/Documents/webscrape/to_date_papers/acs/"

    afterMonth = 1
    afterYear = 2000
    beforeMonth = 1
    beforeYear = 2023
    for start in range(0, 1000, 100):
        main(query=query, afterMonth=afterMonth, afterYear=afterYear, beforeMonth=beforeMonth,
        beforeYear=beforeYear, file_location=file_location, start=start)