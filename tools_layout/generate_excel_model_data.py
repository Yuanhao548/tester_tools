from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QGridLayout, QComboBox, \
    QFrame, QHBoxLayout, QMessageBox, QDialog

from comfunc.confwidget_operate_encapsulation import ConfWidgetFuncEncap
from comfunc.mock_data import mock_datas
from comfunc.operate_excel import read_excel_by_row, load_excel_and_write_mock

class Tab1(QWidget, ConfWidgetFuncEncap):
    def __init__(self):
        super().__init__()
        self.setLayout(self.init_layout())

    def init_layout(self):
        self.tab1_layout = QVBoxLayout()
        label1 = QLabel("打开模板Excel（模板字段可指定行号）")
        self.template_line_edit = QLineEdit(self)
        # 设置默认提示文本
        self.template_line_edit.setPlaceholderText("请输入行号")
        self.number_line_edit_validator(self.template_line_edit)

        self.open_excel_button = QPushButton()
        self.open_excel_button.clicked.connect(self.open_file)  # 连接按钮点击事件
        icon = QIcon("picture/EXCEL.png")  # 请将 "path_to_your_icon.png" 替换为你实际的图标文件路径
        self.open_excel_button.setIcon(icon)
        self.open_excel_button.setIconSize(icon.actualSize(self.open_excel_button.iconSize()))  # 使图标大小与按钮大小匹配
        self.open_excel_button.setFixedSize(100, 100)  # 设置按钮的固定大小

        self.tab1_layout.addWidget(label1)
        self.tab1_layout.addWidget(self.template_line_edit)
        self.tab1_layout.addWidget(self.open_excel_button)
        return self.tab1_layout

    def open_file(self):
        # 弹出文件对话框，让用户选择文件
        self.tab1_excel_row_index = self.validate_required_input(self.template_line_edit)
        if self.tab1_excel_row_index:
            self.tab1_file_name, _ = QFileDialog.getOpenFileName(self, "选择excel模板文件", "", "excel文件 (*.xlsx);;")
            # 检查用户是否选择了文件
            if self.tab1_file_name:
                row_data = read_excel_by_row(self.tab1_file_name, self.tab1_excel_row_index)
                self.show_child_dialog(row_data)

    def show_child_dialog(self, row_data):
        tab1_dialog = ChildDialog(self, row_data)
        tab1_dialog.exec_()


class ChildDialog(QDialog, ConfWidgetFuncEncap):
    def __init__(self, parent=None, row_data=None):
        super().__init__(parent)
        self.setWindowTitle("按Excel模板生成数据")
        self.setGeometry(200, 200, 400, 400)
        self.child_layout = QVBoxLayout()
        self.setLayout(self.child_layout)
        self.init_layout(row_data)
        self.tab1_file_name = parent.tab1_file_name
        self.tab1_excel_row_index = parent.tab1_excel_row_index

    def init_layout(self, params):
        self.tab1_grid_layout = QGridLayout()
        self.child_layout.addLayout(self.tab1_grid_layout)
        combobox_keys = [_['key'] for _ in mock_datas]
        combobox_keys.append('自定义')
        self.tab1_data = []
        self.tab1_comboboxs = []
        self.tab1_custom_lineEdit_dict = {}

        def tab1_combobox_changed(combobox):
            i = self.tab1_comboboxs.index(combobox)
            selected_text = combobox.currentText()
            # 若是选择了自定义，就增加输入的控件
            if selected_text == '自定义':
                line_edit = QLineEdit(self)
                self.tab1_custom_lineEdit_dict[i] = line_edit
                # 设置默认提示文本
                line_edit.setPlaceholderText("请输入枚举值，若需要从多个枚举值中随机取值，多个值之间用逗号分隔")
                self.tab1_grid_layout.addWidget(line_edit, i, 2)  # 在第 i 行，第 2 列添加自定义输入
            else:
                # 清楚在（i，2）位置上的控件，并且移除如果之前设置为自定义，但现在已不是的
                self.clear_item_grid_layout_widget(self.tab1_grid_layout, i, 2)
                self.tab1_custom_lineEdit_dict = {_k: _v for _k, _v in self.tab1_custom_lineEdit_dict.items()
                                                  if _k != i}

        for _i, _v in enumerate(params):
            # 设置字段的数据类型
            tab1_combobox = QComboBox(self)
            self.tab1_comboboxs.append(tab1_combobox)
            # 添加选项
            tab1_combobox.addItems(combobox_keys)
            # 连接下拉列表选项改变事件
            tab1_combobox.currentIndexChanged.connect(lambda index, cb=tab1_combobox: tab1_combobox_changed(cb))
            self.tab1_grid_layout.addWidget(QLabel(_v), _i, 0)  # 在第 i 行，第 0 列添加标签
            self.tab1_grid_layout.addWidget(tab1_combobox, _i, 1)  # 在第 i 行，第 1 列添加按钮

        self.create_line(self.layout())

        generate_data_layout = QHBoxLayout()
        self.layout().addLayout(generate_data_layout)
        # 创建文本框
        self.tab1_data_much_edit = QLineEdit(self)
        self.number_line_edit_validator(self.tab1_data_much_edit)
        generate_data_layout.addWidget(QLabel("生成多少行"))
        generate_data_layout.addWidget(self.tab1_data_much_edit)

        generate_button = QPushButton('开始生成')
        self.layout().addWidget(generate_button)
        generate_button.clicked.connect(self.generate_data)  # 连接按钮点击事件

    def generate_data(self):
        custom_value_dict = {}
        excel_item_data = []
        generate_number = int(self.validate_required_input(self.tab1_data_much_edit, 0))
        if generate_number:
            mock_k_v_dict = {_i['key']: _i['value'] for _i in mock_datas}
            for _i, _v in self.tab1_custom_lineEdit_dict.items():
                custom_value_dict[_i] = self.validate_required_input(_v)
                if not custom_value_dict[_i]:
                    return
            custom_value_indexs = [_ci for _ci in custom_value_dict.keys()]
            # 获取当前选中的文本
            if self.tab1_comboboxs:
                for i, combo_box in enumerate(self.tab1_comboboxs):
                    selected_text = combo_box.currentText()
                    excel_item_data.append(selected_text)
                for _i, _e in enumerate(excel_item_data):
                    if _e == '自定义':
                        excel_item_data[_i] = custom_value_dict[_i]
                    else:
                        excel_item_data[_i] = mock_k_v_dict[_e]
                print('excel_item_data:', excel_item_data)
                load_excel_and_write_mock(self.tab1_file_name, excel_item_data, int(self.tab1_excel_row_index) + 1,
                                          generate_number, custom_value_indexs)
                self.accept()
