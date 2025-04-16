from flask import Flask, jsonify, request, make_response
import pandas as pd
import os

app = Flask(__name__)

CSV_PATH = "k8s_failure_training_data.csv"

@app.route('/', methods=['GET'])
def home():
    # Custom header to skip ngrok browser warning
    response = make_response("✅ CSV Data API is running! Use /data (GET), /latest (GET), or /update (POST).")
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

@app.route('/data', methods=['GET'])
def get_data():
    if not os.path.exists(CSV_PATH):
        return jsonify({"error": f"CSV file '{CSV_PATH}' not found."}), 404
    try:
        df = pd.read_csv(CSV_PATH)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/latest', methods=['GET'])
def get_latest_row():
    if not os.path.exists(CSV_PATH):
        return jsonify({"error": f"CSV file '{CSV_PATH}' not found."}), 404
    try:
        df = pd.read_csv(CSV_PATH)
        if df.empty:
            return jsonify({"error": "CSV file is empty."}), 204
        latest_row = df.tail(1).to_dict(orient="records")[0]
        return jsonify(latest_row)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update', methods=['POST'])
def update_data():
    try:
        new_data = request.get_json()
        if not new_data:
            return jsonify({"error": "No data provided"}), 400

        df = pd.DataFrame(new_data)
        if not os.path.exists(CSV_PATH):
            df.to_csv(CSV_PATH, index=False)
        else:
            df_existing = pd.read_csv(CSV_PATH)
            df_combined = pd.concat([df_existing, df], ignore_index=True)
            df_combined.to_csv(CSV_PATH, index=False)

        return jsonify({"message": "✅ CSV updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3366, debug=True)
