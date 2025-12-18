import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.agent_factory import create_gemini_agent
from services.tts_utils import speak

# 1. 에이전트 초기화
# 💡 이 과정에서 LLM, 도구, 페르소나가 모두 로드됩니다.
AGENT = create_gemini_agent()

# 2. 메인 실행 함수
def run_agent_tts(prompt: str):
    print(f"\n==========================================")
    print(f"🗣️ 사용자 요청: {prompt}")
    print(f"==========================================\n")

    try:
        # 에이전트 실행 (LangGraph 기반의 create_agent.invoke)
        # 💡 최신 버전의 create_agent는 메시지 리스트를 상태로 받습니다.
        result = AGENT.invoke(
            {
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )
        
        # 결과에서 최종 메시지 내용 추출
        final_message = result["messages"][-1]
        final_answer = final_message.content

        print("\n--- ✨ 최종 응답 ---")
        print(final_answer)
        print("--------------------")
        
        # 3. TTS 재생
        print("\n🎧 음성 재생 시작...")
        speak(final_answer)
        
        return final_answer
        
    except Exception as e:
        error_msg = f"❌ 에이전트 실행 중 오류: {e}"
        print(error_msg)
        speak("에이전트 실행 중 오류가 발생했습니다.")
        return error_msg

# ====================================================================
# 프로그램 시작
# ====================================================================

if __name__ == "__main__":
    # 💡 실행 전, GEMINI_API_KEY 환경 변수가 설정되어 있는지 확인하세요.
    if os.getenv("GEMINI_API_KEY"):
        # 단순 대화 요청 (페르소나 테스트)
        run_agent_tts("야, 너 어제 뭐 했어?")
    else:
        print("⚠️ 실행 불가: GEMINI_API_KEY 환경 변수를 먼저 설정해야 합니다.")