from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPlainTextEdit, QHBoxLayout, QPushButton, QGridLayout, \
    QLineEdit, QTextEdit

from comfunc.confwidget_operate_encapsulation import ConfWidgetFuncEncap

ex_infos = [
    {'btn_name': '按正则表达式提取', 'hold_text': '在此处输入正则表达式'},
    {'btn_name': '按JSONPATH提取', 'hold_text': '在此处输jsonpath表达式'}
]

class Tab2(QWidget, ConfWidgetFuncEncap):
    def __init__(self):
        super().__init__()
        self.init_layout()

    def init_layout(self):
        self.tab2_layout = QHBoxLayout()
        self.setLayout(self.tab2_layout)
        self.resp_layout = QVBoxLayout()
        self.ex_layout = QVBoxLayout()
        self.layout().addLayout(self.resp_layout)
        self.create_line(self.layout(), 'VLine')
        self.layout().addLayout(self.ex_layout)
        self.resp_widget_init()
        self.ex_widget_init()
        return self.tab2_layout

    def resp_widget_init(self):
        # 创建 QPlainTextEdit 实例
        self.resp_text_edit = QPlainTextEdit()
        self.add_widget_to_layout(self.resp_layout, self.resp_text_edit)
        # 设置初始文本
        self.resp_text_edit.setPlaceholderText("在此处粘贴文本内容")

        # 创建button按钮布局
        resp_btn_payout = QHBoxLayout()
        self.resp_layout.addLayout(resp_btn_payout)

        resp_btn_json = QPushButton("提取JSON")
        # 设置按钮的提示信息
        resp_btn_json.setToolTip("（按正则的贪婪模式匹配到的第一个json）")
        resp_btn_json.clicked.connect(self.get_resp_json)
        self.add_widget_to_layout(resp_btn_payout, resp_btn_json)

        resp_btn_clear = QPushButton("清空文本")
        resp_btn_clear.clicked.connect(lambda: self.clear_plain_text(self.resp_text_edit))
        self.add_widget_to_layout(resp_btn_payout, resp_btn_clear)

    def ex_widget_init(self):
        ex_grid_layout = QGridLayout()
        self.ex_layout.addLayout(ex_grid_layout)
        for i, _ex in enumerate(ex_infos):
            for _k, _v in _ex.items():
                if _k == 'btn_name':
                    ex_grid_layout.addWidget(QPushButton(_v), i, 1)
                else:
                    line_edit = QLineEdit(self)
                    line_edit.setPlaceholderText(_v)
                    ex_grid_layout.addWidget(line_edit, i, 0)
        # 创建一个QTextEdit控件并设置其内容
        text_edit = QTextEdit()
        text_edit.setPlainText('formatted_json')
        text_edit.setReadOnly(True)  # 设置为只读模式
        self.ex_layout.addWidget(text_edit)

    def get_resp_json(self):
        pass

