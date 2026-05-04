import yfinance as yf
import pandas as pd
from config import START_DATE, STOCKS

def get_etf_prices(start_date=START_DATE):
    """ETF 가격 데이터 다운로드"""
    tickers = ["SPY", "QQQ", "BND", "SCHD"]
    data = yf.download(tickers, start=start_date)
    prices = data["Close"].dropna()
    print(f"ETF 데이터 로드 완료: {prices.shape[0]}일치, {start_date}~현재")
    return prices

def get_stock_prices(start_date=START_DATE):
    """개별 주식 가격 데이터 다운로드"""
    data = yf.download(STOCKS, start=start_date)
    prices = data["Close"].dropna()
    print(f"주식 데이터 로드 완료: {prices.shape[0]}일치, {start_date}~현재")
    return prices

def get_returns(prices):
    """일별 수익률 계산"""
    return prices.pct_change().dropna()

def get_summary(prices):
    """연평균 수익률 & 변동성 요약"""
    returns = get_returns(prices)
    annual_return = returns.mean() * 252
    annual_vol = returns.std() * (252 ** 0.5)
    
    summary = pd.DataFrame({
        '연평균 수익률': (annual_return * 100).round(2).astype(str) + '%',
        '연간 변동성': (annual_vol * 100).round(2).astype(str) + '%'
    })
    return summary