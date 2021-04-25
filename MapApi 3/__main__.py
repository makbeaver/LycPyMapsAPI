import sys
from PyQt5.QtWidgets import QApplication
from Modules.MapApp import MapApp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    map_app = MapApp()
    map_app.show()
    sys.exit(app.exec_())
