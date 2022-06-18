"""
命令行读取
@author hujing
"""
import getopt
import sys


class Args:
    """
    用于处理全局参数
    """

    def __init__(self):
        self.show_help = False
        self.in_file = None
        self.out_file = None
        self.use_id = False
        self.debug = False
        self.encoding = 'utf-8'
        tmp, args = getopt.getopt(sys.argv[1:], 'i:o:d:e:h', ['encoding=', 'out=', 'in=', 'id=', 'help', 'debug'])
        # 读取参数
        for comm in tmp:
            # 帮助文档
            if comm[0] == '-h' or comm[0] == '--help':
                self.show_help = True
            elif comm[0] == '-i' or comm[0] == '--in':
                self.in_file = comm[1]
            elif comm[0] == '-o' or comm[0] == '--out':
                self.out_file = comm[1]
            elif comm[0] == '-d' or comm[0] == '--id':
                self.use_id = comm[1]
            elif comm[0] == '-e' or comm[0] == '--encoding':
                self.encoding = comm[1]
            elif comm[0] == '--debug':
                self.debug = True
        # 设置默认参数
        self.out_file = self.out_file if self.out_file else str(self.in_file) + '2.md'

    def need_print_help(self) -> bool:
        """
        检查是否需要输出帮助文档
        :return:
        """
        if self.show_help:
            return True
        if not self.in_file or not self.out_file:
            return True
        return False

    @staticmethod
    def print_help() -> None:
        """
        输出帮助文档
        """
        print("""
参数如下: 
    -h/--help: 显示帮助文档
    -i/--in: md文件路径, 必填
    -o/--out: md输出文件路径, 默认 原文件名.md2.md
    -d/--id: 是否使用id表示, 默认不适用, 0(不使用),1(使用)
    -e/--encoding: 文件编码, 默认utf-8
    --debug: 是否启动调试模式. 默认不启用
            启动调试模式后, 会显示一些用于调试的错误信息. 如图片压缩失败后的错误信息等
        制作者: 靖哥哥
        """)
        exit()

    @staticmethod
    def check_version():
        """
        检查python版本号
        """
        # Python2显示升级提示
        if sys.version < '3':
            print("""
抱歉, 暂不支持Python2
    请升级Python版本后重试
                """)
            exit()


# 实例化, 保证单例
arg = Args()
