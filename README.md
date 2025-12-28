# 🌍 pandas-global-economic-indicators-analysis

A **Pandas-based global economic indicators comparison and trend analysis** project.  
The project follows a **layered data pipeline architecture**, separating raw data cleaning, time-series feature engineering, trend analysis, and visual storytelling.

The primary goal is to analyze **economic growth, inflation dynamics, and stability patterns** across countries and over time using interpretable statistical methods rather than predictive models.

---

## 📌 Project Overview

Understanding global economic behavior requires more than observing raw indicators such as GDP or inflation.  
This project focuses on **how these indicators evolve over time**, how countries differ structurally, and how global trends emerge.

The project provides:

- A multi-stage data pipeline (`raw → cleaned → intermediate → trends`)
- Time-series feature engineering (growth rates, rolling averages)
- Country-level and global-level trend analysis
- Static PNG visualizations and an interactive HTML dashboard
- A consistent pastel turquoise visual theme for visual storytelling

---

## 📊 Dataset

The dataset contains country-level macroeconomic indicators measured annually.

**Key indicators include:**
- GDP (Current USD)
- GDP per Capita
- Inflation (CPI %)
- Unemployment Rate
- Interest Rate
- Government Revenue & Expenditure
- Public Debt (% of GDP)

**Data organization:**
- Raw data: `data/raw`
- Cleaned data: `data/cleaned`
- Feature-engineered data: `data/intermediate`

---

## 📈 Example Outputs

### 🌍 Global Economic Overview
- Global inflation trend over time  
- Global GDP growth trend with recession indicators  

### 🌎 Country Comparison
- Top countries by average GDP  
- Countries with the highest number of crisis years  

### 🔍 Country Case Study
- GDP vs rolling average for a selected country  
- Inflation vs rolling average for a selected country  

### 🌐 Interactive Dashboard
🖱️ **Live Dashboard:**  
https://busracevik.github.io/pandas-global-economic-indicators-analysis/index.html

---

## 📁 Project Structure

```text
pandas-global-economic-indicators-analysis/
│
├── data/
│   ├── raw/                # Original dataset
│   ├── cleaned/            # Cleaned and standardized data
│   └── intermediate/       # Time-series enriched dataset
│
├── outputs/
│   ├── csv/                # Aggregated and trend analysis outputs
│   └── png/                # Static visualizations
│
├── src/
│   ├── data_preparation.py
│   ├── economic_analysis.py
│   └── visualization.py
│
├── docs/
│   └── index.html          # Interactive dashboard (GitHub Pages)
│
├── main.py                 # End-to-end pipeline execution
└── README.md
```

---

## 🛠 Technologies Used

- **Python** – Core programming language  
- **Pandas** – Data preprocessing and time-series analysis  
- **NumPy** – Numerical computations  
- **Matplotlib** – Static PNG visualizations  
- **Plotly** – Interactive choropleth map  
- **GitHub Pages** – Hosting the interactive dashboard  

---

## 🧠 Analytical Approach

This project emphasizes **economic interpretability** over predictive modeling.  
No machine learning models are used.

Instead, the analysis relies on:

- Time-series transformations  
- Statistical aggregation  
- Trend and stability indicators  

The focus is on answering **economic questions**, not forecasting.

---

## 📐 Mathematical Definitions & Economic Metrics

Below are the core calculations used throughout the project, along with their mathematical definitions and economic interpretations.

---

### 1️⃣ GDP Growth Rate (Year-over-Year)

**Formula:**

\[
GDP\_Growth_t = \frac{GDP_t - GDP_{t-1}}{GDP_{t-1}} \times 100
\]

**Explanation:**  
Measures how much a country’s economy has grown or contracted compared to the previous year.  
Negative values indicate economic contraction.

---

### 2️⃣ Inflation Change Rate

**Formula:**

\[
Inflation\_Change_t = Inflation_t - Inflation_{t-1}
\]

**Explanation:**  
Captures short-term inflation shocks and sudden price-level changes.

---

### 3️⃣ Rolling Average (Trend Indicator)

**Formula:**

\[
RollingAvg_t = \frac{1}{N} \sum_{i=0}^{N-1} X_{t-i}
\]

**Explanation:**  
Smooths short-term fluctuations to reveal long-term trends.  
Used for both GDP and inflation.

---

### 4️⃣ Mean GDP Growth (Last N Years)

**Formula:**

\[
MeanGrowth = \frac{1}{N} \sum_{i=1}^{N} GDP\_Growth_{t-i}
\]

**Explanation:**  
Represents recent economic performance rather than historical averages.  
Used to assess current economic momentum.

---

### 5️⃣ GDP Volatility (Economic Stability)

**Formula:**

\[
GDP\_Volatility = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (GDP_i - \bar{GDP})^2}
\]

**Explanation:**  
Measures how unstable or volatile an economy is over time.  
Higher values indicate stronger economic fluctuations.

---

### 6️⃣ Inflation Trend Direction

**Formula:**

\[
Inflation\_Trend = Inflation_{last} - Inflation_{first}
\]

**Explanation:**  
A simple slope approximation indicating whether inflation is trending upward or downward over the observed period.

---

### 7️⃣ Crisis Year Count

**Definition:**  
A year is classified as a **crisis year** if:

\[
GDP\_Growth_t < 0
\]

**Explanation:**  
Counts the number of years in which an economy experienced contraction.  
Used as an indicator of economic vulnerability.

---

## 🧭 Conclusion

This project demonstrates how **time-series analysis and statistical feature engineering** can be used to extract meaningful economic insights without relying on complex models.

By combining:

- layered data pipelines,  
- interpretable metrics,  
- and clear visual storytelling,  

the project provides a structured and transparent view of global economic dynamics.
