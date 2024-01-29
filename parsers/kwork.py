import asyncio

from playwright.async_api import async_playwright
from bs4 import BeautifulSoup as BSoup
from fake_useragent import UserAgent


class Kwork:
    def __init__(self, page):
        self.page = page

    async def main(self):
        jobs = []
        pages_htmls = await self.export_pages_htmls()
        for page_html in pages_htmls:
            for job in self.parse_page(page_html):
                jobs.append(job)

        return jobs

    async def export_pages_htmls(self):
        url = 'https://kwork.ru/projects?c=41&attr=211'
        pages_htmls = []

        await self.page.goto(url)
        await self.page.wait_for_load_state(state='domcontentloaded')

        while True:
            pages_htmls.append(await self.page.content())
            next_page_link = await self.page.query_selector('a.next')
            if next_page_link is None:
                break

            await next_page_link.click()
            await self.page.wait_for_load_state(state='domcontentloaded')

        return pages_htmls

    @staticmethod
    def parse_page(page_html: str = None):
        page_soup = BSoup(page_html, 'lxml')
        job_stacks = page_soup.find(class_='project-list position-relative').find('div').find_all('div', recursive=False)

        for job_stack in job_stacks:
            job_tag = job_stack.find('a')
            job_name = job_tag.text
            job_url = 'https://kwork.ru/' + job_tag['href']
            job = {'name': job_name,
                   'url': job_url}
            yield job
    #
    #     return jobs


if __name__ == '__main__':
    user_agent = UserAgent().random

    async def creater():
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=False)
            context = await browser.new_context(
                ignore_https_errors=True,
                user_agent=user_agent)
            browser_page = await context.new_page()
            a = Kwork(browser_page)
            return await a.main()

    asyncio.run(creater())


