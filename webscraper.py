import asyncio
from bs4 import BeautifulSoup
import aiohttp
from ghrepository import GHRepository
from csvhandler import CsvHandler
from repositorydataenum import RepositoryData
from datetime import datetime
from random import randint
from view import View
import json
from types import SimpleNamespace

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
        self.remaining_calls_min = 2
        self.token_list = ["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", "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"]

        # settings
        self.wanted_file_name = "temp_name.csv"
        self.file_name = "simplecsv.csv"
        self.delimiter = ";"
        self.nr_of_repos_scraped = 0

        # data
        self.urls: list = []
        self.repo_list: list = []

    # -------------------------------------------------------------- FETCH
    async def fetch(self,session: aiohttp.ClientSession, url: str) -> GHRepository:
        #print("fetching for url: ", url)
        #print("---------------------------------------------------------------------------------")

        repo = GHRepository(url=url)

        repo.data[RepositoryData.HAS_GHA.name] = await self.check_if_has_gha(session=session, url=url)
        
        

        print(await self.get_remaining_calls_rate_limit(session=session))
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
        # Get repo list here
        #---------------------------
        self.repo_list = CsvHandler.readCsvFile(self.file_name, self.delimiter)
        #---------------------------
        # Get urls here
        #---------------------------
        self.extract_urls_from_dict(file_name=self.file_name, delimiter=self.delimiter)

        # prepare a task for every repository

        headers = [RepositoryData.NAME.name, RepositoryData.HAS_GHA.name]
        rows = []
        data_dict = {"header": headers, "rows" : rows}
        CsvHandler.createCsvFile(data=data_dict,wanted_file_name=self.wanted_file_name)

        nr_of_urls_done = 0
        repositories = []
        while True:

            for token in self.token_list:

                if nr_of_urls_done >= len(self.urls):
                    print("breaking for loop, all urls done")
                    break

                req_headers = {
                    "Authorization" : "token " + token
                }
                async with aiohttp.ClientSession(headers=req_headers) as session:
                    for url in self.urls: # make sure to begin where the previous left of.
                        tasks.append(self.fetch(session, url))
                        
                    repositories.extend(await asyncio.gather(*tasks))

                    nr_of_urls_done += len(repositories)
                    
                    print("starting to write csv file...")
                   
                    rows = []
                    for repo in repositories:
                        if isinstance(repo, GHRepository):

                            rows.append(repo.to_csv_row())
                            self.nr_of_repos_scraped += 1
                        else:
                            self.write_to_log("Error: repo is not stored as a GHRepository object.")
                    
                    data_dict = {"rows" : rows}
                    CsvHandler.write_to_csv_file(data=data_dict,file_name=self.wanted_file_name)
                    print("done writing to file!")
            
            if nr_of_urls_done >= len(self.urls):
                break

        self.write_to_log("Repos scraped: " + str(self.nr_of_repos_scraped))
        self.write_to_log("Errors on run: " + str(self.nr_of_errors))
        self.write_to_log("Program Ended")
        self.write_log_to_file()
        print("Finished running web scraping session...")
    # ----------------------------------------------------------------------------- Help functions

    def extract_urls_from_dict(self):
        for row in self.repo_list["rows"]:
            self.urls.append(row[RepositoryData.NAME.value])
            
    def extract_stars_from_dict(self):
        for row in self.repo_list["rows"]:
            self.urls.append(row[RepositoryData.NR_OF_STARS.value])
            

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

    

    async def get_remaining_calls_rate_limit(self, session: aiohttp.ClientSession):
        async with session.get("https://api.github.com/rate_limit") as response:
            json_resp = await response.json()
            replaced_json_resp = str(json_resp).replace("\'", "\"")

            json_object = json.loads(replaced_json_resp, object_hook=lambda d: SimpleNamespace(**d))

            return json_object.resources.core.remaining
            
    async def check_if_has_gha(self, session: aiohttp.ClientSession, url: str) -> bool:
         print("https://api.github.com/repos/"+url+"/actions/workflows")
         async with session.get("https://api.github.com/repos/"+url+"/actions/workflows") as response:
            json_resp = await response.json()
            replaced_json_resp = str(json_resp).replace("\'", "\"")

            json_object = json.loads(replaced_json_resp, object_hook=lambda d: SimpleNamespace(**d))

            print(json_object)

            try:
                if json_object.total_count > 0:
                    return True
                else:
                    return False
            except:
                return False
