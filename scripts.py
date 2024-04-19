import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


url = 'https://org.fa.ru/'

class univer:
    def __init__(self, course: str, log, passw):
        self.course = course
        self.url = url
        self.log = log
        self.passw = passw

    
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
        self.driver.find_element(By.NAME, 'USER_LOGIN').send_keys(self.log)
        self.driver.find_element(By.NAME, 'USER_PASSWORD').send_keys(self.passw)
        self.driver.find_element(By.CLASS_NAME, 'login-btn').click()

    def parsing(self):
        self.__setup()
        self.driver.get('https://org.fa.ru/app/profile;mode=edu/marks')
        self.driver.implicitly_wait(10)
        table = self.driver.find_element(By.CSS_SELECTOR, 'table.table-hover.table-sm')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        table_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            row_data = [cell.text for cell in cells]
            table_data.append(row_data)
        json_data = json.dumps(table_data, ensure_ascii=False)
        with open('table_data.json', 'w', encoding='utf-8') as f:
            f.write(f'[{json_data[5:-1]}]')
        with open('table_data.json', 'r', encoding='utf-8') as f:
            zach = json.load(f)
        a = ''
        for i in range(0, len(zach)):
            a = a + f'✅ Дисциплина: {zach[i][0]}, вид контроля: {zach[i][1]}, результат: {zach[i][5]}, текущий контроль: {zach[i][6]}, работа в семестре: {zach[i][7]}, зачет/экзамен: {zach[i][8]}, итого: {zach[i][9]} \n \n'
        return a

