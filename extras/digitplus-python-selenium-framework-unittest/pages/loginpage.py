class LoginPage():
    username_textbox_id = 'userName'
    password_textbox_id = 'password'
    login_button_xpath  = '//button[text()="Login"]'

    def __init__(self, driver):
        self.driver = driver

    def enter_username(self, username):
        self.driver.find_element_by_id(self.username_textbox_id).send_keys(username)
    
    def enter_password(self, password):
        self.driver.find_element_by_id(self.password_textbox_id).send_keys(password)
    
    def click_login(self):
        self.driver.find_element_by_xpath(self.login_button_xpath).click()