import os.path

from prjstore.ui.pyside.utils.qt_core import *


class PyPushBottom(QPushButton):
    def __init__(self, text='', height=40, minimum_width=50, text_padding=55, text_color='#C3CCDF', icon_path='',
                 icon_color='#C3CCDF', btn_color='#44475A', btn_hover='#4F5368', btn_pressed='#282A36',
                 is_active=False):
        super().__init__()
        self.setText(text)
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.setCursor(Qt.PointingHandCursor)

        self.minimum_width = minimum_width
        self.text_padding = text_padding
        self.text_color = text_color
        self.icon_path = icon_path
        self.icon_color = icon_color
        self.btn_color = btn_color
        self.btn_hover = btn_hover
        self.btn_pressed = btn_pressed
        self.is_active = is_active

        self.set_style(text_padding=self.text_padding, text_color=self.text_color, btn_color=self.btn_color,
                       btn_hover=self.btn_hover, btn_pressed=self.btn_pressed, is_active=self.is_active)

    def set_style(self, text_padding=55, text_color='#C3CCDF', btn_color='#44475A', btn_hover='#4F5368',
                  btn_pressed='#282A36', is_active=False):
        style = f'QPushButton {{' \
                f'  color: {text_color};' \
                f'  background-color: {btn_color};' \
                f'  padding-left: {text_padding}px;' \
                f'  text-align: left;' \
                f'  border: none;' \
                f'}}' \
                f'QPushButton:hover {{' \
                f'  background-color: {btn_hover};' \
                f'}}' \
                f'QPushButton:pressed {{' \
                f'  background-color: {btn_pressed};' \
                f'}}'
        active_style = f'QPushButton {{' \
                       f'  background-color: {btn_hover};' \
                       f'  border-right: 5px solid #282A36;' \
                       f'}}'
        if not is_active:
            self.setStyleSheet(style)
        else:
            self.setStyleSheet(style + active_style)

    def set_active(self, is_active):
        self.set_style(text_padding=self.text_padding, text_color=self.text_color, btn_color=self.btn_color,
                       btn_hover=self.btn_hover, btn_pressed=self.btn_pressed, is_active=is_active)

    def paintEvent(self, event):
        QPushButton.paintEvent(self, event)

        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(Qt.NoPen)
        rect = QRect(0, 0, self.minimum_width, self.height())
        self.draw_icon(qp, self.icon_path, rect)
        qp.end()

    @staticmethod
    def draw_icon(qp, image, rect):
        # Format path
        app_path = os.path.abspath(os.getcwd())
        folder = 'main_window/images/icons'
        path = os.path.join(app_path, folder)
        icon_path = os.path.normpath(os.path.join(path, image))
        # Draw icon
        icon = QPixmap(icon_path)
        qp.drawPixmap((rect.width() - icon.width()) / 2, (rect.height() - icon.height()) / 2, icon)
