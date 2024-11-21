from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

# Load the Excel data
data = pd.read_excel("VOTE.xlsx")

@app.route('/get-data', methods=['POST'])
def get_data():
    try:
        # Get the input data from the request
        user_input = request.json['query']
        
        # Convert both HRMS and IPAS columns to string for comparison
        data['HRMS'] = data['HRMS'].astype(str)
        data['IPAS'] = data['IPAS'].astype(str)
        
        # Search for the input in either 'HRMS' or 'IPAS' columns
        result = data[(data['HRMS'] == user_input) | (data['IPAS'] == user_input)]
        
        if result.empty:
            return jsonify({"message": "No data found"}), 404
        return jsonify(result.to_dict(orient='records')), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
