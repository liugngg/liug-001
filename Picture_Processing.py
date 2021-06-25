#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import  tkinter as tk
from tkinter import filedialog
import pathlib2 as Path

if __name__ == '__main__':
    # 打开图片
    app = tk.Tk()  # 初始化GUI程序
    app.withdraw()  # 仅显示对话框，隐藏主窗口
    print("请选择存放图片的文件夹：\n")
    foldPath = filedialog.askdirectory(title="请选择存放图片的文件夹：")
    path = Path.WindowsPath(foldPath)
    filesufix = input('请输入需要识别的图片类型（如BMP、JPG等）：')
    # isHebing = input("扫描完成后，是否需要合并到一个文本文件？如需要，请输入'Y': ")
    # listimg = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".bmp")]
    listimg = [e for e in path.glob('*.' + filesufix)]
    if len(listimg) == 0:
        print('你选择的文件夹里没有后缀为"%s"的文件！' % filesufix)
        exit(1)
    # i = 0
    # (w_sum, h_sum) = (0, 0)
    # res = str(listimg[0].with_name('result-all.jpg'))

    # 裁剪图片，并将文件名转换为时间戳增加到图片前面
    for ff in listimg:
        lname = ff.stem.split('_')
        if len(lname) != 9:
            listimg.remove(ff)
            continue
        time_txt = f'{lname[0]}:{lname[1]}:{lname[2]}dhdh{lname[3]}fengefu{lname[5]}:{lname[6]}:{lname[7]}dhdh{lname[8]}'
        #左右各裁剪掉80像素，取下面145像素高：
        im = Image.open(str(ff))
        width, height = im.size
        imm = im.crop((80, height - 145, width - 80, height))
        # 在图片上面打上时戳
        dr_im = ImageDraw.Draw(imm)
        font_size = 30
        font = ImageFont.truetype("arial.ttf", font_size)
        dr_im.text((0, 0), time_txt, font=font, fill=(255, 0, 0))
        imm.save(str(ff))

    print(f"共裁剪了{len(listimg)}个图片文件")

    # 合并图片
    ims = []
    for image_file in sorted(listimg):
        ims.append(Image.open(str(image_file)))
    # 单幅图像尺寸
    width, height = ims[0].size

    # 创建空白长图
    result = Image.new(ims[0].mode, (width, height * len(ims)))

    # 拼接图片
    for i, im in enumerate(ims):
        result.paste(im, box=(0, i * height))

    # 保存图片
    res = str(listimg[0].with_name('result.jpg'))
    result.save(res)
    print(f"共合并了{len(listimg)}个图片文件")
