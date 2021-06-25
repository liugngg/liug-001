shengao=input("请输入你的身高(CM)：")
tizhong=input('请输入你的体重(Kg):')
bmi=int(tizhong)/(int(shengao)/100)**2
if bmi<=18.5:
    print("你的BMI指数为：%.2f,体重太轻了！"%bmi)
elif bmi<=25:
    print("你的BMI指数为：%.2f,体重正常。" % bmi)
elif bmi<=28:
    print("你的BMI指数为：%.2f,体重过重。" % bmi)
elif bmi<=32:
    print("你的BMI指数为：%.2f,属于肥胖！" % bmi)
else :
    print("你的BMI指数为：%.2f,严重肥胖！！" % bmi)




