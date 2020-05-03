"""
Created on 2019/5/18 19:12
将markdown文件中的图片转换成 base64编码
@author: hujing
"""
from src.Args import arg
from src.MarkdownFile import MarkdownFile


if __name__ == '__main__':
    # 检查版本号
    arg.check_version()
    # 判断是否输出帮助文档
    if arg.need_print_help():
        arg.print_help()
    # 处理文件
    MarkdownFile.change_md_image()
    print('成功处理文件: ' + arg.in_file)
    print('处理后的文件为: ' + arg.out_file)
