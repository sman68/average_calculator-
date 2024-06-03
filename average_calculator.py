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

def calculate_period_average(period_type):
    """Generic function to calculate averages for a given period."""
    full_date_string = '%Y-%m-%d %H:%M:%S'
    day_string = '%Y-%m-%d'
    month_string = '%Y-%m'
    data = request.get_json()
    print(f"Received data for {period_type} average calculation: {data}")
    if not data or 'data' not in data:
        return jsonify({'error': 'Data is missing'}), 400

    try:
        period_funcs = {
            'daily': lambda date: date.strftime(day_string),
            'weekly': lambda date: (date - timedelta(days=date.weekday())).strftime(day_string),
            'monthly': lambda date: date.strftime(month_string)
        }
        entries = [{'date': datetime.strptime(entry['date'], full_date_string), 'amount': entry['amount']} for entry in data['data']]
        period_data = group_by_period(entries, period_funcs[period_type])
        period_average = calculate_average(period_data)
        print(f"Calculated {period_type} averages: {period_average}")
        return jsonify({'average': period_average}), 200
    except (TypeError, ValueError) as e:
        print(f"Error processing data: {e}")
        return jsonify({'error': 'Invalid data provided'}), 400

@app.route('/average/<period_type>', methods=['POST'])
def calculate_average_for_period(period_type):
    accepted_period_types = ['daily', 'weekly', 'monthly']
    if period_type not in accepted_period_types:
        return jsonify({'error': 'Invalid period type'}), 400
    return calculate_period_average(period_type)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True, port=5004)
