import sqlite3


class ProductManager:
    def __init__(self, db_name='database.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                proteins INTEGER NOT NULL,
                                fats INTEGER NOT NULL,
                                carbohydrates INTEGER NOT NULL,
                                calories INTEGER NOT NULL
                                )''')
        self.conn.commit()

    def add_product(self, name, proteins, fats, carbohydrates, calories):
        self.cursor.execute(
            '''INSERT INTO products (name, proteins, fats, carbohydrates, calories) VALUES (?, ?, ?, ?, ?)''',
            (name, proteins, fats, carbohydrates, calories))
        self.conn.commit()

    def delete_product(self, product_id):
        self.cursor.execute('''DELETE FROM products WHERE id = ?''', (product_id,))
        self.conn.commit()

    def update_product(self, product_id, new_name, new_proteins, new_fats, new_carbohydrates, new_calories):
        self.cursor.execute(
            '''UPDATE products SET name = ?, proteins = ?, fats = ?, carbohydrates = ?, calories = ? WHERE id = ?''',
            (new_name, new_proteins, new_fats, new_carbohydrates, new_calories, product_id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


class DailyProductManager:
    def __init__(self, db_name='database.db'):
        self.conn = sqlite3.connect(db_name)
        #      self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS daily_products (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                date TEXT NOT NULL,
                                product_id INTEGER NOT NULL,
                                amount INTEGER NOT NULL,
                                FOREIGN KEY (product_id) REFERENCES products(id)
                                )''')
        self.conn.commit()

    def add_daily_product(self, date, product_id, amount):
        self.cursor.execute('''INSERT INTO daily_products (date, product_id, amount) VALUES (?, ?, ?)''',
                            (date.isoformat(), product_id, amount))
        self.conn.commit()

    def delete_daily_product(self, daily_product_id):
        self.cursor.execute('''DELETE FROM daily_products WHERE id = ?''', (daily_product_id,))
        self.conn.commit()

    def update_daily_product(self, daily_product_id, new_date, new_product_id, new_amount):
        self.cursor.execute('''UPDATE daily_products SET date = ?, product_id = ?, amount = ? WHERE id = ?''',
                            (new_date.isoformat(), new_product_id, new_amount, daily_product_id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
