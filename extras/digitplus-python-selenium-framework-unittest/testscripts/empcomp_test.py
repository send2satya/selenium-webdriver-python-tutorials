import logging
import os
import platform
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from utils.excel_lib import ExcelLib
from utils.generic_lib import GenericLib
from pages.loginpage import LoginPage
from pages.homepage import HomePage
from pages.empcomppage import EmployeeCompensationPage
from runner.testrunner import DATETIME_FORMAT, EXCEL_REPORT_FILE_PATH, PROP_FILE_PATH


IMG_FILE_NAME  = 'employee_compensation.png'
LOG_FILE_NAME  = 'employee_compensation.log'
test_status    = 'fail'

class EmployeeCompensationTest(unittest.TestCase):
    # Defining class variables
    lib = GenericLib()
    elib = ExcelLib()

    # Create and configure logger
    LOG_FORMAT = '%(asctime)s : %(levelname)s  - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt='%d/%m/%Y %I:%M:%S %p',
        handlers=[
            logging.FileHandler('logs/' + DATETIME_FORMAT + ' - ' + LOG_FILE_NAME),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger()

    @classmethod
    def setUpClass(cls):
        # Configure Google Chrome browser
        options = Options()

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-web-security')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')

        
        cls.download_dir = os.getcwd() + '\\downloads\\' if platform.system() == 'Windows' else os.getcwd() + '/downloads/'
        options.add_experimental_option('prefs', {
            'download.default_directory': cls.download_dir,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': 'false'
        })

        if cls.lib.get_data_from_properties(PROP_FILE_PATH, 'headless').strip().lower() == 'true':
            # options.set_headless(headless=True))
            # options.headless = True
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1280,800')
            # options.add_argument('--start-maximized')

        # Initializing driver and opening up the url
        cls.driver = webdriver.Chrome(executable_path='drivers/chromedriver.exe', options=options)
        cls.logger.info("Opening up the browser window")
        cls.driver.maximize_window()
        cls.logger.info("Maximizing the browser window")
        cls.driver.implicitly_wait(int(cls.lib.get_data_from_properties(PROP_FILE_PATH, 'implicit_wait').strip()))
        cls.driver.get(cls.lib.get_data_from_properties(PROP_FILE_PATH, 'url').strip())
        cls.logger.info("Loading up " + cls.lib.get_data_from_properties(PROP_FILE_PATH, 'url').strip())

        # Creating an entry for 'Employee Compensation' in the active excel sheet
        cls.active_row = cls.elib.get_row_count(EXCEL_REPORT_FILE_PATH)
        cls.elib.write(EXCEL_REPORT_FILE_PATH, cls.active_row + 1, 1, 'Employee Compensation')
    
    def setUp(self):
        login = LoginPage(self.driver)

        login.enter_username(self.lib.get_data_from_properties(PROP_FILE_PATH, 'username').strip())
        self.logger.info("Entered '" + self.lib.get_data_from_properties(PROP_FILE_PATH, 'username').strip() + "' into the 'Username' textbox")

        login.enter_password(self.lib.get_data_from_properties(PROP_FILE_PATH, 'password').strip())
        self.logger.info("Entered '" + self.lib.get_data_from_properties(PROP_FILE_PATH, 'password').strip() + "' into the 'Password' textbox")

        login.click_login()
        self.logger.info("Clicked on the 'Login' button")
        time.sleep(5)
        
    def test_issue_policy(self):
        home = HomePage(self.driver)

        # self.assertTrue(home.visibility_of_user_tab(), 'Home page verification failed')
        self.assertEqual(self.driver.current_url.split("#")[1], '/home')
        self.logger.info("Verify if landing to 'Home' page is successful")

        home.click_employee_comp()
        self.logger.info("Click on the 'Employee Comp' tab")
        time.sleep(5)

        # ---------------------------------------------------------------------------------------------------

        empcomp = EmployeeCompensationPage(self.driver)

        #self.assetTrue(empcomp.visibility_of_header_text(), 'Employee Compensation page verification failed')
        self.assertEqual(self.driver.current_url.split("#")[1], '/employee-comp')
        self.logger.info("Verify if we are in the 'Employee Compensation' page")

        empcomp.select_value_from_medical_exp_extn('75,000')
        self.logger.info("Selected a value from the 'Medical Expenses Extn. Limit per person' dropdown")

        self.lib.scroll_to_end(self.driver)
        empcomp.select_value_from_work_desc('Architects')
        self.logger.info("Selected 'Architects' from the 'Work Description' dropdown list")

        empcomp.select_value_from_sub_category('NA')
        self.logger.info("Selected 'NA' from the 'Sub Category' dropdown list")

        empcomp.enter_short_desc_of_work('Skilled')
        self.logger.info("Entered value 'Skilled' into 'Short Description of Work' textbox")

        empcomp.enter_wages('35000')
        self.logger.info("Entered value '35000' into 'Wages/Salary Per Month Per Person' textbox")

        empcomp.enter_total_no_of_emp('10')
        self.logger.info("Entered value '10' into 'Total oo of employees' textbox")

        empcomp.click_show_premium()
        self.logger.info("Clicked on the 'Show Premium' button")
        time.sleep(5)

        quick_quote_premium = empcomp.get_premium()
        self.elib.write(EXCEL_REPORT_FILE_PATH, self.active_row + 1, 3, quick_quote_premium)
        
        empcomp.scroll_to_cutomer_details()
        self.logger.info("Scrolled down to the 'Customer Details' section")

        empcomp.fill_customer_details('Deepjyoti Barman', '7687881748', 'deepjyoti.barman@godigit.com')
        self.logger.info("Filled in all the fields of the 'Customer Details' section with valid details")

        empcomp.fill_risk_location_details('Sector V, Salt Lake, Kolkata - North 24 Parganas', '700102')
        self.logger.info("Filled in all the fields of the 'Risk Location' section with valid details")

        self.lib.scroll_to_end(self.driver)
        empcomp.fill_com_location_details('Nischintapur, Budge Budge, Kolkata - South 24 Parganas', '700137')
        self.logger.info("Filled in all the fields of the 'Communication Location' section with valid details")

        empcomp.click_save_quote()
        self.logger.info("Clicked on the 'Save Quote' button")
        time.sleep(10)

        save_quote_premium = empcomp.get_premium()
        self.elib.write(EXCEL_REPORT_FILE_PATH, self.active_row + 1, 4, save_quote_premium)
        globals()['test_status'] = 'pass' if quick_quote_premium == save_quote_premium else 'fail'
        self.assertEqual(quick_quote_premium, save_quote_premium, "Premium mismatch is observed - 'Quick quote' premium is not matching with 'Save Quote' premium")
        self.logger.info("Verify if 'Quick Quote' premium matches with 'Save Quote' premium")

        quote_no = empcomp.get_quote_number()
        self.elib.write(EXCEL_REPORT_FILE_PATH, self.active_row + 1, 2, quote_no)
        self.logger.info("Quote Number (Employee Comp): " + quote_no)

        empcomp.download_proposal()
        quote_regex = quote_no + '*PROPOSAL.pdf'
        max_download_time_in_secs = 20
        download_time_in_secs = self.lib.wait_for_download_to_complete(self.download_dir, quote_regex, max_download_time_in_secs)
        if download_time_in_secs < max_download_time_in_secs:
            self.elib.write(EXCEL_REPORT_FILE_PATH, self.active_row + 1, 5, 'Success')
            self.logger.info(f"Downloaded the PROPOSAL document for '{quote_no}'")
        else:
            self.elib.write(EXCEL_REPORT_FILE_PATH, self.active_row + 1, 5, 'Failed')
            self.logger.info(f"Downloading of the PROPOSAL document for '{quote_no}' failed")
        globals()['test_status'] = 'pass' if download_time_in_secs < max_download_time_in_secs else 'fail'

        empcomp.click_submit()
        empcomp.click_yes_on_final_submit()
        self.logger.info("Click on the 'Submit' button and selected 'Yes' on final submit")
        time.sleep(5)
        
        self.lib.scroll_to_end(self.driver)
        empcomp.select_value_from_payment_mode('Agent Float')
        self.logger.info("Selected 'Agent Float' from 'Payment mode' dropdown list")

        empcomp.click_proceed_to_pay()
        self.logger.info("Clicked on 'Proceed to pay' button")

        # ---------------------------------------------------------------------------------------------------

        time.sleep(5)
        self.driver.get_screenshot_as_file('screenshots/' + DATETIME_FORMAT + ' - ' + IMG_FILE_NAME)
        home.click_on_digitplus_logo()
        self.logger.info("Clicked on 'Digitplus' brand logo")

        self.assertEqual(self.driver.current_url.split("#")[1], '/home')
        self.logger.info("Verify if landing to 'Home' page is successful")

    def tearDown(self):
        home = HomePage(self.driver)
        home.logout()
        self.logger.info("Logging out of the Digitplus portal")

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.lib.batch_cleanup()

        if test_status == 'pass':
            cls.elib.write(EXCEL_REPORT_FILE_PATH, cls.active_row + 1, 8, 'PASS', '00008000', True)
        else:
            cls.elib.write(EXCEL_REPORT_FILE_PATH, cls.active_row + 1, 8, 'FAIL', '00FF0000', True)
