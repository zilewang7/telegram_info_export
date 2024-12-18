import requests
import markdown
from app.version import VERSION
from PyQt5.QtCore import pyqtSignal, QThread
from app.utils.utils import get_resource_path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextBrowser
)


class AboutPageUpdater(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, about_path):
        super().__init__()
        self.about_path = about_path

    def run(self):
        markdown_text = ""
        try:
            with open(self.about_path, "r", encoding="utf-8") as f:
                markdown_text = f.read()
        except Exception as e:
            print(f"加载本地 about.md 失败: {e}")

        markdown_text = markdown_text.replace(
            '{current_version}', VERSION
        )
        base_url = 'https://raw.githubusercontent.com/jiongjiongJOJO/telegram_info_export/refs/heads/master/'
        try:
            # 获取远程 about.md 内容
            response_markdown_text = requests.get(
                base_url + 'app/about.md',
                timeout=5  # 设置超时时间为5秒
            )
            response_markdown_text.raise_for_status()  # 如果请求不成功，抛出异常
            markdown_text = response_markdown_text.text
            print('成功获取远程 about.md')
        except requests.exceptions.RequestException as e:
            print(f"获取远程 about.md 文件失败: {e}")
        try:
            # 获取远程 version.py 文件
            response_latest_version = requests.get(
                base_url + 'app/version.py',
                timeout=5  # 设置超时时间为5秒
            )
            response_latest_version.raise_for_status()  # 如果请求不成功，抛出异常
            latest_version = response_latest_version.text
            namespace = {}
            exec(latest_version, namespace)
            markdown_text = markdown_text.replace(
                '{latest_version}',
                namespace.get('VERSION', '<span style="color: red;">unknown</span>')
            )
            print('成功获取远程 version.py')
        except requests.exceptions.RequestException as e:
            print(f"获取远程 version.py 文件失败: {e}")
            markdown_text = markdown_text.replace(
                '{latest_version}', '<span style="color: red;">unknown</span>'
            )

        markdown_text = markdown_text.replace(
            '{current_version}', VERSION
        )
        self.update_signal.emit(markdown_text)


class UiAboutPage(QWidget):
    def __init__(self):
        super().__init__()
        self.about_page_updater = None
        self.about_text = None
        self.about_path = get_resource_path("app/about.md")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        self.about_text = QTextBrowser()
        self.about_text.setReadOnly(True)
        markdown_text = ""
        try:
            with open(self.about_path, "r", encoding="utf-8") as f:
                markdown_text = f.read()
        except Exception as e:
            print(f"加载本地 about.md 失败: {e}")

        markdown_text = markdown_text.replace(
            '{current_version}', VERSION
        )
        markdown_text = markdown_text.replace(
            '{latest_version}', '<span style="color: #2196f3;">正在获取……</span>'
        )

        html = markdown.markdown(markdown_text)
        self.about_text.setHtml(html)
        self.about_text.setOpenExternalLinks(True)
        layout.addWidget(self.about_text)
        # 实例化 QThread线程
        self.about_page_updater = AboutPageUpdater(self.about_path)
        # 连接信号槽
        self.about_page_updater.update_signal.connect(self.update_about_text_browser)
        # 启动线程
        self.about_page_updater.start()

    def update_about_text_browser(self, markdown_text):
        html = markdown.markdown(markdown_text)
        self.about_text.setHtml(html)
