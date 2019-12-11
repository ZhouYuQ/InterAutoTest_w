from common.Base import init_db
from config.Conf import ConfigYaml
from utils.AssertUtil import AssertUtil
from utils.RequestsUtil import Request

request =Request()
url_path = ConfigYaml().get_conf_url()
# 登录用例
def test_login():
    # 定义测试数据
    url = url_path + "/authorizations/"
    data = {"username": "python", "password": "12345678"}

    # 发送post请求
    r = request.post(url, json=data)

    # 输出结果
    print(r)

    # 验证
    # 返回状态码
    code = r["code"]
    # assert code == 201
    AssertUtil().assert_code(code,200)

    # 返回结果内容
    body = r["body"]
    AssertUtil().assert_in_body(body,'"username": "python", "user_id": 1')

    # 1.初始化数据库对象(数据库断言）
    conn = init_db("db_1")
    # 2.查询结果
    res_db = conn.fetchone("select id,username from tb_users where username='python'")
    print("数据库查询结果",res_db)
    # 3.验证
    user_id = body["user_id"]
    assert user_id == res_db["id"]
    token = r["body"]["token"]
    return token




# 个人信息用例
def test_info():
    # 1.参数
    url = url_path + "/user/"
    token = test_login()
    headers = {
        'Authorization' : 'JWT ' + token
    }
    # 2.get请求
    r =request.get(url, headers=headers)
    # 3.输出
    print(r)

# 获取商品列表数据
def test_goods_list():
    # 1.参数
    url = url_path + "/categories/115/skus"
    data = {
        "page": "1",
        "page_size": "10",
        "ordering": "create_time"
    }
    # 2.请求
    r = request.get(url, json=data)
    # 3.输出
    print(r)

# 添加购物车成功
def test_cart():
    # 参数
    url = url_path + "/cart/"
    data = {"sku_id": "3","count": "1","selected": "true"}
    token = test_login()
    headers = {
        'Authorization': 'JWT ' + token
    }
    #请求
    r = request.post(url,json=data,headers=headers)
    # 输出
    print(r)

# 订单
def test_order():
    url =url_path + "/orders/"
    data = {
        "address": "1",
        "pay_method": "1",
    }
    token = test_login()
    headers = {
        'Authorization': 'JWT ' + token
    }
    r = request.post(url,json=data,headers=headers)
    print(r)


if __name__ == '__main__':
    # login()
    # info()
    # goods_list()
    # cart()
    test_order()


    # 1.根据默认运行原则，调整py文件命名，函数命名
    # 2.pytest.main()yunx，或者命令行直接pytest运行
    # pytest.main(["-s"])
