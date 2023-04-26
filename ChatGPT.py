import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import yaml

class ChatGPT:

    def __init__(self):
        self.driver = uc.Chrome()
        with open('config.yaml', 'r') as f:
            self.settings = yaml.load(f, Loader=yaml.CLoader)

    def chat(self, text):
        self.send_chat(text)
        return self.get_response()

    def send_chat(self, text):
        wait = WebDriverWait(self.driver, 15)
        start_chat = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div[1]/main/div[2]/form/div/div[2]/textarea')))
        start_chat.click()
        start_chat.send_keys(text)
        start_chat.send_keys(Keys.ENTER)

    def get_response(self):
        xpath = '//*[@id="__next"]/div/div[1]/main/div[1]/div/div/div/div[last()-1]/div/div[2]/div[1]/div/div/p'
        response = None

        while response is None:
            check = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div[1]/main/div[2]/form/div/div[1]/button')
            if len(check) > 0:
                response = self.driver.find_element(By.XPATH, xpath).text
            time.sleep(2)

        return response

    def new_session(self):
        wait = WebDriverWait(self.driver, 15)
        
        new_session = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div[2]/div/div/nav/a[1]')))
        new_session.click()

        start_chat = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div[1]/main/div[2]/form/div/div[2]/textarea')))
        start_chat.click()

    def close_session(self):
        wait = WebDriverWait(self.driver, 15)
        close_session = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div[2]/div/div/nav/a[2]')))
        close_session.click()
        self.driver.quit()

    def start_session(self):
        self.driver.get('https://chat.openai.com/chat')
        wait = WebDriverWait(self.driver, 15)

        go_to_login = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div/div[4]/button[1]')))
        go_to_login.click()

        email = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
        time.sleep(0.5)
        email.send_keys(self.settings['chatgpt']['credentials']['email'])

        password = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
        time.sleep(0.5)
        password.send_keys(self.settings['chatgpt']['credentials']['password'])
        
        login = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/div/div/div/form/div[2]/button')))
        login.click()
        time.sleep(1)

        next_prompt = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[4]/button[2]')))
        next_prompt.click()
        next_prompt = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[4]/button[2]')))
        next_prompt.click()
        next_prompt = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[4]/button[2]')))
        next_prompt.click()


if __name__ == '__main__':
    chat = ChatGPT()
    chat.start_session()
    time.sleep(5)

    with open('settings.yaml', 'r') as f:
        settings = yaml.load(f, Loader=yaml.CLoader)
        
    chat.send_chat(settings['start_chat'])
    time.sleep(5)

    chat.close_session()
    