import sys
from Modules.General import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI.UI_MapAppMainWindow import Ui_MapAppMainWindow
from PyQt5.Qt import QPixmap, QImage, Qt
from Modules.ScalingImage import ScalingImage
# from Modules.EasyThreadsQt import queue_thread_qt


START_SCALE = 13


class MapApp(Ui_MapAppMainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.map_api_server = MAP_API_SERVER
        self.map_type = 'map'                  # Параметр l
        self.scale = START_SCALE               # Параметр z
        self.map_pos = [37.588392, 55.734036]  # Параметр ll
        self.pix_maps = {}  # Словарь с уже загруженными ранее картинками

        # Попытка поиграться с потоками. Загружает все изображения в отдельных
        # потоках, из-за чего программа не подвисает при изменении масштаба.
        # Не стал добавлять это в конечную версию, так как другим будет сложно
        # в этом разобраться, да и потоки могут привести к поломке программы.
        # Можете игнорировать этот кусок кода.
        # for i in wave_range(0, self.scale, 18):
        #     self.load_pix_map(i)

        self.map_label = ScalingImage(self)
        self.gridLayout.addWidget(self.map_label)
        self.override_map_params()

    # Часть работы с потоками. Игнорируйте этот код.
    # @queue_thread_qt
    # def load_pix_map(self, i):
    #     self.get_pix_map_by_scale(scale=i)

    def get_pix_map(self, map_type=None, map_pos=None, scale=None):
        """Получение изображения карты."""

        # Если в метод не переданы какие-либо параметры, используем текущие
        # параметры карты
        if map_type is None:
            map_type = self.map_type
        if map_pos is None:
            map_pos = self.map_pos
        if scale is None:
            scale = self.scale

        map_params = {
            "l": map_type,
            'll': ','.join(map(str, map_pos)),
            'z': str(scale)
        }
        key = tuple(map_params.values())
        pix_map = self.pix_maps.get(key)
        if pix_map is None:
            response = perform_request(self.map_api_server, params=map_params)
            image = QImage().fromData(response.content)
            pix_map = QPixmap().fromImage(image)
            self.pix_maps[key] = pix_map
        return pix_map

    def override_map_params(self):
        """Изменение параметров карты."""
        self.map_label.setPixmap(self.get_pix_map())

    def keyPressEvent(self, *args, **kwargs):
        key = args[0].key()
        if key == Qt.Key_PageUp:
            if self.scale < 17:
                self.scale += 1
            self.override_map_params()
        elif key == Qt.Key_PageDown:
            if self.scale > 0:
                self.scale -= 1
            self.override_map_params()


app = QApplication(sys.argv)
map_app = MapApp()
map_app.show()
sys.exit(app.exec_())
