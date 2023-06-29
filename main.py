import csv
import os

import settings


class MiniBilling:
    __slots__ = ['cdr_directory', 'prefixes_filename', 'volumes_path', 'volumes']

    cdr_directory: str
    prefixes_filename: str
    volumes_path: str

    volumes: dict

    def __init__(self,
                 cdr_directory,
                 prefixes_filename,
                 volumes_path):
        self.cdr_directory = cdr_directory
        self.prefixes_filename = prefixes_filename
        self.volumes_path = volumes_path

        self.volumes = {}

    @staticmethod
    def load_prefixes(filename):
        prefixes = {}
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                prefix_zone = row[0]
                prefixes[row[1]] = prefix_zone
        return prefixes

    def process_cdr_files(self):
        prefixes = self.load_prefixes(self.prefixes_filename)

        cdr_files = os.listdir(self.cdr_directory)
        for cdr_file in cdr_files:
            cdr_path = os.path.join(self.cdr_directory, cdr_file)
            with open(cdr_path, 'r') as file:
                reader = csv.reader(file)
                lines = list(reader)

            for line in lines:
                msisdn = line[5]
                dialed = line[6]
                duration = int(line[8]) if line[8] else 0

                msisdn_prefix = max((prefix for prefix in prefixes if msisdn.startswith(prefix)), default='Unknown')
                dialed_prefix = max((prefix for prefix in prefixes if dialed.startswith(prefix)), default='Unknown')

                line[9] = prefixes.get(msisdn_prefix, 'Unknown')
                line[10] = prefixes.get(dialed_prefix, 'Unknown')

                volumes_key = f"{line[9]},{line[10]}"
                self.volumes[volumes_key] = self.volumes.get(volumes_key, 0) + duration

            with open(cdr_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(lines)

    def make_volumes(self):
        with open(self.volumes_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for key, value in self.volumes.items():
                writer.writerow([key, value])


if __name__ == "__main__":
    mini_billing = MiniBilling(settings.cdr_directory,
                               settings.prefixes_filename,
                               settings.volumes_path)
    mini_billing.process_cdr_files()
    mini_billing.make_volumes()
