import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import json
import time


url = 'https://org.fa.ru/'

class univer:
    def __init__(self, course:str):
        self.course = course
        self.url = url
        self.conn = sqlite3.connect('database.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
        )
        ''')


    
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

    def __login(self, username, password):
        self.driver.get(url)
        self.driver.find_element(By.NAME, 'USER_LOGIN').send_keys(username)
        self.driver.find_element(By.NAME, 'USER_PASSWORD').send_keys(password)
        self.driver.find_element(By.CLASS_NAME, 'login-btn').click()

    def parsing(self, logdata):
        self.__setup()
        self.__login(logdata[0], logdata[1])
        self.driver.get('https://org.fa.ru/app/profile;mode=edu/marks')
        time.sleep(5)
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
            book = json.load(f)
        text_output = ''
        for data in range(0, len(book)):
            for cnt in range(0,9):
                if book[data][cnt] == '':
                    book[data][cnt] = 'Пусто'
            text_output = text_output + f'✅ Дисциплина: {book[data][0]}\n Вид контроля: {book[data][1]}\n Результат: {book[data][5]}\n Текущий контроль: {book[data][6]}\n Работа в семестре: {book[data][7]}\n Зачет/экзамен: {book[data][8]}\n Итого: {book[data][9]} \n \n'
        return text_output
    
    def database_auth(self, login_data, chat_id):
        self.cur.execute("""INSERT INTO users (username, password, chat_id) VALUES (?, ?, ?)""", (login_data[0],login_data[1],chat_id))
        self.conn.commit()
        return 'Данные сохранены ✅'
    
    def check_user_id_to_parsing(self, chat_id):
        self.cur.execute("""SELECT * FROM users WHERE chat_id = ?""", (chat_id,))
        print(chat_id)
        result = self.cur.fetchone()
        if result is None:
            return False
        else:
            username = result[1] 
            password = result[2]
            logdata = [username, password]
            print('Username: ' + username + '\nPassword: '+ password)
            return logdata

