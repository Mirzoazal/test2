import logging
from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Database connection string
conn_str = (
    "Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    "DBQ=C:\\Users\\rmirz\\Desktop\\test.accdb;"   # Change this to the path of your Access DB
)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    if not data:
        logging.error("No data received")
        return jsonify({'error': 'No data received'}), 400

    submissions = data.get('content', [])
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    for submission in submissions:
        try:
            submission_id = submission.get("id")
            full_name = submission.get("answers", {}).get("1", {}).get("answer", "Unknown")
            cursor.execute("INSERT INTO Table1 (ID, fullName) VALUES (?, ?)", (submission_id, full_name))
            logging.info(f"Inserted submission: {submission_id} - {full_name}")
        except Exception as e:
            logging.error(f"Error inserting record: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'status': 'Data imported successfully'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
