
# Microservice: Average Calculator

## Overview
This microservice calculates daily, weekly, and monthly averages of numerical data based on the provided JSON input. You can send a POST request to the appropriate endpoint, and it will return the calculated averages.

## Instructions

### Clone The Repository 

```
git clone https://github.com/sman68/CS361.git
cd CS361/Microservice_A
```

### Set Up Virtural Environment and Install Dependencies

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
### Run Programs

```
python main_program.py
```
```
python average_calculator.py
```

## How to Request Data

To request data from the microservice, make a POST request to the following URLs (or any of your choosing):

- **Daily Average**: `http://localhost:5000/average/daily`
- **Weekly Average**: `http://localhost:5000/average/weekly`
- **Monthly Average**: `http://localhost:5000/average/monthly`

### Request Format
The request body should be a JSON object with the following structure:

```json
{
    "data": [
        {
            "date": "YYYY-MM-DD HH:MM:SS",
            "amount": <int>
        },
        ...
    ]
}
```

## Example Request

```
import requests

url = 'http://localhost:5000/average/daily'
data = {
    "data": [
        {"date": "2024-05-08 14:49:01", "amount": 800},
        {"date": "2024-05-08 14:48:52", "amount": 1000}
    ]
}
response = requests.post(url, json=data)
print(response.json())
```

## How to Recieve Data

The respons from the microservice will be a JSON object containing the average numerical data for the requested period time period.

## Response Format

```
{
    "average": <float>
}
```

## Example Response

```
{
    "average": 900.0
}
```

# UML Sequence Diagram

```plaintext
+--------------------+        +-------------------------+
|    WTMainProgram   |        |   Average Calculator    |
+--------------------+        +-------------------------+
            |                             |
            |    POST /average/daily      |
            |---------------------------->|
            |                             |
            |   handle_daily_average()    |
            |                             |
            |  parse_and_validate_data()  |
            |                             |
            |      group_by_period()      |
            |                             |
            |    calculate_average()      |
            |                             |
            |         Response            |
            |<----------------------------|
            |                             |

```

## Contact
For any questions or issues, please contact Steven Pamplin at spamplin@gmail.com or pamplins@oregonstate.edu



