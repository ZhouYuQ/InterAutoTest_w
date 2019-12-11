import requests

from utils.LogUtil import my_log


# 1.创建get封装方法
def request_get(url, headers):

# 2.发送requests get 请求
    r = requests.get(url, headers)

# 3.获取结果相应内容
    code = r.status_code
    try:
        body = r.json()
    except Exception as e:
        body = r.text
# 4.内容存到字典
    res = dict()
    res["code"] = code
    res["body"] = body

# 5.字典返回
    return res


# 创建post封装方法(上面的方式不使用；使用此类方法）
def request_post(url,json=None,headers=None):
    r = requests.post(url,json=json,headers=headers)
    # 3.获取结果相应内容
    code = r.status_code
    try:
        body = r.json()
    except Exception as e:
        body = r.text
    # 4.内容存到字典
    res = dict()
    res["code"] = code
    res["body"] = body

    # 5.字典返回
    return res



# 重构
# 1.创建类
class Request:
    # 2.定义公共方法
    def __init__(self):
        self.log = my_log("Requests")

    def request_api(self, url, json=None, headers=None, cookies=None, method="get"):
        # 1.增加方法的参数，根据参数来验证方法get/post，方法请求
        if method == "get":
            # get请求
            self.log.debug("发送get请求")
            r = requests.get(url, headers=headers,cookies=cookies)
        elif method == "post":
            # post请求
            self.log.debug("发送post请求")
            r = requests.post(url, json=json, headers=headers,cookies=cookies)

        # 2.重复的内容，复制进来(获取结果内容）
        code = r.status_code
        try:
            body = r.json()
        except Exception as e:
            body = r.text
        # 4.内容存到字典
        res = dict()
        res["code"] = code
        res["body"] = body
        # 5.字典返回
        return res

# 3.重构get/post方法
    # get
    # 1.定义方法
    def get(self, url, **kwargs):

        # 2.定义参数url,json,headers,cookies,method
        # 3.调用公共方法
        return self.request_api(url, method="get", **kwargs)

    def post(self, url, **kwargs):
        return self.request_api(url, method="post", **kwargs)
