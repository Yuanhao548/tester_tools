from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMessageBox, QWidget, QFrame


class ConfWidgetFuncEncap:
    def __init__(self):
        pass

    @staticmethod
    # 创建一个 QIntValidator 并设置范围
    def number_line_edit_validator(line_edit, top=10000):
        int_validator = QIntValidator()
        int_validator.setRange(1, top)  # 允许输入的范围是 0 到 10000，可以根据需要修改
        line_edit.setValidator(int_validator)

    # 校验line_edit组件必填
    def validate_required_input(self, line_edit, default=None):
        text = line_edit.text()
        if not text:
            QMessageBox.warning(self, "Input Error", "This field is required.")
            return default
        return text

    # 定义一个函数来清空布局并重新添加控件
    @staticmethod
    def clear_layout(layout):
        # 清空布局
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    # 清空gridlayout布局某个位置的控件
    @staticmethod
    def clear_item_grid_layout_widget(grid_layout, row, column):
        item = grid_layout.itemAtPosition(row, column)
        if item:
            widget = item.widget()
            if widget:
                grid_layout.removeWidget(widget)
                widget.setParent(None)
                print(f"Cleared widget at ({row}, {column})")
        else:
            print(f"No widget at ({row}, {column})")

    @staticmethod
    def add_widget_to_layout(layout, widget):
        layout.addWidget(widget)

    @staticmethod
    def clear_plain_text(plain_text_edit):
        plain_text_edit.clear()

    def create_line(self, layout, frame_shape='HLine'):
        # 创建一个水平分割线并添加到当前布局
        horizontal_separator = QFrame()
        horizontal_separator.setFrameShape(getattr(QFrame, frame_shape))
        horizontal_separator.setFrameShadow(QFrame.Sunken)
        # layout.addWidget(horizontal_separator)
        self.add_widget_to_layout(layout, horizontal_separator)