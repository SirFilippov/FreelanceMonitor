from random import randint
import asyncio

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from mongodb import DBManager
from parsers.main import ParseManager
from settings import TELEGA_ADMIN_ID, TELEGA_TOKEN
from kb import kb

bot = Bot(token=TELEGA_TOKEN, parse_mode=ParseMode.HTML)
router = Router()
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)
pars_is_on = False


def format_jobs(jobs: list) -> str:
    formatted_jobs = []
    for counter, (job_url, job_name) in enumerate(jobs, start=1):
        formatted_jobs.append(f'{counter}. <a href="{job_url}">{job_name}</a>')
    formatted_vacancies = '\n'.join(formatted_jobs)
    return formatted_vacancies


@router.message(F.text == "Start Parsing")
async def parser_manager(message: Message) -> None:
    global pars_is_on
    pars_is_on = True
    await message.answer(f'Парсер включен pars_is_on={pars_is_on}')
    await send_msg()


@router.message(F.text == "Stop Parsing")
async def parser_manager(message: Message) -> None:
    global pars_is_on
    pars_is_on = False
    await message.answer(f'Парсер остановлен pars_is_on={pars_is_on}')


async def main() -> None:
    await dp.start_polling(bot)


@router.message(CommandStart())
async def message_handler(message: Message) -> None:
    await message.answer('Привет, начнем?', reply_markup=kb)


async def send_msg():
    while pars_is_on:
        a = ParseManager()
        b = DBManager()

        job_request = await a.run()
        job_request = b.handle_input_jobs(job_request)
        job_request = format_jobs(job_request)
        if job_request:
            await bot.send_message(TELEGA_ADMIN_ID,
                                   job_request,
                                   disable_web_page_preview=True)

        await asyncio.sleep(randint(30, 40))


@router.message(F.text == "Show Current")
async def parser_manager(message: Message) -> None:
    db_connect = DBManager()
    current_jobs = format_jobs(db_connect.tg_current_jobs())
    await message.answer(current_jobs,
                         reply_markup=kb,
                         disable_web_page_preview=True)


if __name__ == "__main__":
    asyncio.run(main())
