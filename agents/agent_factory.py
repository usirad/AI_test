from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from tools.tools import ALL_TOOLS # 도구 임포트
from services.persona import SYSTEM_INSTRUCTION # 페르소나 임포트

def create_gemini_agent():
    """
    Gemini 모델과 정의된 도구, 페르소나를 사용하여 LangChain 에이전트 객체를 생성합니다.
    """
    try:
        # LLM 모델 인스턴스 생성
        # temperature=0으로 설정하여 논리적이고 안정적인 도구 사용을 유도합니다.
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        
        # create_agent를 사용하여 에이전트 구축
        agent = create_agent(
            model=llm,
            tools=ALL_TOOLS, # 도구 목록 전달
            system_prompt=SYSTEM_INSTRUCTION # 페르소나 전달
        )
        
        print("🤖 LangChain 에이전트 객체 생성 완료.")
        return agent
        
    except Exception as e:
        print(f"❌ 에이전트 생성 오류: {e}")
        # config.py의 ValueError가 발생할 경우 여기서 처리되거나, config.py에서 바로 종료됩니다.
        raise