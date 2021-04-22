import sys
from Modules.General import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI.UI_MapAppMainWindow import Ui_MapAppMainWindow
from PyQt5.Qt import QPixmap, QImage
from io import BytesIO


class MapApp(Ui_MapAppMainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        map_params = {
            "l": "map",
            'll': '1,1'
        }
        response = perform_request(map_api_server, params=map_params)
        image = QImage().fromData(response.content)
        pix_map = QPixmap().fromImage(image)
        self.map_label.setPixmap(pix_map)


app = QApplication(sys.argv)
map_app = MapApp()
map_app.show()
sys.exit(app.exec_())
