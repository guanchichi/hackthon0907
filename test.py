from flask import Flask
from flask_mysqldb import MySQL

def init_db(app):
    mysql = MySQL(app)
    print("Database initialized.")
    return mysql

def test_db_connection(app, mysql):
    with app.app_context():
        try:
            if mysql.connection is None:
                raise ValueError("MySQL connection is not initialized.")
            cur = mysql.connection.cursor()
            cur.execute("SELECT 1")
            cur.fetchone()  # Fetch the result to clear the result set
            print("Database connection successful.")
            cur.close()
        except Exception as e:
            print(f"Database connection error: {e}")

# Initialize Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'chichi77'
app.config['MYSQL_DB'] = 'hackpussython'

# Initialize database
mysql = init_db(app)

# Test database connection
test_db_connection(app, mysql)
