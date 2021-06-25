#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
import re
import base64
import  tkinter as tk
from tkinter import filedialog
import pathlib2 as Path
# 百度高精度文字识别：
from aip import AipOcr
from PIL import Image, ImageDraw, ImageFont
from langconv import *

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client
from tencentcloud.ocr.v20181119.models import (
    GeneralAccurateOCRRequest,
    EnglishOCRRequest,
    GeneralBasicOCRRequest,
    GeneralEfficientOCRRequest,
    GeneralFastOCRRequest,
    GeneralHandwritingOCRRequest
)


def simple2tradition(line):
    # 将简体转换成繁体
    line = Converter('zh-hant').convert(line.decode('utf-8'))
    line = line.encode('utf-8')
    return line

def tradition2simple(line):
    # 将繁体转换成简体
    line = Converter('zh-hans').convert(line)
    return line

class BaiduOrc(object):
    def __init__(self, user_id=1):
        self.APP_ID ='19311570'
        self.API_KEY ='IhPjfLP15e8y4CwK8nonGI9y'
        self.SECRET_KEY ='YusaYUkvqYC8oyBXVAB7IaABiUm18ueX'
        if user_id != 1:
           # 手机的账号：
           self.APP_ID = '19855676'
           self.API_KEY = 'A0QoTEAP6NNPUKsqPar1xPr2'
           self.SECRET_KEY = 'BB0EdiB2avCtV0484l8HP36EeuRqswdF'
        self.client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    # path 为需要识别的图片路径和文件名称，类型为Path。保存的结果存为同路径、同名的TXT文件
    def get_localimage_text(self, path):
        with open(path, "rb") as img_file:
            result = self.client.basicAccurate(img_file.read())

        resultTxt = Path.WindowsPath(path).with_suffix('.txt')
        with open(resultTxt, "a", encoding='utf-8') as resfile:
            for item in result['words_result']:
                resfile.write(item['words'])
                resfile.write('\n')
        print('%s 图片文件已识别完成。' % path)
        return resultTxt

