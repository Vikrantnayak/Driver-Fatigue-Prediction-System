#  Driver Fatigue Prediction System

An AI-powered **driver fatigue prediction** and analytics web app built with **Streamlit, Scikit-learn, XGBoost, and Plotly**.

This project simulates real-world driver fatigue assessment using behavioral and physiological factors such as sleep hours, driving duration, caffeine intake, and stress level. The system computes a **Fatigue Score** and predicts whether a driver is **Alert** or **Fatigued** using a Random Forest classifier.

---

## 🧠 Features

- 🔹 **Machine Learning Model:** Random Forest classifier trained on a synthetically generated dataset.
- 🔹 **Machine Learning Models:**
  - Random Forest classifier trained on synthetic behavioral data (main app)
  - XGBoost classifier with SMOTE on a questionnaire dataset (new Questionnaire page)
- 🔹 **Fatigue Scoring Logic:** Weighted fatigue score based on behavioral and time-of-day factors.
- 🔹 **Interactive Dashboard:** Real-time fatigue analysis, radar and gauge visualizations.
- 🔹 **Analytics View:** Fatigue trends, score distributions, and top fatigued drivers.
- 🔹 **Session Management:** Saves and exports driver records in CSV format.
- 🔹 **Dark Professional UI:** Fully custom CSS for a premium dashboard look.

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend / UI | Streamlit |
| Data / ML | Pandas, NumPy, Scikit-learn, XGBoost, imbalanced-learn |
| Visualization | Plotly |
| Styling | Custom CSS |
| Language | Python 3.x |

---

## 🧩 Project Structure

```
driver_fatigue_app/
├── app.py          # Main Streamlit UI and navigation
├── model.py        # ML model training and prediction
├── utils.py        # Visualization and helper functions
├── style.css       # Dark theme styling
└── README.md       # Project documentation
```

---

## 🚀 How to Run Locally

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/driver-fatigue-monitor.git
   cd driver-fatigue-monitor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

4. The app will open in your browser at:
   ```
   http://localhost:8501
   ```

---

## 📊 Model Overview

- **Algorithms:**
  - Random Forest Classifier (`n_estimators=300`) for behavioral features
  - XGBoost Classifier (`n_estimators=200`, `max_depth=4`) with SMOTE for questionnaire
- **Datasets:**
  - 3,000 synthetic samples generated programmatically (behavioral)
  - 500 synthetic questionnaire samples (persisted under `data/driver_fatigue_questionnaire_synthetic.csv`)
- **Accuracy (simulated):** ~94%
- **Features Used (behavioral):**
  - Sleep Hours  
  - Driving Hours  
  - Caffeine Intake  
  - Rest Breaks  
  - Stress Level  
  - Time of Day  
  - Age  

- **Features Used (questionnaire):**
  - Q1..Q14 Likert-scale (1-5)

---

## 🔮 Future Improvements

- Integrate real-world fatigue datasets (e.g., facial landmarks, heart rate).
- Add deep learning–based drowsiness detection.
- Save and load pre-trained model (`.pkl` file) instead of retraining.
- Calibrate probabilities and add AUC for the questionnaire model.
- Add email/SMS alerts for fatigued drivers.

---

## 🧑‍💻 Author

**Your Name**  
🎓 Final-Year Engineering Student | AI & ML  
📫 [vickynayak966@gmail.com]  
🌐 [LinkedIn or GitHub link]

---

## ⚠️ Disclaimer
This app is a **prototype** for educational and demonstration purposes only.  
It is **not a certified medical or safety tool** and should not be used for real driver health decisions.
