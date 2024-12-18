from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit,
    QHBoxLayout, QGridLayout, QRadioButton
)


class UiSettingsPage(QWidget):
    # 定义信号
    save_verify_button_clicked_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
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

        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout(self)
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
