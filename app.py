# app.py — PhishGuard AI Flask Backend
import pickle, os, json
from flask import Flask, request, jsonify, render_template
from feature_extraction import extract_features

app = Flask(__name__)

MODEL_PATH = 'model.pkl'
if not os.path.exists(MODEL_PATH):
    print("⚠️  model.pkl not found! Run: python train_model.py"); model = None
else:
    with open(MODEL_PATH,'rb') as f: model = pickle.load(f)
    print("✅ Model loaded.")

FEATURE_NAMES = ['URL Length','Has IP Address','Dot Count','Has @ Symbol',
                 'Uses HTTPS','Suspicious Keywords','Hyphen Count','Subdomain Count']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error':'Model not loaded. Run train_model.py first.'}),500
    data = request.get_json()
    url = data.get('url','').strip()
    if not url:
        return jsonify({'error':'No URL provided.'}),400
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    features = extract_features(url)
    prediction = model.predict([features])[0]
    probability = model.predict_proba([features])[0]
    return jsonify({
        'url': url,
        'prediction': int(prediction),
        'label': 'Phishing' if prediction == 1 else 'Safe',
        'confidence': round(float(max(probability)) * 100, 1),
        'features': [{'name': n, 'value': v} for n, v in zip(FEATURE_NAMES, features)]
    })

@app.route('/stats')
def stats():
    """Return model statistics for the dashboard tab."""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    try:
        df = pd.read_csv('dataset.csv')
        X = [extract_features(u) for u in df['url']]
        y = df['label'].tolist()
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:,1]
        return jsonify({
            'total_samples': len(df),
            'safe_count': int((df.label==0).sum()),
            'phishing_count': int(df.label.sum()),
            'accuracy':  round(accuracy_score(y_test,y_pred)*100, 2),
            'precision': round(precision_score(y_test,y_pred)*100, 2),
            'recall':    round(recall_score(y_test,y_pred)*100, 2),
            'f1_score':  round(f1_score(y_test,y_pred)*100, 2),
            'roc_auc':   round(roc_auc_score(y_test,y_prob), 4),
            'chart_available': os.path.exists('static/model_performance.png')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n🚀 PhishGuard AI running at http://127.0.0.1:5000\n")
    app.run(debug=True)
