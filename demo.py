import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit, QPushButton


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建布局
        layout = QVBoxLayout()

        # 创建 QPlainTextEdit 实例
        self.plain_text_edit = QPlainTextEdit()
        self.plain_text_edit.setPlainText("欢迎使用 QPlainTextEdit！")

        # 创建按钮
        self.btn_clear = QPushButton("清空文本")
        self.btn_clear.clicked.connect(self.clear_text)

        self.btn_get_text = QPushButton("获取文本")
        self.btn_get_text.clicked.connect(self.get_text)

        # 将控件添加到布局中
        layout.addWidget(self.plain_text_edit)
        layout.addWidget(self.btn_clear)
        layout.addWidget(self.btn_get_text)

        # 设置布局
        self.setLayout(layout)

        # 设置窗口属性
        self.setWindowTitle('QPlainTextEdit 示例')
        self.setGeometry(300, 300, 400, 300)

    def clear_text(self):
        self.plain_text_edit.clear()

    def get_text(self):
        text = self.plain_text_edit.toPlainText()
        print("当前文本内容：", text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())