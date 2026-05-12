# Korean Investor Portfolio Optimizer

> **세금을 고려한 한국 개인투자자용 AI 포트폴리오 백테스팅 시스템**  
> Tax-aware backtesting + LLM-generated reports + multi-strategy comparison

한국 투자자 현실에 맞게 **양도세·ISA 절세 효과를 직접 반영**한 포트폴리오 백테스팅 시스템입니다.  
4가지 전략을 비교하고, LLM으로 한국어 투자 리포트를 자동 생성합니다.

---

## Pipeline / 파이프라인

> 아래 다이어그램은 전체 실행 흐름입니다. (이미지로 교체 권장: Gemini / Napkin AI 등 활용)

```
데이터 수집 (yfinance, 2020~현재)
        ↓
ETF 누적 수익률 분석
        ↓
개별주식 최적 비중 산출 (최소분산 + 리스크패리티 → 블렌딩)
        ↓
4가지 전략 월별 백테스팅
    ├── ETF 균형형
    ├── 블렌딩 (MV+RP)
    ├── 모멘텀
    └── 시가총액
        ↓
한국 세금 계산 (양도세 22%, ISA 비과세 시뮬레이션)
        ↓
NVO 투자 신호 분석 (RSI + 이동평균 + 뉴스 감성)
        ↓
LLM 리포트 생성 (Groq API → 한국어 투자 요약)
```

<!-- 파이프라인 이미지 삽입 권장 위치 -->
<!-- ![Pipeline Diagram](images/pipeline.png) -->

---

## Getting Started / 실행 방법

```bash
git clone https://github.com/sujin809/portfolio-optimizer.git
cd portfolio-optimizer
pip install -r requirements.txt
```

`.env` 파일을 프로젝트 루트에 생성하고 Groq API 키를 입력하세요:

```
GROQ_API_KEY=your_groq_api_key_here
```

이후 `main.ipynb`를 실행하면 전체 파이프라인이 순서대로 동작합니다.

---

## Key Result / 핵심 결과

> 백테스팅 기간: 2020~2026 | 월 투자금: ₩300,000 | 유니버스: 미국 주식 7종 + ETF 4종

**시가총액 전략이 수익률 266.4%, 샤프 1.88로 가장 우수한 성과를 기록.**  
ETF 균형형은 MDD -6.54%로 가장 안정적인 하방 방어력을 보임.

| 전략 | 수익률 | 샤프 비율 | MDD |
|------|--------|-----------|-----|
| ETF 균형형 | 63.9% | 1.85 | -6.54% |
| 블렌딩 (MV+RP) | 191.3% | 1.86 | -20.72% |
| 모멘텀 | 155.8% | 1.84 | -19.01% |
| 시가총액 | **266.4%** | **1.88** | -24.49% |

![4가지 전략 포트폴리오 가치 및 수익률 비교](images/06_4strategy_compare.png)

> 상세 결과는 [`results/`](./results/) 폴더를 참고하세요.

---

## Project Overview / 프로젝트 개요

이 프로젝트의 핵심은 **한국 투자자 현실을 반영한 세금 시뮬레이션**입니다.  
단순 수익률 비교에서 끝나지 않고, 양도세 22%와 ISA 계좌 절세 효과를 직접 계산해 **실질 수익**을 비교합니다.

| 항목 | ETF 균형형 | 블렌딩 (MV+RP) |
|------|-----------|--------------|
| 총 투자 원금 | 2,310만원 | 2,310만원 |
| 세전 최종 자산 | 3,786만원 | 6,729만원 |
| 일반 계좌 세금 (양도세 22%) | 270만원 | 917만원 |
| ISA 계좌 세금 | 126만원 | 418만원 |
| **ISA 절세 효과** | **143만원** | **499만원** |

---

## Universe / 투자 유니버스

### 개별 주식 (7종목)

| Sector | Tickers |
|--------|---------|
| Technology | AAPL, MSFT, GOOGL, META, NVDA |
| Consumer | AMZN, TSLA |

**블렌딩 비중 (최소분산 + 리스크패리티):**

| Ticker | 최소분산 | 리스크패리티 | 블렌딩 |
|--------|---------|------------|------|
| AAPL | 25.2% | 17.2% | **21.2%** |
| GOOGL | 33.7% | 17.3% | **25.5%** |
| MSFT | 20.5% | 16.8% | **18.6%** |
| NVDA | 5.7% | 15.4% | **10.5%** |
| AMZN | 5.0% | 13.0% | **9.0%** |
| META | 5.0% | 10.4% | **7.7%** |
| TSLA | 5.0% | 9.9% | **7.5%** |

### ETF 포트폴리오

| ETF | 설명 | Ann. Return | Ann. Volatility |
|-----|------|-------------|-----------------|
| QQQ | 나스닥 100 추종 | 22.18% | 24.98% |
| SPY | S&P 500 추종 | 16.35% | 20.43% |
| SCHD | 배당 성장 ETF | 13.06% | 19.03% |
| BND | 미국 채권 ETF | 1.07% | 6.54% |

---

## Tech Stack / 기술 스택

| Category | Libraries |
|----------|-----------|
| Data | `yfinance`, `pandas`, `numpy` |
| Optimization | `scipy`, `cvxpy` |
| Visualization | `matplotlib`, `seaborn` |
| LLM | `groq` (llama-3.3-70b-versatile) |

---

## File Structure

```
portfolio-optimizer/
├── main.ipynb        # 메인 노트북 — 전체 파이프라인
├── portfolio.py      # 포트폴리오 최적화 모듈
├── backtest.py       # 백테스팅 함수
├── visualize.py      # 시각화 함수
├── tax.py            # 세금 계산 모듈
├── report.py         # LLM 리포트 생성
├── .env              # API 키 설정 (미업로드)
├── images/           # 차트 이미지
├── results/          # 상세 결과 (전략별 md)
└── README.md
```

---

## Author

**정수진 (Sujin Jeong)**  
Industrial Engineering + Biomedical Engineering (Minor), UNIST  
Founder, FIC (Finance Investment Club — UNIST, KAIST, POSTECH, DGIST, GIST)  
GitHub: [@sujin809](https://github.com/sujin809)