class TencentOcr(object):
    """
    计费说明：1,000次/月免费
    https://cloud.tencent.com/document/product/866/17619
    """
    # 刘刚的账号：
    SECRET_ID = "AKIDGI3XlsKOmuSQEjD8ScZJxPfgSyEYIo31"
    SECRET_KEY = "e6JIwLVO1lERN21jBNKXWFincASWpsfq"
    client = ''
    # 通用文字识别相关接口
    # https://cloud.tencent.com/document/api/866/37173
    mapping = {
        # 通用印刷体识别（高精度版） ok
        "GeneralAccurateOCR": GeneralAccurateOCRRequest,
        # 英文识别 ok
        "EnglishOCR": EnglishOCRRequest,
        # 通用印刷体识别 一般
        "GeneralBasicOCR": GeneralBasicOCRRequest,
        # 通用印刷体识别（精简版）（免费公测版）no
        "GeneralEfficientOCR": GeneralEfficientOCRRequest,
        # 通用印刷体识别（高速版）一般
        "GeneralFastOCR": GeneralFastOCRRequest,
        # 通用手写体识别 ok
        "GeneralHandwritingOCR": GeneralHandwritingOCRRequest,
    }

    def __init__(self, user_id=1):
        # 地域列表
        # https://cloud.tencent.com/document/api/866/33518#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8
        Region = "ap-beijing"
        endpoint = "ocr.tencentcloudapi.com"
        if user_id != 1:
           # 小牛牛的账号：
            SECRET_ID = "AKIDcWCepgkBxRghSxHQebOSKyMX6i6GpgQu"
            SECRET_KEY = "OWQ3QXihSyDCqVv469vXtymM7LJCnOhk"

        cred = credential.Credential(self.SECRET_ID, self.SECRET_KEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = endpoint
        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"
        clientProfile.httpProfile = httpProfile
        self.client = ocr_client.OcrClient(cred, Region, clientProfile)

    # 将本地图片文件编码为Base64，Tencent OCR 接口要求该格式，另外一种是URL链接：
    def imgget(self, path):
        with open(path, "rb") as f:  # 转为二进制格式
            base64_data = base64.b64encode(f.read())  # 使用base64进行加密
        return base64_data.decode('utf-8')

    # 调用方式：image_url为需要OCR图片的URL地址，result_file为识别后保存结果的文件名称：
    def get_urlimage_text(self, image_url, result_file, ocr="GeneralAccurateOCR"):
        req = self.mapping[ocr]
        req.ImageUrl = image_url
        resp = getattr(self.client, ocr)(req)
        temp = json.loads(resp.to_json_string())
        with open(result_file, "a", encoding='utf-8') as resfile:
            for item in temp['TextDetections']:
                resfile.write(item['DetectedText'])
                resfile.write('\n')
        print('URL中的图片文件已识别完成。')
        return 0

    # path 为需要识别的图片路径和文件名称，类型为Path。保存的结果存为同路径、同名的TXT文件
    def get_localimage_text(self, path, ocr="GeneralAccurateOCR"):
        req = self.mapping[ocr]()
        params = self.imgget(str(path))
        req.ImageBase64 = str(params)
        resp = getattr(self.client, ocr)(req)
        temp = json.loads(resp.to_json_string())
        resultTxt = Path.WindowsPath(path).with_suffix('.txt')
        with open(resultTxt, "a", encoding='utf-8') as resfile:
            for item in temp['TextDetections']:
                resfile.write(item['DetectedText'])
                resfile.write('\n')
        print('%s 图片文件已识别完成。' % path)
        return resultTxt

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


# 合并result所在文件夹下的所有TXT后缀的文档，合并后的文件存为result.txt
def merge_txt_file(result):
    res = result.joinpath('result.txt')
    listtxt = [e for e in res.parent.glob('*.txt')]
    if len(listtxt) < 2:
        print('该文件夹下TXT文件数小于2，无需合并!！')
        return -1
    i = 0
    with open(res, 'a', encoding='utf-8') as f:
        for ff in sorted(listtxt):
            i = i + 1
            with ff.open('r', encoding='utf-8') as ffp:
                f.writelines(ffp.readlines())
                # f.writelines('\n')
            print('第%d个文件"%s"已完成合并处理' % (i, ff))
    print('恭喜！合并完成，识别合并后的结果已存为：\n %s' % res)
    os.system('notepad' + ' ' + res)
    return 0


# 裁剪图片，并将文件名转换为时间戳增加到图片前面
# 如果tryon等于1，则试着裁减前10张图片
def crop_images(path, filesufix, w=0, h=145, tryon=0, fontsize=40):
    listimg = [e for e in path.glob('*.' + filesufix)]
    if len(listimg) == 0:
        print('你选择的文件夹里没有后缀为"%s"的文件！' % filesufix)
        return -1
    if tryon == 1:
        if len(listimg) > 10:
            listimg = listimg[0:10]

    # 新建子目录‘\results’存放裁减后的图片
    path_new = path / 'results'
    path_new.mkdir(exist_ok=True)

    # 需要合并的图片文件格式例子：0_02_06_292__0_02_08_669.jpeg
    for ff in listimg:
        lname = ff.stem.split('_')
        if len(lname) != 9:
            listimg.remove(ff)
            continue
        time_txt = '   ' + f'{lname[0]}H{lname[1]}H{lname[2]}H{lname[3]}H{lname[5]}H{lname[6]}H{lname[7]}H{lname[8]}'
        time_txt = time_txt.replace('0', 'K')

        # 左右各裁剪掉w像素，取下面h像素高：
        im = Image.open(str(ff))
        width, height = im.size
        imm = im.crop((w, height - h, width - w, height))
        # 在图片上面打上时戳
        dr_im = ImageDraw.Draw(imm)
        fz = fontsize
        font = ImageFont.truetype("arial.ttf", fz)
        dr_im.text((0, 0), time_txt, font=font, fill=(0, 0, 0))
        ref = path_new / f'{ff.stem}.jpg'
        imm.save(str(ref))

    print(f"共裁剪了{len(listimg)}个图片文件")
    return path_new

 # 合并图片
def merge_images(path, filesufix='jpg', n=20):
    listimg = sorted([e for e in path.glob('*.' + filesufix)])
    llen = len(listimg)
    alist = []
    if llen == 0:
        print('你选择的文件夹里没有后缀为"%s"的文件！' % filesufix)
        exit(-1)
    elif llen <= n:
        alist.append(listimg)
    else:
        alist = [listimg[i:i+n] for i in range(0, llen, n)]

    ii = 0
    for each_list in alist:
        ii += 1
        ims = []
        for image_file in each_list:
            ims.append(Image.open(str(image_file)))
            # 单幅图像尺寸
            width, height = ims[0].size

            # 创建空白长图
            result = Image.new(ims[0].mode, (width, height * len(ims)))

            # 拼接图片
            for i, im in enumerate(ims):
                result.paste(im, box=(0, i * height))

            # 保存图片
            rname = "result" + str(ii).rjust(3, '0') + '.jpg'
            res = str(listimg[0].with_name(rname))
            result.save(res)
        print(f"第{ii}次合并完成。")
    print(f"已成功合并了{llen}张图片，分别保存为{ii}个文件。")


def merge_subtitle_txt(path):
    listtxt = sorted([e for e in path.glob('*.txt')])
    if len(listtxt) < 1:
        print("所选文件内未发现TXT文件。")
        return -1
    res = str(Path.WindowsPath(listtxt[0]).with_name('result-all.srt'))
    i = 0
    patten = re.compile(r'^[K\dH].*?H')
    with open(res, 'w', encoding='utf-8') as f:
        for ff in sorted(listtxt):
            with ff.open('r', encoding='utf-8') as ffp:
                str_time = ''
                str_content = ''
                for eachline in ffp.readlines():
                    eachline = (str(eachline).upper()).strip()
                    if re.match(patten, eachline):
                        if i > 0:
                            if len(str_content) > 0:
                                str_01 = f'{i}\n{str_time}\n{str_content}\n\n'
                                f.writelines(tradition2simple(str_01))
                                # str_time = ''
                                str_content = ''
                        eachlien = eachline.upper()
                        lname = (eachline.replace('K', '0')).split("H")
                        i += 1
                        if len(lname) == 8:
                            str_time = f'{lname[0]}:{lname[1]}:{lname[2]},{lname[3]} --> {lname[4]}:{lname[5]}:{lname[6]},{lname[7]}'
                        else:
                            str_time = "error!\n" + str_time + '\n' + ('H'.join(lname)).replace('K', '0')
                    else:
                        if len(eachline):
                            if len(str_content):
                                str_content = str_content + '\n' + eachline
                            else:
                                str_content = eachline
                # 最后一句需要添加：
                if len(str_content) > 0:
                    str_01 = f'{i}\n{str_time}\n{str_content}\n\n'
                    f.writelines(tradition2simple(str_01))
            print('%s 文件已处理' % str(ff))
    print('恭喜！TXT文件合并已完成，识别合并后的结果已存为：\n %s' % res)
    os.system('notepad' + ' ' + res)
    return 0

# 处理用户输入
def userinput():
    while(True):
        print("*"*50)
        print("请选择任务类型：")
        func = input('1：试裁10张图片(默认)\n2：裁剪所有图片\n3：跳过裁减直接OCR\n4：一键完成OCR\n5：修改默认参数\nX：退出本程序\n您的选择：')
        if func in ['', '1', '2', '3', '4', '5', 'x', 'X']:
            return func
        print("*"*50)
        print('您的选择有误！！！请重新选择')




global file_sufix
global img_width
global img_height
global font_size
global merg_img_count

def main():
    global file_sufix
    global img_width
    global img_height
    global font_size
    global merg_img_count
    file_sufix = 'jpeg'
    img_width = 0
    img_height = 145
    font_size = 40
    merg_img_count = 10
    while True:
        func = userinput()
        if func.upper() == 'X':
            return 0

        if func == '5':
            print(f"当前需要识别的图片类型为：{file_sufix}")
            sufix_temp = input('请输入需要识别的图片类型（默认为jpeg）：')
            if len(sufix_temp) > 2:
                file_sufix = sufix_temp

            print(f"\n当前图片需要裁减的宽度和高度分别为：{img_width}，{img_height}")
            wtemp = input('请输入图片需要裁减的宽度(默认0)：')
            if wtemp.isdigit():
                img_width = int(wtemp)
            htemp = input('请输入图片需要保留的高度(默认145)：')
            if htemp.isdigit():
                img_height = int(htemp)

            print(f"\n当前时戳字体大小为：{font_size}")
            fz_temp = input('请输入时戳字体大小（默认为40）：')
            if fz_temp.isdigit():
                font_size = int(fz_temp)

            print(f"\n当前单次识别图片的数量为：{merg_img_count}")
            mc_temp = input('请输入单次识别图片的数量（默认为10）：')
            if mc_temp.isdigit():
                merg_img_count = int(mc_temp)
            continue

        path = get_file_path()
        if path == '':
            print('选择的文件夹有误！')
            break

        # 试裁图片
        if func in ['', '1']:
            # 裁减目录下的10张图片，并将时间戳信息加入到图片中
            print(f'当前设定的图片裁剪参数为：\n宽度：{img_width}   高度：{img_height}    字体大小：{font_size}')
            print('开始对图片进行裁剪，请耐心等待....\n')
            path = crop_images(path, file_sufix, img_width, img_height, tryon=1, fontsize=font_size)
            if path != -1:
                print('已对前10张图片裁剪并添加了时戳！')
            continue
        elif func in ['2', '4']:
            # 裁减目录下的所有图片，并将时间戳信息加入到图片中
            print(f'当前设定的图片裁剪参数为：\n宽度：{img_width}   高度：{img_height}    字体大小：{font_size}\n')
            print('开始对图片进行裁剪，请耐心等待....\n')
            path = crop_images(path, file_sufix, img_width, img_height, fontsize=font_size)
            if path != -1:
                print('已完成所有图片裁剪并添加了时戳！')
            if func == '2':
                continue
        else:
            # 跳过裁剪步骤：
            path = path / 'results'
            print('\n已跳过图片裁剪过程\n')
        print('开始对图片OCR识别....\n')
        ocr_client = input('请输入OCR方式：\n1 百度账号1（默认）\n2 百度账号2\n3 腾讯(本人）\n4 腾讯(小牛牛)\n您的选择：')
        if ocr_client not in ['1', '2', '3', '4']:
            ocr_client = '1'

        if ocr_client == '1':
            ocr_method = BaiduOrc(1)
        elif ocr_client == '2':
            ocr_method = BaiduOrc(2)
        elif ocr_client == '3':
            ocr_method = TencentOcr(1)
        else:
            ocr_method = TencentOcr(2)

        # # 以num为单位合并图片
        merge_images(path, filesufix='jpg', n=merg_img_count)

        # # 开始识别合并后的图片
        listimg = [e for e in path.glob('result*.jpg')]
        for file in listimg:
            ocr_method.get_localimage_text(file)

        # 合并识别结果TXT文档为字幕
        merge_subtitle_txt(path)
        break


if __name__ == '__main__':
    main()
