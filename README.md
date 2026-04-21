Give it a star ⭐ and feel free to fork!
# 🚀 PhishGuard AI — Phishing URL Detection System

> A full-stack machine learning web application that detects phishing URLs in real-time using feature engineering and classification models.

---

## 📌 Overview

PhishGuard AI is an end-to-end cybersecurity project designed to identify malicious URLs using machine learning. It combines **feature engineering**, **model training**, and a **Flask-based web interface** to provide real-time predictions with explainability.

---

## ✨ Key Highlights

* 🔍 Real-time URL phishing detection
* 🧠 Machine Learning model (Logistic Regression)
* 📊 Model performance dashboard (Accuracy, Precision, Recall, F1, ROC-AUC)
* 🔎 Explainable predictions (feature-wise breakdown)
* ⚡ Fully local deployment (no external APIs)
* 🌐 Clean web interface using Flask

---

## 🧠 How It Works

```
User Input (URL)
        ↓
Feature Extraction (8 engineered features)
        ↓
Trained ML Model
        ↓
Prediction: Safe ✅ or Phishing ❌ + Confidence Score
```

---

## ⚙️ Tech Stack

| Layer            | Technology Used                    |
| ---------------- | ---------------------------------- |
| Backend          | Python, Flask                      |
| Machine Learning | Scikit-learn (Logistic Regression) |
| Data Processing  | Pandas, NumPy                      |
| Visualization    | Matplotlib                         |
| Frontend         | HTML, CSS, JavaScript              |

---

## 📊 Features Used for Detection

The model analyzes the following URL characteristics:

* URL Length
* Presence of IP Address
* Number of Dots
* Presence of `@` Symbol
* HTTPS Usage
* Suspicious Keywords (e.g., login, verify, secure)
* Hyphen Count
* Subdomain Count

---

## 📁 Project Structure

```
phishguard-ai/
│
├── app.py
├── train_model.py
├── feature_extraction.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── model_performance.png
```

---

## 🚀 Setup & Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/phishguard-ai.git
cd phishguard-ai
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Train the model

```bash
python train_model.py
```

### 5️⃣ Run the application

```bash
python app.py
```

### 6️⃣ Open in browser

```
http://127.0.0.1:5000
```

---

## 📈 Model Performance

* Accuracy: ~99%
* Precision: ~99%
* Recall: ~99%
* F1 Score: ~99%
* ROC-AUC: ~1.0

*(Metrics may vary slightly depending on dataset split)*

---

## 📂 Dataset

The dataset consists of labeled URLs:

* Safe URLs
* Phishing URLs

📌 Note: Dataset is not included due to size limitations.
You can use publicly available datasets from Kaggle or similar sources.

---

## 🔮 Future Improvements

* Add advanced models (Random Forest, XGBoost)
* Integrate WHOIS/domain age features
* Deploy as a live web app
* Build browser extension
* Enable bulk URL scanning

---

## 💼 Skills Demonstrated

* Machine Learning Pipeline Development
* Feature Engineering
* Model Evaluation & Metrics
* Backend Development (Flask)
* Full-Stack Integration
* Problem Solving in Cybersecurity Domain

---

## 🙋‍♂️ Author

Swasti Suman

* GitHub: https://github.com/Swasti11S
* LinkedIn: https://linkedin.com/in/swasti-suman-9218722b0/

---

## ⭐ If you found this useful

Give it a star ⭐ and feel free to fork!
