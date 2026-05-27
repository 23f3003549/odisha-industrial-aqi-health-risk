# 🌫️ Odisha Industrial AQI & Health Risk Prediction System

An ongoing Machine Learning and Time Series Analytics project focused on monitoring, analyzing, and predicting Air Quality Index (AQI) trends across Odisha’s industrial regions along with estimating probable health risks for industrial workers.

The project combines environmental monitoring, real-time data engineering, machine learning, time-series forecasting, and health-risk analysis using AQI and weather data collected from multiple APIs.

---

# 🚀 Project Overview

Industrial regions in Odisha such as Talcher, Brajrajnagar, Jharsuguda, and Rourkela frequently experience poor air quality due to:

- Coal mining
- Thermal power plants
- Steel industries
- Industrial emissions

This project aims to:

- Predict AQI trends in industrial cities
- Forecast future AQI levels in advance
- Analyze seasonal and weekday/weekend AQI patterns
- Estimate probable health risks for industrial workers
- Categorize AQI levels based on WHO standards
- Compare industrial cities with baseline non-industrial regions

---

# 🎯 Project Objectives

✅ Real-time AQI monitoring  
✅ AQI forecasting using ML & Time Series models  
✅ Industrial pollution trend analysis  
✅ Weather-based AQI analysis  
✅ Health risk estimation for industrial workers  
✅ WHO-standard AQI categorization  
✅ Seasonal and temporal AQI trend analysis  

---

# 🌍 Target Cities

## Industrial Regions
- Talcher
- Brajrajnagar
- Jharsuguda
- Rourkela
- Sambalpur

## Baseline Comparison Region
- Baripada

---

# 🏭 Industry-Based Health Risk Analysis

The project considers occupational exposure risks based on dominant industries in each region.

| Region | Major Industry |
|--------|----------------|
| Talcher | Coal Mining & Thermal Power |
| Jharsuguda | Coal & Aluminum Industry |
| Rourkela | Steel Industry |
| Brajrajnagar | Coal Mining |
| Sambalpur | Industrial & Urban Pollution |

Health-risk estimation is planned for:
- Coal workers
- Steel plant employees
- Thermal power plant workers
- Industrial laborers
- Urban residents

---

# 📡 Data Sources

## AQI Data
- WAQI API (World Air Quality Index)

## Weather Data
- OpenWeather API

---

# ⏳ Automated Data Collection

The system automatically collects:
- AQI data
- Weather parameters

at:

```txt
1-hour intervals
```

using automated workflows and scheduled jobs.

---

# 🔄 Automation Workflow

The project uses:
- GitHub Actions for automated hourly data collection
- API-based ingestion pipelines
- Continuous data updates and storage

---

# 📊 Historical Data Coverage

Historical AQI data is being collected from:

```txt
2019 → Present
```

for:
- Talcher
- GM Office Brajrajnagar
- Jharsuguda

These regions are used to:
- train forecasting models
- analyze industrial pollution trends
- generalize AQI prediction for other Odisha cities

---

# 🧠 Machine Learning Pipeline

```txt
Real-Time AQI & Weather Data
                ↓
Data Cleaning & Preprocessing
                ↓
EDA & Trend Analysis
                ↓
Feature Engineering
                ↓
AQI Categorization
                ↓
Model Training
                ↓
AQI Forecasting
                ↓
Health Risk Estimation
```

---

# 📈 Analysis Objectives

The project focuses on:

- AQI forecasting
- Seasonal trend analysis
- Weekday vs Weekend AQI comparison
- Weather impact on AQI
- Industrial pollution pattern analysis
- Health risk estimation
- WHO-standard AQI classification

---

# 🛠️ Machine Learning Models

## Current Models
- XGBoost

## Planned Models
- LSTM (Long Short-Term Memory)
- Time Series Forecasting Models

---

# 🌡️ AQI Classification

AQI levels are categorized based on WHO/standard AQI ranges:

| AQI Range | Category |
|-----------|----------|
| 0–50 | Good |
| 51–100 | Moderate |
| 101–150 | Unhealthy for Sensitive Groups |
| 151–200 | Unhealthy |
| 201–300 | Very Unhealthy |
| 300+ | Hazardous |

---

# 🩺 Planned Health Risk Estimation

Potential health risks analyzed based on AQI exposure:

- Respiratory irritation
- Asthma risk
- Lung-related health risks
- Long-term industrial exposure risks
- Occupational pollution exposure

---

# 🧰 Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Core Programming |
| Pandas | Data Processing |
| NumPy | Numerical Computation |
| Matplotlib | Visualization |
| Seaborn | Data Analysis |
| Scikit-learn | ML Models |
| XGBoost | AQI Prediction |
| TensorFlow/Keras | LSTM Models |
| GitHub Actions | Automated Data Collection |
| WAQI API | AQI Data |
| OpenWeather API | Weather Data |

---

# 📂 Project Structure

```txt
odisha-industrial-aqi-health-risk/
│
├── data/
├── notebooks/
├── scripts/
├── models/
├── .github/workflows/
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 🔮 Future Improvements

- LSTM-based AQI forecasting
- Real-time dashboard visualization
- AQI alert notification system
- Health risk scoring system
- Interactive city comparison dashboard
- GIS-based pollution visualization
- API deployment
- Deep learning forecasting models

---

# 📚 Learning Outcomes

This project helped in understanding:

- Environmental data analysis
- Real-time data engineering
- API integration
- AQI analytics
- Machine learning pipelines
- Time series forecasting
- Automation workflows
- Industrial pollution analysis
- Health risk estimation

---

# 👩‍💻 Author

**Subhasmita Nayak**   

---

# 📜 License

This project is developed for educational and research purposes.
