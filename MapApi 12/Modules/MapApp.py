from Modules.General import *
from PyQt5.QtWidgets import QMainWindow
from UI.UI_MapAppMainWindow import Ui_MapAppMainWindow
from PyQt5.Qt import QPixmap, QImage, Qt
from Modules.MapObjects import Toponym, Organization
import datetime
from Modules.EasyThreadsQt import queue_thread_qt


START_SCALE = 13
START_DISPLAY_AREA = [90, 45]
START_POS = [37.588392, 55.734036]

MAP_DEGREE_WIDTH = 360
MAP_DEGREE_HEIGHT = 180

MIN_DISPLAY_AREA = 0.000009
MAX_DISPLAY_AREA = 180

MAP_TYPES = ['map', 'sat']
GO_NAMES_TYPE = 'skl'  # GO - geographic objects
TRAFFIC_JAMS_TYPE = 'trf'

ERROR_STYLESHEET = '*{color:red;}'
INFO_LABEL_STYLESHEET = '*{color:black;}'

TOPONYM_NOT_FOUND_ERROR_MSG = 'Объект не найден'
BAD_RESPONSE_ERROR = 'Ошибка при запросе'
ORGANIZATION_NOT_FOUND_ERROR_MSG = 'Организация не найдена'
UNEXPECTED_ERROR_MSG = 'Произошла непредвиденная ошибка'

ORGANIZATIONS_SEARCH_RADIUS = 50  # Значение в метрах


