from app.utils.utils import get_resource_path
from app.controller.controller_proxy import ControllerProxy
from app.controller.controller_export import ControllerExport


class Controller:
    def __init__(self, ui):
        self.style_path = get_resource_path("style/style.qss")
        self.ui = ui
        self.ui.load_stylesheet(self.style_path)  # 在这里加载样式表
        self.proxy_settings = None
        self.is_main_button_running = False

        self.proxy_controller = ControllerProxy(self, ui)
        self.export_controller = ControllerExport(self, ui)

        self.setup_connections()

    def setup_connections(self):
        self.ui.set_page_signal.connect(self.on_set_page)

    def on_set_page(self, index):
        self.ui.set_current_page(index)
        self.proxy_controller.on_set_page(index)  # 调用proxy控制器的相关方法
