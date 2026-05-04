import matplotlib.pyplot as plt
from config import FIGURE_SIZE, FONT_FAMILY

# 한글 폰트 설정
plt.rcParams['font.family'] = FONT_FAMILY
plt.rcParams['axes.unicode_minus'] = False

def plot_cumulative_returns(prices):
    """ETF 누적 수익률 시각화"""
    returns = prices.pct_change().dropna()
    cumulative = (1 + returns).cumprod()

    plt.figure(figsize=FIGURE_SIZE)
    for ticker in prices.columns:
        plt.plot(cumulative.index, cumulative[ticker], label=ticker)

    plt.title('ETF 누적 수익률')
    plt.xlabel('날짜')
    plt.ylabel('누적 수익률 (1 = 원금)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_backtest(result, title='포트폴리오 백테스팅'):
    """백테스팅 결과 시각화"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    ax1.plot(result.index, result['포트폴리오 가치'] / 10000,
             label='포트폴리오 가치', color='blue')
    ax1.plot(result.index, result['투자 원금'] / 10000,
             '--', label='투자 원금', color='gray')
    ax1.fill_between(result.index,
                     result['투자 원금'] / 10000,
                     result['포트폴리오 가치'] / 10000,
                     alpha=0.2, color='blue')
    ax1.set_title(title)
    ax1.set_ylabel('금액 (만원)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    profit_rate = (result['포트폴리오 가치'] / result['투자 원금'] - 1) * 100
    ax2.plot(result.index, profit_rate, color='green')
    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax2.fill_between(result.index, 0, profit_rate,
                     where=profit_rate >= 0, color='green', alpha=0.2)
    ax2.fill_between(result.index, 0, profit_rate,
                     where=profit_rate < 0, color='red', alpha=0.2)
    ax2.set_title('수익률 변화')
    ax2.set_ylabel('수익률 (%)')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def plot_comparison(etf_result, stock_result):
    """ETF vs 개별주식 비교 시각화"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    ax1.plot(etf_result.index, etf_result['포트폴리오 가치'] / 10000,
             label='ETF 균형형', color='blue')
    ax1.plot(stock_result.index, stock_result['포트폴리오 가치'] / 10000,
             label='개별주식 블렌딩', color='red')
    ax1.plot(etf_result.index, etf_result['투자 원금'] / 10000,
             '--', label='투자 원금', color='gray', alpha=0.5)
    ax1.set_title('ETF vs 개별주식 비교 (월 30만원)')
    ax1.set_ylabel('금액 (만원)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    etf_profit = (etf_result['포트폴리오 가치'] / etf_result['투자 원금'] - 1) * 100
    stock_profit = (stock_result['포트폴리오 가치'] / stock_result['투자 원금'] - 1) * 100
    ax2.plot(etf_result.index, etf_profit, label='ETF 균형형', color='blue')
    ax2.plot(stock_result.index, stock_profit, label='개별주식 블렌딩', color='red')
    ax2.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    ax2.set_title('수익률 비교')
    ax2.set_ylabel('수익률 (%)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def plot_weights(weights, tickers, title='포트폴리오 비중'):
    """포트폴리오 비중 파이차트"""
    plt.figure(figsize=(8, 8))
    plt.pie(weights, labels=tickers, autopct='%1.1f%%', startangle=90)
    plt.title(title)
    plt.tight_layout()
    plt.show()

def plot_monthly_comparison(prices, weights, amounts):
    """월 투자금별 비교"""
    from backtest import backtest_monthly
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    labels = [f'{a//10000}만원' for a in amounts]

    plt.figure(figsize=FIGURE_SIZE)
    for amount, label, color in zip(amounts, labels, colors):
        r = backtest_monthly(prices, weights, amount)
        plt.plot(r.index, r['포트폴리오 가치'] / 10000,
                 label=label, color=color)

    plt.title('월 투자금별 포트폴리오 가치 비교')
    plt.xlabel('날짜')
    plt.ylabel('금액 (만원)')
    plt.legend(title='월 투자금')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()