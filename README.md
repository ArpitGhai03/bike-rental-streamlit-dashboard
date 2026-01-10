# 🚲 Bike Rental Demand Analysis & Streamlit Dashboard

This project analyzes the **Bike Sharing (Hourly) dataset** from Kaggle using exploratory data analysis (EDA) 
and presents the findings through an **interactive Streamlit dashboard**.

The goal of the project is to understand how **time, weather, and working-day factors** influence bike rental demand.

---

## 📊 Dataset

- **Source:** Kaggle – Bike Sharing Dataset  
- **Type:** Hourly bike rental data  
- **Years Covered:** 2011–2012  
- **Target Variable:** Total hourly bike rentals (`count`)

The dataset includes information on:
- Time (hour, day, month, season)
- Weather conditions
- Temperature and humidity
- Working and non-working days
- Casual vs registered users

---

## 🔍 Exploratory Data Analysis (EDA)

The following analyses and visualizations were performed:

- Distribution analysis of numerical variables (histograms & boxplots)
- Mean hourly rental patterns across:
  - Working vs non-working days
  - Months and seasons
  - Hours of the day
  - Days of the week
- Weather impact analysis with **95% confidence intervals**
- Correlation analysis of key numerical variables

---

  **📈 Streamlit Dashboard Features**

  - 📌 **Hourly rental trends**
  - 📌 **Day-of-week and seasonal usage patterns**
  - 📌 **Weather impact with confidence intervals**
  - 📌 **Working vs non-working day comparison**
  - 📌 **Correlation heatmap of key variables**

  **Interactive Widgets (sidebar)**

  - **Date range picker** — filter the dataset by calendar dates
  - **Year selector** — multi-select one or more years
  - **Season filter** — multi-select seasons (Spring/Summer/Fall/Winter)
  - **Hour range slider** — focus on specific hours of day
  - **Weather type filter** — multi-select weather categories
  - **User type selector** — choose `All`, `Registered`, or `Casual` rentals

---

## 🛠️ Tech Stack

- **Python**
- **Pandas, NumPy**
- **Matplotlib, Seaborn**
- **Plotly**
- **Streamlit**
- **SciPy**

---

## 🚀 Live Dashboard

👉 **Streamlit App:**  
[Streamlit Community Cloud](https://bike-rental-app-dashboard-52ftujdrkgwyyshmyo2kvy.streamlit.app/)

---

## 📁 Project Structure

bike-rental-streamlit-dashboard/
│
├── notebooks/
│ └── bike_rental_eda.ipynb
│
├── data/
│ └── bike_rental_cleaned.csv
│
├── app.py
├── requirements.txt
└── README.md


---

## 📌 Key Insights

- Bike rentals peak during **morning and evening commute hours**
- **Working days** show higher demand on weekdays
- **Weather conditions** significantly impact rental behavior
- Temperature has a strong positive correlation with rental count
- Poor weather leads to noticeably reduced bike usage

---

## 📎 Notes

- This project was developed as part of an academic assignment.
- The dataset originates from Kaggle and is used for educational purposes only.

---

## 👤 Author

**Arpit Ghai**
