import asyncio
import time
from itertools import chain

from playwright.async_api import async_playwright
from fake_useragent import UserAgent

from parsers.kwork import Kwork
from parsers.fl import Fl
from mongodb import DBManager


class ParseManager:
    def __init__(self):
        self.user_agent = UserAgent().random
        self.parsers = (Kwork, Fl)

    async def run(self):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=False)
            context = await browser.new_context(
                ignore_https_errors=True,
                user_agent=self.user_agent)

            pages = [await context.new_page() for _ in range(len(self.parsers))]
            jobs = [parser(browser_page).main() for browser_page, parser in zip(pages, self.parsers)]
            jobs = await asyncio.gather(*jobs)
            jobs = list(chain.from_iterable(jobs))
            return jobs


if __name__ == "__main__":
    a = ParseManager()
    b = DBManager()
    while True:
        res = asyncio.run(a.run())
        b.handle_input_jobs(res)
        time.sleep(60)
