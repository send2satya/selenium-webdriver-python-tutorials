class EmployeeCompensationSuccessPage():
    policy_success_text_xpath          = '//b[contains(text(), "Successfully issued the policy")]'
    policy_no_text_xpath               = '//p[contains(text(), "Policy No")]'
    schedule_download_link_xpath       = '//b[text()="Download Policy"]'
    create_another_policy_button_xpath = "//button[text()='Create Another Policy']"

    def __init__(self, driver):
        self.driver = driver

    def visibility_of_policy_success_text(self):
        return self.driver.find_element_by_xpath(self.policy_success_text_xpath).is_displayed()

    def get_policy_number(self):
        policy_no_label = self.driver.find_element_by_xpath(self.policy_no_text_xpath).text.strip()
        policy_no = policy_no_label.split(' ')[-1]
        return policy_no

    def download_schedule(self):
        self.driver.find_element_by_xpath(self.schedule_download_link_xpath).click()

    def click_create_another_policy(self):
        self.driver.find_element_by_xpath(self.create_another_policy_button_xpath).click()