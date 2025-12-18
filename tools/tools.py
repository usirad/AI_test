from langchain.tools import tool

@tool
def calculate(expression: str) -> float:
    """
    제공된 수학 표현식(예: '73840 * 0.26 + 15300')을 계산하고 결과를 부동소수점(float)으로 반환합니다.
    이 도구는 복잡하거나 정확한 수학 문제나 계산이 필요할 때 사용됩니다.
    
    인수(argument): 
        expression (str): 계산할 유효한 단일 수학 표현식 문자열입니다.
    """
    try:
        clean_expression = expression.replace(',', '').strip()
        result = eval(clean_expression) 
        return float(result)
    except Exception as e:
        return f"계산 오류 발생: {e}. 수식이 유효한지 확인하세요."

# 💡 향후 여기에 web_search, get_weather 등 다른 도구를 추가할 수 있습니다.
ALL_TOOLS = [calculate]