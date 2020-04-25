"""
Created on 2019/5/18 19:12
将markdown文件中的图片转换成 base64编码
@author: hujing
"""
from src.ImageBase64 import ImageBase64
import re
import uuid
import os
from src.Args import arg


def dispose_image_to_base64(file_path, content):
    """
    将内容中的图片标签转换成base64编码后返回
    :param file_path: 文件路径
    :param content: 字符串内容
    :return:
    """
    # 正则匹配图片tag
    img_tag_pattern = re.compile(r'!\[[^\]]*\]\([^()]*\)')
    # 正则匹配图片标签中的图片url
    img_url_pattern = re.compile(r'\(([^)]*)')
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
        if not arg.use_id:
            # 将base64转到图片标签中
            content = content.replace(img_url_word, img_base64)
        # 将图片标签中存放id, id放到文件最后
        else:
            img_id = str(uuid.uuid1())
            img_id_map[img_id] = img_base64
            content = content.replace('(' + img_url_word + ')', '[' + img_id + ']')
    return content, img_id_map


def change_md_image():
    """
    将markdown文件中的图片路径修改为base64编码
    :rtype: object
    """
    # 保存图片id的map,在最后将id写出到文件
    img_id_map = dict()
    with open(arg.out_file, 'w+', encoding=arg.encoding) as out_file, \
            open(arg.in_file, 'r', encoding=arg.encoding) as in_file:
        # 读取输入文件
        for line in in_file.readlines():
            line, this_img_id_map = dispose_image_to_base64(arg.in_file, line)
            img_id_map.update(this_img_id_map)
            # 写入输出文件
            out_file.write(line)
        # 遍历完成, 将id写入文件最后
        for key, value in img_id_map.items():
            out_file.write(os.linesep + '[' + key + ']:' + value + os.linesep)


if __name__ == '__main__':
    # 检查版本号
    arg.check_version()
    # 判断是否输出帮助文档
    if arg.need_print_help():
        arg.print_help()
    # 处理文件
    change_md_image()
    print('成功处理文件: ' + arg.in_file)
    print('处理后的文件为: ' + arg.out_file)
