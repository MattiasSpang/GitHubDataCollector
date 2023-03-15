import asyncio
from bs4 import BeautifulSoup
import aiohttp
from ghrepository import GHRepository
import csvHandler

class WebScraper:

    def __init__(self) -> None:
        # settings
        self.start_from: int = 0
        self.save_interval: int = 5000
        self.save_in_seperate_files: bool = False
        self.log: list = []

        # data
        self.urls = []

    def load_urls_from_file(file_path: str, column_containing_url: int) -> list:
        file = open(file_path, "r")

        #for row in file:


    def write_to_file(file_path: str):
        pass

    async def fetch(self,session: aiohttp.ClientSession, url: str) -> GHRepository:
        pass


    async def run(self):

        # --------------------------
        # call view functions here to gather settings info
        # --------------------------

        # prepare a task for every repository
        tasks = []
        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                tasks.append(self.fetch(session, url))

            repositories = await asyncio.gather(*tasks)


    def write_log_to_file():
        pass