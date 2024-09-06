from flask_mysqldb import MySQL

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
            c.price AS price
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
                'price': record[2]
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
                Area AS area
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
                Area AS area
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
                'area': record[7]
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
            AND DATE(t.StartTime) = %s;
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

