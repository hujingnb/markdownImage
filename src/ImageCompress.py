"""
Created on 2019/5/18 19:06
对图片进行压缩处理
@author: hujing
"""
import requests

from .Config import Config, ConfigName


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
            key = Config.get_compress_config(ConfigName.COMPRESS_TINIFY_KEY)
            if not key:
                return False
            tinify.key = key
            with open(file_path, 'rb') as f:
                buffer = f.read()
                result = tinify.from_buffer(buffer).to_buffer()
                return result
        except Exception as e:
            return False

    @classmethod
    def compress_krakenio(cls, file_path):
        """
        通过 krakenio 对图片进行压缩
        :param file_path:
        :return:
        """
        try:
            from krakenio import Client
            key = Config.get_compress_config(ConfigName.COMPRESS_KRAKEN_KEY)
            secret = Config.get_compress_config(ConfigName.COMPRESS_KRAKEN_SECRET)
            if not key or not secret:
                return False
            api = Client(key, secret)
            data = {
                'wait': True
            }
            result = api.upload(file_path, data)
            if result.get('success'):
                url = result.get('kraked_url')
                response = requests.get(url)
                if response.status_code == 200:
                    return response.content
            else:
                return False
        except Exception as e:
            return False