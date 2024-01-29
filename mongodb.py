from datetime import datetime
from pymongo import MongoClient
from settings import MONGO_HOST, MONGO_PORT


# current_jobs


class DBManager:
    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client.freelance_monitor

    def handle_input_jobs(self, requested_jobs: list) -> list:
        """Записывает и возвращает только новые заявки в базу данных"""

        current_jobs_urls = [job['url'] for job in self.read_current_jobs()]
        requested_jobs_urls = {job['url'] for job in requested_jobs}
        new_jobs = []

        # Удаляем уже несуществующие заявки
        for job_url in current_jobs_urls:
            if job_url not in requested_jobs_urls:
                print(f'Удалена заявка: {job_url}')
                self.db.current_jobs.delete_one({'url': job_url})

        # Заносим новые заявки
        for job in requested_jobs:
            if job['url'] not in current_jobs_urls:
                job['add_date'] = datetime.now()
                new_jobs.append((job['url'], job['name']))
                self.db.current_jobs.insert_one(job)

        return new_jobs

    def read_current_jobs(self) -> list:
        """Читает текущие заявки из базы данных"""

        current_jobs = list(self.db.current_jobs.find({}, {"_id": 0, "url": 1, "name": 1}).sort("add_date", -1))

        return current_jobs


if __name__ == '__main__':
    a = DBManager()
    b = {'url': 'мочsswа',
         'name': 'asd',
         'mmm': 'asdww'}
    # a.rewrite_current_jobs(b)
    print(a.read_current_jobs())
