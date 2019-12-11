import os

from utils.YamlUtil import YamlReader

# 1.获取项目基本目录
# 获取当前项目的绝对路径
current = os.path.abspath(__file__)

# 获取父级目录
BASE_DIR = os.path.dirname(current)
BASE_DIR = os.path.dirname(os.path.dirname(current))

# 2.定义config目录的路径
_config_path = BASE_DIR + os.sep + "config"
# .定义data目录的路径
_config_data_path = BASE_DIR + os.sep + "data"

# 3.定义conf.yml的路径
_config_file = _config_path + os.sep + "conf.yml"
# 定义db_conf.yml路径
_db_config_file = _config_path + os.sep +"db_conf.yml"


# 定义logs目录路径
_log_path = BASE_DIR + os.sep + "logs"


# 定义report目录的路径
_report_path = BASE_DIR + os.sep + "report"


def get_report_path():
    """
    获取report绝对路径
    :return:
    """
    return _report_path

def get_data_path():
    return _config_data_path

def get_config_path():
    return _config_path

def get_config_file():
    return _config_file

def get_db_config_file():
    return _db_config_file

def get_log_path():
    """
    获取log文件路径
    :return:
    """
    return _log_path

# 4.读取配置文件
# 创建类
class ConfigYaml:
    # 初始yaml读取配置文件
    def __init__(self):
        self.config = YamlReader(get_config_file()).data()
        self.db_config = YamlReader(get_db_config_file()).data()

    # 定义方法获取需要信息
    def get_execl_file(self):
        """
        获取测试用例execl名称
        :return:
        """
        return self.config["BASE"]["test"]["case_file"]

    def get_execl_sheet(self):
        """
        获取测试用例execl名称
        :return:
        """
        return self.config["BASE"]["test"]["case_sheet"]

    def get_conf_url(self):
        """获取接口ip"""
        return self.config["BASE"]["test"]["url"]

    def get_db_conf_info(self,db_alias):
        """
        根据db_alias获取 该名称下的数据库信息
        :param db_alias:
        :return:
        """
        return self.db_config[db_alias]


    def get_conf_log_level(self):
        """
        获取日志级别
        """
        return self.config["BASE"]["log_level"]

    def get_conf_log_extension(self):
        """
        获取文件扩展名
        """
        return self.config["BASE"]["log_extension"]


    def get_email_info(self):
        """
        获取邮件配置相关信息
        """
        return self.config["email"]


if __name__ == '__main__':
    conf_read = ConfigYaml()
    # print(conf_read.get_conf_url())
    # print(conf_read.get_conf_log_level())
    # print(conf_read.get_conf_log_extension())
    # print(conf_read.get_db_conf_info("db_1"))
    # print(conf_read.get_execl_file())
    # print(conf_read.get_execl_sheet())
    print(conf_read.get_email_info())