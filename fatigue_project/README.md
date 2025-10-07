#  Driver Fatigue Monitoring System

An AI-powered **driver fatigue monitoring** web app built with **Streamlit, Scikit-learn, and Plotly**.

The app collects inputs such as sleep hours, driving duration, caffeine intake, rest breaks, age, time of day, and stress level. It computes a **Fatigue Score** and predicts whether a driver is **Alert** or **Fatigued** using a Random Forest classifier.

---

## 🧠 Features

- 🔹 **Machine Learning Model:** Random Forest classifier trained on a synthetically generated dataset.
- 🔹 **Fatigue Scoring Logic:** Weighted fatigue score based on behavioral and time-of-day factors.
- 🔹 **Interactive Dashboard:** Real-time fatigue analysis, radar and gauge visualizations.
- 🔹 **Analytics View:** Fatigue trends and score distributions.
- 🔹 **Session Management:** Saves and exports driver records in CSV format.
- 🔹 **Dark Professional UI:** Fully custom CSS for a premium dashboard look.
 - 🔹 **Input Validation:** All numeric inputs are non‑negative; stress level constrained to 1–10.

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
fatigue_project/
├── streamlit_app.py   # Main Streamlit UI and navigation
├── model.py           # ML model training and prediction
├── utils.py           # Visualization and helper functions
├── style.css          # Dark theme styling (optional; app runs without it)
├── requirements.txt   # Python dependencies
├── runtime.txt        # Python version pin for Streamlit Cloud
├── driver_fatigue_questionnaire_synthetic.csv  # Example data (optional)
└── README.md          # Project documentation
```

---

## 🚀 How to Run Locally

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/driver-fatigue-monitor.git
   cd driver-fatigue-monitor
   ```

2. **(Recommended) Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**
   ```bash
   streamlit run streamlit_app.py
   ```

5. The app will open in your browser at:
   ```
   http://localhost:8501
   ```

Notes:
- The app will automatically load `style.css` if it exists next to `streamlit_app.py`. If the file is missing, the app still runs.
- Inputs are validated: values cannot be negative; stress level is limited to 1–10.

---

## 📊 Model Overview

- **Algorithm:**
  - Random Forest Classifier (`n_estimators=300`) for behavioral features
- **Dataset:**
  - 3,000 synthetic samples generated programmatically (behavioral)
- **Accuracy (simulated):** ~94%
- **Features Used (behavioral):**
  - Sleep Hours  
  - Driving Hours  
  - Caffeine Intake  
  - Rest Breaks  
  - Stress Level  
  - Time of Day  
  - Age  

  
---

## ☁️ Deploying on Streamlit Community Cloud

1. Push this folder to GitHub.
2. In Streamlit Cloud, set:
   - Repository: your repo
   - Branch: main
   - Main file path: `fatigue_project/streamlit_app.py` (or adjust based on your repo layout)
   - Requirements file: `requirements.txt` (repo root)
3. Optional but recommended: keep `runtime.txt` with `python-3.12` at the repo root.
4. After deploying, use “Clear cache” → “Rerun” if you update the model or code.

---

## 🔮 Future Improvements

- Integrate real-world fatigue datasets (e.g., facial landmarks, heart rate).
- Add deep learning–based drowsiness detection.
- Save and load pre-trained model (`.pkl` file) instead of retraining.
- Calibrate probabilities and add AUC for the questionnaire model.
- Add email/SMS alerts for fatigued drivers.


  🧑‍💻 Author
   Vikrant Nayak  
📫 vickynayak966@gmail.com  



## ⚠️ Disclaimer
This app is a **prototype** for educational and demonstration purposes only.  
It is **not a certified medical or safety tool** and should not be used for real driver health decisions.
