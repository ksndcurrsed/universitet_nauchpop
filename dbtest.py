import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('имя_вашей_базы_данных.sqlite')
cur = conn.cursor()
cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
        )
        ''')

# Запрос к базе данных для получения логина и пароля по chat_id
chat_id_to_check = 123456789  # Замените на ваше chat_id
cur.execute("SELECT username, password FROM users WHERE chat_id = ?", (chat_id_to_check,))
result = cur.fetchone()

if result:
    username, password = result
    print(f"Логин: {username}, Пароль: {password}")
else:
    print("Запись с таким chat_id не существует.")

