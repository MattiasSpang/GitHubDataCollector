import asyncio
from bs4 import BeautifulSoup
import aiohttp
from ghrepository import GHRepository
from csvhandler import CsvHandler
from repositorydataenum import RepositoryData
from datetime import datetime
from random import randint
from view import View

class WebScraper:



    def __init__(self) -> None:
        # settings
        self.start_from: int = 0
        self.save_interval: int = 5000
        self.save_in_seperate_files: bool = False
        self.log: list = []
        self.github_url: str = "https://www.github.com/"
        self.nr_of_errors: int = 0
        self.nr_of_repos_scraped = 1

        # settings
        self.wanted_file_name = "temp_name.csv"
        self.file_name = "simplecsv.csv"
        self.delimiter = ";"
        self.nr_of_repos_scraped = 0

        # data
        self.urls: list = []

    # -------------------------------------------------------------- FETCH
    async def fetch(self,session: aiohttp.ClientSession, url: str) -> GHRepository:
        #print("fetching for url: ", url)
        #print("---------------------------------------------------------------------------------")

        repo = GHRepository(url=url)

        #await self.print_rate_limit(session=session)
        repo.set_url(url=url)
        

        return repo
        
        
    # -------------------------------------------------------------- RUN

    async def run(self):

        self.write_to_log("Program started")
        print("Started running web scraping session.")
        
        tasks = []
        
        # --------------------------
        # call view functions here to gather settings info
        # --------------------------
        self.file_name = View.set_input_file_name()
        self.delimiter = View.set_input_file_delimiter()

        #---------------------------
        # Get urls here
        #---------------------------
        self.extract_urls_from_file(file_name=self.file_name, delimiter=self.delimiter)

        # prepare a task for every repository
        
        #req_headers = {
        #    "Authorization" : "token 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"
        #}
        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                tasks.append(self.fetch(session, url))
                
            repositories = await asyncio.gather(*tasks)
            
            print("starting to write csv file...")
            headers = [RepositoryData.NAME.name, RepositoryData.HAS_GHA.name]
            rows = []
            for repo in repositories:
                if isinstance(repo, GHRepository):

                    rows.append(repo.to_csv_row())
                    self.nr_of_repos_scraped += 1
                else:
                    self.write_to_log("Error: repo is not stored as a GHRepository object.")
            
            data_dict = {"header": headers, "rows" : rows}
            CsvHandler.createCsvFile(data=data_dict,wanted_file_name=self.wanted_file_name)
            print("done writing to file!")
            await self.print_rate_limit(session=session)
        self.write_to_log("Repos scraped: " + str(self.nr_of_repos_scraped))
        self.write_to_log("Errors on run: " + str(self.nr_of_errors))
        self.write_to_log("Program Ended")
        self.write_log_to_file()
        print("Finished running web scraping session...")
    # ----------------------------------------------------------------------------- Help functions

    def extract_urls_from_file(self, file_name, delimiter):
        csv_handler = CsvHandler
        input_data = csv_handler.readCsvFile(file_name=file_name, delimiter=delimiter)
        for row in input_data["rows"]:
            self.urls.append(self.github_url + row[RepositoryData.NAME.value])

    def write_to_log(self, msg: str):
        now = str(datetime.now())
        self.log.append("\n" + "Timestamp: " + now + "  : " +msg) 

    def write_log_to_file(self):
        date = str(datetime.now().date())
        rand_id = randint(1, 999)
        log_file_name = "Log_" + date + "_" + str(rand_id) + ".txt"
        log_file = open(log_file_name, "w+")
        log_file.writelines(self.log)
        print("Wrote to new log file: " + log_file_name)

    async def print_rate_limit(self, session: aiohttp.ClientSession):
        async with session.get("https://api.github.com/rate_limit") as response:
            print("#######################################################################")
            print("reate limit: ")
            print(await response.json())
            print("#######################################################################")
