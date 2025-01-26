import ast
import json


def is_parentheses_matched(pattern):
    stack = []
    for char in pattern:
        if char == '(':
            # 遇到左括号，将其压入栈中
            stack.append(char)
        elif char == ')':
            if not stack:
                # 栈为空，说明右括号没有对应的左括号，不匹配
                return False
            # 弹出栈顶元素
            stack.pop()
    # 遍历结束后，栈为空表示所有括号都匹配
    return len(stack) == 0

def ast_to_str(unicode_str):
    text = ast.literal_eval(unicode_str)
    return text

def is_valid_json(json_str):
    try:
        # 尝试将字符串解析为 Python 对象
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        # 若解析过程中抛出 JSONDecodeError 异常，说明字符串不是有效的 JSON 格式
        return False

def parse_json_path(json_data, json_path):
    """
    解析 JSON 路径并返回对应的值，支持通配符 `[*]`。

    :param json_data: 要解析的 JSON 数据（字典或列表）
    :param json_path: JSON 路径字符串，例如 "result[*].name"
    :return: 路径对应的值，如果路径无效则返回 None
    """
    json_data = json_data.replace('null', '"null"').replace('true', '"true"').replace('false', '"false"')
    if (is_valid := is_valid_json(json_data)):
        json_data = eval(json_data)
        parts = json_path.split('.')
        current_data = [json_data]

        for part in parts:
            new_data = []
            if part.endswith('[*]'):
                key = part[:-3]
                for item in current_data:
                    if isinstance(item, dict) and key in item:
                        sub_items = item[key]
                        if isinstance(sub_items, list):
                            new_data.extend(sub_items)
            elif '[' in part and ']' in part:
                key, index_str = part.split('[')
                index = int(index_str[:-1])
                for item in current_data:
                    if isinstance(item, dict) and key in item:
                        sub_item = item[key]
                        if isinstance(sub_item, list) and 0 <= index < len(sub_item):
                            new_data.append(sub_item[index])
            else:
                for item in current_data:
                    if isinstance(item, dict) and part in item:
                        new_data.append(item[part])

            if not new_data:
                return None
            current_data = new_data

        return current_data
    else:
        raise Exception('JSONDecodeError异常，源数据不是有效的 JSON 格式')
