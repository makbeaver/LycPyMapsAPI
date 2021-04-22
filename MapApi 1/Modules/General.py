import requests
from Modules.ApiKeys import *


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
    geo_coder_request = 'https://geocode-maps.yandex.ru/1.x'
    geo_coder_params = {'apikey': GEOCODER_API_KEY,
                        'format': 'json',
                        'geocode': geocode}

    for k, v in kwargs.items():
        geo_coder_params[k] = v

    response = perform_request(geo_coder_request, params=geo_coder_params)

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    return list(map(float, toponym_coodrinates.split(' ')))
