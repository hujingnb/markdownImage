"""
命令行读取
@author hujing
"""
import sys
import time
from .Args import arg


def print_debug_info(msg):
    """
    输出调试信息
    :param msg:
    :return:
    """
    if arg.debug:
        date_str = time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime())
        print("debug info: " + date_str, end="")
        print(msg)
        # 输出文件与行号
        if hasattr(sys, "_getframe"):
            trace = sys._getframe(1)
            print(f"\t{trace.f_code.co_filename}:{trace.f_lineno}  function: {trace.f_code.co_name}")
