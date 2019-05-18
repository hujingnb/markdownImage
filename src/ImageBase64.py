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
    def compressImg(cls, imgFilePath):
        """
        对图片进行压缩
        :param imgFilePath 图片文件路径
        :rtype: str
        """
        # 获取类的所有压缩方法
        funs = list(
            filter(
                lambda m: m.startswith('compress') and callable(getattr(ImageCompress, m)),
                dir(ImageCompress)
            )
        )
        # 根据方法依次对图片进行压缩, 直到压缩成功
        for fun in funs:
            r = methodcaller(fun, imgFilePath)(ImageCompress)
            if r:
                return r
        return ''

    @classmethod
    def getImgBase64Prefix(cls, imgType):
        """
        获取图片的base64前缀
        :param 图片类型
        :rtype: str
        """
        imgTypeMap = {
            'jpg': 'data:image/jpeg;base64,',
            'jpeg': 'data:image/jpeg;base64,',
            'png': 'data:image/png;base64,',
        }
        return imgTypeMap[imgType]

    @classmethod
    def base64Img(cls, imgPath):
        """
        拿到图片的base64编码结果
        :param imgPath 图片路径
        :rtype: str
        """
        # 对图片进行压缩
        compressImgContent = cls.compressImg(imgPath)
        # 压缩失败,读取文件内容
        if not compressImgContent:
            with open(imgPath, 'rb') as f:
                compressImgContent = f.read()
        # 对图片内容编码
        return cls.getImgBase64Prefix(os.path.splitext(imgPath)[1][1:]) + \
            str(base64.b64encode(compressImgContent), 'utf-8')
