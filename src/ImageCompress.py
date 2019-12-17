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
    def compress_tiny_png(cls, file_path):
        """
        使用tinypng对图片进行压缩
        :param file_path 待压缩的文件路径
        :rtype: 压缩后的文件内容
        """
        try:
            import tinify
            tinify.key = '123432'
            with open(file_path, 'rb') as f:
                buffer = f.read()
                result = tinify.from_buffer(buffer).to_buffer()
                print('成功压缩图片: ' + file_path)
                return result
        except Exception as e:
            return False
