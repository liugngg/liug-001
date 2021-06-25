#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import  tkinter as tk
from tkinter import filedialog
import pathlib2 as Path
import chardet
import codecs
from langconv import *

def tradition2simple(line):
    # 将繁体转换成简体
    line = Converter('zh-hans').convert(line)
    return line

# 采用图形界面获取文件夹路径
def get_file_path():
    app = tk.Tk() # 初始化GUI程序
    app.withdraw() # 仅显示对话框，隐藏主窗口
    print("请选择文件夹：\n")
    foldPath = filedialog.askopenfilename(title="请选择文件夹")
    app.destroy()
    if foldPath:
        print(f'选择的文件为：{foldPath}')
        return Path.WindowsPath(foldPath)
    return ''


# 将繁体字幕、其他格式的文本文件转换为简体、UTF-8格式保存的文件：
def file2simple(path):
    # content = codecs.open(str(path), 'rb').read()
    # str_temp = content.decode(chardet.detect(content)['encoding'])
    # # print(str_temp)
    # print(tradition2simple(str_temp))

    try:
        # codecs.open()这个方法打开的文件读取返回的将是unicode。
        content = codecs.open(str(path), 'rb').read()
        # chardet.detect 获取编码格式
        source_encoding = chardet.detect(content)['encoding']
        print(f'该文件的编码为：{source_encoding}')
        if 'GB' in source_encoding.upper():
            source_encoding = 'gb18030'
        if source_encoding != None:  # 空的文件,返回None
            content = content.decode(source_encoding)
            file_data = tradition2simple(content)
            codecs.open(str(str(path)), 'w', encoding='utf-8').write(file_data)
    except IOError as err:
        print("I/O error:{0}".format(err))
    print('%s 文件已完成简体化处理。' % str(path))

path = get_file_path()

file2simple(path)


# content = codecs.open(str(path), 'rb').read()
# str_temp = content.decode(chardet.detect(content)['encoding'])
# print(str_temp)
# print(tradition2simple(str_temp))
#                 # chardet.detect 获取编码格式
#                 source_encoding = chardet.detect(content)['encoding']
#                 if source_encoding != None:  # 空的文件,返回None
#                     content = content.decode(source_encoding).encode('utf-8')
# with  path.open('rb') as f:
#     ff=f.readline()
#     # 这里试着换成read(5)也可以，但是换成readlines()后报错
#     enc = chardet.detect(ff)
#     print(enc['encoding'])

# path_new = path / '0_05_56_856__0_05_57_889.mp4'
# print(path_new.stem)
# print(path.as_uri())
# print(path.is_absolute())
# print(path.home())
# print(path.suffix)
# exts = ('*.mp4', '*.txt')
# dirs = [f for ext in exts for f in path.glob(ext)]

# res = str(dirs[0].with_name('result-all.txt'))
# patten = re.compile(r'^\d.*')
# i = 0
# with open(res, 'w', encoding='utf-8') as f:
#     for fp in sorted(dirs):
#         with fp.open('r', encoding='utf-8') as ffp:
#             for eachline in ffp.readlines():
#                 i = i + 1
#                 str_01 = eachline
#                 if re.match(patten, eachline):
#                     # re.sub('dhdh', ',', eachline)
#                     # re.sub('fengefu', ' --> ',eachline)
#                     str_01 = eachline.replace('dhdh', ',')
#                     str_02 = str_01.replace('fengefu', ' --> ')
#                     str_01 = f'\n{i}\n{str_02}'
#                 f.writelines(str_01)
#         print('%s 文件已处理' % fp)
# print(dirs)
