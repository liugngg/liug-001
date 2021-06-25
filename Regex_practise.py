import re
import os

m = re.compile(r'([a-zA-Z]{2,5})(00|-)(\d{3,4})')
line = '102e3434snis-08dd'
sch = m.search(line)
print(sch)
os.system(r'notepad H:\soe-422.txt')
if sch:
    str = sch.group(1) + '-' + sch.group(3)
    print(str)
else:
    print('No found!')


