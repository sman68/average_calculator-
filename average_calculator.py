from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import statistics

app = Flask(__name__)

def parse_data(data):
    """Parses the input data and returns a list of values."""
    return [entry['amount'] for entry in data]

def group_by_period(data, period_func):
    grouped_data = {}
    for entry in data:
        period = period_func(entry['date'])
        if period not in grouped_data:
            grouped_data[period] = []
        grouped_data[period].append(entry['amount'])
    return grouped_data

def calculate_average(grouped_data):
    return {period: statistics.mean(amounts) for period, amounts in grouped_data.items()}

@app.route('/average/daily', methods=['POST'])
def calculate_daily_average():
    data = request.get_json()
    print(f"Received data for daily average calculation: {data}")
    if not data or 'data' not in data:
        return jsonify({'error': 'Data is missing'}), 400
    try:
        entries = [{'date': datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S'), 'amount': entry['amount']} for entry in data['data']]
        daily_data = group_by_period(entries, lambda date: date.strftime('%Y-%m-%d'))
        daily_average = calculate_average(daily_data)
        print(f"Calculated daily averages: {daily_average}")
        return jsonify({'average': daily_average}), 200
    except (TypeError, ValueError) as e:
        print(f"Error processing data: {e}")
        return jsonify({'error': 'Invalid data provided'}), 400

@app.route('/average/weekly', methods=['POST'])
def calculate_weekly_average():
    data = request.get_json()
    print(f"Received data for weekly average calculation: {data}")
    if not data or 'data' not in data:
        return jsonify({'error': 'Data is missing'}), 400
    try:
        entries = [{'date': datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S'), 'amount': entry['amount']} for entry in data['data']]
        weekly_data = group_by_period(entries, lambda date: (date - timedelta(days=date.weekday())).strftime('%Y-%m-%d'))
        weekly_average = calculate_average(weekly_data)
        print(f"Calculated weekly averages: {weekly_average}")
        return jsonify({'average': weekly_average}), 200
    except (TypeError, ValueError) as e:
        print(f"Error processing data: {e}")
        return jsonify({'error': 'Invalid data provided'}), 400

@app.route('/average/monthly', methods=['POST'])
def calculate_monthly_average():
    data = request.get_json()
    print(f"Received data for monthly average calculation: {data}")
    if not data or 'data' not in data:
        return jsonify({'error': 'Data is missing'}), 400
    try:
        entries = [{'date': datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S'), 'amount': entry['amount']} for entry in data['data']]
        monthly_data = group_by_period(entries, lambda date: date.strftime('%Y-%m'))
        monthly_average = calculate_average(monthly_data)
        print(f"Calculated monthly averages: {monthly_average}")
        return jsonify({'average': monthly_average}), 200
    except (TypeError, ValueError) as e:
        print(f"Error processing data: {e}")
        return jsonify({'error': 'Invalid data provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
