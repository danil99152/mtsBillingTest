import csv

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import paths
from .models import Call, Volume


def load_prefixes(filename) -> dict[str]:
    prefixes: dict = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            prefix_zone = row[0]
            prefixes[row[1]] = prefix_zone
    return prefixes


@csrf_exempt
def process_cdr_file(request):
    if request.method == "POST":
        volumes = {}
        try:
            title = request.FILES['file'].name
            uploaded_file = request.FILES['file']
            file_content = uploaded_file.read().decode('utf-8')
            prefixes: dict[str] = load_prefixes(paths.prefixes_filename)

            lines = file_content.split('\n')
            for line in lines:
                if line:
                    line = line.split(',')
                    msisdn: str = line[5]  # Вызывающий абонент
                    dialed: str = line[6]  # Вызываемый абонент
                    duration: int = int(line[8]) if line[8] else 0  # Длительность соединения в секундах

                    start_time: str = line[7]  # Время начала телефонного вызова
                    circuit_in: str = line[30]  # Входящая транковая группа
                    circuit_out: str = line[31]  # Исходящая транковая группа

                    # Определение префикса вызывающего абонента
                    # (Создается генераторный объект, из которого выбирается наибольшее по длине значение префикса)
                    msisdn_prefix: str = max((prefix for prefix in prefixes if msisdn.startswith(prefix)),
                                             default='Unknown')
                    # Определение префикса вызываемого абонента
                    dialed_prefix: str = max((prefix for prefix in prefixes if dialed.startswith(prefix)),
                                             default='Unknown')

                    msisdn_zone = prefixes.get(msisdn_prefix, 'Unknown')  # Запись зоны префикса абонента
                    dialed_zone = prefixes.get(dialed_prefix, 'Unknown')  # Запись зоны префикса набранного абонента

                    # Ключ-пара префиксных зон
                    volumes_key: str = f"{msisdn_zone},{dialed_zone}"
                    # Наполнение словаря длительности секунд
                    volumes[volumes_key] = volumes.get(volumes_key, 0) + duration

                    Call.objects.create(
                        msisdn=msisdn,
                        dialed=dialed,
                        start_time=start_time,
                        duration=duration,
                        circuit_in=circuit_in,
                        circuit_out=circuit_out,
                        file_name=title,
                        file_index=int(title.split("_")[3].split(".")[0])
                    )

            for i, v in volumes.items():
                Volume.objects.create(
                    file_index=int(title.split("_")[3].split(".")[0]),
                    prefix_zones=i,
                    duration=v
                )

            return JsonResponse(volumes)

        except Exception as e:
            return JsonResponse({"Exception": e})
