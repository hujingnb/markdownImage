"""
配置文件读取
@author hujing
"""
import configparser
import os


class ConfigName:
    IMAGE_COMPRESS = 'image_compress'
    COMPRESS_TINIFY_KEY = 'tinify_key'
    COMPRESS_KRAKEN_KEY = 'kraken_key'
    COMPRESS_KRAKEN_SECRET = 'kraken_secret'


class Config:
    @classmethod
    def get_compress_config(cls, config_name):
        """
        获取图片压缩相关配置
        :param cls:
        :param config_name: 配置名称
        :return:
        """
        return cls._get_config_instance().get(ConfigName.IMAGE_COMPRESS, config_name)

    _config = None

    @classmethod
    def _get_config_instance(cls):
        """
        获取配置文件实例
        :return:
        """
        if not cls._config:
            cls._config = configparser.ConfigParser()
            cls._config.read(os.path.dirname(__file__) + os.path.sep + '..' +
                             os.path.sep + 'config' + os.path.sep + 'config.cfg')
        return cls._config


if __name__ == '__main__':
    key = Config.get_compress_config(ConfigName.COMPRESS_TINIFY_KEY)
    print(key)
