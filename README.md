# AI-Based Behavioral Intrusion Detection System

This project focuses on detecting **suspicious login behavior** using machine learning instead of relying only on passwords.

Attackers often gain access using stolen credentials, so this system analyzes **how a user logs in**, not just whether the password is correct.

---

## What this project does

- Detects abnormal login behavior using:
  - Typing speed
  - Login time
  - Device familiarity
  - Location change
- Uses a machine learning model to flag unusual login attempts
- Displays results in a simple interactive dashboard

---

## How it works

1. Normal login behavior is collected as training data
2. A machine learning model learns what “normal” looks like
3. New login attempts are compared against this baseline
4. Suspicious behavior is flagged as an anomaly

---

## Tech used

- Python
- Scikit-learn
- Pandas, NumPy
- Streamlit
- Git & GitHub

---


