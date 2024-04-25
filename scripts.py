import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pysqlcipher3 import dbapi2 as sqlite
import json
import time
import string
import secrets
import os

url = 'https://org.fa.ru/'

class univer:
    def __init__(self, course:str):
        self.course = course
        self.url = url
        self.conn = sqlite.connect('database.sqlite')
        self.cur = self.conn.cursor()
        self.password_rn = ''
        try:
            with open('password.txt', 'rb') as file:
                self.password_rn = file.read().decode('utf-8')
        except:
            self.password_rn = self.__passgen()
        self.db_path = 'encrypted_database.db'
        self.new_password = ''
        self.__connection()


    def __connection(self):
        with open('password.txt', 'rb') as file:
            self.password_rn = file.read().decode('utf-8')
        self.cur.execute(f'PRAGMA key="{self.password_rn}"')
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
        )
        ''')

    def __setup(self):
        o = Options()
        o.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome()

    def __login(self, username, password):
        self.driver.get(url)
        self.driver.find_element(By.NAME, 'USER_LOGIN').send_keys(username)
        self.driver.find_element(By.NAME, 'USER_PASSWORD').send_keys(password)
        self.driver.find_element(By.CLASS_NAME, 'login-btn').click()

    def __passgen(self):
        characters = string.ascii_lowercase + string.ascii_uppercase + "[];',./"
        self.password_key = ''.join(secrets.choice(characters) for _ in range(16))
        with open('password.txt', 'w') as file:
            file.write(self.password_rn)
        print(self.password_key)
        return self.password_key
    
    def __change_password(self):
        self.conn = sqlite.connect(self.db_path)
        self.conn.execute("PRAGMA key='%s'" % self.password_rn)
        self.new_password = self.__passgen()
        self.conn.execute("ATTACH DATABASE ? AS new_db KEY ?", ('temp.db', self.new_password))
        self.conn.execute("SELECT sqlcipher_export('new_db')")
        self.conn.execute("DETACH DATABASE new_db")

        self.conn.close()

        os.rename('temp.db', self.db_path)
        return self.new_password
    
    def schedule(self, course):
        linkresp = 'http://www.fa.ru/fil/kaluga/student/Documents/%d0%a0%d0%b0%d1%81%d0%bf%d0%b8%d1%81%d0%b0%d0%bd%d0%b8%d0%b5/'+ course + '%20%d0%ba%d1%83%d1%80%d1%81.pdf'
        response = requests.get(linkresp)
        with open('расписание.pdf', 'wb') as file:
            file.write(response.content)
        return 'сделано'
    

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
        self.__change_password()
        self.__connection()
        self.cur.execute("""INSERT INTO users (username, password, chat_id) VALUES (?, ?, ?)""", (login_data[0],login_data[1],chat_id))
        self.conn.commit()
        self.conn.close()
        return 'Данные сохранены ✅'
    
    def check_user_id_to_parsing(self, chat_id):
        self.__change_password()
        self.__connection()
        self.cur.execute("""SELECT * FROM users WHERE chat_id = ?""", (chat_id,))
        print(chat_id)
        result = self.cur.fetchone()
        if result is None:
            self.conn.close()
            return False
        else:
            username = result[1] 
            password = result[2]
            logdata = [username, password]
            print('Username: ' + username + '\nPassword: '+ password)
            self.conn.close()
            return logdata

