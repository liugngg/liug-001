from aip import AipOcr
import re
import os

APP_ID ='19311570'
API_KEY ='IhPjfLP15e8y4CwK8nonGI9y'
SECRET_KEY ='YusaYUkvqYC8oyBXVAB7IaABiUm18ueX'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
path = os.getcwd()
listimg = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".png")]

for file in listimg:
    i = open(file, 'rb').read()
    result = client.basicAccurate(i)
    with open("result.txt", "a", encoding='utf-8') as resfile:
        for item in result['words_result']:
            resfile.write(item['words'])
            resfile.write('\n')
    print(file)
