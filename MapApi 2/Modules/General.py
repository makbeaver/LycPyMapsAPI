import requests
from Modules.ApiKeys import *


MAP_API_SERVER = 'http://static-maps.yandex.ru/1.x/'
GEOCODER_API_SERVER = 'https://geocode-maps.yandex.ru/1.x'


def wave_range(start, middle, end, step=1):
    # Это нужно было мне для организации потоков
    if step < 0:
        step *= -1
        left = end - 1
        right = start
        start, end = middle + 1, middle
    else:
        left = middle - 1
        right = middle + 1
    while True:
        not_left_bound = left >= start
        if not_left_bound:
            yield left
            left -= step
        not_right_bound = right < end
        if not_right_bound:
            yield right
            right += step
        if not (not_left_bound or not_right_bound):
            return

          
class RequestError(Exception):
    pass


def perform_request(request, *args, **kwargs):
    response = requests.get(request, *args, **kwargs)
    if not response:
        text = (f'\nОшибка выполнения запроса:\n'
                f'{response.url}\n'
                f'Http статус: {response.status_code} ({response.reason})')
        raise RequestError(text)
    return response


def get_pos(geocode, **kwargs) -> [float, float]:
    geo_coder_params = {'apikey': GEOCODER_API_KEY,
                        'format': 'json',
                        'geocode': geocode}

    for k, v in kwargs.items():
        geo_coder_params[k] = v
        
    response = perform_request(GEOCODER_API_SERVER, params=geo_coder_params)
    
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    return list(map(float, toponym_coodrinates.split(' ')))
