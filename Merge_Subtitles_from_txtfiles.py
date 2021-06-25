# -*- coding: utf-8 -*-
import json
import base64
import  tkinter as tk
from tkinter import filedialog
import pathlib2 as Path

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

def imgget(path):
    with open(path,"rb") as f:#转为二进制格式
        base64_data = base64.b64encode(f.read())#使用base64进行加密
    return base64_data.decode('utf-8')

class TencentOcr(object):
    """
    计费说明：1,000次/月免费
    https://cloud.tencent.com/document/product/866/17619
    """
    SECRET_ID = "AKIDGI3XlsKOmuSQEjD8ScZJxPfgSyEYIo31"
    SECRET_KEY = "e6JIwLVO1lERN21jBNKXWFincASWpsfq"
    # 地域列表
    # https://cloud.tencent.com/document/api/866/33518#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8
    Region = "ap-beijing"
    endpoint = "ocr.tencentcloudapi.com"
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

    def __init__(self):
        cred = credential.Credential(self.SECRET_ID, self.SECRET_KEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = self.endpoint
        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"
        clientProfile.httpProfile = httpProfile
        self.client = ocr_client.OcrClient(cred, self.Region, clientProfile)

    def get_urlimage_text(self, image_url, ocr="GeneralAccurateOCR"):
        req = self.mapping[ocr]()
        req.ImageUrl = image_url
        resp = getattr(self.client, ocr)(req)
        temp = json.loads(resp.to_json_string())
        with open("result.txt", "a", encoding='utf-8') as resfile:
            for item in temp['TextDetections']:
                resfile.write(item['DetectedText'])
                resfile.write('\n')
        print('URL中的图片文件已识别完成。')
        return 0

    def get_localimage_text(self, path, ocr="GeneralAccurateOCR"):
        req = self.mapping[ocr]()
        params = imgget(path)
        req.ImageBase64 = str(params)
        # req.from_json_string(params)
        resp = getattr(self.client, ocr)(req)
        temp = json.loads(resp.to_json_string())
        resultStr = ''
        for item in temp['TextDetections']:
            resultStr += (item['DetectedText']) + "\n"

        # with open("result.txt", "a", encoding='utf-8') as resfile:
        #     for item in temp['TextDetections']:
        #         resfile.write(item['DetectedText'])
        #         resfile.write('\n')
        # print('%s 图片文件已识别完成。' % path)
        return resultStr


def main():
    tencentOcr = TencentOcr()
    # url = "https://ocr-demo-1254418846.cos.ap-guangzhou.myqcloud.com/general/GeneralBasicOCR/GeneralBasicOCR3.jpg"
    # print(tencentOcr.get_image_text(url, ocr="GeneralHandwritingOCR"))

    # print(tencentOcr.get_localimage_text(r'e:\test.png'))
    app = tk.Tk() # 初始化GUI程序
    app.withdraw() # 仅显示对话框，隐藏主窗口
    print("请选择存放图片的文件夹：\n")
    foldPath = filedialog.askdirectory(title="请选择存放图片的文件夹：")
    path = Path.WindowsPath(foldPath)
    listtxt = [e for e in path.glob('*.txt')]
    res = str(Path.WindowsPath(listtxt[0]).with_name('result-all.srt'))
    i = 0
    with open(res, 'w', encoding='utf-8') as f:
        for ff in sorted(listtxt):
            fp = Path.WindowsPath(ff)
            i = i + 1
            with fp.open('r', encoding='utf-8') as ffp:
                lname = fp.stem.split('_')
                if len(lname) != 9:
                    continue

                f.writelines("%d\n" % i)
                f.writelines(f'{lname[0]}:{lname[1]}:{lname[2]},{lname[3]} --> {lname[5]}:{lname[6]}:{lname[7]},{lname[8]}\n')
                f.writelines(ffp.readlines())
            print('第%d个文件"%s"已完成合并处理\n' % (i, fp))
    print('恭喜！图片OCR已完成，识别合并后的结果已存为：\n %s' % res)
    return 0


if __name__ == '__main__':
    main()