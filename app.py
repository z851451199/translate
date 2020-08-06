from flask import Flask,render_template,request,session
from datetime import datetime
# 测试数据库CRUD
from pysql import basedao
dao = basedao.BaseDao()#定义类对象

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

# 商品
# 商品首页
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('all/index.html')

# 轮播展示
@app.route('/show',methods=['GET','POST'])
def show():
    return render_template('all/show.html')
# 用户登录
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('all/login.html')
    else:
        phone = request.form.get('phone')#phone = 13354705244
        pwd = request.form.get('pwd')#pwd = 123
        user = "select * from user WHERE uphone={}".format(phone)
        dao.execute(user)
        dao.commit()
        reslust = dao.fetch()
        if len(reslust)>0:
            for resl in reslust:
                if pwd == resl['upwd']:
                    session['user_id'] = resl['uid']
                    # 如果想在31天内不需要登录
                    session.permanent = True
                    return '<script>alert("登录成功！");location.href="/"</script>'
                else:
                    return '<script>alert("账号或密码不正确！");location.href="/login"</script>'
        else:
            return '<script>alert("用户不存在，请重新从输入！");location.href="/login"</script>'
# 注销
@app.route('/logout/')
def logout():
    session.clear()
    return '<script>alert("注销成功，请重新登录！");location.href="/login"</script>'
# 登录状态显示
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = "select * from user WHERE uid={}".format(user_id)
        dao.execute(user)
        dao.commit()
        reslust = dao.fetch()
        for res in reslust:
            username = res['uname']
            if username:
                return {'user':username,'uid':user_id}
    return {}
# 用户注册
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user = request.form['user']
        pwd1 = request.form['pwd']
        pwd2 = request.form['cpwd']
        phone = request.form['phone']
        phones = "select * from user WHERE uphone={}".format(phone)
        dao.execute(phones)
        dao.commit()
        res = dao.fetch()
        if len(res)>0:
            return '<script>alert("手机号已被注册！");location.href="/register"</script>'
        else:
            if pwd1 == pwd2:
                sqlInsert = 'insert into user(uname,uphone,upwd) values (%s,%s,%s)'
                params=[user,phone,pwd1]
                result =dao.execute(sqlInsert,params)
                dao.commit()#提交
                if result>0:
                    return '<script>alert("注册成功！");location.href="/login"</script>'
            else:
                return '<script>alert("两次密码不一致！");location.href="/register"</script>'
    else:
        return render_template('all/register.html')
# 商品展示
@app.route('/shopping',methods=['GET','POST'])
def shopping():
    sqlSelect = "select * from shopping"
    dao.execute(sqlSelect)
    dao.commit()
    result = dao.fetch()
    return render_template('all/shopping.html',result=result)
# 商品详情
@app.route('/detail')
def detail():
    ids = request.args.get('id')#6
    data = 'select  * from shopping WHERE sid={}'.format(6)
    dao.execute(data)
    dao.commit()
    reslust = dao.fetch()
    if len(reslust) > 0:
        return render_template('all/detail.html', rl=reslust[0])
    else:
        return '网页丢失！'
# 商品搜索
@app.route('/search',methods=['POST','GET'])
def search():
    if request.method == 'GET':
        return '<script>alert("未知内容！");location.href="/shopping"</script>'
    else:
        name = request.form.get('name')
        data = 'select  * from shopping WHERE sname LIKE "{}%" or  sname LIKE "%{}" or  sname LIKE "%{}%"'.format(name,name,name)
        dao.execute(data)
        dao.commit()
        reslust = dao.fetch()
        if len(reslust) > 0:
            return render_template('all/more_detail.html', rvlist=reslust,name=name)
        else:
            return '<script>alert("未知内容！");location.href="/shopping"</script>'
# 以下为购物车
# 商品加入购物车
@app.route('/add_car1')
def add_car1():
    Did = request.args.get('Did')
    uId = request.args.get('uId')
    page = request.args.get('page')
    data = 'select  * from shoppingcar WHERE sid={} AND uid={}'.format(Did,uId)
    dao.execute(data)
    dao.commit()
    reslust = dao.fetch()
    return add_car(reslust, Did, uId, page)
