from flask import Flask, request, jsonify
import re
import os
import urllib
import json

try:
    import tracepointdebug
    tracepointdebug.start()
except ImportError as e:
    pass

app = Flask(__name__)


def send_request(endpoint_url, data):
    endpoint = f"{endpoint_url}/calculate"
    req = urllib.request.Request(endpoint)
    data_as_bytes = data.encode('utf-8')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    response = urllib.request.urlopen(req, data_as_bytes)
    return response.read()

def parse_task(task_str):
    pattern=r"(add|subtract|multiply|divide) (\d+) (by|and|from) (\d+)"
    try:
        (operator, X, word, Y) = re.search(pattern, task_str).groups()
        if operator == 'add':
            return {"x":X, "y":Y, "op": "+" }, True
        elif operator == "subtract":
            return {"x":Y, "y":X, "op": "-" }, True # Since the task says subtracting num1 from num2 hence reversing the order
        elif operator == "multiply":    
            return {"x":X, "y":Y, "op": "*" }, True
        elif operator == "divide":    
            return {"x":X, "y":Y, "op": "/" }, True
        else:
            return f"Unknown operator {operator} found.", False
    except:
        return f"Error while parsing input '{task_str}'.", False


@app.get("/health")
def get_health():
    return "This is the health endpoint."

@app.post("/calculate")
def perform_calculation():
    endpoint=os.environ.get('BACKEND_SERVICE_URL')
    if request.is_json:
        reqeust_json = request.get_json()
        task_str = reqeust_json['task']
        parsed_request, parse_result = parse_task(task_str.lower())
        if parse_result:
            return send_request(endpoint, json.dumps(parsed_request)), 200
        else:
            return parsed_request, 500
    return {"error": "Request must be JSON"}, 415


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)