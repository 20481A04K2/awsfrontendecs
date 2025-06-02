from flask import Flask, send_file

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
