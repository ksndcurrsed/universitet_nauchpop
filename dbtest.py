from pysqlcipher3 import dbapi2 as sqlite

def change_database_password(db_path, current_password, new_password):
    conn = sqlite.connect(db_path)
    conn.execute("PRAGMA key='%s'" % current_password)

    conn.execute("ATTACH DATABASE ? AS new_db KEY ?", ('temp.db', new_password))
    conn.execute("SELECT sqlcipher_export('new_db')")
    conn.execute("DETACH DATABASE new_db")

    conn.close()

    import os
    os.rename('temp.db', db_path)

db_path = 'encrypted_database.db'
current_password = 'current_password'
new_password = 'new_password'

change_database_password(db_path, current_password, new_password)

print("Пароль базы данных успешно изменен.")
