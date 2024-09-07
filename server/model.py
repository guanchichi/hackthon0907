from flask_mysqldb import MySQL
from PIL import Image
import base64
from io import BytesIO
def extract_portion(input_string):
    # 找到第一個冒號的位置
    colon_index = input_string.find(':')

    start = colon_index - 2
    end = start + 3  # 包括冒號和後面兩個字符

    output = input_string[start:end + 2]
    return output

def encodeimage(imagepath):
    with Image.open(imagepath) as image:
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()

def init_db(app):
    mysql = MySQL()
    mysql.init_app(app)
    print("Database initialized.")
    return mysql

def get_user_history(mysql, user_id):
    # SQL query for user history
    query = """
        SELECT 
            c.Location AS location, 
            t.StartTime AS time, 
            c.price AS price,
            t.IsEntry AS is_entry
        FROM 
            booking b
        JOIN 
            time t ON b.Address = t.Address
        JOIN 
            company c ON b.Address = c.Address
        WHERE 
            b.ID = %s AND t.userID = %s
        ORDER BY 
            t.StartTime;
    """
    
    # Get database connection and execute query
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (user_id, user_id))
        history_records = cur.fetchall()
        cur.close()
    
        # If no records are found, return None
        if not history_records:
            print(f"No history found for user ID: {user_id}")  # Add debug log
            return None
    
        # Convert results to a list of dictionaries
        history = [
            {
                'location': record[0],
                'time': record[1],
                'price': record[2],
                'isEntry': record[3]
            }
            for record in history_records
        ]
    
        return history
    except Exception as e:
        print(f"Error fetching user history: {e}")
        return None



def get_companies_by_area(mysql, area):
    # SQL query for companies based on area
    if area == "全部":
        query = """
            SELECT 
                Location AS location,
                People AS people,
                Content AS content,
                Address AS address,
                Contact AS contact,
                Phone AS phone,
                IsOpen AS isOpen,
                Area AS area,
                ImagePath AS imagepath
            FROM 
                company;
        """
    else:
        query = """
            SELECT 
                Location AS location,
                People AS people,
                Content AS content,
                Address AS address,
                Contact AS contact,
                Phone AS phone,
                IsOpen AS isOpen,
                Area AS area,
                ImagePath AS imagepath
            FROM 
                company
            WHERE 
                Area = %s;
        """
    
    # Get database connection and execute query
    try:
        cur = mysql.connection.cursor()
        if area == "全部":
            cur.execute(query)
        else:
            cur.execute(query, (area,))
        
        company_records = cur.fetchall()
        cur.close()
    
        # If no records are found, return an empty list
        if not company_records:
            print(f"No companies found for area: {area}")  # Add debug log
            return []
    
        # Convert results to a list of dictionaries
        companies = [
            {
                'location': record[0],
                'people': record[1],
                'content': record[2],
                'address': record[3],
                'contact': record[4],
                'phone': record[5],
                'isOpen': record[6],
                'area': record[7],
                'image': encodeimage(record[8])
            }
            for record in company_records
        ]
    
        return companies
    except Exception as e:
        print(f"Error fetching companies: {e}")
        return []



def get_available_times(mysql, location, date):
    # SQL query to retrieve available times based on location and date
    query = """
        SELECT 
            t.StartTime, 
            t.EndTime, 
            t.IsBooked, 
            c.Location, 
            DATE(t.StartTime) AS Date
        FROM 
            time t
        JOIN 
            company c ON t.Address = c.Address
        WHERE 
            c.Location = %s
            AND TIME(t.StartTime) = %s;
    """
    
    # Get database connection and execute query
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (location, date))
        time_records = cur.fetchall()
        cur.close()
        
        # If no records are found, return None
        if not time_records:
            print(f"No available times found for location: {location} and date: {date}")  # Add debug log
            return None
        
        # Convert results to a list of dictionaries
        available_times = [
            {
                'StartTime': record[0],
                'EndTime': record[1],
                'IsBooked': bool(record[2])
                # 'Location': record[3],
                # 'Date': record[4]
            }
            for record in time_records
        ]
        
        return available_times
    except Exception as e:
        print(f"Error fetching available times: {e}")
        return None

