from Modules.General import *
import abc
from numbers import Number


# Абстрактный класс, не предполагает создания экземпляров этого класса. Все
# наследующиеся классы обязаны реализовать абстрактные методы.
# (для тех кто не знает что это)
class MapObject(abc.ABC):
    @property
    @abc.abstractmethod
    def object(self):
        pass

    @property
    @abc.abstractmethod
    def pos(self):
        pass

    @property
    @abc.abstractmethod
    def address(self):
        pass


class Toponym(MapObject):
    # multipledispatch некорректно работает со статическими методами,
    # из-за чего для каждого класса нужно создавать своё пространство имён
    dispatch_namespace = {}

    @staticmethod
    @dispatch(Number, Number, namespace=dispatch_namespace)
    def get_objects(x, y, **kwargs):
        return list(map(Toponym, get_toponyms(x, y, **kwargs)))

    @staticmethod
    @dispatch(str, namespace=dispatch_namespace)
    def get_objects(address, **kwargs):
        return list(map(Toponym, get_toponyms(address, **kwargs)))

    @dispatch(dict)
    def __init__(self, toponym):
        self._object = toponym
        self._address = get_address_by_toponym(self._object)
        self._pos = get_pos_by_toponym(self._object)
        self._post_address = get_post_address_by_toponym(self._object)

    @property
    def object(self):
        return self._object

    @property
    def pos(self):
        return self._pos

    @property
    def address(self):
        return self._address

    @property
    def post_address(self):
        return self._post_address


class Organization(MapObject):
    dispatch_namespace = {}

    @staticmethod
    @dispatch(Number, Number, namespace=dispatch_namespace)
    def get_objects(x, y, **kwargs):
        return list(map(Organization, get_organizations(x, y, **kwargs)))

    @staticmethod
    @dispatch(str, namespace=dispatch_namespace)
    def get_objects(text, **kwargs):
        return list(map(Organization, get_organizations(text, **kwargs)))

    @staticmethod
    def get_objects_in_radius(x, y, radius):
        organizations = get_organizations_in_radius(x, y, radius)
        return list(map(Organization, organizations))

    def is_in_radius(self, center, radius):
        return is_organization_in_radius(center, self._object, radius)

    @dispatch(dict)
    def __init__(self, organization):
        self._object = organization
        self._address = get_address_by_organization(self._object)
        self._pos = get_pos_by_organization(self._object)
        self._name = self._object["properties"]["CompanyMetaData"]["name"]

    @property
    def name(self):
        return self._name

    @property
    def object(self):
        return self._object

    @property
    def pos(self):
        return self._pos

    @property
    def address(self):
        return self._address