class MapApp(Ui_MapAppMainWindow, QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.map_label.set_map_app(self)

        # Назначаем функции на элементы UI
        self.map_type_box.currentIndexChanged.connect(self.update_map_type)
        self.go_names_btn.clicked.connect(self.update_map_type)
        self.post_address_box.currentIndexChanged.connect(self.update_address)
        self.traffic_jams_btn.clicked.connect(self.update_map_type)
        self.find_obj_btn.clicked.connect(self.get_object)
        self.reset_result_btn.clicked.connect(self.reset_result)
        self.object_input.returnPressed.connect(
            self.object_input_return_pressed)

        # Пусть карта позиционируется на Москве, дабы было понятно что
        # программа работает
        self.map_pos = START_POS                # Параметр ll
        self.map_type = 'map'                   # Параметр l
        self.display_area = START_DISPLAY_AREA  # Параметр spn
        self.tags = []                          # Параметр pt

        # Переменная отвечает за масштаб карты. Аналогична параметру z в
        # Yandex Static API, только в качестве такового в запрос не передаётся.
        # Вместо этого с помощью этой переменной вычисляется значение spn,
        # которое уже передаётся в параметрах запроса.
        self.display_area_scale = START_SCALE

        self.address = None
        self.map_object = None
        self.post_address = None

        self.pix_maps = {}  # Словарь с уже загруженными ранее картинками

        self.first_map_load()

    @queue_thread_qt
    def first_map_load(self):
        # Вынесено в отдельную функцию, дабы была возможность добавить
        # многопоточность
        self.override_map_params()

    def object_input_return_pressed(self):
        self.object_input.clearFocus()
        self.get_object()

    def get_view_box(self, map_pos=None):
        """Функция для получения параметра bbox в картах через map_pos"""
        # Функция в программе не задействована
        if map_pos is None:
            map_pos = self.map_pos
        half_w = (MAP_DEGREE_WIDTH / 2 ** self.display_area_scale) / 2
        half_h = (MAP_DEGREE_HEIGHT / 2 ** self.display_area_scale) / 2
        x1 = map_pos[0] + half_w / 2
        y1 = map_pos[1] + half_h / 2
        x2 = map_pos[0] - half_w / 2
        y2 = map_pos[1] - half_h / 2
        if x1 < -MAP_DEGREE_WIDTH / 2:
            x1 = -MAP_DEGREE_WIDTH / 2
        elif x1 > MAP_DEGREE_WIDTH / 2:
            x1 = MAP_DEGREE_WIDTH / 2
        if y1 < -MAP_DEGREE_HEIGHT / 2:
            y1 = -MAP_DEGREE_HEIGHT / 2
        elif y1 > MAP_DEGREE_HEIGHT / 2:
            y1 = MAP_DEGREE_HEIGHT / 2
        if x2 < -MAP_DEGREE_WIDTH / 2:
            x2 = -MAP_DEGREE_WIDTH / 2
        elif x2 > MAP_DEGREE_WIDTH / 2:
            x2 = MAP_DEGREE_WIDTH / 2
        if y2 < -MAP_DEGREE_HEIGHT / 2:
            y2 = -MAP_DEGREE_HEIGHT / 2
        elif y2 > MAP_DEGREE_HEIGHT / 2:
            y2 = MAP_DEGREE_HEIGHT / 2
        return [[x1, y1], [x2, y2]]

    @staticmethod
    def is_click_on_map(relative_pos):
        mouse_x, mouse_y = relative_pos
        return 0 <= mouse_x <= 1 and 0 <= mouse_y <= 1

    def is_pos_on_map(self, pos):
        left = self.map_pos[0] + self.display_area[0]
        right = self.map_pos[0] - self.display_area[0]
        top = self.map_pos[1] + self.display_area[0]
        bottom = self.map_pos[1] - self.display_area[1]

        return right <= pos[0] <= left and bottom <= pos[1] <= top

    def click_coordinates(self, relative_pos):
        mouse_x, mouse_y = relative_pos
        x = self.map_pos[0] + (2 * mouse_x - 1) * self.display_area[0]
        y = self.map_pos[1] - (2 * mouse_y - 1) * self.display_area[1]
        return x, y

    def handle_map_click(self, relative_pos, button):
        if button == Qt.LeftButton:
            self.get_object_by_click(relative_pos)
        elif button == Qt.RightButton:
            self.get_organization_by_click(relative_pos)

    @queue_thread_qt
    def get_organization_by_click(self, relative_pos):
        """Находит организацию в области правого клика в радиусе
        ORGANIZATIONS_SEARCH_RADIUS."""
        if not self.is_click_on_map(relative_pos):
            return
        x, y = self.click_coordinates(relative_pos)
        try:
            if not (toponyms := Toponym.get_objects(x, y)):
                self.print_error(ORGANIZATION_NOT_FOUND_ERROR_MSG)
                return
            toponym = toponyms[0]
            organizations = Organization.get_objects(toponym.address)
        except RequestError:
            self.print_error(BAD_RESPONSE_ERROR)
            return
        except Exception as e:
            self.log_unexpected_error(e)
            return
        if not organizations:
            self.print_error(ORGANIZATION_NOT_FOUND_ERROR_MSG)
            return
        for organization in organizations:
            pos = organization.pos
            is_in_radius = organization.is_in_radius(
                (x, y), ORGANIZATIONS_SEARCH_RADIUS
            )
            if self.is_pos_on_map(pos) and is_in_radius:
                self.map_object = organization
                self.clear_tags()
                self.add_tag(pos)
                self.address = (
                        self.map_object.name + ', ' + self.map_object.address
                )
                self.set_address_label()
                self.clear_info_label()
                self.post_address = toponym.post_address
                self.update_address()
                self.override_map_params()
                return
            else:
                continue
        self.print_error(ORGANIZATION_NOT_FOUND_ERROR_MSG)

    def log_unexpected_error(self, exception):
        with open('error_log.txt', mode='a') as file:
            time = datetime.datetime.now()
            file.write(f'{time}: {exception}\n')
        self.print_error(UNEXPECTED_ERROR_MSG)

    @queue_thread_qt
    def get_object_by_click(self, relative_pos):
        """Метод принимает на вход относительную позицию точки на карте
        (относительные координаты показывают, какую часть от области показа
        составляет реальная координата)"""
        if not self.is_click_on_map(relative_pos):
            return
        x, y = self.click_coordinates(relative_pos)

        try:
            toponyms = Toponym.get_objects(x, y)
        except RequestError:
            self.print_error(BAD_RESPONSE_ERROR)
            return
        except Exception as e:
            self.log_unexpected_error(e)
            return
        for toponym in toponyms:
            pos = toponym.pos
            if self.is_pos_on_map(pos):
                self.map_object = toponym
                self.clear_tags()
                self.add_tag(pos)
                self.address = self.map_object.address
                self.set_address_label()
                self.clear_info_label()
                self.post_address = self.map_object.post_address
                self.update_address()
                self.override_map_params()
                return
        self.print_error(TOPONYM_NOT_FOUND_ERROR_MSG)

    def reset_result(self):
        """Сброс результата поиска."""
        self.map_pos = START_POS
        self.tags = []
        self.address = None
        self.post_address = None
        self.address_label.setText('')
        self.map_object = None
        self.override_map_params()

    def get_pix_map(self, map_type=None, map_pos=None, scale=None, tags=None,
                    display_area=None):
        """Получение изображения карты."""

        # Если в метод не переданы какие-либо параметры, используем текущие
        # параметры карты
        if map_type is None:
            map_type = self.map_type
        if map_pos is None:
            map_pos = self.map_pos
        if tags is None:
            tags = self.tags
        if scale is None:
            scale = self.display_area_scale
        if display_area is None:
            display_area = [MAP_DEGREE_WIDTH / 2 ** scale / 2,
                            MAP_DEGREE_HEIGHT / 2 ** scale / 2]
        self.display_area = display_area

        map_params = {
            "l": map_type,
            'll': ','.join(map(str, map_pos)),
            # 'z': str(scale),
            'spn': ','.join(map(str, display_area)),
            # 'bbox': format_map_view_box(self.view_box),
            'pt': '~'.join(map(str, tags))
        }
        key = tuple(map_params.values())
        if (pix_map := self.pix_maps.get(key)) is None:
            response = perform_request(MAP_API_SERVER, params=map_params)
            image = QImage().fromData(response.content)
            pix_map = QPixmap().fromImage(image)
            self.pix_maps[key] = pix_map
        return pix_map

    def override_map_params(self):
        """Изменение параметров карты."""
        try:
            pix_map = self.get_pix_map()
        except RequestError:
            self.print_error(BAD_RESPONSE_ERROR)
            return
        except Exception as e:
            self.log_unexpected_error(e)
            return
        if pix_map:
            self.map_label.setPixmap(pix_map)
            self.clear_info_label()

    def keyPressEvent(self, *args, **kwargs):
        key = args[0].key()

        # Изменение масштаба карты по нажатию клавиш
        if key == Qt.Key_PageUp:
            if self.display_area_scale < 17:
                self.display_area_scale += 1
                self.override_map_params()
        elif key == Qt.Key_PageDown:
            if self.display_area_scale > 0:
                self.display_area_scale -= 1
                self.override_map_params()

        # Перемещение по нажанию стрелок
        if key in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
            x_step = self.display_area[0] * 2
            y_step = self.display_area[1] * 2
            x_offset = {Qt.Key_Left: -x_step, Qt.Key_Right: x_step}.get(key, 0)
            y_offset = {Qt.Key_Up: y_step, Qt.Key_Down: -y_step}.get(key, 0)
            self.map_pos[0] += x_offset
            self.map_pos[1] += y_offset

            max_x = MAP_DEGREE_WIDTH / 2 - self.display_area[0] * 2
            min_x = -MAP_DEGREE_WIDTH / 2 + self.display_area[1] * 2

            max_y = MAP_DEGREE_HEIGHT / 2 - self.display_area[1] * 2
            min_y = -MAP_DEGREE_HEIGHT / 2 + self.display_area[1] * 2

            if self.map_pos[0] > max_x:
                self.map_pos[0] = max_x
            elif self.map_pos[0] < min_x:
                self.map_pos[0] = min_x

            if self.map_pos[1] > max_y:
                self.map_pos[1] = max_y
            elif self.map_pos[1] < min_y:
                self.map_pos[1] = min_y
            self.override_map_params()

    def update_address(self):
        if self.post_address_box.currentIndex():
            self.set_address_label()
        else:
            self.set_address_label(self.post_address)

    def set_address_label(self, post_address=None):
        if post_address and self.post_address_box.currentIndex() == 0:
            self.address_label.setText(f'{self.address}, почтовый адрес:'
                                       f' {self.post_address}')
        else:
            self.address_label.setText(self.address)

    def update_map_type(self):
        """Обновить текущий тип карты, основываясь на выбранном пользователем в
        окне программы типом карты."""
        map_type = [MAP_TYPES[self.map_type_box.currentIndex()]]
        if self.go_names_btn.isChecked():
            map_type += [GO_NAMES_TYPE]
        if self.traffic_jams_btn.isChecked():
            map_type += [TRAFFIC_JAMS_TYPE]
        self.map_type = ','.join(map_type)
        self.override_map_params()

    def add_tag(self, pos):
        """Добавить метку на карту"""
        self.tags.append(f'{",".join(map(str, pos))},comma')

    @queue_thread_qt
    def get_object(self, *args):
        """Изменить топоним, основываясь на адресе, введённым пользователем в
        окне программы."""
        try:
            toponyms = Toponym.get_objects(self.object_input.text())
            if not toponyms:
                self.print_error(TOPONYM_NOT_FOUND_ERROR_MSG)
            else:
                self.map_object = toponyms[0]
                self.map_pos = self.map_object.pos
                self.tags.append(f'{",".join(map(str, self.map_pos))},comma')
                self.address = self.map_object.address
                self.post_address = self.map_object.post_address
                self.set_address_label(self.post_address)
                self.clear_info_label()
                self.override_map_params()
        except RequestError:
            self.print_error(BAD_RESPONSE_ERROR)

    def print_error(self, msg):
        """Вывести сообщение об ошибке в окне программы."""
        self.info_label.setStyleSheet(ERROR_STYLESHEET)
        self.info_label.setText(msg)

    def clear_info_label(self):
        self.info_label.setStyleSheet(INFO_LABEL_STYLESHEET)
        self.info_label.setText('')
    
    def clear_tags(self):
        """Очистить все метки на карте."""
        self.tags = []
