import pandas as pd
from config import MONTHLY_AMOUNT

def backtest_monthly(prices, weights, monthly_amount=MONTHLY_AMOUNT):
    """월 적립식 백테스팅"""
    # 월별 마지막 거래일 추출
    monthly_prices = prices.resample('ME').last().dropna()
    
    portfolio_value = []
    total_invested = []
    shares = {ticker: 0 for ticker in prices.columns}
    invested = 0

    for date, row in monthly_prices.iterrows():
        # 매월 투자금 배분
        for ticker, weight in weights.items():
            if ticker in row.index and row[ticker] > 0:
                alloc = monthly_amount * weight
                shares[ticker] += alloc / row[ticker]
        
        invested += monthly_amount
        
        # 현재 포트폴리오 가치
        value = sum(shares[t] * row[t] for t in shares if t in row.index)
        portfolio_value.append(value)
        total_invested.append(invested)

    result = pd.DataFrame({
        '포트폴리오 가치': portfolio_value,
        '투자 원금': total_invested
    }, index=monthly_prices.index)

    return result

def get_performance(result):
    """성과 지표 계산"""
    final_value = result['포트폴리오 가치'].iloc[-1]
    total_invested = result['투자 원금'].iloc[-1]
    profit = final_value - total_invested
    profit_rate = (final_value / total_invested - 1) * 100

    # 샤프 비율
    monthly_returns = result['포트폴리오 가치'].pct_change().dropna()
    sharpe = (monthly_returns.mean() / monthly_returns.std()) * (12 ** 0.5)

    # 최대 낙폭 (MDD)
    rolling_max = result['포트폴리오 가치'].cummax()
    drawdown = (result['포트폴리오 가치'] - rolling_max) / rolling_max * 100
    mdd = drawdown.min()

    return {
        '최종 자산': final_value,
        '투자 원금': total_invested,
        '총 수익': profit,
        '수익률': profit_rate,
        '샤프 비율': round(sharpe, 2),
        'MDD': round(mdd, 2)
    }