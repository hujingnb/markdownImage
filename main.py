"""
Created on 2019/5/18 19:12
将markdown文件中的图片转换成 base64编码
@author: hujing
"""
from src.ImageBase64 import ImageBase64
import re
import uuid
import getopt
import os
import sys


def dispose_image_to_base64(file_path, content, is_use_id):
    """
    将内容中的图片标签转换成base64编码后返回
    :param file_path: 文件路径
    :param content: 字符串内容
    :param is_use_id: 是否使用id替换内容
    :return:
    """
    # 正则匹配图片tag
    img_tag_pattern = re.compile(r'!\[[^\]]*\]\([^\(\)]*\)')
    # 正则匹配图片标签中的图片url
    img_url_pattern = re.compile(r'\(([^\)]*)')
    search = img_tag_pattern.findall(content)
    # 不存在图片标签
    if not search:
        return content, dict()
    img_id_map = dict()
    # 遍历处理每一个图片内容
    for each in search:
        # 拿到图片url
        img_url_word = img_url_pattern.search(each)
        # 若没有匹配到, 跳过
        if not img_url_word:
            continue
        img_url_word = img_url_word.group(1)
        # 若路径是相对路径,将路径与md文件目录拼接
        if not os.path.isabs(img_url_word):
            img_url = os.path.join(os.path.dirname(file_path), img_url_word)
        else:
            img_url = img_url_word
        # 获取图片的base64
        img_base64 = ImageBase64.base64_img(img_url)
        # 将图片base64直接放到标签中
        if not is_use_id:
            # 将base64转到图片标签中
            content = content.replace(img_url_word, img_base64)
        # 将图片标签中存放id, id放到文件最后
        else:
            img_id = str(uuid.uuid1())
            img_id_map[img_id] = img_base64
            content = content.replace('(' + img_url_word + ')', '[' + img_id + ']')
    return content, img_id_map


def change_md_image(in_file_path, out_file_path, is_use_id=False, encoding='utf-8'):
    """
    将markdown文件中的图片路径修改为base64编码
    :param in_file_path 输入markdown文件路径
    :param out_file_path 输出markdown文件路径
    :param is_use_id 是否在markdown文件中使用id, 存放到文件最后
    :param encoding 文件编码, 默认utf8
    :rtype: object
    """
    # 保存图片id的map,在最后将id写出到文件
    img_id_map = dict()
    with open(out_file_path, 'w+', encoding=encoding) as out_file, \
            open(in_file_path, 'r', encoding=encoding) as in_file:
        # 读取输入文件
        for line in in_file.readlines():
            line, this_img_id_map = dispose_image_to_base64(in_file_path, line, is_use_id)
            img_id_map.update(this_img_id_map)
            # 写入输出文件
            out_file.write(line)
        # 遍历完成, 将id写入文件最后
        for key, value in img_id_map.items():
            out_file.write(os.linesep + '[' + key + ']:' + value+ os.linesep)


def print_help():
    """
    输出帮助文档
    :rtype: object
    """
    print("""
参数如下: 
    -h/--help: 显示帮助文档
    -i/--in: md文件路径, 必填
    -o/--out: md输出文件路径, 默认 原文件名.md2.md
    -d/--id: 是否使用id表示, 默认不适用, 0(不使用),1(使用)
    -e/--encoding: 文件编码, 默认utf-8
        制作者: 靖哥哥
    """)


def read_args():
    """
    读取命令行参数
    :return 参数map
    """
    # 读取参数
    result = dict()
    tmp, args = getopt.getopt(sys.argv[1:], 'i:o:d:e:h', ['encoding=', 'out=', 'in=', 'id=', 'help'])
    # 读取参数
    for comm in tmp:
        # 帮助文档
        if comm[0] == '-h' or comm[0] == '--help':
            result['help'] = True
        elif comm[0] == '-i' or comm[0] == '--in':
            result['in'] = comm[1]
        elif comm[0] == '-o' or comm[0] == '--out':
            result['out'] = comm[1]
        elif comm[0] == '-d' or comm[0] == '--id':
            result['id'] = comm[1]
        elif comm[0] == '-e' or comm[0] == '--encoding':
            result['encoding'] = comm[1]
    return result


if __name__ == '__main__':
    # Python2显示升级提示
    if sys.version < '3':
        print("""
抱歉, 暂不支持Python2
    请升级Python版本后重试
        """)
        exit()
    # 读取参数
    params = None
    try:
        params = read_args()
    except getopt.GetoptError as e:
        # 出错了, 显示提示文档
        print_help()
        exit()
    # 是否显示帮助文档
    if not params or params.get('help') or not params.get('in'):
        print_help()
        exit()
    # 设置默认参数
    params['out'] = params['out'] if params.get('out') else str(params['in'])+'2.md'
    params['encoding'] = params['encoding'] if params.get('encoding') else 'utf-8'
    params['id'] = params['id'] if params.get('id') else False
    # 处理文件
    change_md_image(params['in'], params['out'], params['id'], params['encoding'])
    print('成功处理文件: ' + params['in'])
    print('处理后的文件为: ' + params['out'])
