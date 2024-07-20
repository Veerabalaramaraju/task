from flask import Flask, render_template, request, jsonify
import boto3
import uuid

app = Flask(__name__)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table_name = 'testpoc'
table = dynamodb.Table(table_name)

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle adding data to DynamoDB
@app.route('/add', methods=['POST'])
def add_data():
    name = request.form['name']
    emp_id = request.form['empID']
    phone_number = request.form['phoneNumber']
    # Add data to DynamoDB
    table.put_item(
        Item={
            'id': str(uuid.uuid4()),
            'empID': emp_id,
            'name': name,
            'phoneNumber': phone_number
        }
    )

    return jsonify({"message": "Data added successfully"})

# Route to list all data from DynamoDB
@app.route('/list', methods=['GET'])
def list_data():
    response = table.scan()
    items = response['Items']
    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
