import csv
import os


def load_prefixes(filename):
    prefixes = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            prefix_zone = row[0]
            prefixes[row[1]] = prefix_zone
    return prefixes


def process_cdr_files(cdr_directory, prefixes_filename, volumes_path):
    prefixes = load_prefixes(prefixes_filename)
    volumes = {}

    cdr_files = os.listdir(cdr_directory)
    for cdr_file in cdr_files:
        cdr_path = os.path.join(cdr_directory, cdr_file)
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
            volumes[volumes_key] = volumes.get(volumes_key, 0) + duration

        with open(cdr_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(lines)

    with open(volumes_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for key, value in volumes.items():
            writer.writerow([key, value])


resources_path = 'resources'
cdr_directory = f'{resources_path}/sintetic_data'
prefixes_filename = f'{resources_path}/prefixes/PREFIXES.TXT'
volumes_path = f'{resources_path}/volumes/VOLUMES.TXT'

if __name__ == "__main__":
    process_cdr_files(cdr_directory, prefixes_filename, volumes_path)

