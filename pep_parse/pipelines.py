import csv
import datetime as dt
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    """
    Обработка полученных данных и сохраняет результат в results.
    Считает количество PEP в зависимости от статуса. Обобщает результат.
    """

    def open_spider(self, spider):
        current_datetime = dt.datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
        file_name = 'status_summary_' + formatted_datetime + '.csv'
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        file_path = results_dir / file_name
        self.file = open(file_path, 'w', newline='', encoding='utf-8')
        self.csvwriter = csv.writer(self.file)
        self.csvwriter.writerow(['Статус', 'Количество'])
        self.temp = {}

    def process_item(self, item, spider):
        status = item.get('status')
        self.temp[status] = self.temp.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        for status, count in self.temp.items():
            self.csvwriter.writerow([status, count])
        self.csvwriter.writerow(['Total', sum(self.temp.values())])
        self.file.close()