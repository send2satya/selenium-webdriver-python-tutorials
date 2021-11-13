from selenium.webdriver.common.by import By

from utils.generic_lib import GenericLib


class HomePage():
    employee_comp_tab_xpath  = '//p[text()="Employee Comp"]'
    user_icon_xpath          = '//i[contains(text(), "person")]'
    logout_button_xpath      = '//a[text()="Logout"]'
    digitplus_logo_xpath     = '//img[@alt="DigitPlus"]'

    lib = GenericLib()

    def __init__(self, driver):
        self.driver = driver

    def visibility_of_user_tab(self):
        return self.driver.find_element_by_xpath(self.user_icon_xpath).is_displayed()
    
    def click_employee_comp(self):
        self.driver.find_element_by_xpath(self.employee_comp_tab_xpath).click()

    def click_on_digitplus_logo(self):
        self.driver.find_element_by_xpath(self.digitplus_logo_xpath).click()

    def logout(self):
        self.lib.move_and_hover(self.driver, By.XPATH, self.user_icon_xpath)
        self.driver.find_element_by_xpath(self.logout_button_xpath).click()