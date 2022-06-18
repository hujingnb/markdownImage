"""
markdown文件处理
@author hujing
"""
import os
import re
import uuid

from .Args import arg
from .ImageBase64 import ImageBase64


class MarkdownFile:

    @staticmethod
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
                line, this_img_id_map = MarkdownFile.dispose_image_to_base64(arg.in_file, line)
                img_id_map.update(this_img_id_map)
                # 写入输出文件
                out_file.write(line)
            # 遍历完成, 将id写入文件最后
            for key, value in img_id_map.items():
                out_file.write(os.linesep + '[' + key + ']:' + value + os.linesep)

    @staticmethod
    def dispose_image_to_base64(file_path, content):
        """
        将内容中的图片标签转换成base64编码后返回
        若不需要使用ID, 则将base64内容直接放到图片中
        :param file_path: 文件路径
        :param content: 字符串内容
        :return:
        """
        # 正则匹配图片tag
        img_tag_pattern = re.compile(r'!\[[^\]]*\]\([^()]*\)')
        # 正则匹配图片标签中的图片url
        img_url_pattern = re.compile(r'\(([^)]*)')
        # 正则匹配 img 标签
        img_size_tag_pattern = re.compile(r'<img.*/>')
        # 正则图片 img 标签的图片 url
        img_size_url_pattern = re.compile(r'src="([^"]*)"')
        # 匹配原始图片标签
        img_id_map = dict()
        content, tmp_id_map = MarkdownFile.change_img_to_base_64(img_tag_pattern, img_url_pattern,
                                                                 content, file_path, arg.use_id)
        img_id_map.update(tmp_id_map)
        # img 标签暂时不支持使用图片 ID 的形式. 因此, 即使参数指定使用 ID, 也不使用, 否则无法识别
        content, _ = MarkdownFile.change_img_to_base_64(img_size_tag_pattern, img_size_url_pattern, content, file_path)
        return content, img_id_map

    @staticmethod
    def change_img_to_base_64(img_tag_pattern, img_url_pattern, content, file_path, use_id=False):
        """
        对内容进行匹配, 将匹配到的图片转换成 base 64
        :param file_path: md 文件路径, 用于拼接相对路径图片
        :param img_tag_pattern: 图片标签匹配正则
        :param img_url_pattern: 将图片标签中的图片地址拿出来
        :param content: 文本内容
        :param use_id: 是否使用 ID
        :return:
        """
        img_id_map = dict()
        img_search = img_tag_pattern.findall(content)
        if not img_search:
            return content, img_id_map
        # 遍历处理每一个图片内容
        for each in img_search:
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
            # 若文件不存在, 跳过
            if not os.path.exists(img_url):
                continue
            # 获取图片的base64
            img_base64 = ImageBase64.base64_img(img_url)
            # 将图片base64直接放到标签中
            if not use_id:
                # 将base64转到图片标签中
                content = content.replace(img_url_word, img_base64)
            # 将图片标签中存放id, id放到文件最后
            else:
                img_id = str(uuid.uuid1())
                img_id_map[img_id] = img_base64
                content = content.replace('(' + img_url_word + ')', '[' + img_id + ']')
        return content, img_id_map
