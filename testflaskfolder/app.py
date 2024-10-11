from flask import Flask, jsonify, request
import requests
from io import BytesIO
import base64
from requestcheck.anthrocalls import request_test_query

app = Flask(__name__)

@app.route('/test', methods=['POST', 'OPTIONS'])
def test():
    # Set CORS headers for all responses
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    # Handle OPTIONS request
    if request.method == 'OPTIONS':
        return ('', 204, headers)

    # Check if the request has JSON data
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400, headers

    # Get the JSON data
    data = request.get_json()

    # Check if 'pdf_url' is in the JSON data
    if 'querytext' not in data:
        return jsonify({"error": "querytext is not set in the JSON data"}), 400, headers

    querytext = data['querytext']
    if not querytext:
        return jsonify({"error": "querytext query parameter is not set"}), 400, headers

    try:
        response = request_test_query(querytext)
        print(response)
        # Return status with processed results and monthly averages
        return jsonify({
            "status": "success"
        }), 200, headers

    except requests.RequestException as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500, headers
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500, headers
