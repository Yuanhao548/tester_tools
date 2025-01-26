import ast
import json
import re

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPlainTextEdit, QHBoxLayout, QPushButton, QGridLayout, \
    QLineEdit, QTextEdit, QMessageBox

from comfunc.conf import is_parentheses_matched, ast_to_str, parse_json_path
from comfunc.conf_constant import RE_PATTERN_WITH_PARENTHESES
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
        resp_btn_clear.clicked.connect(lambda: self.clear_plain_text_edit(self.resp_text_edit))
        self.add_widget_to_layout(resp_btn_payout, resp_btn_clear)

    def ex_widget_init(self):
        ex_grid_layout = QGridLayout()
        self.ex_layout.addLayout(ex_grid_layout)
        self.ex_btns = []
        self.ex_line_edits = []
        # 创建一个QTextEdit控件并设置其内容
        ex_text_edit = QTextEdit()

        for i, _ex in enumerate(ex_infos):
            for _k, _v in _ex.items():
                if _k == 'btn_name':
                    ex_btn = QPushButton(_v)
                    self.ex_btns.append(ex_btn)
                    ex_grid_layout.addWidget(ex_btn, i, 1)
                else:
                    ex_line_edit = QLineEdit(self)
                    self.ex_line_edits.append(ex_line_edit)
                    ex_line_edit.setPlaceholderText(_v)
                    ex_grid_layout.addWidget(ex_line_edit, i, 0)
            # 使用默认参数解决 lambda 函数参数问题
            self.ex_btns[i].clicked.connect(lambda _, index=i: self.ex_btn_clicked(index, ex_text_edit))

        self.set_plain_text_edit(ex_text_edit, '输出符合格式的内容')
        self.add_widget_to_layout(self.ex_layout, ex_text_edit)

    def ex_btn_clicked(self, i, text_edit):
        result_str = ''
        if (resp_plain_text := self.plain_text_edit_validate_required(self.resp_text_edit, message='待提取的源数据不能为空')):
            if i == 0:
                try:
                    if (ex_line_re := self.validate_required_input(self.ex_line_edits[i], message='正则表达式不能为空')):
                        if (is_multi_groups := (re.search(RE_PATTERN_WITH_PARENTHESES, ex_line_re, re.S))):
                            if (is_parentheses := is_parentheses_matched(ex_line_re)):
                                re_extract_value = re.findall(ex_line_re, resp_plain_text, re.S)
                            else:
                                raise Exception('正则表达式中的圆括号需成对出现，如需要匹配括号本身，请加转义符号，例如"\)"')
                        else:
                            try:
                                re_extract_value = re.search(ex_line_re.replace('(', '\(').replace(')', '\)'),
                                                             resp_plain_text, re.S).group()
                            except Exception:
                                re_extract_value = ''
                        if isinstance(re_extract_value, list) and re_extract_value:
                            for _i, _v in enumerate(re_extract_value):
                                result_str += f'第{_i+1}组匹配上的内容为：{ast_to_str(json.dumps(_v))}.\n'
                        else:
                            result_str += f'匹配该正则表达式的内容为：{ast_to_str(json.dumps(re_extract_value))}' \
                                if re_extract_value else '没有匹配该正则表达式的内容'
                except Exception as e:
                    self.message_box_warning(str(e))
            else:
                if (ex_line_json := self.validate_required_input(self.ex_line_edits[i], message='jsonPath表达式不能为空')):
                    try:
                        json_str = parse_json_path(resp_plain_text, ex_line_json)
                        result_str += f'符合该jsonPath路径的内容为：{ast_to_str(json.dumps(json_str))}' \
                            if json_str else '没有匹配该jsonPath表达式的内容'
                    except Exception as e:
                        self.message_box_warning(str(e))
            self.set_plain_text_edit(text_edit, result_str) if result_str else None

    def get_resp_json(self):
        if (resp_plain_text := self.plain_text_edit_validate_required(self.resp_text_edit, message='待提取的源数据不能为空')):
            try:
                re_extract_value = re.search('\{.*\}', resp_plain_text, re.S).group()
                self.set_plain_text_edit(self.resp_text_edit, re_extract_value, False)
            except Exception:
                self.message_box_warning('待匹配内容中没有满足json格式的数据')
                self.set_plain_text_edit(self.resp_text_edit, '', False)
