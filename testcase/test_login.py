import os

import pytest

from config import Conf
from config.Conf import ConfigYaml
from utils.RequestsUtil import Request
from utils.YamlUtil import YamlReader

# 1.获取测试用例内容list
# 获取testlogin.yml文件路径
test_file = os.path.join(Conf.get_data_path(),"testlogin.yml")

# 使用工具类来读取多个文档内容
data_list = YamlReader(test_file).data_all()

#2.参数化执行测试用例
@pytest.mark.parametrize("login",data_list)
def test_yaml(login):
    # 初始化url，data
    url = ConfigYaml().get_conf_url() +login["url"]
    print("url%s"%url)
    data = login["data"]
    print("data%s"%data)
    request =Request()
    res = request.post(url,json=data)
    print(res)

if __name__ == '__main__':
    pytest.main(["-s","test_login.py"])


