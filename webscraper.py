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
        self.repo_index_start_from = 0
        self.repo_index_stop_from = 0

        # data
        self.urls: list = []
        self.stars: list = []
        self.repo_list: list = []

    # -------------------------------------------------------------- FETCH
    async def fetch(self,session: aiohttp.ClientSession, url: str, id: int) -> GHRepository:
        #print("fetching for url: ", url)
        #print("---------------------------------------------------------------------------------")

        repo = GHRepository(url=url)

        repo.data[RepositoryData.HAS_GHA.name] = await self.check_if_has_gha(session=session, url=url)
        repo.data[RepositoryData.MEDIAN_PR_TIME.name] = await self.get_median_pull_request_time_in_seconds(session=session, url=url)
        repo.data[RepositoryData.MEDIAN_ISSUES_TIME.name] = await self.get_median_issues_time_in_seconds(session=session, url=url)
        repo.data[RepositoryData.NR_OF_CONTRIBUTORS.name] = self.extract_contributors_from_dict(id=id)
        repo.data[RepositoryData.NR_OF_STARS.name] = self.extract_stars_from_dict(id=id)
        
        

        #print(await self.get_remaining_calls_rate_limit(session=session))
        return repo
        
        
    # -------------------------------------------------------------- RUN

    async def run(self):

        self.write_to_log("Program started")
        print("Started running web scraping session.")
        
        #tasks = []
        
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
        self.extract_urls_from_dict()


        # prepare a task for every repository

        headers = [RepositoryData.NAME.name, RepositoryData.HAS_GHA.name, RepositoryData.MEDIAN_PR_TIME.name, RepositoryData.MEDIAN_ISSUES_TIME.name, RepositoryData.NR_OF_CONTRIBUTORS.name, RepositoryData.NR_OF_STARS.name]
        rows = []
        data_dict = {"header": headers, "rows" : rows}
        CsvHandler.createCsvFile(data=data_dict,wanted_file_name=self.wanted_file_name)

        nr_of_urls_done = 0
        repositories = []

        for token in self.token_list:
            tasks = []

            req_headers = {
                "Authorization" : "token " + token
            }
            async with aiohttp.ClientSession(headers=req_headers) as session:
                if nr_of_urls_done >= len(self.urls):
                    print("breaking for loop, all urls done")
                    break

                current_rate_limit = await self.get_remaining_calls_rate_limit(session=session)
                print("current rate limit: ", current_rate_limit)
                repo_capacity = (current_rate_limit/len(headers)-1) - len(headers)-1 # this is for the for loop. we only loop through this amount.
                
                if nr_of_urls_done > 0:
                    nr_of_urls_done + 1
                length_of_urls = len(self.urls)
                loop_index = 0
                if length_of_urls > repo_capacity:
                    loop_index = nr_of_urls_done + repo_capacity
                else:
                    loop_index = length_of_urls

                print("###########################" + str(loop_index))
                for i in range(int(nr_of_urls_done),int(loop_index)): 
                    tasks.append(asyncio.create_task(self.fetch(session, self.urls[i], i)))
                    
                #repositories.extend(await asyncio.gather(*tasks))
                completed_tasks, pending_tasks = await asyncio.wait(tasks)

                for task in completed_tasks:
                    repositories.append(task.result())

                nr_of_urls_done += loop_index
                
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
                print(await self.get_remaining_calls_rate_limit(session=session))
        
        self.write_to_log("Repos scraped: " + str(self.nr_of_repos_scraped))
        self.write_to_log("Errors on run: " + str(self.nr_of_errors))
        self.write_to_log("Program Ended")
        self.write_log_to_file()
        print("Finished running web scraping session...")
    # ----------------------------------------------------------------------------- Help functions

    def extract_urls_from_dict(self):
        for row in self.repo_list["rows"]:
            self.urls.append(row[RepositoryData.NAME.value])
            
    def extract_stars_from_dict(self, id: int) -> int:
        return self.repo_list["rows"][id][RepositoryData.NR_OF_STARS.value]
            
    def extract_contributors_from_dict(self, id: int) -> int:
        return self.repo_list["rows"][id][RepositoryData.NR_OF_CONTRIBUTORS.value]
        

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
        async with session.get("https://api.github.com/rate_limit", ssl=False) as response:
            json_resp = await response.json()
            replaced_json_resp = str(json_resp).replace("\'", "\"")

            json_object = json.loads(replaced_json_resp, object_hook=lambda d: SimpleNamespace(**d))

            return json_object.resources.core.remaining
            
    async def check_if_has_gha(self, session: aiohttp.ClientSession, url: str) -> bool:
         #print("https://api.github.com/repos/"+url+"/actions/workflows")
         async with session.get("https://api.github.com/repos/"+url+"/actions/workflows", ssl=False) as response:
            json_resp = json.dumps(await response.json())

            json_object = json.loads(json_resp, object_hook=lambda d: SimpleNamespace(**d))

            try:
                if json_object.total_count > 0:
                    return True
                else:
                    return False
            except:
                return False
            
    async def get_median_pull_request_time_in_seconds(self, session: aiohttp.ClientSession, url: str) -> float:

        async with session.get("https://api.github.com/repos/"+url+"/pulls?state=closed&per_page=100", ssl=False) as response:
            json_resp = json.dumps(await response.json())

            json_object = json.loads(json_resp, object_hook=lambda d: SimpleNamespace(**d))
            number_of_closed_pulls = 0
            total_seconds = 0
            try: #this try is here because the json object has no lenght sometimes and crashes, find a better solution
                if len(json_object) > 0:
                    for issue in json_object:
                        if issue.closed_at != None:
                            number_of_closed_pulls += 1
                            format_string = '%Y-%m-%dT%H:%M:%SZ'
                            created_at = datetime.strptime(issue.created_at, format_string)
                            closed_at = datetime.strptime(issue.closed_at, format_string)
                            duration = closed_at - created_at
                            seconds = duration.total_seconds()
                            total_seconds += seconds
                    median = total_seconds/number_of_closed_pulls
                    return median
                return 0
            except:
                return 0
        
    async def get_median_issues_time_in_seconds(self, session: aiohttp.ClientSession, url: str) -> float:

        print(url)
        async with session.get("https://api.github.com/repos/"+url+"/issues?state=closed&per_page=100", ssl=False) as response:
            json_resp = json.dumps(await response.json())

            json_object = json.loads(json_resp, object_hook=lambda d: SimpleNamespace(**d))
            number_of_closed_issues = 0
            total_seconds = 0
            try: #this try is here because the json object has no lenght sometimes and crashes, find a better solution
                
                if len(json_object) > 0:
                    for issue in json_object:
                        if issue.closed_at != None:
                            number_of_closed_issues += 1
                            format_string = '%Y-%m-%dT%H:%M:%SZ'
                            created_at = datetime.strptime(issue.created_at, format_string)
                            closed_at = datetime.strptime(issue.closed_at, format_string)
                            duration = closed_at - created_at
                            seconds = duration.total_seconds()
                            total_seconds += seconds
                    median = total_seconds/number_of_closed_issues
                    return median
                return 0
            except:
                self.write_to_log(url + "   : Json object cannot be compared to an integer")
                return 0
            
    # async def get_contributors(self, session: aiohttp.ClientSession, url: str) -> int:

    #     print(url)
    #     async with session.get("https://api.github.com/repos/"+url+"/contributors?per_page=100&anon=true", ssl=False) as response:
    #         resp = await response.json()
            
    #         try:
    #             if type(resp) == list:
    #                 return len(resp)
    #             else:
    #                 return 0
    #         except:
    #             self.write_to_log(url + "   : Trouble getting the reposonse for nr of contributors")
    #             return 0
