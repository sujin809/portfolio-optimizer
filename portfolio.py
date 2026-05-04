import numpy as np
from scipy.optimize import minimize
from config import STOCKS, WEIGHT_BOUNDS
import pandas as pd
import yfinance as yf

def get_cov_matrix(returns):
    """연간화된 공분산 행렬 계산"""
    return returns.cov() * 252

def minimum_variance(cov_matrix):
    """최소분산 포트폴리오 비중 계산"""
    n = len(cov_matrix)
    
    def portfolio_variance(weights):
        return weights @ cov_matrix.values @ weights
    
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    bounds = [WEIGHT_BOUNDS] * n
    
    result = minimize(
        portfolio_variance,
        x0=np.ones(n) / n,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )
    return result.x

def risk_parity(cov_matrix):
    """리스크 패리티 포트폴리오 비중 계산"""
    n = len(cov_matrix)
    
    def risk_parity_objective(weights):
        port_vol = np.sqrt(weights @ cov_matrix.values @ weights)
        marginal_risk = cov_matrix.values @ weights / port_vol
        risk_contribution = weights * marginal_risk
        target = port_vol / n
        return np.sum((risk_contribution - target) ** 2)
    
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    bounds = [WEIGHT_BOUNDS] * n
    
    result = minimize(
        risk_parity_objective,
        x0=np.ones(n) / n,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )
    return result.x

def blend_weights(mv_weights, rp_weights):
    """최소분산 + 리스크패리티 블렌딩"""
    blended = (mv_weights + rp_weights) / 2
    return blended / blended.sum()

def get_optimal_weights(returns):
    """전체 최적화 파이프라인"""
    cov = get_cov_matrix(returns)
    mv = minimum_variance(cov)
    rp = risk_parity(cov)
    blended = blend_weights(mv, rp)
    
    import pandas as pd
    result = pd.DataFrame({
        '최소분산': (mv * 100).round(1),
        '리스크패리티': (rp * 100).round(1),
        '블렌딩': (blended * 100).round(1)
    }, index=STOCKS)
    
    return blended, result

def momentum_weights(prices, lookback=126):
    """모멘텀 전략 — 최근 6개월 수익률 기반 비중"""
    # 최근 lookback일 수익률 계산
    recent_returns = prices.iloc[-1] / prices.iloc[-lookback] - 1
    
    # 수익률이 양수인 종목만 선택
    positive = recent_returns[recent_returns > 0]
    
    if len(positive) == 0:
        # 모두 음수면 동일비중
        n = len(prices.columns)
        return np.ones(n) / n
    
    # 수익률 비례해서 비중 설정
    weights = positive / positive.sum()
    
    # 없는 종목은 0으로 채우기
    all_weights = pd.Series(0.0, index=prices.columns)
    all_weights[weights.index] = weights
    
    return all_weights.values

def market_cap_weights(tickers):
    """시가총액 비중 — 실제 시가총액 데이터 가져오기"""
    market_caps = {}
    for ticker in tickers:
        info = yf.Ticker(ticker).info
        cap = info.get('marketCap', 0)
        market_caps[ticker] = cap
        print(f"{ticker}: {cap/1e12:.2f}조 달러")
    
    total = sum(market_caps.values())
    weights = np.array([market_caps[t] / total for t in tickers])
    return weights