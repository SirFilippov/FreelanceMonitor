import asyncio

from playwright._impl._errors import TimeoutError
from bs4 import BeautifulSoup as BSoup
from playwright.async_api import async_playwright
from fake_useragent import UserAgent


class Fl:
    def __init__(self, page):
        self.page = page

    async def main(self):
        print('Начинаю парсить fl')
        jobs = []
        pages_htmls = await self.export_pages_htmls()

        for page_html in pages_htmls:
            for job in self.parse_page(page_html):
                jobs.append(job)

        for i in jobs:
            print(f'{i["name"]}: {i["url"]}')

        print(f'Распарсил fl: {len(jobs)}')
        return jobs
    
    async def export_pages_htmls(self):
        pages_htmls = []
        count = 0
        url = 'https://www.fl.ru/projects/?kind=1#'

        await self.page.goto(url)

        category_field = self.page.locator('//*[@id="vs1__combobox"]/div[1]/input')
        special_field = self.page.locator('//*[@id="vs2__combobox"]/div[1]/input')
        apply_button = self.page.locator('//*[@id="project-filter"]/button[1]/div')

        await category_field.fill('Программирование')
        await category_field.press('Enter')

        await asyncio.sleep(0.5)

        await special_field.fill('Парсинг данных')
        await special_field.press('Enter')

        await apply_button.click()

        try:
            await self.page.wait_for_load_state(state='networkidle', timeout=10000)
        except TimeoutError:
            pass

        while True:
            count += 1
            print(f'Текущая страница: {count}')
            pages_htmls.append(await self.page.content())
            next_page_link = self.page.locator('//*[@id="PrevLink"]')

            if not await next_page_link.is_visible():
                break

            await next_page_link.click()

            try:
                await self.page.wait_for_load_state(state='networkidle', timeout=10000)
            except TimeoutError:
                pass
    
        return pages_htmls

    @staticmethod
    def parse_page(page_html: str):
        page_soup = BSoup(page_html, 'lxml')
        job_stacks = page_soup.find(id='projects-list').find_all('div', recursive=False)[:-2]
    
        for job_stack in job_stacks:
            if 'Исполнитель определён' not in job_stack.text:
                job_tag = job_stack.find('a', class_='text-dark text-decoration-none link-hover-danger cursor-pointer')
                job_name = job_tag.text
                job_url = 'https://www.fl.ru' + job_tag['href']
                job = {'name': job_name,
                       'url': job_url}

                yield job


if __name__ == '__main__':
    user_agent = UserAgent().random


    async def creater():
        while True:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=True)
                context = await browser.new_context(
                    ignore_https_errors=True,
                    user_agent=user_agent)
                browser_page = await context.new_page()
                a = Fl(browser_page)
                return await a.main()

    async def mainmain():
        while True:
            await creater()
            await asyncio.sleep(20)

    asyncio.run(mainmain())
