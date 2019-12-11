import json
import os

import allure
import pytest

from common import Base
from common import ExeclConfig
from common.ExeclData import Data
from config import Conf
from config.Conf import ConfigYaml
from utils.AssertUtil import AssertUtil
from utils.LogUtil import my_log
from utils.RequestsUtil import Request

# 1.初始化信息
# 初始化测试用例文件
case_file = os.path.join(Conf.get_data_path(),ConfigYaml().get_execl_file())
# 测试用例sheet名称
sheet_name = ConfigYaml().get_execl_sheet()
# 获取运行测试用例列表
data_init = Data(case_file, sheet_name)
# 判断用例是否运行
run_list = data_init.get_run_data()

print(run_list)
# 日志
log = my_log()

data_key = ExeclConfig.DataConfig

# 2.测试用例方法,参数化运行
# 一个用例的执行


class TestExecl:
    def run_api(self, url, method, params=None, header=None, cookie=None):
        """
        发送请求api
        :return:
        """
        # 2.接口请求
        request = Request()
        # params转义json(参数是字符类型的要转义）
        # 验证params有没有内容
        if len(str(params).strip()) != 0:
            params = json.loads(params)
            print(params)
        # method post/get
        if str(method).lower() == "get":
            res = request.get(url, json=params, headers=header, cookies=cookie)
        elif str(method).lower() == "post":
            res = request.post(url, json=params, headers=header, cookies=cookie)
        else:
            log.error("错误请求method：%s" % method)
        return res

    def run_pre(self, pre_case):
        # 初始化数据(执行的前置条件的用例）
        url = ConfigYaml().get_conf_url() + pre_case[data_key.url]
        method = pre_case[data_key.method]
        params = pre_case[data_key.params]
        expect_result = pre_case[data_key.expect_result]
        headers = pre_case[data_key.headers]
        cookies = pre_case[data_key.cookies]

        # 1.判断headers是否存在，json转义，无需
        header = Base.json_parse(headers)
        cookie = Base.json_parse(cookies)

        res = self.run_api(url, method, params, header, cookie)
        print("前置用例执行：%s" %res)
        return res

    # 1.增加pytest
    # 2.修改方法参数
    # 3.重构函数内容
    # 4.pytest.main
    # 1).初始化信息，url，data
    # 1. 增加pytest
    @pytest.mark.parametrize("case", run_list)
    def test_run(self, case):

        # run_list第一个用例，用例，key获取values
        url =ConfigYaml().get_conf_url() + case[data_key.url]
        print(url)
        case_id = case[data_key.case_id]
        print(case_id)
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        pre_exec = case[data_key.pre_exec]
        method = case[data_key.method]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        expect_result = case[data_key.expect_result]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        code = case[data_key.code]
        db_verify = case[data_key.db_verify]

        # 动态关联
        # 1.验证前置条件
        if pre_exec:
        # 2.找到需要执行的用例
        # 判前置条件的用例
            pre_case = data_init.get_cass_pre(pre_exec)
            print("前置条件用例信息为:%s" %pre_case)
            pre_res = self.run_pre(pre_case)
            headers, cookies = self.get_correlation(headers, cookies, pre_res)
        header = Base.json_parse(headers)
        cookie = Base.json_parse(cookies)
        res = self.run_api(url, method, params, header, cookie)
        print("测试用例执行：%s" % res)

        #allure
        #sheet名称 feature 一级标签
        allure.dynamic.feature(sheet_name)
        #模块    story 二级标签
        allure.dynamic.story(case_model)
        #用例id+接口名称  title
        allure.dynamic.title(case_id+case_name)
        # 请求url  请求 类型  期望结果 实际结果
        desc = "<font color='red'>请求URL:<font>{}<Br/>" \
               "<font color='red'>请求类型：<font>{}<Br/>" \
               "<font color='red'>期望结果：<font>{}<Br/>" \
               "<font color='red'>实际结果：<font>{}".format(url, method, expect_result, res)
        allure.dynamic.description(desc)


        # 断言验证
        # 状态码 返回结果内容 数据库相关的结果验证
        assert_util = AssertUtil()
        # 状态码
        assert_util.assert_code(int(res["code"]), int(code))
        # 返回结果内容
        assert_util.assert_in_body(str(res["body"]), str(expect_result))
        #数据库结果断言
        Base.assert_db("db_1", res["body"], db_verify)


        # 以下代码封装与base中的方法：
        # # 1.初始化数据库
        # from common.Base import init_db
        # sql = init_db("db_1")
        # # # 2.查询sql，execl定义好的
        # db_res = sql.fetchone(db_verify)
        # log.debug("数据库查询结果{}".format(str(db_res)))
        #
        # # 3.数据库的结果与接口返回的结果验证
        # # 获取数据库结果的key；根据key获取数据库的结果以及接口的结果
        # verify_list = list(dict(db_res).keys())
        #
        # for line in verify_list:
        #     res_line = res["body"][line]
        #     res_db_line = dict(db_res)[line]
        # # 验证
        #     assert_util.assert_body(res_line, res_db_line)


    def get_correlation(self, headers, cookies, pre_res):

        """
        关联
        :param headers:
        :param cookies:
        :param pre_res:
        :return:
        """
        # 验证是否有关联
        headers_para, cookies_para = Base.params_find(headers, cookies)
        print("获取到的headers_para值是：%s"%headers_para)
        # 有关联，执行前置用例，获取结果
        if len(headers_para):
            headers_data = pre_res['body'][headers_para[0]]
            print("token是：%s"%headers_data)
            headers = Base.res_sub(headers, headers_data)

        if len(cookies_para):
            cookies_data = pre_res["body"][cookies_para[0]]
            # 结果替换
            cookies = Base.res_sub(cookies, cookies_data)
        return headers, cookies


if __name__ == '__main__':
    report_path = Conf.get_report_path()+os.sep+"result"
    report_html_path = Conf.get_report_path()+os.sep+"html"
    # pytest.main(["test_excel_case.py", "--alluredir","./report/result"])
    pytest.main(["-s", "--alluredir",report_path])
    # Base.allure_report("./report/result","./report/html")
    # Base.allure_report(report_path, report_html_path)
    # Base.send_mail(title="接口测试报告",content=report_html_path)







