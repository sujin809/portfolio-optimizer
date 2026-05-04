from config import (
    GENERAL_TAX_RATE, ISA_TAX_RATE,
    GENERAL_DEDUCTION, ISA_DEDUCTION
)

def calculate_general_tax(profit):
    """일반 계좌 양도소득세 계산"""
    taxable = max(0, profit - GENERAL_DEDUCTION)
    tax = taxable * GENERAL_TAX_RATE
    return tax

def calculate_isa_tax(profit):
    """ISA 계좌 세금 계산"""
    taxable = max(0, profit - ISA_DEDUCTION)
    tax = taxable * ISA_TAX_RATE
    return tax

def get_tax_report(performance):
    """세금 비교 리포트"""
    profit = performance['총 수익']
    final_value = performance['최종 자산']
    total_invested = performance['투자 원금']

    general_tax = calculate_general_tax(profit)
    isa_tax = calculate_isa_tax(profit)
    tax_saving = general_tax - isa_tax

    report = {
        '총 투자 원금': total_invested,
        '세전 최종 자산': final_value,
        '총 수익': profit,
        '수익률': performance['수익률'],
        '샤프 비율': performance['샤프 비율'],
        'MDD': performance['MDD'],
        '일반 계좌 세금': general_tax,
        'ISA 계좌 세금': isa_tax,
        '일반 계좌 세후 자산': final_value - general_tax,
        'ISA 계좌 세후 자산': final_value - isa_tax,
        'ISA 절세 효과': tax_saving,
    }

    print("=" * 45)
    for k, v in report.items():
        if k in ['수익률', '샤프 비율', 'MDD']:
            print(f"{k:20} {v:.2f}")
        else:
            print(f"{k:20} {v/10000:>10,.0f}만원")
    print("=" * 45)

    return report