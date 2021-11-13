import unittest
import HtmlTestRunner
from datetime import datetime

from utils.excel_lib import ExcelLib
from testscripts.empcomp_test import *


DATETIME_FORMAT        = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
EXCEL_REPORT_FILE_PATH = 'excelreports/' + DATETIME_FORMAT + ' - report.xlsx'
PROP_FILE_PATH         = 'testdata/app-config.properties'

def run_tests():
    test_classes = [
        EmployeeCompensationTest
    ]

    suite_list = []
    for test_class in test_classes:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite_list.append(suite)

    test_suite = unittest.TestSuite(suite_list)
    # unittest.TextTestRunner(verbosity=2).run(test_suite)
    runner = HtmlTestRunner.HTMLTestRunner(output='htmlreports/')
    runner.run(test_suite)

if __name__ == '__main__':
    ExcelLib().create(EXCEL_REPORT_FILE_PATH)
    run_tests()