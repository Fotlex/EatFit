import sqlite3


class ProductManager:
    def __init__(self, db_name='database.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self) -> None:
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                proteins INTEGER NOT NULL,
                                fats INTEGER NOT NULL,
                                carbohydrates INTEGER NOT NULL,
                                calories INTEGER NOT NULL
                                )''')
        self.conn.commit()

    def add_product(self, name, proteins, fats, carbohydrates, calories) -> None:
        self.cursor.execute('''SELECT id FROM products WHERE name = ?''', (name,))
        existing_product = self.cursor.fetchone()
        if not existing_product:
            self.cursor.execute(
                '''INSERT INTO products (name, proteins, fats, carbohydrates, calories) 
                VALUES (?, ?, ?, ?, ?)''',
                (name, proteins, fats, carbohydrates, calories))
            self.conn.commit()

    def delete_product(self, product_name) -> None:
        self.cursor.execute('''DELETE FROM products WHERE name = ?''', (product_name,))
        self.conn.commit()

    def update_product(self, product_name, new_name, new_proteins, new_fats, new_carbohydrates, new_calories) -> None:
        self.cursor.execute('''SELECT id FROM products WHERE name = ?''', (new_name,))
        existing_product = self.cursor.fetchone()
        self.cursor.execute('''SELECT id FROM products WHERE name = ?''', (product_name,))
        existing_old_product = self.cursor.fetchone()
        if not existing_product or existing_old_product and existing_product[0] == existing_old_product[0]:
            self.cursor.execute(
                '''UPDATE products SET name = ?, proteins = ?, fats = ?, carbohydrates = ?, calories = ?
                 WHERE name = ?''',
                (new_name, new_proteins, new_fats, new_carbohydrates, new_calories, product_name))
            self.conn.commit()

    def get_products(self) -> list:
        self.cursor.execute("""SELECT name, proteins, fats, carbohydrates, calories FROM products""")
        products = self.cursor.fetchall()
        return products

    def get_all_names_products(self) -> list:
        self.cursor.execute("SELECT name FROM products")
        names = self.cursor.fetchall()
        return names

    def get_product_id(self, product_name):
        self.cursor.execute("SELECT id FROM products WHERE name = ?", (product_name,))
        product_id = self.cursor.fetchone()[0]
        return product_id

    def __del__(self):
        self.conn.close()


class DailyProductManager:
    def __init__(self, db_name='database.db') -> None:
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self) -> None:
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS daily_products (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                date TEXT NOT NULL,
                                product_id INTEGER NOT NULL,
                                amount INTEGER NOT NULL,
                                FOREIGN KEY (product_id) REFERENCES products(id)
                                )''')
        self.conn.commit()

    def add_daily_product(self, date, product_id, amount) -> None:
        existing_daily_product = self.get_daily_product(date, product_id)
        if existing_daily_product:
            daily_product_id = existing_daily_product[0]
            amount += existing_daily_product[1]
            self.update_daily_product(daily_product_id, date, product_id, amount)
        else:
            self.cursor.execute('''INSERT INTO daily_products (date, product_id, amount) VALUES (?, ?, ?)''',
                                (date, product_id, amount))
            self.conn.commit()

    def delete_daily_product(self, daily_product_id) -> None:
        self.cursor.execute('''DELETE FROM daily_products WHERE id = ?''', (daily_product_id,))
        self.conn.commit()

    def update_daily_product(self, daily_product_id, new_date, new_product_id, new_amount) -> None:
        if self.cursor.execute("SELECT id FROM daily_products WHERE id = ?", (daily_product_id,)).fetchone():
            self.cursor.execute('''UPDATE daily_products SET date = ?, product_id = ?, amount = ? WHERE id = ?''',
                                (new_date, new_product_id, new_amount, daily_product_id))
            self.conn.commit()

    def edit_daily_product(self, daily_product_id, new_date, new_product_id, new_amount) -> None:
        existing_daily_product = self.get_daily_product(new_date, new_product_id)
        if existing_daily_product and existing_daily_product[0] != daily_product_id:
            self.delete_daily_product(daily_product_id)
            daily_product_id = existing_daily_product[0]
            new_amount += existing_daily_product[1]

        self.update_daily_product(daily_product_id, new_date, new_product_id, new_amount)

    def get_daily_products(self, date) -> list:
        self.cursor.execute(
            """
                SELECT 
                    dp.date, 
                    p.name, 
                    dp.amount, 
                    (p.proteins * dp.amount / 100) AS proteins, 
                    (p.fats * dp.amount / 100) AS fats, 
                    (p.carbohydrates * dp.amount / 100) AS carbohydrates, 
                    (p.calories * dp.amount / 100) AS calories
                FROM daily_products dp
                JOIN products p ON dp.product_id = p.id
                WHERE dp.date = ?
            """,
            (date,)
        )
        daily_products = self.cursor.fetchall()
        return daily_products

    def get_daily_product(self, date, product_id):
        self.cursor.execute("SELECT id, amount FROM daily_products WHERE date = ? AND product_id = ?",
                            (date, product_id))
        daily_product = self.cursor.fetchone()
        return daily_product

    def __del__(self):
        self.conn.close()


class UserDataManager:
    def __init__(self, db_name='database.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_info (
                id INTEGER PRIMARY KEY,
                height INTEGER,
                weight INTEGER,
                age INTEGER
            )
        ''')
        self.cursor.execute("INSERT OR IGNORE INTO user_info (id, height, weight, age) VALUES (1, 100, 40, 10)")
        self.conn.commit()

    def update_user_info(self, height, weight, age) -> None:
        updates, values = [], []

        if height:
            updates.append("height=?")
            values.append(height)
        if weight:
            updates.append("weight=?")
            values.append(weight)
        if age:
            updates.append("age=?")
            values.append(age)

        if updates:
            update_query = "UPDATE user_info SET " + ", ".join(updates) + " WHERE id=1"
            self.cursor.execute(update_query, tuple(values))
            self.conn.commit()

    def get_user_info(self):
        self.cursor.execute('SELECT height, weight, age FROM user_info')
        result = self.cursor.fetchone()
        return result

    def __del__(self):
        self.conn.close()
