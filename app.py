from flask import Flask, send_file, request, jsonify
import requests
import boto3
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=["http://vamsi-loadbalancer-1451045427.ap-south-1.elb.amazonaws.com:8080"])
# Backend internal load balancer URL
BACKEND_URL = "http://internal-instance-ll-rr-1942256296.ap-south-1.elb.amazonaws.com:8080"

# Hardcoded SQS setup (Update your values here)
SQS_QUEUE_URL = "https://sqs.ap-south-1.amazonaws.com/209561933103/capstone-1595"  # Replace with your actual Queue URL
sqs_client = boto3.client('sqs', region_name='ap-south-1')

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/get_data')
def get_data():
    return send_file('get_data.html')

@app.route('/delete')
def delete():
    return send_file('delete.html')

@app.route('/submitteddata')
def submitted():
    return send_file('submitteddata.html')

@app.route('/data')
def data():
    return send_file('data.html')

# Proxy /submit to backend + SQS push
@app.route('/submit', methods=['POST'])
def proxy_submit():
    form_data = request.form.to_dict()
    try:
        # Step 1: Send form data to the backend
        response = requests.post(f"{BACKEND_URL}/submit", data=form_data)
        backend_response = response.json()

        # Step 2: Push the same data to SQS for Lambda → SES
        email = form_data.get("email")
        if email:
            message = {
                "email": email,
                "form_data": form_data
            }
            sqs_client.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=json.dumps(message)
            )

        return jsonify(backend_response), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Proxy /get-data/<id> to backend
@app.route('/get-data/<int:user_id>', methods=['GET'])
def proxy_get_data(user_id):
    try:
        response = requests.get(f"{BACKEND_URL}/get-data/{user_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Proxy /delete/<id> to backend
@app.route('/delete/<int:user_id>', methods=['DELETE'])
def proxy_delete(user_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/delete/{user_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
