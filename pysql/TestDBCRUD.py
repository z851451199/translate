# 测试数据库CRUD
from basedao import BaseDao

dao = BaseDao()#定义类对象
f = open('date.txt',encoding='utf-8')
for line in f:
    text = line.split('**')
    sqlInsert = 'insert into shopping(sname,sprice,stock,imgUrl) values (%s,%s,%s,%s)'
    params=[text[0],text[1],text[2],text[3].replace('\n','')]
    result =dao.execute(sqlInsert,params)
    dao.commit()#提交
    #不需要执行 fetchall 操作
    if result>0:
        print('商品添加成功！')
        pass
#
sqlInsert2 = 'insert into admin(adname,adpwd) values (%s,%s)'
params=['admin','123']
result =dao.execute(sqlInsert2,params)
dao.commit()#提交
#不需要执行 fetchall 操作
if result>0:
    print('管理员添加成功！')
    pass