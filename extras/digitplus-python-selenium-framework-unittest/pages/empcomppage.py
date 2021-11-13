import time
from selenium.webdriver.common.by import By

from utils.generic_lib import GenericLib


class EmployeeCompensationPage():
    header_text_xpath                    = '//p[text()="Employee Compensation"]'
    medical_exp_extn_dropdown_xpath      = '//mat-select[@name="medical_expense_select"]'
    work_desc_dropdown_xpath             = '//div[@class="work_des"]/input'
    sub_cat_dropdown_xpath               = '//div[@class="sub_cat"]/input'
    short_desc_textbox_xpath             = '//div[@class=" short_des"]/input'
    salary_pm_textbox_xpath              = '//div[@class="salary"]/input'
    total_emp_textbox_xpath              = '//div[@class="no_emp"]/input'
    show_premium_button_xpath            = '//span[text()="Show Premium"]'
    customer_details_header_xpath        = '//p[text()="Customer Details"]'
    name_of_the_insured_textfield_id     = 'firstName'
    mobile_no_textfield_name             = 'mobileNumber'
    email_id_textfield_name              = 'emailId'
    risk_full_addr_textfield_xpath       = '//input[@ng-reflect-name="address0"]'
    risk_pincode_textfield_xpath         = '//input[@ng-reflect-name="pincode0"]'
    anywhere_in_india_checkbox_xpath     = '//input[@ng-reflect-name="anywhere0"]'
    com_full_addr_textfield_name         = 'com_address'
    com_pincode_textfield_name           = 'com_pincode'
    save_quote_button_xpath              = '//button[contains(text(), "Save Quote")]'
    quote_number_label_xpath             = '//p[text()="Quote Number"]/parent::div/div/p'
    proposal_download_link_xpath            = '//i[@title="Download quote"]'
    total_payable_amt_footer_label_xpath = '//div[contains(@class, "footer")]/descendant::p[text()="Total Payable Amount"]/following-sibling::p'
    submit_button_xpath                  = '//span[text()="Submit"]'
    final_submit_option_yes_xpath        = '//div[@class="refferal-cta-container"]/button[text()="Yes"]'
    final_submit_option_no_xpath         = '//div[@class="refferal-cta-container"]/button[text()="No"]'
    payment_mode_dropdown_xpath          = '//label[text()="Payment Mode"]/following::mat-select'
    proceed_to_pay_button_xpath          = '//span[text()="Proceed to pay"]'
    
    lib = GenericLib()

    def __init__(self, driver):
        self.driver = driver

    def visibility_of_header_text(self):
        return self.driver.find_element_by_xpath(self.header_text_xpath).is_displayed()

    def select_value_from_medical_exp_extn(self, value):
        self.driver.find_element_by_xpath(self.medical_exp_extn_dropdown_xpath).click()
        self.driver.find_element_by_xpath('//mat-option/span[contains(text(), "' + value + '")]').click()

    def select_value_from_work_desc(self, desc):
        self.driver.find_element_by_xpath(self.work_desc_dropdown_xpath).send_keys(desc)
        time.sleep(2)
        self.lib.move_and_click_by_offset(self.driver, By.XPATH, self.work_desc_dropdown_xpath, 50, 30)

        #self.driver.find_element_by_xpath('//div[@class="work_des"]/descendant::option[contains(text(), "' + value + '")]').click()

    def select_value_from_sub_category(self, subcat):
        self.driver.find_element_by_xpath(self.sub_cat_dropdown_xpath).send_keys(subcat)
        time.sleep(2)
        self.lib.move_and_click_by_offset(self.driver, By.XPATH, self.sub_cat_dropdown_xpath, 50, 30)

    def enter_short_desc_of_work(self, short_desc):
        self.driver.find_element_by_xpath(self.short_desc_textbox_xpath).send_keys(short_desc)

    def enter_wages(self, sal):
        self.driver.find_element_by_xpath(self.salary_pm_textbox_xpath).clear()
        self.driver.find_element_by_xpath(self.salary_pm_textbox_xpath).send_keys(sal)

    def enter_total_no_of_emp(self, no_of_emp):
        self.driver.find_element_by_xpath(self.total_emp_textbox_xpath).clear()
        self.driver.find_element_by_xpath(self.total_emp_textbox_xpath).send_keys(no_of_emp)

    def click_show_premium(self):
        self.driver.find_element_by_xpath(self.show_premium_button_xpath).click()

    def scroll_to_cutomer_details(self):
        self.lib.scroll_to_element(self.driver, self.driver.find_element_by_xpath(self.customer_details_header_xpath))

    def fill_customer_details(self, name, mobile, email):
        self.driver.find_element_by_id(self.name_of_the_insured_textfield_id).send_keys(name)
        self.driver.find_element_by_name(self.mobile_no_textfield_name).send_keys(mobile)
        self.driver.find_element_by_name(self.email_id_textfield_name).send_keys(email)

    def fill_risk_location_details(self, loc, pincode):
        self.driver.find_element_by_xpath(self.risk_full_addr_textfield_xpath).send_keys(loc)
        self.driver.find_element_by_xpath(self.risk_pincode_textfield_xpath).send_keys(pincode)

    def fill_com_location_details(self, loc, pincode):
        self.driver.find_element_by_name(self.com_full_addr_textfield_name).send_keys(loc)
        self.driver.find_element_by_name(self.com_pincode_textfield_name).send_keys(pincode)

    def click_save_quote(self):
        self.driver.find_element_by_xpath(self.save_quote_button_xpath).click()

    def download_proposal(self):
        self.driver.find_element_by_xpath(self.proposal_download_link_xpath).click()

    def click_submit(self):
        self.driver.find_element_by_xpath(self.submit_button_xpath).click()

    def click_yes_on_final_submit(self):
        self.driver.find_element_by_xpath(self.final_submit_option_yes_xpath).click()

    def click_no_on_final_submit(self):
        self.driver.find_element_by_xpath(self.final_submit_option_no_xpath).click()

    def select_value_from_payment_mode(self, mode):
        self.driver.find_element_by_xpath(self.payment_mode_dropdown_xpath).click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//label[text()="Payment Mode"]/following::span[contains(text(), "' + mode + '")]').click()

    def click_proceed_to_pay(self):
        self.driver.find_element_by_xpath(self.proceed_to_pay_button_xpath).click()

    def get_premium(self):
        return self.driver.find_element_by_xpath(self.total_payable_amt_footer_label_xpath).text

    def get_quote_number(self):
        return self.driver.find_element_by_xpath(self.quote_number_label_xpath).text