
import psycopg2

conn = psycopg2.connect(dbname='database', user='db_user', 
                        password='mypassword', host='localhost')
cursor = conn.cursor()

# создадим структуру БД

def create_database_structure():
    conn = psycopg2.connect(dbname="your_dbname", user="your_username", password="your_password", host="your_host")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE clients (
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL
        );
    ''')
    cur.execute('''
        CREATE TABLE phones (
            phone_id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(client_id),
            phone_number VARCHAR(20) NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

# создадим функцию для добавления нового клиента
    
def add_new_client(first_name, last_name, email):
    conn = psycopg2.connect(dbname="your_dbname", user="your_username", password="your_password", host="your_host")
    cur = conn.cursor()
    cur.execute("INSERT INTO clients (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING client_id;", 
                (first_name, last_name, email))
    client_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return client_id

# создадим функцию для добавления телефона для существующего клиента

def add_phone_for_client(client_id, phone_number):
    conn = psycopg2.connect(dbname="your_dbname", user="your_username", password="your_password", host="your_host")
    cur = conn.cursor()
    cur.execute("INSERT INTO phones (client_id, phone_number) VALUES (%s, %s);", (client_id, phone_number))
    conn.commit()
    conn.close()

# создадим функцию, возвращающую информацию о клиенте
    
def get_client_info(client_id):
    conn = psycopg2.connect(dbname="your_dbname", user="your_username", password="your_password", host="your_host")
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients WHERE client_id = %s;", (client_id,))
    client_info = cur.fetchone()
    conn.close()
    return client_info

# создадим функцию для получения всех телефонов клиента по его id

def get_client_phones(client_id):
    conn = psycopg2.connect(dbname="your_dbname", user="your_username", password="your_password", host="your_host")
    cur = conn.cursor()
    cur.execute("SELECT phone_number FROM phones WHERE client_id = %s;", (client_id,))
    phones = cur.fetchall()
    conn.close()
    return phones

# создадим функцию для обновления информации о клиенте

def update_client_info(client_id, **kwargs):
    conn = psycopg2.connect(dbname="your_dbname", user="your_username", password="your_password", host="your_host")
    cur = conn.cursor()
    
    update_query = "UPDATE clients SET "
    update_values = []
    for key, value in kwargs.items():
        update_query += f"{key} = %s, "
        update_values.append(value)
    update_query = update_query.rstrip(", ")  # Удаляем лишнюю запятую и пробел в конце строки
    update_query += f" WHERE client_id = %s;"
    update_values.append(client_id)

    cur.execute(update_query, tuple(update_values))
    conn.commit()
    conn.close()


# создадим функцию, позволяющую удалить существующего клиента
    
def delete_client(client_id):
    conn = psycopg2.connect(dbname="your_dbname", user="your_username", password="your_password", host="your_host")
    cur = conn.cursor()

    # Проверяем, есть ли у клиента привязанные номера телефонов
    cur.execute("SELECT COUNT(*) FROM phone_numbers WHERE client_id = %s", (client_id,))
    phone_count = cur.fetchone()[0]

    if phone_count > 0:
        print("Невозможно удалить клиента, так как у него есть привязанные номера телефонов.")
    else:
        cur.execute("DELETE FROM clients WHERE client_id = %s", (client_id,))
        conn.commit()
        print("Клиент успешно удален.")

    conn.close()

# создадим функцию, позволяющую найти клиента по его данным
    
def search_clients(**kwargs):
    conn = psycopg2.connect(dbname="your_dbname", user="your_username", password="your_password", host="your_host")
    cur = conn.cursor()

    # Формируем список полей для поиска
    search_fields = []
    search_values = []
    for key, value in kwargs.items():
        if value:  # Проверяем, было ли предоставлено значение для поля
            search_fields.append(key + " = %s")  # Добавляем поле в список для поиска
            search_values.append(value)  # Добавляем значение в список для параметризованного запроса

    # Формируем SQL-запрос
    query = "SELECT * FROM clients"
    if search_fields:  # Если были предоставлены параметры для поиска
        query += " WHERE " + " AND ".join(search_fields)  # Добавляем условие WHERE

    cur.execute(query, search_values)  # Выполняем запрос
    result = cur.fetchall()  # Получаем результаты поиска

    conn.close()  # Закрываем соединение
    return result  # Возвращаем результаты поиска

if __name__ == "__main__":
    conn = psycopg2.connect(dbname='database', user='db_user', 
                        password='mypassword', host='localhost')
    create_database_structure(conn)
    conn.close()
