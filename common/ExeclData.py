
from common.ExeclConfig import DataConfig
from utils.ExcelUtil import ExcelReader


class Data:
    def __init__(self, testcase_file, sheet_name):
        # 1.使用execl工具类，获取结果list
        self.reader = ExcelReader(testcase_file, sheet_name)

    #2.列是否运行内容:y
    def get_run_data(self):
        """
        根据是否运行列==y，获取执行的测试用例
        :return:
        """
        run_list = list()
        for line in self.reader.data():
            # print(line)
            if str(line[DataConfig().is_run]).lower() == "y":
                run_list.append(line)
        # 3.保留要执行结果，放到新的列表
        return run_list

    def get_case_list(self):
        """
        获取全部的测试用例
        :return:
        """
        run_list = list()
        for line in self.reader.data():
            run_list.append(line)
        return run_list

        # run_list = [line for line in self.reader.data()]
        # return run_list

    def get_cass_pre(self, pre):
        """
        根据前置条件，从全部测试用例取到测试用例
        :param pre:
        :return:
        """
        # 获取全部的测试用例
        run_list = self.get_case_list()
        #list判断，执行，获取
        for line in run_list:
            if pre in dict(line).values():
                return line
        return None






# reader =  ExcelReader("../data/testdatabase.xlsx","美多商城")
# print(reader.data())
# run_list = list()
# for line in reader.data():
#     if line["是否运行"] == "y":
#         # print(line)
#         run_list.append(line)
# print(run_list)


# Data("../data/testdatabase.xlsx","美多商城").get_run_data()
