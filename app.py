from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from server.controller import get_history
from server.controller import get_companies
from server.controller import check_availability
from server.controller import showPeopleInfo

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
CORS(app)

# MySQL database configuration
# MySQL database configuration
app.config['MYSQL_HOST'] = '0.tcp.jp.ngrok.io'  # Ngrok host
app.config['MYSQL_PORT'] = 10459  # Ngrok port
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'chichi77'
app.config['MYSQL_DB'] = 'hackpussython'

# Initialize database
mysql = init_db(app)

# Test database connection
test_db_connection(app, mysql)

# Initialize routes
@app.route('/')
def home():
    return "Welcome to HackPussyThon"

@app.route('/search_history', methods=['POST'])
def history():
    return get_history(mysql)

@app.route('/search_companies', methods=['POST'])
def companies():
    return get_companies(mysql)

@app.route('/select_date', methods=["POST"])
def check_availability_route():
    return check_availability(mysql)

@app.route('/show_people_info', methods=["POST"])
def show_people_info():
    return showPeopleInfo(mysql)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
