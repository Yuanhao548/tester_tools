import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from tools_layout.generate_excel_model_data import Tab1
from tools_layout.batch_send_http_request import Tab2
from tools_layout.time_format_processsing import Tab3

version = 1.0
base_dir = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"测试者工具{version}")
        self.setGeometry(100, 100, 1000, 500)
        # 创建一个主部件，用于放置布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 创建一个水平布局
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # 创建一个垂直布局，用于放置 QTabWidget
        tab_layout = QVBoxLayout()
        main_layout.addLayout(tab_layout)

        # 创建一个伸缩项，用于将 QTabWidget 推到右侧
        # spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # main_layout.addItem(spacer)

        # 创建一个 QTabWidget
        tab_widget = QTabWidget()
        tab_widget.setGeometry(200, 0, 300, 300)  # 设置 QTabWidget 的位置和大小

        # 设置字体
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        tab_widget.setFont(font)

        tab1 = Tab1()
        tab2 = Tab2()
        tab3 = Tab3()

        # 将选项卡添加到 QTabWidget 中
        tab_widget.addTab(tab1, "按Excel模板生成数据")
        # tab_widget.addTab(tab2, "批量发送HTTP请求")
        tab_widget.addTab(tab2, "提取json中的数据")
        tab_widget.addTab(tab3, "时间格式处理")

        # 将 QTabWidget 放置在 tab_layout 中
        tab_layout.addWidget(tab_widget)


if __name__ == '__main__':
    # 创建应用程序对象
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # 进入应用程序事件循环
    sys.exit(app.exec_())