# 购物车展示
@app.route('/shpcar')
def shpcar():
    uId = request.args.get('uId')
    data = 'select  * from shoppingcar join shopping on shopping.sid=shoppingcar.sid WHERE uid={}'.format(uId)
    dao.execute(data)
    dao.commit()
    reslust = dao.fetch()
    if len(reslust) > 0:
        return render_template('all/shpcar.html',rvlist=reslust)
    else:
        return render_template('all/shpcar.html')
# 购物车商品删除
@app.route('/cardel')
def cardels():
    idd = request.args.get('id')
    uid = request.args.get('uid')
    sqlDelete = "delete from shoppingcar where sid = %s"
    params = [idd]
    result =dao.execute(sqlDelete,params)
    dao.commit()#提交
    #不需要执行 fetchall 操作
    if result>0:
        return '<script>alert("删除成功！");location.href="/shpcar?uId='+uid+'"</script>'
    else:
        return '<script>alert("无法删除！");location.href="/shpcar?uId='+uid+'"</script>'
# 购物车商品下单
@app.route('/order')
def order():
    uid = request.args.get('uid')
    ids = request.args.get('id').split('-')
    nums = request.args.get('num').split('-')
    now = datetime.now()
    sqlInsert1 = "INSERT INTO `orders`(uid,otime)VALUES(%s,%s)"
    params1 = [uid,now]
    result = dao.execute(sqlInsert1, params1)
    dao.commit()  # 提交
    if result > 0:
        sqloId = "SELECT MAX(oid) FROM `orders`"
        dao.execute(sqloId)
        dao.commit()
        result2 = dao.fetch()
        oid = result2[0]['MAX(oid)']
        for id,num in zip(ids,nums):
            sqlInsert2 = 'INSERT INTO orderdetail(sid,onum,oid) VALUES (%s,%s,%s)'
            params2 = [id,num,oid]
            result2 = dao.execute(sqlInsert2, params2)
            dao.commit()
            if result2>0:
                print('添加成功')
            else:
                print(id,"-",num,"-",oid)
        return '<script>alert("下单成功！");location.href="/shopping"</script>'
    else:
        return '<script>alert("下单失败！");location.href="/shopping"</script>'
# 全部订单
@app.route('/order_more')
def order_more():
    uid = request.args.get('uid')
    sqlSelect = "select * from `orders` join `user` on `orders`.uid=`user`.uid  WHERE `orders`.uid = {}".format(uid)
    dao.execute(sqlSelect)
    dao.commit()
    result = dao.fetch()
    return render_template('all/orders.html',result=result)
# 订单详情
@app.route('/order_detail')
def order_detail():
    oid = request.args.get('oid')
    sqlSelect ='select * from orderdetail join shopping on shopping.sid=orderdetail.sid WHERE oid={}'.format(oid)
    dao.execute(sqlSelect)
    dao.commit()
    result = dao.fetch()
    return render_template('all/order_detail.html', result=result)
# 删除订单
@app.route('/order_delete')
def order_delete():
    uid = request.args.get('uid')
    oid = request.args.get('oid')
    sqlDelete = "DELETE FROM orderdetail where oid = %s"
    params = [oid]
    result = dao.execute(sqlDelete, params)
    dao.commit()  # 提交
    # 不需要执行 fetchall 操作
    if result > 0:
        sqlDelete2 = "delete from `orders` where oid = %s"
        params2 = [oid]
        result = dao.execute(sqlDelete2, params2)
        dao.commit()  # 提交
        # 不需要执行 fetchall 操作
        if result > 0:
            return '<script>alert("订单取消成功！");location.href="/order_more?uid='+uid+'"</script>'
        else:
            return '<script>alert("订单无法取消！");location.href="/order_more?uid='+uid+'"</script>'
    else:
        return '<script>alert("订单无法取消！");location.href="/order_more?uid='+uid+'"</script>'





# 封装函数，需要时引用
def add_car(reslust,Did, uId,page):
    if len(reslust) > 0:
        return '<script>alert("添加到购物车成功！");location.href="/'+page+'"</script>'
    else:
        sqlInsert = 'insert into shoppingcar(sid,uid) values (%s,%s)'
        params = [Did, uId]
        result = dao.execute(sqlInsert, params)
        dao.commit()  # 提交
        if result > 0:
            return '<script>alert("添加到购物车成功！");location.href="/'+page+'"</script>'
        else:
            return '<script>alert("添加到购物车失败！");location.href="/'+page+'"</script>'



