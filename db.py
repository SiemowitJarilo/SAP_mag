import sqlite3

def db_create():
    conn = sqlite3.connect('simple.db')
    cursor = conn.cursor()

    # Tabela customers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        post_code TEXT,
        city TEXT,
        address TEXT,
        no_building TEXT,
        phone INTEGER,
        shipping_address INTEGER,
        FOREIGN KEY (shipping_address) REFERENCES shipping_addresses (id)
    )
    ''')

    # Tabela shipping_addresses
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS shipping_addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        company_name TEXT,
        post_code TEXT,
        city TEXT,
        address TEXT,
        no_building TEXT,
        phone INTEGER
    )
    ''')

    # Tabela ordered_products
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ordered_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number INTEGER,
        shipping_date DATE,
        product TEXT,
        count INTEGER,
        customer_id INTEGER,
        employer_id INTEGER,
        informations TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers (id),
        FOREIGN KEY (employer_id) REFERENCES employers (id)
    )
    ''')

    # Tabela employers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    ''')
    conn.commit()
