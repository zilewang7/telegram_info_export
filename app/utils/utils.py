import os
import re
import sys


def get_resource_path(relative_path):
    """ Get absolute path to resource, resource files are located to exe file directory
    """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def get_display_width(s):
    """
    计算字符串的显示宽度
    中文字符算2个宽度，英文字符算1个宽度
    """
    if not isinstance(s, str):
        s = str(s)
    # 使用正则表达式分辨中文字符和非中文字符
    zh_pattern = re.compile(u'[\u4e00-\u9fa5]')
    width = 0
    for ch in s:
        if zh_pattern.match(ch):
            width += 2
        else:
            width += 1
    return width
