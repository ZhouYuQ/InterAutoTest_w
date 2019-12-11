import os

import pytest

from config import Conf

if __name__ == '__main__':
    report_path = Conf.get_report_path()+os.sep+"result"
    report_html_path = Conf.get_report_path()+os.sep+"html"
    pytest.main(["test_excel_case.py", "--alluredir","./report/result"])
    # pytest.main(["test_excel_case.py", "--alluredir",report_path])