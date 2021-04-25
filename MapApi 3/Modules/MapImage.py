from Modules.ScalingImage import ScalingImage


class MapImage(ScalingImage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.map_app = None

    def set_map_app(self, map_app):
        self.map_app = map_app

    def mousePressEvent(self, event):
        x, y = event.x(), event.y()
        x -= self.image_rect.x()
        y -= self.image_rect.y()
        w, h = self.image_rect.width(), self.image_rect.height()
        self.map_app.get_object_by_click([x / w, y / h])
