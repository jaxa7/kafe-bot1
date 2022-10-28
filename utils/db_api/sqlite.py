import sqlite3
from datetime import datetime


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            language varchar(3),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    def create_categories2(self):
        sql = """
        CREATE TABLE Category(
            id int NOT NULL PRIMARY KEY ,
            name varchar(255) NOT NULL UNIQUE       
        );
        """
        self.execute(sql, commit=True)

    def create_sub_categories2(self):
        sql = """
        CREATE TABLE SubbCategory(
            id int NOT NULL PRIMARY KEY,
            name varchar(255) NOT NULL UNIQUE,
            cat_id int NOT NULL    
        );
        """
        self.execute(sql, commit=True)

    def create_productss(self):
        sql = """
        CREATE TABLE Product(
            id int NOT NULL PRIMARY KEY,
            name varchar(255) NOT NULL UNIQUE,
            desc text NOT NULL,
            image text NOT NULL,
            price REAL NOT NULL,
            sub_cat_id INT NOT NULL
        );

        """
        self.execute(sql, commit=True)
    
    def create_cart(self):
        sql = """
        CREATE TABLE Cart(
            tg_id int NOT NULL,
            product varchar(255) NOT NULL,
            amount int NOT NULL,
            price int NOT NULL
        );

        """
        self.execute(sql, commit=True)

    def create_order(self):
        sql = """
        CREATE TABLE Orders (
            id INTEGER PRIMARY KEY,
            tg_id int NOT NULL,
            product TEXT NOT NULL,
            total_price INTEGER NOT NULL,
            phone varchar(255) NOT NULL,
            loc_lat REAL NOT NULL,
            loc_lon REAL NOT NULL,
            created datetime NOT NULL  
        );

        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, email: str = None, language: str = 'uz'):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, Name, email, language) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, email, language), commit=True)
    
    def  check_product(self, tg_id, name):
        sql = """
        SELECT * FROM Cart WHERE tg_id=? AND product=?
        """
        return self.execute(sql, (tg_id, name), fetchone=True)
    
    def add_product_cart(self, tg_id: int, product: str, amount: int, price: int):
        sql = """
        INSERT INTO Cart(tg_id, product, amount, price) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(tg_id, product, amount, price), commit=True)

    def add_order(self, tg_id: int, product: str, total_price: int, phone: int, lat: float, lon: float, create: datetime):
        sql = """
        INSERT INTO Orders (tg_id, product, total_price, phone, loc_lat, loc_lon, created) VALUES(?, ?, ?, ?, ?, ?, ?);
        """
        self.execute(sql, parameters=(tg_id, product, total_price, phone, lat, lon, create), commit=True)


    def update_product_cart(self, tg_id, name, amount):
        sql = """
        UPDATE Cart SET amount=? WHERE tg_id=? AND product=?;
        """
        self.execute(sql, (amount, tg_id, name), commit=True)        

    def delete_product_cart(self, tg_id, name):
        sql = """
        DELETE FROM Cart WHERE tg_id=? AND product=?
        """
        self.execute(sql, (tg_id, name), commit=True)
    
    def clean_cart(self, tg_id):
        sql = """
        DELETE FROM Cart WHERE tg_id=?;
        """
        self.execute(sql, (tg_id, ), commit=True)
    
    def get_cart_products(self, tg_id):
        sql = """
        SELECT * FROM Cart WHERE tg_id=?
        """
        return self.execute(sql, (tg_id, ), fetchall=True)

    def get_order(self, tg_id):
        sql = """
        SELECT * FROM Orders WHERE tg_id=?
        """
        return self.execute(sql, (tg_id, ), fetchone=True)
    
    def  get_next_order(self, tg_id, order_id):
        sql = """
        SELECT * FROM Orders WHERE tg_id=? AND id > ?;
        """
        return self.execute(sql, (tg_id, order_id), fetchone=True)
    
    def  get_prev_order(self, tg_id, order_id):
        sql = """
        SELECT * FROM Orders WHERE tg_id=? AND id < ?;
        """
        return self.execute(sql, (tg_id, order_id), fetchall=True)
    
    def  get_payment_order(self, tg_id, order_id):
        sql = """
        SELECT * FROM Orders WHERE tg_id=? AND id = ?;
        """
        return self.execute(sql, (tg_id, order_id), fetchone=True)


    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_all_categories(self):
        sql = """
        SELECT * FROM Category;
        """
        return self.execute(sql, fetchall=True)

    def select_sub_cat_id(self, name):
        sql= """SELECT * FROM Category WHERE name=?;"""
        return self.execute(sql, (name, ), fetchone=True)

    def select_all_sub_cat(self, cat_id):
        sql= """SELECT name FROM SubbCategory WHERE cat_id=?;"""
        return self.execute(sql, (cat_id, ), fetchall=True)
    
    def select_all_sub_back(self, id):
        sql= """SELECT cat_id FROM SubbCategory WHERE id=?;"""
        return self.execute(sql, (id, ), fetchone=True)
    
    def get_sub_cat_id(self, name):
        sql= """SELECT id FROM SubbCategory WHERE name=?;"""
        return self.execute(sql, (name, ), fetchone=True)

    def get_prod_info(self, name):
        sql= """SELECT * FROM Product WHERE name=?;"""
        return self.execute(sql, (name, ), fetchone=True)


    def select_all_products(self, sub_cat_id):
        sql = """SELECT name FROM Product WHERE sub_cat_id=?"""
        return self.execute(sql, (sub_cat_id, ), fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)



    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")
