
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask import Flask

print("this should run only once")
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
            CREATE TABLE IF NOT EXISTS Resources (
                id INTEGER PRIMARY KEY,
                name VARCHAR(25),
                description JSON,
                keywords JSON,
                polyline JSON,
                x_coordinate DECIMAL,
                y_coordinate DECIMAL,
                course_id INTEGER,
                type INTEGER,
                embedding JSON
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Topics (
                id INTEGER PRIMARY KEY,
                name VARCHAR(250),
                description JSON,
                keywords JSON,
                polyline JSON,
                x_coordinate decimal,
                y_coordinate decimal,
                course_id INTEGER,
                embedding json
            )
        """)

        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS Learners (
                id INTEGER PRIMARY KEY,
                registered_date TIMESTAMP,
                name VARCHAR(250),
                cgpa VARCHAR(2),
                username VARCHAR(50),
                password VARCHAR(50)
            );
        """)

        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS Courses (
                id INTEGER PRIMARY KEY,
                name VARCHAR(250),
                description JSON
            );
        """)

        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS Activity (
                id INTEGER PRIMARY KEY,
                time DATETIME,
                type_id INTEGER,
                enroll_id INTEGER,
                resource_id INTEGER
            );
        """)

        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS Enrolls (
                id INTEGER PRIMARY KEY,
                learner_id INTEGER,
                course_id INTEGER,
                x_coordinate DECIMAL,
                y_coordinate DECIMAL,
                polyline JSON
            );
        """)

        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS Contribution (
                id INTEGER PRIMARY KEY,
                enroll_id INTEGER,
                submitted_on DATETIME,
                file_path VARCHAR(1024),
                description JSON,
                prev_polyline JSON,
                polyline JSON,
                x_coordinate DECIMAL,
                y_coordinate DECIMAL,
                embedding JSON
            );
        """)

        cursor.execute("""
            ALTER TABLE Enrolls
            ADD CONSTRAINT fk_enrolls_learner
            FOREIGN KEY (learner_id) REFERENCES Learners(id)
            ON DELETE CASCADE ON UPDATE CASCADE;  
        """)

        cursor.execute("""
            ALTER TABLE Topics
            ADD CONSTRAINT fk_topics_course
            FOREIGN KEY (course_id) REFERENCES Courses(id)
            ON DELETE CASCADE ON UPDATE CASCADE;  
        """)

        cursor.execute("""  
            ALTER TABLE Enrolls
            ADD CONSTRAINT fk_enrolls_course
            FOREIGN KEY (course_id) REFERENCES Courses(id)
            ON DELETE CASCADE ON UPDATE CASCADE; 
        """)

        cursor.execute("""
            ALTER TABLE Resources
            ADD CONSTRAINT fk_resource_course
            FOREIGN KEY (course_id) REFERENCES Courses(id)
            ON DELETE CASCADE ON UPDATE CASCADE;
        """)

        cursor.execute(""" 
            ALTER TABLE Activity
            ADD CONSTRAINT fk_activity_enroll
            FOREIGN KEY (enroll_id) REFERENCES Enrolls(id)
            ON DELETE CASCADE ON UPDATE CASCADE;  
        """)

        cursor.execute(""" 
            ALTER TABLE Activity
            ADD CONSTRAINT fk_activity_resource
            FOREIGN KEY (resource_id) REFERENCES Resources(id)
            ON DELETE CASCADE ON UPDATE CASCADE;  
        """)

        cursor.execute(""" 
            ALTER TABLE Contribution
            ADD CONSTRAINT fk_contribution_enroll
            FOREIGN KEY (enroll_id) REFERENCES Enrolls(id)
            ON DELETE CASCADE ON UPDATE CASCADE;  
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
            cursor = mysql.connection.cursor()
            cursor.execute("use navigated_learning")
        else:
            print("Database is not present.")
            create_database(mysql)
            app.config['MYSQL_DB'] = 'navigated_learning'
            cursor = mysql.connection.cursor()
            cursor.execute("use navigated_learning")


main()
