from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import statistics

app = Flask(__name__)

def parse_data(data):
    """Parses the input data and returns a list of values."""
    # Extract and return the 'amount' field from each entry in the data
    return [entry['amount'] for entry in data]

def group_by_period(data, period_func):
    """Groups data by a specified period (e.g., daily, weekly, monthly)."""
    grouped_data = {}
    for entry in data:
        # Determine the period for the current entry using the provided period function
        period = period_func(entry['date'])
        # Initialize the period key if not already present
        if period not in grouped_data:
            grouped_data[period] = []
        # Append the entry's amount to the corresponding period group
        grouped_data[period].append(entry['amount'])
    return grouped_data

def calculate_average(grouped_data):
    """Calculates the average for each group of data."""
    # Calculate and return the mean for each period group
    return {period: statistics.mean(amounts) for period, amounts in grouped_data.items()}

@app.route('/average/daily', methods=['POST'])
def calculate_daily_average():
    """Calculates the daily average of the provided data."""
    data = request.get_json()
    print(f"Received data for daily average calculation: {data}")
    if not data or 'data' not in data:
        return jsonify({'error': 'Data is missing'}), 400
    try:
        # Parse the dates and amounts from the input data
        entries = [{'date': datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S'), 'amount': entry['amount']} for entry in data['data']]
        # Group the data by day
        daily_data = group_by_period(entries, lambda date: date.strftime('%Y-%m-%d'))
        # Calculate the average for each day
        daily_average = calculate_average(daily_data)
        print(f"Calculated daily averages: {daily_average}")
        return jsonify({'average': daily_average}), 200
    except (TypeError, ValueError) as e:
        print(f"Error processing data: {e}")
        return jsonify({'error': 'Invalid data provided'}), 400

@app.route('/average/weekly', methods=['POST'])
def calculate_weekly_average():
    """Calculates the weekly average of the provided data."""
    data = request.get_json()
    print(f"Received data for weekly average calculation: {data}")
    if not data or 'data' not in data:
        return jsonify({'error': 'Data is missing'}), 400
    try:
        # Parse the dates and amounts from the input data
        entries = [{'date': datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S'), 'amount': entry['amount']} for entry in data['data']]
        # Group the data by week (starting from Monday)
        weekly_data = group_by_period(entries, lambda date: (date - timedelta(days=date.weekday())).strftime('%Y-%m-%d'))
        # Calculate the average for each week
        weekly_average = calculate_average(weekly_data)
        print(f"Calculated weekly averages: {weekly_average}")
        return jsonify({'average': weekly_average}), 200
    except (TypeError, ValueError) as e:
        print(f"Error processing data: {e}")
        return jsonify({'error': 'Invalid data provided'}), 400

@app.route('/average/monthly', methods=['POST'])
def calculate_monthly_average():
    """Calculates the monthly average of the provided data."""
    data = request.get_json()
    print(f"Received data for monthly average calculation: {data}")
    if not data or 'data' not in data:
        return jsonify({'error': 'Data is missing'}), 400
    try:
        # Parse the dates and amounts from the input data
        entries = [{'date': datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S'), 'amount': entry['amount']} for entry in data['data']]
        # Group the data by month
        monthly_data = group_by_period(entries, lambda date: date.strftime('%Y-%m'))
        # Calculate the average for each month
        monthly_average = calculate_average(monthly_data)
        print(f"Calculated monthly averages: {monthly_average}")
        return jsonify({'average': monthly_average}), 200
    except (TypeError, ValueError) as e:
        print(f"Error processing data: {e}")
        return jsonify({'error': 'Invalid data provided'}), 400

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
