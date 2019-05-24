#!/usr/bin/python
#-*- coding: UTF-8 -*-
"""
Created on 2019/5/18 19:06
对图片进行压缩处理
@author: hujing
"""


class ImageCompress:
    """
    对图片进行压缩的类
    其中所有以 compress 开头的类方法, 都是进行压缩的方法
        可自行扩充, 参数为文件路径
        返回压缩后的文件内容
        若失败,返回False
    """
    @classmethod
    def compressTinypng(cls, filePath):
        """
        使用tinypng对图片进行压缩
        :param filePath 待压缩的文件路径
        :rtype: 压缩后的文件内容
        """
        try:
            import tinify
            tinify.key = 'J2N7fcrkRwEdPe2LEjfOS6dINwTOeLJj'
            with open(filePath, 'rb') as f:
                buffer = f.read()
                result = tinify.from_buffer(buffer).to_buffer()
                print('成功压缩图片: ' + filePath)
                return result
        except Exception as e:
            return False
