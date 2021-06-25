#!/usr/bin/python3
# -*- coding: utf-8 -*-

import  tkinter as tk
from tkinter import filedialog
import pathlib2 as Path
import re
import codecs
import chardet
from langconv import *

# 采用图形界面获取文件夹路径
def get_file_path():
    app = tk.Tk() # 初始化GUI程序
    app.withdraw() # 仅显示对话框，隐藏主窗口
    print("请选择文件夹：\n")
    foldPath = filedialog.askdirectory(title="请选择文件夹")
    app.destroy()
    if foldPath:
        print(f'选择的文件夹为：{foldPath}')
        return Path.WindowsPath(foldPath)
    return ''


def simple2tradition(line):
    # 将简体转换成繁体
    line = Converter('zh-hant').convert(line.decode('utf-8'))
    line = line.encode('utf-8')
    return line

def tradition2simple(line):
    # 将繁体转换成简体
    line = Converter('zh-hans').convert(line)
    return line

# 将繁体字幕、其他格式的文本文件转换为简体、UTF-8格式保存的文件：
def file2simple(path):
    try:
        # codecs.open()这个方法打开的文件读取返回的将是unicode。
        content = codecs.open(str(path), 'rb').read()
        # chardet.detect 获取编码格式
        source_encoding = chardet.detect(content)['encoding']
        print(f'{str(path)} 文件编码为：{source_encoding}')
        if 'GB' in source_encoding.upper():
            source_encoding = 'gb18030'
        if source_encoding != None:  # 空的文件,返回None
            content = content.decode(source_encoding)
            file_data = tradition2simple(content)
            codecs.open(str(str(path)), 'w', encoding='utf-8').write(file_data)
    except IOError as err:
        print("I/O error:{0}".format(err))
    print('%s 文件已完成简体化处理。' % str(path))


# 先替换输入字典中的值，然后匹配固定的字符串模式后修改文件名称：
def rename_files(path, include_sub=True, **kw):
    exts = ('*.mp4', '*.wmv', '*.mkv', '*.avi', '*.ass', '*.ssa', '*.srt', 'vtt')
    exts_zimu = ('.ass', '.ssa', '.srt', '.vtt')
    if include_sub:
        dirs = [f for ext in exts for f in path.rglob(ext)]
        # dirs_zimu = [f for ext in exts_zimu for f in path.rglob(ext)]
    else:
        dirs = [f for ext in exts for f in path.glob(ext)]
        # dirs_zimu = [f for ext in exts_zimu for f in path.glob(ext)]

    i = 0
    m = re.compile(r'([a-zA-Z]{2,5})(00|-)?(\d{3,4})(-[c|C])?')
    zhong = re.compile(r'中.*字')

    for ff in dirs:
        old_name = ff.stem.strip()
        temp_name = old_name
        for k, w in kw.items():
            temp_name = re.sub(k, w, old_name, flags=re.IGNORECASE)
        result = m.search(temp_name)
        if not result:
            continue
        # 找到匹配的文件了：

        # # 字幕文件转换为简体，并保存为UTF-8格式保存：
        str1 = ff.suffix.lower()

        if str1 in exts_zimu:
            file2simple(ff)

        zh = ''
        ss = zhong.search(ff.parent.stem)
        if not result.group(3) or ss:
            zh = '-C'
        new_name = result.group(1).upper() + '-' + result.group(3) + zh + ff.suffix
        if new_name == ff.name:  # 新旧名称一样，不需要更改文件名称
            continue
        rr = path / 'Rename_Result.txt'
        if i == 0:
            with open(rr, 'w') as f:
                f.writelines('{:<8}{:<46}{}\n'.format("序号", "旧文件名", "新文件名"))

        try:
            ff.rename(ff.with_name(new_name))
        except Exception as e:
            print(f"{'*' * 50}")
            print(f"重命名文件'{ff.name}'时出现错误:\n{e}")
            continue



        i = i + 1
        with open(rr, 'a') as f:
            f.writelines('{:<10}{:<50}{}\n'.format(i, old_name, new_name))

        print(f"{i} {old_name}------> {new_name}")
    print(f"共有{i}个文件已重命名，感谢使用！")



def main():
    path = get_file_path()
    include_sub = input('请选择是否包含子文件夹？ Y or N(默认):')
    # sub = input('请输入需要替换为空的字符：')
    sub_dict = {'hhd800': ''}
    if include_sub.upper() == 'Y':
        rename_files(path, include_sub=True, **sub_dict)
    else:
        rename_files(path, include_sub=False, **sub_dict)

    return 0


if __name__ == '__main__':
    main()