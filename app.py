import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the Excel file using an environment variable
excel_file = os.getenv('EXCEL_FILE', 'VOTE.xlsx')
data = pd.read_excel(excel_file)

@app.route('/get-data', methods=['POST'])
def get_data():
    try:
        user_input = request.json['query']
        data['HRMS'] = data['HRMS'].astype(str)
        data['IPAS'] = data['IPAS'].astype(str)

        result = data[(data['HRMS'] == user_input) | (data['IPAS'] == user_input)]

        if result.empty:
            return jsonify({"message": "No data found"}), 404
        return jsonify(result.to_dict(orient='records')), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
