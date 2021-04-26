import requests
import math
from Modules.ApiKeys import *
from multipledispatch import dispatch
from numbers import Number


MAP_API_SERVER = 'http://static-maps.yandex.ru/1.x/'
GEOCODER_API_SERVER = 'https://geocode-maps.yandex.ru/1.x/'
GEOSEARCH_API_SERVER = 'https://search-maps.yandex.ru/v1/'

METER_IN_DEGREE_OF_LONGITUDE = 1 / (111 * 1000)
METER_IN_DEGREE_OF_LATITUDE = 1 / (111.111 * 1000)


class ToponymNotFound(Exception):
    pass


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
    if not (response := requests.get(request, *args, **kwargs)):
        text = (f'\nОшибка выполнения запроса:\n'
                f'{response.url}\n'
                f'Http статус: {response.status_code} ({response.reason})')
        raise RequestError(text)
    return response


# get_toponyms - мультиметод. Принимает на вход либо строку, либо два числа.
@dispatch(str)
def get_toponyms(geocode, **kwargs):
    geo_coder_params = {'apikey': GEOCODER_API_KEY,
                        'format': 'json',
                        'geocode': geocode}

    for k, v in kwargs.items():
        geo_coder_params[k] = v

    response = perform_request(GEOCODER_API_SERVER, params=geo_coder_params)
    json_response = response.json()
    toponyms = json_response["response"]["GeoObjectCollection"][
        "featureMember"]
    return toponyms


@dispatch(Number, Number)
def get_toponyms(x, y, **kwargs):
    return get_toponyms(','.join(map(str, [x, y])), **kwargs)


def get_pos_by_toponym(toponym):
    toponym_coodrinates = toponym["GeoObject"]["Point"]["pos"]
    return list(map(float, toponym_coodrinates.split(' ')))


def get_address_by_toponym(toponym):
    toponym_address = toponym["GeoObject"]["metaDataProperty"][
        "GeocoderMetaData"]["text"]
    return toponym_address


def get_post_address_by_toponym(toponym):
    toponym_post_address = None
    try:
        toponym_post_address = toponym["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["Address"]["postal_code"]
    except KeyError:
        pass
    finally:
        return toponym_post_address


def get_pos(geocode, **kwargs) -> [float, float]:
    geo_coder_params = {'apikey': GEOCODER_API_KEY,
                        'format': 'json',
                        'geocode': geocode}

    for k, v in kwargs.items():
        geo_coder_params[k] = v

    response = perform_request(GEOCODER_API_SERVER, params=geo_coder_params)
    json_response = response.json()
    toponyms = json_response["response"]["GeoObjectCollection"][
        "featureMember"]
    if len(toponyms) == 0:
        raise ToponymNotFound(response.url)
    toponym = toponyms[0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    return list(map(float, toponym_coodrinates.split(' ')))


def get_address_by_geocode(geocode):
    geocoder_params = {'apikey': GEOCODER_API_KEY,
                       'geocode': geocode,
                       'format': 'json'}

    response = perform_request(GEOCODER_API_SERVER, params=geocoder_params)
    json_response = response.json()
    toponyms = json_response["response"]["GeoObjectCollection"][
        "featureMember"]
    toponym_address = toponyms[0]["GeoObject"]["metaDataProperty"][
        "GeocoderMetaData"]["text"]
    return toponym_address


def get_tile(tile_w, tile_h, pos):
    # Не используется, нужно было при попытке решить 11 задачу
    x = pos[0] // tile_w
    y = pos[1] // tile_h
    return x, y


def format_map_view_box(view_box):
    # Не используется, нужно было при попытке решить 11 задачу
    return '~'.join(map(lambda p: ','.join(map(str, p)), view_box))


@dispatch(str)
def get_organizations(text, **kwargs):
    geosearch_params = {
        'apikey': GEOSEARCH_API_KEY,
        'text': text,
        'type': 'biz',
        'lang': 'ru_RU'
    }
    for k, v in kwargs.items():
        geosearch_params[k] = v
    response = perform_request(GEOSEARCH_API_SERVER, params=geosearch_params)
    json_response = response.json()
    return json_response['features']


@dispatch(Number, Number)
def get_organizations(x, y, **kwargs):
    geosearch_params = {
        'apikey': GEOSEARCH_API_KEY,
        'text': '*',
        'type': 'biz',
        'lang': 'ru_RU',
        'll': ','.join(map(str, [x, y]))
    }
    for k, v in kwargs.items():
        geosearch_params[k] = v
    response = perform_request(GEOSEARCH_API_SERVER, params=geosearch_params)
    json_response = response.json()
    return json_response['features']


# radius выражается в метрах
def get_organizations_in_radius(x, y, radius):
    search_area = (radius * METER_IN_DEGREE_OF_LONGITUDE,
                   radius * METER_IN_DEGREE_OF_LATITUDE)
    params = {
        'spn': ','.join(map(str, search_area))
    }
    return get_organizations(x, y, **params)


def lonlat_distance(a, b):

    degree_to_meters_factor = 111 * 1000 # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def is_pos_in_radius(center, pos, radius):
    return lonlat_distance(center, pos) <= radius


def get_pos_by_organization(organization):
    return organization["geometry"]["coordinates"]


def is_organization_in_radius(center, organization, radius):
    pos = get_pos_by_organization(organization)
    return is_pos_in_radius(center, pos, radius)


def get_address_by_organization(organization):
    return organization["properties"]["CompanyMetaData"]["address"]
