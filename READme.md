# Stock Market Trend Prediction

## Overview

This project uses Simple Moving Average (SMA) and Linear Regression (LR) to predict stock price trends based on historical Yahoo Finance data. It is built as a command-line application with real-time prediction capabilities and graphing features.

## Team

- Joshua Caron (`josh-caron` on GitHub)
- Nicholas Lara (`Nicolara10` on GitHub)

GitHub: [https://github.com/josh-caron/Stock-Market-Trend-Prediction.git](https://github.com/josh-caron/Stock-Market-Trend-Prediction.git)

## Features Implemented

- Interactive console menu
- Dynamic data loading (any ticker)
- SMA (50-day) prediction with signals
- Linear regression prediction with signals
- Accuracy, speed, and ROI comparison
- Graph visualization for SMA and LR
- Combined graph feature for visual comparison
- Robust error handling

## Tools & Libraries Used

- **Language:** Python 3
- **APIs/Libraries:**
  - `yfinance` for stock data
  - `pandas` for data handling
  - `matplotlib` for plotting
  - `scikit-learn` for regression
  - `numpy`, `time`, `os`

## Data Description

- Source: Yahoo Finance
- Format: Historical daily price data (OHLCV)
- Scope: Any stock with Yahoo Finance data

## ▶️ How to Run

### 🔧 Requirements

- Python 3.10 or later
- Internet connection (to fetch Yahoo Finance data)

### 📦 Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/josh-caron/Stock-Market-Trend-Prediction.git
cd Stock-Market-Trend-Prediction
```

2. **(Optional) Set up a virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate       # macOS/Linux
.venv\Scripts\activate          # Windows
```

3. **Install required dependencies:**

```bash
pip install -r requirements.txt
```

4. **Run the program:**

```bash
cd src
python main.py
```

5. **Use the menu in the terminal:**

```
=== Stock Trend Predictor by Josh Caron and Nico Lara ===
1. Load Dataset
2. Run SMA Prediction
3. Run Linear Regression Prediction
4. Compare & Display Both Results
5. Exit
```

## 📈 Graphing Options

- Choose 'V' after SMA or LR predictions to view their graphs.
- In the comparison option, press:
  - `'S'` → SMA Graph
  - `'L'` → LR Graph
  - `'B'` → Combined SMA + LR + Actual Graph
