# -*- coding: utf-8 -*-
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=str(GROQ_API_KEY))

def generate_report(etf_tax_report, stock_tax_report, blend_weights, stocks, comparison_df):
    """Groq LLM으로 최종 투자 리포트 생성"""
    
    weight_str = ', '.join([f"{t} {w*100:.1f}%" 
                            for t, w in zip(stocks, blend_weights)])
    
    # 비교 테이블 문자열로 변환
    comparison_str = comparison_df.to_string()
    
    prompt = f"""
당신은 한국인 투자자를 위한 전문 금융 어드바이저입니다.
반드시 한국어로만 작성해주세요. 다른 언어를 절대 사용하지 마세요.

[4가지 전략 성과 비교]
{comparison_str}

[ETF 균형형 세금 정보]
- 총 원금: {etf_tax_report['총 투자 원금']/10000:,.0f}만원
- 세전 최종 자산: {etf_tax_report['세전 최종 자산']/10000:,.0f}만원
- ISA 세후 자산: {etf_tax_report['ISA 계좌 세후 자산']/10000:,.0f}만원
- ISA 절세 효과: {etf_tax_report['ISA 절세 효과']/10000:,.0f}만원

[개별주식 블렌딩 세금 정보]
- 총 원금: {stock_tax_report['총 투자 원금']/10000:,.0f}만원
- 세전 최종 자산: {stock_tax_report['세전 최종 자산']/10000:,.0f}만원
- ISA 세후 자산: {stock_tax_report['ISA 계좌 세후 자산']/10000:,.0f}만원
- ISA 절세 효과: {stock_tax_report['ISA 절세 효과']/10000:,.0f}만원

[핵심 인사이트]
- 샤프 비율이 모든 전략에서 1.85~1.87로 유사함
- 수익률이 높은 전략일수록 MDD도 커짐
- 모멘텀 전략은 백테스팅 과적합 가능성 있음

반드시 한국어로만 아래 형식으로 작성해주세요:

📊 4가지 전략 종합 비교
(수익률, 샤프 비율, MDD를 종합한 분석. 샤프 비율이 비슷한 이유 설명)

💡 전략별 장단점
(각 전략의 실전 적용 시 장단점)

⚠️ 백테스팅의 한계
(과적합 문제, 미래 수익 보장 불가, 거래비용 미반영 등)

🎯 투자자 유형별 추천
(초보/중급/고급 투자자별 추천 전략과 이유)

🏦 절세 전략
(ISA 계좌, 연금저축펀드 구체적 활용법)
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

