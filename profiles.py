from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from dataclasses import dataclass, field
from time import sleep
from random import uniform
from gpm import Gpm
from conf import wait_time

gpm = Gpm()


@dataclass(kw_only=True)
class Profile:
    id: str = ""

    def __post_init__(self):
        global gpm
        self.detail = gpm.get_detail_profile(profile_id=self.id)
        info = gpm.start_profile(profile_id=self.id)
        options = Options()
        options.add_argument(f"--user-data-dir={info['browser_location']}")
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option(
            "debuggerAddress", info["remote_debugging_address"]
        )
        service = Service(info["driver_path"])
        self.driver = webdriver.Chrome(service=service, options=options)
        print(f"start {self.detail['name']} on {info['remote_debugging_address']}")

    def open_url(self, url):
        self.driver.get(url)

    def wait_element(self, xpath):
        return wait_element(self.driver, xpath)

    def send_text(self, xpath, content, push_enter=False):
        return send_text(self.driver, xpath, content, push_enter)

    def set_select(self, xpath, value):
        return set_select(self.driver, xpath, value)

    def click(self, xpath):
        return click(self.driver, xpath)

    def run_script(self, script):
        return self.driver.execute_script(script)

    def send_keys(self, xpath, content):
        return self.driver.find_element(By.XPATH, xpath).send_keys(content)


def wait_element(driver, xpath, wait_time=20):
    print(f"Đang đợi {xpath} trong {wait_time} giây")
    sleep(uniform(1, 3))
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        sleep(uniform(1, 3))
        return element
    except:
        return False


def send_text(driver, xpath, content, wait_time=20, push_enter=False):
    element = wait_element(driver, xpath, wait_time)
    sleep(uniform(1, 2))
    for char in content:
        element.send_keys(char)
        sleep(uniform(0.1, 1))
    if not push_enter:
        return element
    sleep(uniform(1, 3))
    element.send_keys(Keys.RETURN)
    print(f"{xpath} >> {content}")
    sleep(uniform(1, 3))


def set_select(driver, xpath, value, wait_time=20):
    element = wait_element(driver, xpath, wait_time)
    select_element = Select(element)
    select_element.select_by_value(value)
    sleep(uniform(1, 3))


def click(driver, xpath):
    element = wait_element(driver, xpath, wait_time)
    element.click()
    sleep(uniform(1, 3))
