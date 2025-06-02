from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-data')
def get_data():
    return render_template('get_data.html')

@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/submitteddata')
def submitteddata():
    return render_template('submitteddata.html')

@app.route('/data')
def data():
    return render_template('data.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
