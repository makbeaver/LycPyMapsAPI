from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import QPixmap


class ScalingImage(QWidget):
    """Изображение, которое масштабируется вместе с родительским объектом,
    сохраняя пропорции."""
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.pix_map = QPixmap()
        self.image_rect = QRect()

    def setPixmap(self, pix_map):
        """Задать картинку."""
        self.pix_map = pix_map
        self.update()

    def paintEvent(self, event):
        """Метод отвечает за отрисовку картинки."""
        if not self.pix_map.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            width, height = self.width(), self.height()
            # Из-за бага в PyQt5 (как я понял) высота виджета определяется
            # меньше действительной и изображение получается меньше. Чтобы
            # исправить это, высота умножается на определённое число,
            # вычисленное методом проб и ошибок
            if width > height:
                height *= 1.34
            image_width = self.pix_map.size().width()
            image_height = self.pix_map.size().height()
            ratio = min(width, height) / max(image_width, image_height)
            new_image_width = image_width * ratio
            new_image_height = image_height * ratio
            rect = QRect((width - new_image_width) // 2,
                         (self.height() - new_image_height) // 2,
                         new_image_width, new_image_height)
            self.image_rect = rect
            painter.drawPixmap(rect, self.pix_map)
