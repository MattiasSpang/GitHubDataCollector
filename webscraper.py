import asyncio
from bs4 import BeautifulSoup
import aiohttp
from ghrepository import GHRepository
from csvhandler import CsvHandler
from repositorydataenum import RepositoryData

class WebScraper:

    def __init__(self) -> None:
        # settings
        self.start_from: int = 0
        self.save_interval: int = 5000
        self.save_in_seperate_files: bool = False
        self.log: list = []

        # data
        self.urls: list = []

    async def fetch(self,session: aiohttp.ClientSession, url: str) -> GHRepository:
        print("fetching for url: ", url)
        print("---------------------------------------------------------------------------------")


    async def run(self):

        csv_handler = CsvHandler
        tasks = []
        file_name = "5000csv.csv"
        delimiter = ";"


        # --------------------------
        # call view functions here to gather settings info
        # --------------------------

        #---------------------------
        # Get urls here
        #---------------------------
        input_data = csv_handler.readCsvFile(file_name=file_name, delimiter=delimiter)
        for row in input_data["rows"]:
            self.urls.append(row[RepositoryData.NAME.value])

        # prepare a task for every repository
        
        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                tasks.append(self.fetch(session, url))

            repositories = await asyncio.gather(*tasks)
            print(repositories)


    def write_log_to_file():
        pass