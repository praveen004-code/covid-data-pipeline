from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATA_PATH = None  # Will be set after upload

def load_data():
    if DATA_PATH and os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH, parse_dates=['date'])
        return df
    return pd.DataFrame()

@app.route('/api/upload', methods=['POST'])
def upload_file():
    global DATA_PATH
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    DATA_PATH = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(DATA_PATH)
    
    # Analyze the CSV
    df = pd.read_csv(DATA_PATH)
    analysis = {
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.apply(lambda x: str(x)).to_dict(),
        'rows': len(df)
    }
    return jsonify({'message': 'File uploaded', 'analysis': analysis})

@app.route('/api/get-data', methods=['GET'])
def get_data():
    df = load_data()
    if df.empty:
        return jsonify({'error': 'No data loaded'}), 400

    start = request.args.get('start')
    end = request.args.get('end')
    search = request.args.get('search', '').strip()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    sort_by = request.args.get('sort_by', 'date')
    order = request.args.get('order', 'asc')

    if start:
        df = df[df['date'] >= start]
    if end:
        df = df[df['date'] <= end]
    if search:
        if 'location' in df.columns:
            df = df[df['location'].str.contains(search, case=False, na=False)]
    
    if sort_by in df.columns:
        df = df.sort_values(by=sort_by, ascending=(order=='asc'))

    total = len(df)
    start_idx = (page-1)*per_page
    end_idx = start_idx + per_page
    page_df = df.iloc[start_idx:end_idx].copy()
    page_df['date'] = page_df['date'].dt.strftime('%Y-%m-%d')

    return jsonify({
        'page': page,
        'per_page': per_page,
        'total': total,
        'data': page_df.to_dict(orient='records')
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    df = load_data()
    if df.empty:
        return jsonify({'error': 'No data loaded'}), 400

    latest = df.sort_values('date').iloc[-1]
    total_cases = int(latest.get('total_cases', 0))
    latest_date = latest['date'].strftime('%d-%m-%Y')
    avg_new_cases = float(df.get('new_cases', pd.Series([0])).mean())
    return jsonify({
        'latest_date': latest_date,
        'total_cases': total_cases,
        'avg_new_cases': round(avg_new_cases, 2)
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    root = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    if path != '' and os.path.exists(os.path.join(root, path)):
        return send_from_directory(root, path)
    else:
        return send_from_directory(root, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
