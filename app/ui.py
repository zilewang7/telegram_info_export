from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout,
    QHBoxLayout, QFrame, QRadioButton, QStackedWidget, QGridLayout, QTextBrowser
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
import markdown


class Ui(QWidget):
    # 定义信号
    main_button_clicked_signal = pyqtSignal()
    save_verify_button_clicked_signal = pyqtSignal()
    set_page_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.about_text = None
        self.save_verify_btn = None
        self.verify_label = None
        self.password_input = None
        self.username_input = None
        self.proxy_port_input = None
        self.proxy_ip_input = None
        self.proxy_type_radio_list = None
        self.proxy_type_group = None
        self.socks5_radio = None
        self.socks4_radio = None
        self.http_radio = None
        self.https_radio = None
        self.export_info_label = None
        self.phone_input = None
        self.main_btn_2 = None
        self.api_hash_input = None
        self.id_input = None
        self.setWindowTitle("Telegram数据导出")
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.setMinimumSize(580, 330)
        self.resize(580, 330)

        # 设置样式表 可以在 Controller类中初始化完成
        # self.load_stylesheet("style.qss")

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
        pixmap = QPixmap("assets/logo.png")
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
        self.main_page = QWidget()
        self.setup_main_page()
        self.content_area.addWidget(self.main_page)

        # 设置界面
        self.settings_page = QWidget()
        self.setup_settings_page()
        self.content_area.addWidget(self.settings_page)

        # 关于界面
        self.about_page = QWidget()
        self.setup_about_page()
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

    def setup_main_page(self):
        layout = QGridLayout(self.main_page)
        layout.setContentsMargins(30, 30, 30, 30)

        # ID
        id_label = QLabel("ID:")
        self.id_input = QLineEdit()
        layout.addWidget(id_label, 0, 0)
        layout.addWidget(self.id_input, 0, 1)

        # API Hash
        api_hash_label = QLabel("API Hash:")
        self.api_hash_input = QLineEdit()
        layout.addWidget(api_hash_label, 1, 0)
        layout.addWidget(self.api_hash_input, 1, 1)

        # 手机号
        phone_label = QLabel("手机号:")
        self.phone_input = QLineEdit()
        layout.addWidget(phone_label, 2, 0)
        layout.addWidget(self.phone_input, 2, 1)

        # 保存/获取数据按钮
        self.main_btn_2 = QPushButton("保存并获取数据")
        # 修改信号发射方式
        self.main_btn_2.clicked.connect(
            lambda: self.main_button_clicked_signal.emit())  # 连接 "main_button_clicked" 信号到 main_button 点击事件

        layout.addWidget(self.main_btn_2, 3, 0, 1, 2, Qt.AlignCenter)

        # 显示数据
        self.export_info_label = QLabel("")
        layout.addWidget(self.export_info_label, 4, 0, 1, 2)

    def setup_settings_page(self):
        layout = QGridLayout(self.settings_page)
        layout.setContentsMargins(30, 30, 30, 30)

        # 代理类型
        proxy_type_label = QLabel("代理类型:")
        layout.addWidget(proxy_type_label, 0, 0)

        self.proxy_type_group = QHBoxLayout()
        layout.addLayout(self.proxy_type_group, 0, 1)

        self.socks5_radio = QRadioButton("socks5")
        self.socks4_radio = QRadioButton("socks4")
        self.http_radio = QRadioButton("http")
        self.https_radio = QRadioButton("https")

        self.proxy_type_radio_list = [self.socks5_radio, self.socks4_radio, self.http_radio, self.https_radio]

        for radio in self.proxy_type_radio_list:
            self.proxy_type_group.addWidget(radio)
        self.proxy_type_group.addStretch(1)  # 将单选框左对齐

        self.socks5_radio.setChecked(True)  # 默认选中socks5

        # 代理IP
        proxy_ip_label = QLabel("代理IP:")
        self.proxy_ip_input = QLineEdit()
        layout.addWidget(proxy_ip_label, 1, 0)
        layout.addWidget(self.proxy_ip_input, 1, 1)

        # 代理端口
        proxy_port_label = QLabel("代理端口:")
        self.proxy_port_input = QLineEdit()
        layout.addWidget(proxy_port_label, 2, 0)
        layout.addWidget(self.proxy_port_input, 2, 1)

        # 用户名
        username_label = QLabel("用户名:")
        self.username_input = QLineEdit()
        layout.addWidget(username_label, 3, 0)
        layout.addWidget(self.username_input, 3, 1)

        # 密码
        password_label = QLabel("密码:")
        self.password_input = QLineEdit()
        layout.addWidget(password_label, 4, 0)
        layout.addWidget(self.password_input, 4, 1)

        # 保存并验证按钮和文本标签
        self.save_verify_btn = QPushButton("保存并验证")
        self.save_verify_btn.clicked.connect(self.save_verify_button_clicked_signal.emit)
        self.verify_label = QLabel("")
        layout.addWidget(self.save_verify_btn, 5, 0, 1, 2, Qt.AlignCenter)
        layout.addWidget(self.verify_label, 6, 0, 1, 2)

    def setup_about_page(self):
        layout = QVBoxLayout(self.about_page)
        layout.setContentsMargins(20, 20, 20, 20)
        self.about_text = QTextBrowser()  # 修改 QTextEdit 为 QTextBrowser
        self.about_text.setReadOnly(True)  # 设置为只读
        with open("app/about.md", "r", encoding="utf-8") as f:
            markdown_text = f.read()
        html = markdown.markdown(markdown_text)  # 使用 markdown 将 markdown 文本转换为 html
        self.about_text.setHtml(html)  # 将 html 添加到 QTextBrowser
        # 设置页内的超链接以新窗口的形式打开
        self.about_text.setOpenExternalLinks(True)
        layout.addWidget(self.about_text)

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
