import json
import os
from os.path import join, dirname

import dotenv
import requests


def main():
    dotenv.load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    dotenv.load_dotenv(dotenv_path)
    TOKEN = os.getenv("TOKEN")
    coord_tokyo = geocoding_test(TOKEN, '新宿')
    coord_seika = geocoding_test(TOKEN, '精華町')
    coord_iida = geocoding_test(TOKEN, '飯田')

    duration_tokyo_iida = routing_test(TOKEN, coord_tokyo, coord_iida)
    duration_seika_iida = routing_test(TOKEN, coord_seika, coord_iida)
    h, m, s = duration_to_hms(duration_tokyo_iida)
    print(f"{h}:{m}:{s}")
    h, m, s = duration_to_hms(duration_seika_iida)
    print(f"{h}:{m}:{s}")


def duration_to_hms(duration):
    hours = int(duration//3600)
    minutes = int((duration%3600)//60)
    seconds = int((duration%3600)%60)

    return hours, minutes, seconds


def geocoding_test(api_key, query):
    url = f"https://api.openrouteservice.org/geocode/search?api_key={api_key}&text={query}"
    r = requests.get(url)
    if r.status_code == 200:
        res_data = r.json()
        if len(res_data['features']) < 1:
            print(f"Search {query} failed.")
            raise Exception
        coordinates = res_data['features'][0]['geometry']['coordinates']
        return coordinates


def routing_test(api_key, coord_start, coord_end):
    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={coord_start[0]},{coord_start[1]}&end={coord_end[0]},{coord_end[1]}"
    r = requests.get(url)
    if r.status_code == 200:
        res_data = r.json()
        json.dump(res_data, open('outfile.json', 'w'), ensure_ascii=False, indent=2)
        duration = res_data['features'][0]['properties']['summary']['duration']
        return duration

    return -1


if __name__ == '__main__':
    main()