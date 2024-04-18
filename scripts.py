import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = 'https://org.fa.ru/'

class univer:
    def __init__(self, course: str):
        self.course = course
        self.url = url
    
    def schedule(self, course):
        linkresp = 'http://www.fa.ru/fil/kaluga/student/Documents/%d0%a0%d0%b0%d1%81%d0%bf%d0%b8%d1%81%d0%b0%d0%bd%d0%b8%d0%b5/'+ course + '%20%d0%ba%d1%83%d1%80%d1%81.pdf'
        response = requests.get(linkresp)
        with open('расписание.pdf', 'wb') as file:
            file.write(response.content)
        return 'сделано'
    
    def __setup(self):
        o = Options()
        o.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=o)
        self.__login()

    def __login(self):
        self.driver.get(url)
        self.driver.find_element(By.NAME, 'USER_LOGIN').send_keys('100DOT33SL230303')
        self.driver.find_element(By.NAME, 'USER_PASSWORD').send_keys('FnOa3304')
        self.driver.find_element(By.CLASS_NAME, 'login-btn').click()

    def parsing(self):
        self.__setup()
        self.driver.get('https://org.fa.ru/app/profile;mode=edu/marks')
        return self.driver.find_element(By.CLASS_NAME, 'subject').text()
