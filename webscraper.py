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
from logger import Logger
import time

class WebScraper:


    def __init__(self) -> None:
        # settings
        self.start_from: int = 0
        self.save_interval: int = 5000
        self.save_in_seperate_files: bool = False
        self.logger = Logger()
        self.github_url: str = "https://www.github.com/"
        self.nr_of_errors: int = 0
        self.nr_of_repos_scraped = 1
        self.remaining_calls_min = 2
        self.token_list = ["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", "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"]

        # settings
        self.wanted_file_name = "temp_name.csv"
        self.file_name = "simplecsv.csv"
        self.delimiter = ","
        self.nr_of_repos_scraped = 0
        self.repo_index_start_from = 0
        self.repo_index_stop_from = 0
        self.nr_of_api_calls = 4

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
        repo.data[RepositoryData.TOTAL_PR.name] = self.extract_total_pr_from_dict(id=id)
        repo.data[RepositoryData.MEDIAN_ISSUES_TIME.name] = await self.get_median_issues_time_in_seconds(session=session, url=url)
        repo.data[RepositoryData.TOTAL_ISSUES.name] = self.extract_total_issues_from_dict(id=id)
        repo.data[RepositoryData.NR_OF_CONTRIBUTORS.name] = self.extract_contributors_from_dict(id=id)
        repo.data[RepositoryData.NR_OF_STARS.name] = self.extract_stars_from_dict(id=id)
        repo.data[RepositoryData.MAIN_LANGUAGE.name] = self.extract_main_programming_lang_from_dict(id=id)
        
        contributors = await self.get_contributons_from_top_ten_users(session=session, url=url)
        for index, user in enumerate(contributors):
            contributor_name = "CONTRIBUTOR_" + str(index +1)
            repo.data[contributor_name] = user

        
        
        

        #print(await self.get_remaining_calls_rate_limit(session=session))
        return repo
        
        
    # -------------------------------------------------------------- RUN

    async def run(self):

        view = View()

        self.logger.write_to_log("Program started")
        print("Started running web scraping session.")
        
        #tasks = []
        
        # --------------------------
        # call view functions here to gather settings info
        # --------------------------
        self.file_name = view.set_input_file_name()
        self.delimiter = view.set_input_file_delimiter()

        settings = view.enter_settings()
        self.repo_index_start_from = settings["startline"]
        self.repo_index_stop_from = settings["endline"]
        self.wanted_file_name = settings["filename"]

        print("///////" + str(self.repo_index_start_from), " : " + str(self.repo_index_stop_from))
        #---------------------------
        # Get repo list here
        #---------------------------
        self.repo_list = CsvHandler.readCsvFile(self.file_name, self.delimiter)
        #---------------------------
        # Get urls here
        #---------------------------
        self.extract_urls_from_dict()


        # prepare a task for every repository

        headers = [RepositoryData.NAME.name, 
                   RepositoryData.HAS_GHA.name, 
                   RepositoryData.MEDIAN_PR_TIME.name,
                     RepositoryData.TOTAL_PR.name, 
                     RepositoryData.MEDIAN_ISSUES_TIME.name, 
                     RepositoryData.TOTAL_ISSUES.name, 
                     RepositoryData.NR_OF_CONTRIBUTORS.name, 
                     RepositoryData.NR_OF_STARS.name,
                     RepositoryData.MAIN_LANGUAGE.name,
                     RepositoryData.CONTRIBUTOR_1.name,
                     RepositoryData.CONTRIBUTOR_2.name,
                     RepositoryData.CONTRIBUTOR_3.name,
                     RepositoryData.CONTRIBUTOR_4.name,
                     RepositoryData.CONTRIBUTOR_5.name,
                     RepositoryData.CONTRIBUTOR_6.name,
                     RepositoryData.CONTRIBUTOR_7.name,
                     RepositoryData.CONTRIBUTOR_8.name,
                     RepositoryData.CONTRIBUTOR_9.name,
                     RepositoryData.CONTRIBUTOR_10.name
                     ]
        rows = []
        data_dict = {"header": headers, "rows" : rows}
        CsvHandler.createCsvFile(data=data_dict,wanted_file_name=self.wanted_file_name)

        nr_of_urls_done = self.repo_index_start_from
        if self.repo_index_stop_from <= 0:
            length_of_urls = len(self.urls)
        else:
            length_of_urls = self.repo_index_stop_from
        repositories = []
        done = False
        while True:
            reset_time = 0
        
            for token in self.token_list:
                tasks = []

                req_headers = {
                    "Authorization" : "token " + token
                }
                async with aiohttp.ClientSession(headers=req_headers) as session:
                    self.logger.write_to_log("Starting new session")
                    if nr_of_urls_done >= length_of_urls:
                        print("breaking for loop, all urls done")
                        done = True
                        break

                    current_rate_limit = await self.get_remaining_calls_rate_limit(session=session)
                    self.logger.write_to_log("current rate limit: " + str(current_rate_limit))
                    repo_capacity = (current_rate_limit/self.nr_of_api_calls) - self.nr_of_api_calls # this is for the for loop. we only loop through this amount.
                    self.logger.write_to_log("Token repo capacity is: " + str(repo_capacity))
                    print("calls_left: " + str(current_rate_limit))
                    print("repo_capacity: " + str(repo_capacity))
                    print("nr_of_urls_done: " + str(nr_of_urls_done))
                    if nr_of_urls_done > 0:
                        nr_of_urls_done + 1
                    if repo_capacity < 1:
                        continue
                    #length_of_urls = len(self.urls)
                    loop_index = 0
                    if length_of_urls - nr_of_urls_done > repo_capacity:
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
                        nr_of_urls_done += 1
                    

                    print("starting to write csv file...")
                    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&" + str(nr_of_urls_done))
                    rows = []
                    for repo in repositories:
                        if isinstance(repo, GHRepository):

                            rows.append(repo.to_csv_row())
                            self.nr_of_repos_scraped += 1
                        else:
                            self.logger.write_to_log("Error: repo is not stored as a GHRepository object.")
                    
                    data_dict = {"rows" : rows}
                    CsvHandler.write_to_csv_file(data=data_dict,file_name=self.wanted_file_name)
                    print("done writing to file!")
                    print(await self.get_remaining_calls_rate_limit(session=session))
                    reset_time = float(await self.get_token_refresh_time(session=session))

                    if nr_of_urls_done >= len(self.urls):
                        print("breaking for loop, all urls done")
                        done = True
                        break

            if done:
                self.logger.write_to_log("urls done after run: " + str(self.nr_of_repos_scraped))
                break

            current_time = time.time()
            self.logger.write_to_log("wating for rate limit reset time  :  seconds:  " + str((reset_time - current_time)))
            print("sleeping for: " + str(reset_time - current_time) + " seconds.")
            time.sleep((reset_time - current_time))

            
        self.logger.write_to_log("Repos scraped: " + str(self.nr_of_repos_scraped))
        self.logger.write_to_log("Errors on run: " + str(self.nr_of_errors))
        self.logger.write_to_log("Program Ended")
        self.logger.write_log_to_file()
        print("Finished running web scraping session...")
    # ----------------------------------------------------------------------------- Help functions

    def extract_urls_from_dict(self):
        for row in self.repo_list["rows"]:
            self.urls.append(row[RepositoryData.NAME.value])
            
    def extract_stars_from_dict(self, id: int) -> int:
        return self.repo_list["rows"][id][RepositoryData.NR_OF_STARS.value]
            
    def extract_contributors_from_dict(self, id: int) -> int:
        return self.repo_list["rows"][id][RepositoryData.NR_OF_CONTRIBUTORS.value]
    
    def extract_total_issues_from_dict(self, id: int) -> int:
        return self.repo_list["rows"][id][RepositoryData.TOTAL_ISSUES.value]
    
    def extract_total_pr_from_dict(self, id: int) -> int:
        return self.repo_list["rows"][id][RepositoryData.TOTAL_PR.value]
    
    def extract_main_programming_lang_from_dict(self, id: int) -> str:
        return self.repo_list["rows"][id][RepositoryData.MAIN_LANGUAGE.value]
        
    async def get_remaining_calls_rate_limit(self, session: aiohttp.ClientSession):
        async with session.get("https://api.github.com/rate_limit", ssl=False) as response:
            json_resp = await response.json()
            replaced_json_resp = str(json_resp).replace("\'", "\"")

            json_object = json.loads(replaced_json_resp, object_hook=lambda d: SimpleNamespace(**d))

            return json_object.resources.core.remaining
        
    async def get_token_refresh_time(self, session: aiohttp.ClientSession):
        async with session.get("https://api.github.com/rate_limit", ssl=False) as response:
            json_resp = json.dumps(await response.json())

            json_object = json.loads(json_resp, object_hook=lambda d: SimpleNamespace(**d))



            return json_object.resources.core.reset
            
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

            json_object = json.loads(json_resp)
            number_of_closed_pulls = 0
            total_seconds = 0
            try: #this try is here because the json object has no lenght sometimes and crashes, find a better solution
                if len(json_object) > 0:
                    for issue in json_object:
                        if issue["closed_at"] != None:
                            number_of_closed_pulls += 1
                            format_string = '%Y-%m-%dT%H:%M:%SZ'
                            created_at = datetime.strptime(issue["created_at"], format_string)
                            closed_at = datetime.strptime(issue["closed_at"], format_string)
                            duration = closed_at - created_at
                            seconds = duration.total_seconds()
                            total_seconds += seconds
                    median = total_seconds/number_of_closed_pulls
                    return median
                return 0
            except:
                return 0
        
    async def get_median_issues_time_in_seconds(self, session: aiohttp.ClientSession, url: str) -> float:

        #print(url)
        async with session.get("https://api.github.com/repos/"+url+"/issues?state=closed&per_page=100", ssl=False) as response:
            json_resp = json.dumps(await response.json())

            json_object = json.loads(json_resp)
            number_of_closed_issues = 0
            total_seconds = 0
            try: #this try is here because the json object has no lenght sometimes and crashes, find a better solution
                
                if len(json_object) > 0:
                    for issue in json_object:
                        if issue["closed_at"] != None:
                            number_of_closed_issues += 1
                            format_string = '%Y-%m-%dT%H:%M:%SZ'
                            created_at = datetime.strptime(issue["created_at"], format_string)
                            closed_at = datetime.strptime(issue["closed_at"], format_string)
                            duration = closed_at - created_at
                            seconds = duration.total_seconds()
                            total_seconds += seconds
                    median = total_seconds/number_of_closed_issues
                    return median
                return 0
            except Exception as e:
                self.logger.write_to_log(url + "  ERROR: " + str(e) + "   : Trouble with getting issues closed time")
                return 666
            
    
    
    async def get_contributons_from_top_ten_users(self, session: aiohttp.ClientSession, url: str) -> list:

         #print(url)
         async with session.get("https://api.github.com/repos/"+url+"/contributors?per_page=10&anon=true", ssl=False) as response:
             resp = await response.json()
             try:
                 if type(resp) == list:
                     user_list = []
                     for user in resp:
                         user_list.append(user["contributions"])
                     for index in range(len(resp) + 1, 10 ):
                         user_list.append("No contributor")
                         
                     return user_list
                 else:
                     return ["Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list"]
             except:
                 self.logger.write_to_log(url + "   : Trouble getting the reposonse for top 10 contributions")
                 return ["Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list",
                             "Response not a list"]

