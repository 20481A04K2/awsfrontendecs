import boto3
import json
from flask import Flask, send_file, request, jsonify
import requests

app = Flask(__name__)

# Backend internal load balancer URL
BACKEND_URL = "http://internal-instance-ll-rr-1942256296.ap-south-1.elb.amazonaws.com:8080"

#  SQS configuration
SQS_QUEUE_URL = 'https://sqs.ap-south-1.amazonaws.com/209561933103/capstone-1595'
AWS_REGION = 'ap-south-1'

sqs_client = boto3.client('sqs', region_name=AWS_REGION)

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

#  Proxy /submit to backend and push to SQS
@app.route('/submit', methods=['POST'])
def proxy_submit():
    form_data = request.form.to_dict()
    try:
        # Forward to backend
        response = requests.post(f"{BACKEND_URL}/submit", data=form_data)

        # Push message to SQS
        email = form_data.get("email")
        if email:
            sqs_client.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=json.dumps({
                    "email": email,
                    "form_data": form_data
                })
            )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-data/<int:user_id>', methods=['GET'])
def proxy_get_data(user_id):
    try:
        response = requests.get(f"{BACKEND_URL}/get-data/{user_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete/<int:user_id>', methods=['DELETE'])
def proxy_delete(user_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/delete/{user_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