# 以下为后台管理----超级管理员
# 登录
@app.route('/admin',methods=['POST','GET'])
def admin():
    if request.method == 'GET':
        return render_template('admin/adlogin.html')
    else:
        name = request.form.get('name')
        pwd = request.form.get('pwd')
        sqlSelect = "select * from admin where adname='{}'".format(name)

        dao.execute(sqlSelect)
        dao.commit()
        result = dao.fetch()
        if len(result)>0:
            for rs in result:
                global relt
                relt = rs
                if pwd == relt['adpwd']:
                    session['admin_id'] = relt['adname']
                    # 如果想在31天内不需要登录
                    session.permanent = True
                    return '<script>alert("登录成功！");location.href="/showShopping"</script>'
                else:
                    return '<script>alert("账号或密码不正确！");location.href="/admin"</script>'
        else:
            return '<script>alert("用户不存在，请重新从输入！");location.href="/admin"</script>'
# 登录状态显示
@app.context_processor
def my_context_processor():
    admin_id = session.get('admin_id')

    if admin_id:
        username = admin_id
        if username:
            return {'user':username}
    return {}
# 注销
@app.route('/adlogout/')
def adlogout():
    session.clear()
    return '<script>alert("注销成功，请重新登录！");location.href="/admin"</script>'
# 数据展示
@app.route('/showShopping')
def showShopping():
    return render_template('admin/showList.html')
# 后台用户查看
@app.route('/showList1')
def showList1():
    sqlSelect = "select * from user"
    dao.execute(sqlSelect)
    dao.commit()
    result = dao.fetch()
    return render_template('admin/showList1.html', list=result)
# 后台展示商品
@app.route('/showList2')
def showList2():
    # 数据获取
    sqlSelect = "select  * from shopping"
    dao.execute(sqlSelect)
    dao.commit()
    result = dao.fetch()
    return render_template('admin/showList2.html',show=result)
# 添加
@app.route('/db_add')
def add():
    return render_template('admin/add_db.html')
@app.route('/db_adds/',methods=['POST','GET'])
def adds():
    data = dict(request.form)
    name = request.form.get('name')[0]
    content = request.form.get('content')[0]
    price = data.get('price')[0]
    num = data.get('num')[0]
    img = data.get('img')[0]
    sqlInsert = 'insert into shopping(sname,scontent,sprice,stock,imgUrl) values (%s,%s,%s,%s,%s)'
    params = [name,content,price,num,img]
    result = dao.execute(sqlInsert, params)
    dao.commit()  # 提交
    if result > 0:
        return '<script>alert("添加成功！");location.href="/showList2"</script>'
    else:
        return '<script>alert("数据填写有误！");location.href="/db_add"</script>'
# 删除
@app.route('/del')
def dels():
    ids = request.args.get('id')
    sqlDelete = "delete from shopping where sid = %s"
    params = [ids]
    result =dao.execute(sqlDelete,params)
    dao.commit()#提交
    #不需要执行 fetchall 操作
    if result>0:
        return '<script>alert("数据删除成功！");location.href="/showList2"</script>'
    else:
        return '<script>alert("基础数据无法删除！");location.href="/showList2"</script>'

@app.route('/update')
def update():
    ids = request.args.get('id')
    data = 'select * from shopping WHERE sid={}'.format(ids)
    dao.execute(data)
    dao.commit()
    reslust = dao.fetch()
    if len(reslust) > 0:
        return render_template('admin/update.html',res=reslust[0])
    else:
        return '未知错误！'

@app.route('/updates',methods=['POST','GET'])
def updates():
    data = dict(request.form)
    id = data.get('id')[0]
    name = data.get('name')[0]
    price = data.get('price')[0]
    num = data.get('num')[0]
    scontent = data.get('content')[0]
    img = data.get('img')[0]
    sqlUpdate = "update shopping set sname= %s,sprice= %s,stock= %s,imgUrl= %s,scontent=%s where sid = %s"
    params = [name,price,num,img,scontent,id]
    result =dao.execute(sqlUpdate,params)
    dao.commit()#提交
    if result:
        return '<script>alert("数据修改成功！");location.href="/showList2"</script>'
    else:
        return '<script>alert("数据无法修改！");location.href="/showList2"</script>'



if __name__ == '__main__':
    app.run()
