from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QStackedWidget
)
from app.utils.utils import get_resource_path
from app.ui.main_page import UiMainPage
from app.ui.settings_page import UiSettingsPage
from app.ui.about_page import UiAboutPage


class Ui(QWidget):
    # 定义信号
    main_button_clicked_signal = pyqtSignal()
    save_verify_button_clicked_signal = pyqtSignal()
    set_page_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.logo_path = get_resource_path("assets/logo.png")

        self.setWindowTitle("Telegram数据导出")
        self.setWindowIcon(QIcon(self.logo_path))
        self.setMinimumSize(580, 330)
        self.resize(580, 330)

        # 侧边栏
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar.setFixedWidth(150)

        # 软件 Logo 和名称
        self.logo_name_frame = QFrame()
        self.logo_name_frame.setObjectName("logo_name_frame")
        self.logo_name_layout = QHBoxLayout(self.logo_name_frame)
        self.logo_name_layout.setContentsMargins(0, 0, 0, 0)

        self.logo = QLabel()
        self.logo.setObjectName("logo_label")
        pixmap = QPixmap(self.logo_path)
        self.logo.setPixmap(pixmap.scaledToHeight(50))
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo_name_layout.addWidget(self.logo)

        self.name = QLabel("Telegram\n数据导出")
        self.name.setObjectName("app_name_label")
        self.name.setAlignment(Qt.AlignCenter)
        self.logo_name_layout.addWidget(self.name)
        self.logo_name_layout.addStretch(1)

        self.sidebar_layout.addWidget(self.logo_name_frame)

        # 侧边栏按钮
        self.main_btn = QPushButton("主界面")
        self.settings_btn = QPushButton("设置")
        self.about_btn = QPushButton("关于")
        self.sidebar_buttons = [self.main_btn, self.settings_btn, self.about_btn]
        for button in self.sidebar_buttons:
            button.setFixedHeight(40)
            button.setCheckable(True)
            self.sidebar_layout.addWidget(button)

        self.sidebar_layout.addStretch(1)

        # 右侧内容区域
        self.content_area = QStackedWidget()

        # 主界面
        self.main_page = UiMainPage()
        self.content_area.addWidget(self.main_page)

        # 设置界面
        self.settings_page = UiSettingsPage()
        self.content_area.addWidget(self.settings_page)

        # 关于界面
        self.about_page = UiAboutPage()
        self.content_area.addWidget(self.about_page)

        # 侧边栏按钮绑定(切换界面)
        self.main_btn.clicked.connect(lambda: self.set_current_page(0))
        self.settings_btn.clicked.connect(lambda: self.set_page_signal.emit(1))
        self.about_btn.clicked.connect(lambda: self.set_page_signal.emit(2))
        # 设置初始显示
        self.set_current_page(0)  # 首次加载时更新按钮状态

        # 主布局
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area)
        # 将信号传递到 Ui 类
        self.main_page.main_button_clicked_signal.connect(self.main_button_clicked_signal.emit)
        self.settings_page.save_verify_button_clicked_signal.connect(self.save_verify_button_clicked_signal.emit)

    def set_current_page(self, index):
        self.content_area.setCurrentIndex(index)
        for button in self.sidebar_buttons:
            button.setChecked(False)
        self.sidebar_buttons[index].setChecked(True)

    def load_stylesheet(self, filename):
        """ 加载样式表文件 """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: Style sheet '{filename}' not found.")
