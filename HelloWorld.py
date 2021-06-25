import  tkinter as tk
from tkinter import filedialog
'''打开文件夹/文件选择窗口 选择路径'''
root = tk.Tk()
root.withdraw()

foldPath = filedialog.askdirectory()
filePath = filedialog.askopenfile()

print('你选择的文件夹为：' + foldPath)
print('你选择的文件为：' + filePath.name)







