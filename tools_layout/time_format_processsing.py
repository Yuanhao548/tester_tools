from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from comfunc.confwidget_operate_encapsulation import ConfWidgetFuncEncap


class Tab3(QWidget, ConfWidgetFuncEncap):
    def __init__(self):
        super().__init__()
        self.setLayout(self.init_layout())

    def init_layout(self):
        tab2_layout = QVBoxLayout()
        label2 = QLabel("This is the third tab")
        tab2_layout.addWidget(label2)
        return tab2_layout