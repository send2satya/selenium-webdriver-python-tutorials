import glob
import os
import platform
import subprocess
import time
from jproperties import Properties
from selenium.webdriver.common.action_chains import ActionChains


class GenericLib:
    def get_data_from_properties(self, file_path, key):
        self.prop = Properties()

        with open(file_path, 'rb') as config_file:
            self.prop.load(config_file, 'utf-8')

        return self.prop.get(key).data
    
    def move_and_hover(self, driver, locator, value):
        action = ActionChains(driver)
        action.move_to_element(driver.find_element(locator, value)).perform()

    def move_and_click_by_offset(self, driver, locator, value, xoffset, yoffset):
        action = ActionChains(driver)
        action.move_to_element(driver.find_element(locator, value)).move_by_offset(xoffset, yoffset).click().perform()

    def scroll_to_end(self, driver):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def scroll_to_element(self, driver, element):
        driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def batch_cleanup(self):
        FILE_PATH_WINDOWS = os.getcwd() + '/batches/process_kill_windows.bat'
        FILE_PATH_UNIX    = os.getcwd() + '/batches/process_kill_unix.sh'

        # platform.system() = Linux: Linux / Mac: Darwin / Windows: Windows
        if platform.system() == 'Windows':
            subprocess.call(['cmd.exe', '/c', FILE_PATH_WINDOWS])
        else:
            if os.access(FILE_PATH_UNIX, os.X_OK):
                os.chmod(FILE_PATH_UNIX, 0o777)

            subprocess.call(['sh', '-p', FILE_PATH_UNIX])
    
    def wait_for_download_to_complete(self, download_dir, target_file_regex, max_secs_to_wait):
        secs_elapsed = 0
        while True:
            list = glob.glob(download_dir + target_file_regex)
            time.sleep(1)
            secs_elapsed += 1

            if len(list) > 0 or secs_elapsed == max_secs_to_wait:
                break

        return secs_elapsed