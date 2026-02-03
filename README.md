# 🥗 Calorie & Nutrition Calculator (v1)

A Flask-based web application that helps users analyze their daily food intake, compare it against ideal nutritional requirements, and gain actionable insights to improve their diet.

This project represents the **first iterative version** of a larger vision.
Future versions will introduce advanced tracking, personalization, and long-term nutritional analytics.

---

## 🚀 Project Overview

The Calorie & Nutrition Calculator is a simple yet structured web application designed to:

* Collect a user’s daily food consumption
* Analyse nutritional values using the **Google Gemini API**
* Calculate ideal nutritional requirements based on personal body metrics
* Compare actual vs ideal intake and present meaningful insights

This version focuses on **core functionality**, clarity, and user experience, laying a strong foundation for upcoming enhancements.

---

## 🧠 Key Features (Version 1)

### 1️⃣ Daily Food Intake Collection

Users enter everything they consumed during a single day, including meals and snacks.

📌 Goal: Capture a complete snapshot of daily dietary intake.

---

### 2️⃣ Nutritional Analysis & User Profiling

Using the **Gemini API**, the application:

* Calculates nutritional values (calories, macronutrients, etc.) from the user’s food input
* Collects user-specific details such as age, height, weight, and activity level
* Displays nutritional data in a **clear and visually aesthetic format**

📌 Goal: Help users understand *what* they consumed and *how it maps to nutritional values*.

---

### 3️⃣ Ideal vs Actual Nutrition Comparison

Based on the user’s body details, the app calculates **ideal nutritional intake** and presents insights across three structured sections:

#### a) Ideal Nutritional Requirements

Displays the recommended daily intake values tailored to the user’s body metrics and lifestyle.

#### b) Comparative Nutrition Report

A detailed comparison between:

* **Actual consumption**
* **Ideal consumption**

Each nutrient is labeled as:

* **Surplus**
* **Optimal**
* **Deficit**

Along with clear quantitative differences (e.g. `-100 g`, `+250 kcal`).

#### c) Actionable Insights

Two focused sections:

* ✅ *What the user is doing well*
* ⚠️ *Areas for improvement*

Each section highlights 2–3 concise, practical points to guide better dietary decisions.

📌 Goal: Move beyond raw numbers and provide **actionable, easy-to-understand feedback**.

---

## 🖼️ Application Design & Flow (Sketches)


### 📄 Page 1 – Daily Intake Input
<img width="725" height="576" alt="Page 1 - Daily Intake Input" src="https://github.com/user-attachments/assets/0b45ba60-aa39-4ea0-8466-ab2a0966a89f" />

---

### 📄 Page 2 – Nutritional Analysis & User Details
<img width="768" height="574" alt="Page 2 - Nutritional Analysis and User details" src="https://github.com/user-attachments/assets/82d261dd-ec29-4193-b58c-5df07bceaf05" />

---

### 📄 Page 3 – Ideal vs Actual Nutrition Report
<img width="819" height="798" alt="Page 3 – Ideal vs Actual Nutrition Report" src="https://github.com/user-attachments/assets/9a324034-c68a-4ed4-9148-bbf03ceff2ff" />

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, Tailwind CSS
* **AI Integration:** Google Gemini API
* **Deployment Ready:** Gunicorn + Cloud Hosting
* **Version Control:** Git & GitHub

---

## 🔮 Future Enhancements (Planned)

* Multi-day and weekly nutrition tracking
* User authentication and profiles
* Persistent data storage
* Micronutrient analysis
* Personalised dietary recommendations
* Mobile-responsive optimisations

---

## ⚠️ Disclaimer

This application is intended for **educational and informational purposes only**.
It does not replace professional medical or nutritional advice.

---

## 📬 Feedback & Contributions

Feedback, suggestions, and contributions are welcome.
This project is actively evolving, and improvements will be rolled out in future versions.

---

**Built as a learning-focused, iterative project with an emphasis on clean architecture, clarity, and user-centric insights.**
