
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask import Flask


mysql: MySQL = None
app: Flask = None


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'otageri'
    app.config['MYSQL_PASSWORD'] = '784512963'
    # Optionally specify the database name if it exists
    # app.config['MYSQL_DB'] = 'navigated_learning'

    global mysql
    mysql = MySQL(app)

    return app, mysql


def is_database_present(mysql):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SHOW DATABASES LIKE 'navigated_learning'")
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    except Exception as e:
        print(f"Error checking database presence: {e}")
        return False


def create_database(mysql):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS navigated_learning")
        cursor.close()
        print("Database created")
    except Exception as e:
        print(f"Error creating database: {e}")


def create_tables(mysql):
    try:
        cursor = mysql.connection.cursor()
        # Add SQL statements to create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS example_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
        """)

        cursor.close()
        print("Tables created or already exist.")
    except Exception as e:
        print(f"Error creating tables: {e}")


def main():
    global app, mysql
    app, mysql = create_app()

    with app.app_context():
        if is_database_present(mysql):
            print("Database is present.")
            app.config['MYSQL_DB'] = 'navigated_learning'
        else:
            print("Database is not present.")
            create_database(mysql)
            app.config['MYSQL_DB'] = 'navigated_learning'
            create_tables(mysql)


main()
