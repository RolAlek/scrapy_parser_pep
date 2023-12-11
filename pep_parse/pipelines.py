import csv
import datetime as dt
import os

from pep_parse.settings import BASE_DIR


class PepParsePipeline:
    """
    Обработка полученных данных и сохранение результата в results.
    Считает количество PEP в зависимости от статуса. Обобщает результат.
    """

    def open_spider(self, spider):
        current_datetime = dt.datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'status_summary_{formatted_datetime}.csv'
        RESULTS_DIR = BASE_DIR / 'results'
        os.makedirs(RESULTS_DIR, exist_ok=True)
        file_path = os.path.join(RESULTS_DIR, file_name)
        self.file = open(file_path, 'w', encoding='utf-8')
        self.csvwriter = csv.writer(self.file)
        self.csvwriter.writerow(['Статус', 'Количество'])
        self.status_count = {}

    def process_item(self, item, spider):
        status = item['status']
        self.status_count[status] = self.status_count.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        for status, count in self.status_count.items():
            self.csvwriter.writerow([status, count])
        self.csvwriter.writerow(['Total', sum(self.status_count.values())])
        self.file.close()
