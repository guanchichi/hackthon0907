from flask import request, jsonify
from server.model import get_user_history
from server.model import get_companies_by_area
from server.model import get_available_times
from server.model import get_booking_details

def get_history(mysql):
    try:
        data = request.get_json()
        user_id = data.get("ID")
        
        # If ID is missing, return an error
        if not user_id:
            return jsonify({"status": "error", "message": "缺少ID"}), 200
        
        # Query the user's history
        history = get_user_history(mysql, user_id)
        
        # If no history is found, return an error
        if history is None:
            return jsonify({"status": "error", "message": "查無ID"}), 200
        
        # Return success result with history
        return jsonify({"status": "success", "history": history}), 200
    
    except Exception as e:
        # Handle any other exceptions
        print(f"Error in get_history: {e}")
        return jsonify({"status": "error", "message": "Server error"}), 200


def get_companies(mysql):
    try:
        data = request.get_json()
        area = data.get("area")
        
        # Get companies by area
        companies = get_companies_by_area(mysql, area)
        
        # If no companies are found, return an error
        if companies is None or companies == []:
            return jsonify({"status": "error", "message": "查無資料"}), 404
        
        # Return success result with companies data
        return jsonify({
            "status": "success",
            "data": companies
        }), 200

    except Exception as e:
        # Handle any other exceptions
        print(f"Error in get_companies: {e}")
        return jsonify({"status": "error", "message": "Server error"}), 200


def check_availability(mysql):
    try:
        # Get JSON request data
        req_data = request.get_json()
        location = req_data.get('location')
        date = req_data.get('date')
        
        # Validate request parameters
        if not location or not date:
            return jsonify({"status": "error", "message": "Invalid parameters"}), 200
        
        # Get available times from model
        available_times = get_available_times(mysql, location, date)
        
        if available_times is None or len(available_times) == 0:
            # No available times found for the location and date
            return jsonify({"status": "error", "message": "查無日期"}), 200
        
        # Build the response with available times
        response = {
            "status": "success",
            "location": location,
            "date": date,
            "time": [
                {
                    "IsBooked": time_record['IsBooked'],
                    "StartTime": time_record['StartTime'],
                    "EndTime": time_record['EndTime']
                }
                for time_record in available_times
            ]
        }
        
        # Return the response
        return jsonify(response), 200
    
    except Exception as e:
        # Handle any other exceptions
        print(f"Error in check_availability: {e}")
        return jsonify({"status": "error", "message": "Server error"}), 200


def showPeopleInfo(mysql):
    try:
        req_data = request.get_json()
        location = req_data.get('location')
        date = req_data.get('date')
        start_time = req_data.get('time')

        if not location or not date or not start_time:
            return jsonify({"status": "error", "message": "Invalid parameters"}), 200
        
        booking_details = get_booking_details(mysql, location, date, start_time)

        if booking_details is None:
            return jsonify({"status": "error", "message": "查無時間"}), 200
        
        response = {
            "status": "success",
            "date": booking_details['date'],
            "time": booking_details['start_time'],
            "people": {
                "name": booking_details['name'],
                "phone": booking_details['phone'],
                "ID": booking_details['ID'],
                "mail": booking_details['mail']
            }
        }

        return jsonify(response), 200
    
    except Exception as e:
        # Handle any other exceptions
        print(f"Error in showPeopleInfo: {e}")
        return jsonify({"status": "error", "message": "Server error"}), 200
