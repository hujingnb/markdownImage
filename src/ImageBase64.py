"""
Created on 2019/5/18 19:07
时间处理的工具
@author: hujing
"""
from operator import methodcaller
from .ImageCompress import ImageCompress
import os
import base64


class ImageBase64:
    """
    对图片进行编码操作的类
    """

    @classmethod
    def compress_img(cls, img_file_path):
        """
        对图片进行压缩
        :param img_file_path 图片文件路径
        :rtype: str
        """
        # 获取类的所有压缩方法
        fun_list = list(
            filter(
                lambda m: m.startswith('compress') and callable(getattr(ImageCompress, m)),
                dir(ImageCompress)
            )
        )
        # 根据方法依次对图片进行压缩, 直到压缩成功
        for fun in fun_list:
            r = methodcaller(fun, img_file_path)(ImageCompress)
            if r:
                return r
        return ''

    @classmethod
    def get_img_base64_prefix(cls, img_type):
        """
        获取图片的base64前缀
        :param 图片类型
        :rtype: str
        """
        img_type_map = {
            'jpg': 'data:image/jpeg;base64,',
            'jpeg': 'data:image/jpeg;base64,',
            'png': 'data:image/png;base64,',
        }
        return img_type_map[img_type]

    @classmethod
    def base64_img(cls, img_path):
        """
        拿到图片的base64编码结果
        :param img_path 图片路径
        :rtype: str
        """
        # 对图片进行压缩
        compress_img_content = cls.compress_img(img_path)
        # 压缩失败,读取文件内容
        if not compress_img_content:
            with open(img_path, 'rb') as f:
                compress_img_content = f.read()
        # 对图片内容编码
        return cls.get_img_base64_prefix(os.path.splitext(img_path)[1][1:]) + \
               str(base64.b64encode(compress_img_content), 'utf-8')
