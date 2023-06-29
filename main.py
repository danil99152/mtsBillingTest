import csv
import os

import settings


class MiniBilling:
    __slots__ = ['cdr_directory', 'prefixes_filename', 'volumes_path', 'volumes']

    cdr_directory: str  # Путь до директории, в которой хранятся cdr файлы
    prefixes_filename: str  # Имя файла, содержащего префиксы
    volumes_path: str  # Путь к файлу, в который будут записываться колличества секунд

    volumes: dict  # Переменная для хранения длительности секунд для каждой пары префиксных зон

    def __init__(self,
                 cdr_directory,
                 prefixes_filename,
                 volumes_path):
        self.cdr_directory = cdr_directory
        self.prefixes_filename = prefixes_filename
        self.volumes_path = volumes_path

        self.volumes = {}

    # Генерация словаря, где ключ - префикс, значение - префиксная зона
    @staticmethod
    def load_prefixes(filename) -> dict[str]:
        prefixes: dict = {}
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                prefix_zone = row[0]
                prefixes[row[1]] = prefix_zone
        return prefixes

    def process_cdr_files(self) -> None:
        prefixes: dict[str] = self.load_prefixes(self.prefixes_filename)  # Загружаем словарь префиксов

        cdr_files: list[str] = os.listdir(self.cdr_directory)  # Загружаем пути к cdr файлам
        for cdr_file in cdr_files:  # Проходимся по каждому файлу
            cdr_path = os.path.join(self.cdr_directory, cdr_file)  # Формируем путь до него
            with open(cdr_path, 'r') as file:
                reader = csv.reader(file)  # Читаем файл
                lines: list[list[str]] = list(reader)  # Дробим на список строк записей в файле

            for line in lines:
                msisdn: str = line[5]  # Вызывающий абонент
                dialed: str = line[6]  # Вызываемый абонент
                duration: int = int(line[8]) if line[8] else 0  # Длительность соединения в секундах

                # Определение префикса вызывающего абонента
                # (Создается генераторный объект, из которого выбирается наибольшее по длине значение префикса)
                msisdn_prefix: str = max((prefix for prefix in prefixes if msisdn.startswith(prefix)),
                                         default='Unknown')
                # Определение префикса вызываемого абонента
                dialed_prefix: str = max((prefix for prefix in prefixes if dialed.startswith(prefix)),
                                         default='Unknown')

                line[9] = prefixes.get(msisdn_prefix, 'Unknown')  # Запись зоны префикса абонента
                line[10] = prefixes.get(dialed_prefix, 'Unknown')  # Запись зоны префикса набранного абонента

                # Ключ-пара префиксных зон
                volumes_key: str = f"{line[9]},{line[10]}"
                # Наполнение словаря длительности секунд
                self.volumes[volumes_key] = self.volumes.get(volumes_key, 0) + duration

            # Запись строк обратно в файл
            with open(cdr_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(lines)

    # Создание и наполнение файла VOLUMES.TXT
    def make_volumes(self) -> None:
        with open(self.volumes_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for key, value in self.volumes.items():
                writer.writerow([key, value])


if __name__ == "__main__":
    mini_billing = MiniBilling(settings.cdr_directory,
                               settings.prefixes_filename,
                               settings.volumes_path)  # Создание экземпляра класса MiniBilling
    mini_billing.process_cdr_files()  # Обработка файлов CDR
    mini_billing.make_volumes()  # Создание файла длительности секунд для префиксных зон
