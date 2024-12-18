from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QGridLayout
)


class UiMainPage(QWidget):
    # 定义信号
    main_button_clicked_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.export_info_label = None
        self.phone_input = None
        self.main_btn_2 = None
        self.api_hash_input = None
        self.id_input = None

        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout(self)
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
        self.main_btn_2 = QPushButton("导出数据")
        # 修改信号发射方式
        self.main_btn_2.clicked.connect(
            lambda: self.main_button_clicked_signal.emit())  # 连接 "main_button_clicked" 信号到 main_button 点击事件

        layout.addWidget(self.main_btn_2, 3, 0, 1, 2, Qt.AlignCenter)

        # 显示数据
        self.export_info_label = QLabel("")
        layout.addWidget(self.export_info_label, 4, 0, 1, 2)

