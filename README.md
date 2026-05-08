# 📊 Korean Investor Portfolio Optimizer

> AI-powered portfolio optimization system tailored for Korean retail investors — with tax-aware backtesting, LLM-generated reports, and multi-strategy comparison.

---

## 🗂️ Project Overview

This project implements a **semi-automated portfolio construction and evaluation pipeline** using U.S. equities (21 tickers across 7 sectors). It compares four optimization strategies with S&P 500 as benchmark, incorporates Korean tax structure (양도세, ISA account effects), and generates personalized investment reports via LLM.

**Built as a portfolio project for financial engineering research lab application.**

---

## 📈 Strategies Compared

| Strategy | Description |
|----------|-------------|
| **Global Minimum Variance (GMV)** | Minimizes portfolio volatility |
| **Maximum Sharpe Ratio (MSR)** | Maximizes risk-adjusted return |
| **Risk Parity (ERC)** | Equal Risk Contribution across assets |
| **Equal Weight** | Baseline — 1/N allocation |

Benchmark: **S&P 500 (^GSPC)**

---

## 🏦 Universe — 21 Tickers, 7 Sectors

| Sector | Tickers |
|--------|---------|
| Technology | AAPL, MSFT, GOOGL, META, NVDA |
| Consumer | AMZN, TSLA, MCD, NKE |
| Healthcare | JNJ, UNH, PFE, ABBV |
| Finance | JPM, BAC, GS, BRK-B |
| Energy | XOM, CVX |
| Utilities | NEE, DUK |
| Industrial | CAT, HON |

---

## 🔧 Pipeline

```
Data Collection (yfinance)
        ↓
EDA — Correlation heatmap, risk-return scatter, cumulative returns
        ↓
Portfolio Optimization (scipy / cvxpy)
    ├── GMV
    ├── Max Sharpe
    ├── Risk Parity
    └── Equal Weight
        ↓
Monte Carlo Simulation (20,000 portfolios → Efficient Frontier)
        ↓
Backtesting — Rolling window rebalancing, MDD, Sharpe, Sortino
        ↓
Korean Tax Adjustment (양도세 22%, ISA 비과세 시뮬레이션)
        ↓
LLM Report Generation (Groq API → personalized investment summary)
```

---

## 🇰🇷 Korean Investor Features

- **양도소득세 22%** applied to realized gains
- **ISA 계좌** tax-free simulation (비과세 한도 적용)
- DCA comparison: daily ₩1,000 vs monthly ₩20,000 investment strategies

---

## 📊 Key Outputs

- Efficient frontier visualization with optimal portfolios marked
- Strategy performance table (Annualized Return / Volatility / Sharpe / MDD)
- Rolling Sharpe ratio over time
- LLM-generated personalized portfolio report (Korean)

---

## 🚀 Getting Started

```bash
git clone https://github.com/sujin809/portfolio-optimizer.git
cd portfolio-optimizer
pip install -r requirements.txt
```

Open `main.ipynb` and run all cells.

> ⚠️ LLM report generation requires a Groq API key. Set it in `config.py`.

---

## 🛠️ Tech Stack

| Category | Libraries |
|----------|-----------|
| Data | `yfinance`, `pandas`, `numpy` |
| Optimization | `scipy`, `cvxpy` |
| Visualization | `matplotlib`, `seaborn`, `plotly` |
| LLM | `groq` (llama3-8b-8192) |

---

## 📁 File Structure

```
portfolio-optimizer/
├── main.ipynb          # Main notebook — full pipeline
├── config.py           # API key configuration (not committed)
├── requirements.txt    # Dependencies
└── README.md
```

---

## 👤 Author

**정수진 (Sujin Jeong)**  
Industrial Engineering + Biomedical Engineering (Minor), UNIST  
Founder, FIC (Finance Investment Club — UNIST, KAIST, POSTECH, DGIST, GIST)  
GitHub: [@sujin809](https://github.com/sujin809)
