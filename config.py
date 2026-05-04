import os

# ── 투자자 설정 ──
MONTHLY_AMOUNT = 300_000       # 월 투자금 (원)
START_DATE = "2020-01-01"      # 백테스팅 시작일
RISK_PROFILE = "moderate"      # conservative / moderate / aggressive

# ── ETF 포트폴리오 ──
ETF_WEIGHTS = {
    "conservative": {"SPY": 0.40, "QQQ": 0.15, "BND": 0.35, "SCHD": 0.10},
    "moderate":     {"SPY": 0.45, "QQQ": 0.25, "BND": 0.15, "SCHD": 0.15},
    "aggressive":   {"SPY": 0.30, "QQQ": 0.40, "BND": 0.00, "SCHD": 0.30},
}

# ── 개별 주식 ──
STOCKS = ["AAPL", "NVDA", "MSFT", "AMZN", "GOOGL", "META", "TSLA"]
WEIGHT_BOUNDS = (0.05, 0.40)   # 종목당 최소 5%, 최대 40%

# ── 세금 ──
GENERAL_TAX_RATE = 0.22        # 일반 계좌 양도세
ISA_TAX_RATE = 0.099           # ISA 계좌 분리과세
GENERAL_DEDUCTION = 2_500_000  # 일반 계좌 공제
ISA_DEDUCTION = 2_000_000      # ISA 계좌 공제

# ── API ──
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"

# ── 시각화 ──
FIGURE_SIZE = (12, 6)
FONT_FAMILY = "AppleGothic"