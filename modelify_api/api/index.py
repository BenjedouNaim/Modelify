from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/process-csv', methods=['POST'])
def process_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        df['new_column'] = df['existing_column'] * 2

        temp_dir = tempfile.gettempdir()
        processed_file_path = os.path.join(temp_dir, 'processed_file.csv')
        df.to_csv(processed_file_path, index=False)

        return send_file(processed_file_path, mimetype='text/csv', as_attachment=True)

    return jsonify({'error': 'File is not CSV'}), 400

if __name__ == '__main__':
    app.run(debug=True)
