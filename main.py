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


def changeMDImage(inFilePath, outFilePath, isUseId=False):
    """
    将markdown文件中的图片路径修改为base64编码
    :param inFilePath 输入markdown文件路径
    :param outFilePath 输出markdown文件路径
    :param isUseId 是否在markdown文件中使用id, 存放到文件最后
    :rtype: object
    """
    # 正则匹配图片tag
    imgTagPattern = re.compile(r'!\[[\w\d]*\]\([^\(\)]*\)')
    # 正则匹配图片标签中的图片url
    imgUrlPattern = re.compile(r'\(([^\) ]*)')
    # 保存图片id的map,在最后将id写出到文件
    imgIdMap = dict()
    with open(outFilePath, 'w+') as outFile, open(inFilePath) as inFile:
        # 读取输入文件
        for line in inFile.readlines():
            search = imgTagPattern.findall(line)
            # 不存在图片标签
            if not search:
                outFile.write(line)
                continue
            # 遍历处理每一个图片内容
            for each in search:
                # 拿到图片url
                url = imgUrlPattern.search(each)
                # 若没有匹配到, 跳过
                if not url:
                    continue
                url = url.group(1)
                # 若路径是相对路径,将路径与md文件目录拼接
                if not os.path.isabs(url):
                    url = os.path.join(os.path.dirname(inFilePath), url)
                # 获取图片的base64
                imgBase64 = ImageBase64.base64Img(url)
                # 将图片base64直接放到标签中
                if not isUseId:
                    # 将base64转到图片标签中
                    line = line.replace(url, imgBase64)
                # 将图片标签中存放id, id放到文件最后
                else:
                    imgId = str(uuid.uuid1())
                    imgIdMap[imgId] = imgBase64
                    line = line.replace('(' + url + ')', '[' + imgId + ']')
            # 写入输出文件
            outFile.write(line)
        # 遍历完成, 将id写入文件最后
        for key, value in imgIdMap.items():
            outFile.write('\n\n' + '[' + key + ']:' + value)


def printHelp():
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
        制作者: 靖哥哥
    """)


def readArgs():
    """
    读取命令行参数
    :return 参数map
    """
    # 读取参数
    result = dict()
    tmp, args = getopt.getopt(sys.argv[1:], 'i:o:d:h', ['out=', 'in=', 'id=', 'help'])
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
    return result


if __name__ == '__main__':
    # 读取参数
    params = None
    try:
        params = readArgs()
    except getopt.GetoptError as e:
        # 出错了, 显示提示文档
        printHelp()
        exit()
    # 是否显示帮助文档
    if not params or params.get('help') or not params.get('in'):
        printHelp()
        exit()
    # 处理文件
    outFilePath = params['out'] if params.get('out') else str(params['in'])+'2.md'
    changeMDImage(params['in'], outFilePath,
                  params['id'] if params.get('id') else False)
    print('成功处理文件: ' + params['in'])
    print('处理后的文件为: ' + outFilePath)

