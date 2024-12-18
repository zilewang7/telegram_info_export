import sys
from app.ui.ui import Ui
from app.controller.controller import Controller
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui()
    controller = Controller(ui)
    ui.show()
    sys.exit(app.exec_())
