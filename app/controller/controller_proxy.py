import requests
import traceback
from PyQt5.QtCore import QThread, pyqtSignal


def verify_proxy(proxy):
    try:
        proxy_type = 'https'
        if len(proxy) == 3:
            response = requests.get(
                "https://www.google.com",
                proxies={proxy_type: f"{proxy[0].lower()}://{proxy[1]}:{proxy[2]}"},
                timeout=5
            )
        else:
            response = requests.get(
                "https://www.google.com",
                proxies={proxy_type: f"{proxy[0].lower()}://{proxy[3]}:{proxy[4]}@{proxy[1]}:{proxy[2]}"},
                timeout=5
            )
    except:
        print(traceback.format_exc())
        return False
    if response.status_code == 200:
        return True
    else:
        return False


# 创建一个自定义的线程类
class ProxyVerifyThread(QThread):
    # 定义一个信号，用于在验证完成后向主线程传递信息
    finished_signal = pyqtSignal(bool)

    def __init__(self, proxy):
        super().__init__()
        self.proxy = proxy

    def run(self):
        # 执行代理验证逻辑
        verify_success = verify_proxy(self.proxy)
        # 发送信号，传递验证结果
        self.finished_signal.emit(verify_success)


class ControllerProxy:
    def __init__(self, main_controller, ui):
        self.main_controller = main_controller
        self.ui = ui
        self.proxy_thread = None
        self.ui.save_verify_button_clicked_signal.connect(self.on_save_verify_button_clicked)

    def on_set_page(self, index):
        if index == 1:  # 当切换到设置界面时
            if self.main_controller.proxy_settings:
                #  更新 UI 界面
                self.update_settings_ui()
            else:
                # 如果没有找到配置
                self.clear_settings_ui()
                self.ui.settings_page.verify_label.setText("")

    def update_settings_ui(self):
        if self.main_controller.proxy_settings:
            if len(self.main_controller.proxy_settings) == 3:
                proxy_type, proxy_ip, proxy_port = map(str, self.main_controller.proxy_settings)
                username = ''
                password = ''
            else:
                proxy_type, proxy_ip, proxy_port, username, password = map(str, self.main_controller.proxy_settings)
            for radio in self.ui.settings_page.proxy_type_radio_list:
                radio.setChecked(radio.text() == proxy_type)
            self.ui.settings_page.proxy_ip_input.setText(proxy_ip)
            self.ui.settings_page.proxy_port_input.setText(proxy_port)
            self.ui.settings_page.username_input.setText(username)
            self.ui.settings_page.password_input.setText(password)

    def clear_settings_ui(self):
        for radio in self.ui.settings_page.proxy_type_radio_list:
            radio.setChecked(False)
        self.ui.settings_page.proxy_ip_input.clear()
        self.ui.settings_page.proxy_port_input.clear()
        self.ui.settings_page.username_input.clear()
        self.ui.settings_page.password_input.clear()

    def on_save_verify_button_clicked(self):
        # 禁用按钮
        self.ui.settings_page.save_verify_btn.setEnabled(False)
        self.ui.settings_page.verify_label.setText("正在验证代理...")
        self.ui.settings_page.verify_label.setStyleSheet("color: black")

        proxy_type = ""
        for radio in self.ui.settings_page.proxy_type_radio_list:
            if radio.isChecked():
                proxy_type = radio.text()

        proxy_ip = self.ui.settings_page.proxy_ip_input.text()
        proxy_port = self.ui.settings_page.proxy_port_input.text()
        username = self.ui.settings_page.username_input.text()
        password = self.ui.settings_page.password_input.text()

        # 使用代理访问Google
        if username and password:
            proxy = (proxy_type, proxy_ip, proxy_port, username, password)
        else:
            proxy = (proxy_type, proxy_ip, proxy_port)

        # 创建并启动线程
        self.proxy_thread = ProxyVerifyThread(proxy)
        self.proxy_thread.finished_signal.connect(self.on_verify_finished)
        self.proxy_thread.start()

    def on_verify_finished(self, result):
        if result:
            self.ui.settings_page.verify_label.setText("配置已保存，代理验证成功")
            self.ui.settings_page.verify_label.setStyleSheet("color: green")
            # 保存配置到 Controller
            proxy_type = ""
            for radio in self.ui.settings_page.proxy_type_radio_list:
                if radio.isChecked():
                    proxy_type = radio.text()
            proxy_ip = self.ui.settings_page.proxy_ip_input.text()
            proxy_port = self.ui.settings_page.proxy_port_input.text()
            username = self.ui.settings_page.username_input.text()
            password = self.ui.settings_page.password_input.text()

            if username and password:
                self.main_controller.proxy_settings = (proxy_type, proxy_ip, int(proxy_port), username, password)
            else:
                self.main_controller.proxy_settings = (proxy_type, proxy_ip, int(proxy_port))
            print("proxy saved:", self.main_controller.proxy_settings)
        else:
            self.ui.settings_page.verify_label.setText("代理验证失败，请检查配置")
            self.ui.settings_page.verify_label.setStyleSheet("color: red")
        # 无论如何都需要启用按钮
        self.ui.settings_page.save_verify_btn.setEnabled(True)
