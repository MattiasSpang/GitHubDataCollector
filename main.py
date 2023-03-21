from webscraper import WebScraper
import asyncio


async def run_program():
    scraper = WebScraper()
    await scraper.run()

asyncio.run(run_program())