def get_booking_details(mysql, location, date, start_time):
    query = "SELECT name, phone, ID, mail FROM user ORDER BY RAND() LIMIT 1"
    
    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        booking_details = cur.fetchone()
        cur.close()
        if booking_details:
            return {
                'name': booking_details[0],
                'phone': booking_details[1],
                'ID': booking_details[2],
                'mail': booking_details[3],
                'start_time': start_time,
                'date': date,
                'location': location
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching BookingPeopleInfo: {e}")
        return None

############################################################
def get_peopleNum(mysql, date, time, user_id):
    query = """
        SELECT 
            b.people_num
        FROM 
            booking b
        JOIN 
            time t ON b.Address = t.Address
        JOIN 
            company c ON b.Address = c.Address
        WHERE 
            t.Date = %s AND t.StartTime = %s AND b.ID = %s;
    """
    
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (date, time, user_id))
        booking_record = cur.fetchone()
        cur.close()
        
        if booking_record is None:
            return None
        
        return {
            'people_num': booking_record[0]
        }
    
    except Exception as e:
        print(f"Error fetching booking details: {e}")
        return None
    

def update_time_and_insert_booking(mysql, user_id, address, date, start_time, people_num):
    update_time_query = f"""
        UPDATE time 
        SET IsBooked = 1, UserID = '{user_id}'
        WHERE Address = '{address}' AND Date = '{date}' AND StartTime = '{start_time}';
    """
    insert_booking_query = """
        INSERT INTO booking (ID, Address, PeopleNum)
        VALUES (%s, %s, %s);
    """
    get_booking_details_query = """
        SELECT EndTime, price
        FROM time t
        JOIN company c ON t.Address = c.Address
        WHERE t.Address = %s AND t.StartTime = %s;
    """
    try:
        cur = mysql.connection.cursor()
        
        # update time table
        cur.execute(update_time_query)
        mysql.connection.commit()
        
        # insert booking table
        cur.execute(insert_booking_query, (user_id, address, people_num))
        mysql.connection.commit()
        
        # get booking table
        cur.execute(get_booking_details_query, (address, start_time))
        booking_details = cur.fetchone()
        cur.close()
        
        if booking_details:
            return {
                "end_time": booking_details[0],
                "price": booking_details[1]
            }
        else:
            return None

    except Exception as e:
        print(f"Error updating time and inserting booking: {e}")
        return None

def get_address_by_location(mysql, location):
    query = """
        SELECT Address 
        FROM company 
        WHERE Location = %s;
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (location,))
        address = cur.fetchone()
        cur.close()
        return address[0] if address else None
    except Exception as e:
        print(f"Error fetching address: {e}")
        return None
    
def get_user_details(mysql, user_id):
    query = """
        SELECT Name, Phone, Mail
        FROM user
        WHERE ID = %s;
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (user_id,))
        user_details = cur.fetchone()
        cur.close()
        
        if user_details:
            return {
                "name": user_details[0],
                "phone": user_details[1],
                "mail": user_details[2]
            }
        return None

    except Exception as e:
        print(f"Error fetching user details: {e}")
        return None
    


def update_isEntryToOne_model(mysql, location):
    address = get_address_by_location(mysql, location)
    query = """
        UPDATE time 
        JOIN company ON time.Address = company.Address
        SET time.IsEntry = 1
        WHERE company.Address = %s AND time.UserID IS NOT NULL;
    """

    try:
        cur = mysql.connection.cursor()
        # update time table
        cur.execute(query, (address,))  # 確保提供正確的參數
        mysql.connection.commit()
        cur.close()

    except Exception as e:
        print(f"Error updating: {e}")