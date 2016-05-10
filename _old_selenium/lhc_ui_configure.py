import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

BASE_URL = 'https://lotus-23.lotus.hpdd.lab.intel.com'
HOSTS = [
    'lotus-24',
    'lotus-25',
    'lotus-26',
    'lotus-27'
]

# BASE_URL = 'https://127.0.0.1:8000'
# HOSTS = ['lotus-32vm6']

ACTION_REGISTER_DELAY = 0.2
LOGIN_SCRIPT_DELAY = 5
DEFAULT_LOAD_DELAY = 60
PROFILE_REGISTER_DELAY = 300
LONG_INSTALL_DELAY = 1200

ADD_XPATH = '/html/body/div[1]/div/div/div/div/div/button'
PROCEED_XPATH = '/html/body/div[1]/div/div/step-container/div[3]/override-button/span/span/div/button[1]'
CLOSE_XPATH = '/html/body/div[1]/div/div/div[3]/button'

LOGIN_SCRIPT = """get = angular.element('body').injector().get;
sessionModel = get('SessionModel');
sessionModel.login('admin', 'lustre')
  .$promise
  .then((s) => {
    s.user.accepted_eula = true;
    return s.user.$update();
  })
  .then((s) => {
    window.location = window.location
  });"""


class LHCAutoSetup(object):
    """Manage automated adding of nodes on manager"""

    def __init__(self):
        chromedriver = "./chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)
        self.wait = WebDriverWait(self.driver, DEFAULT_LOAD_DELAY)

    def getel(self, text):
        return self.driver.find_element(By.PARTIAL_LINK_TEXT, text)

    def getelx(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)

    def waitdash(self):
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Dashboard')))

    def waitxpath(self, xpath):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def main(self):
        self.driver.get(BASE_URL)

        self.waitdash()
        if self.getel('Login').is_displayed():
            self.driver.execute_script(LOGIN_SCRIPT)

        time.sleep(LOGIN_SCRIPT_DELAY)

        self.waitdash()
        assert self.getel('Logout').is_displayed(), 'Logon script failed'

        # Add servers
        for host in HOSTS:

            self.driver.get(BASE_URL + '/ui/configure/server')

            # add host
            self.waitdash()
            self.waitxpath(ADD_XPATH).click()

            # host connectivity check
            element = self.wait.until(EC.element_to_be_clickable((By.NAME, 'pdsh')))
            element.click()
            element.send_keys(host)
            time.sleep(ACTION_REGISTER_DELAY)
            self.getelx('/html/body/div[1]/div/div/step-container/div[3]/button').click()

            # deploy agent
            self.waitxpath(PROCEED_XPATH).click()
            try:
                self.waitxpath(CLOSE_XPATH).click()  # close button
            except TimeoutException:
                pass

            # setup agent and install packages
            time.sleep(ACTION_REGISTER_DELAY)
            self.wait = WebDriverWait(self.driver, PROFILE_REGISTER_DELAY)
            self.waitxpath(PROCEED_XPATH).click()
            self.waitxpath(CLOSE_XPATH).click()

            # reset wait time
            self.wait = WebDriverWait(self.driver, DEFAULT_LOAD_DELAY)

        #driver.quit()

if __name__ == '__main__':
    LHCAutoSetup().main()
