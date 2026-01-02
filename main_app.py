import os
import sys
from PyQt6 import QtWidgets, uic, QtCore

# 기존 main_app.py의 경로 설정 로직 유지
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)

# 에이전트 및 TTS 임포트
from agents.agent_factory import create_gemini_agent
from services.tts_utils import speak

class ChatApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. UI 로드 (testui.ui 파일 위치 확인)
        ui_file = get_resource_path("testui.ui")
        uic.loadUi(ui_file, self)

        # 2. API 키 확인 및 설정 (GUI 버전)
        self.check_api_key()

        # 3. 에이전트 초기화
        try:
            self.agent = create_gemini_agent()
            self.textBrowser.append("<b>✨ 시스템:</b> 제미나이가 대화 준비를 마쳤어!")
        except Exception as e:
            self.textBrowser.append(f"<span style='color:red;'>❌ 초기화 실패: {e}</span>")

        # 4. 시그널 연결
        self.pushButton.clicked.connect(self.handle_send)
        self.textEdit.installEventFilter(self)
        # Enter 키 입력 시 전송 (textEdit가 아니라 QLineEdit일 경우 더 쉬움, 여기선 버튼 클릭 위주)
        
        # 💡 대화 기록을 저장할 리스트 생성
        self.chat_history = []

        self.show()

    def check_api_key(self):
        """환경 변수에 키가 없으면 팝업창으로 입력받음"""
        if not os.getenv("GEMINI_API_KEY"):
            key, ok = QtWidgets.QInputDialog.getText(
                self, "API Key 필요", "Gemini API Key가 없네! 입력해줄래?"
            )
            if ok and key:
                os.environ["GEMINI_API_KEY"] = key
            else:
                QtWidgets.QMessageBox.critical(self, "오류", "API 키가 없으면 실행할 수 없어.")
                sys.exit()

    def format_message(self, sender, message, align="left"):
        # 배경색 및 정렬 설정
        if align == "right":  # 나 (오른쪽)
            bg_color = "#fee500" # 노란색
            table_align = "right" # 전체 테이블 내의 정렬
            bubble_margin = "margin-left: 60px;" # 왼쪽 여백
        else:  # 친구 (왼쪽)
            bg_color = "#ffffff" # 흰색
            table_align = "left"
            bubble_margin = "margin-right: 60px;" # 오른쪽 여백

        # 2. 중첩 테이블 구조:
        # 바깥 테이블(width: 100%)은 왼쪽/오른쪽 정렬을 잡고,
        # 안쪽 테이블(width 없음)은 글자 크기만큼만 늘어납니다.
        return f"""
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-bottom: 10px;">
            <tr>
                <td align="{table_align}">
                    <table border="0" cellspacing="0" cellpadding="0" 
                        style="background-color: {bg_color}; 
                                padding: 8px 12px;
                                border: 1px solid #d0d0d0;
                                border-radius: 12px; 
                                {bubble_margin}">
                        <tr>
                            <td style="padding: 10px; font-family: 'Malgun Gothic';">
                                <span style="font-size: 9pt; color: #555555;"><b>{sender}</b></span><br>
                                <span style="font-size: 11pt; color: #000000; line-height: 130%;">{message}</span>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
        """

    def handle_send(self):
        prompt = self.textEdit.toPlainText().strip()
        if not prompt: return

        # 1. 내 메시지 추가 (오른쪽)
        user_html = self.format_message("나", prompt, align="right")
        self.textBrowser.append(user_html) # 💡 반드시 append 사용!
        self.textEdit.clear()

        # 에이전트 실행 로직...
        self.process_agent_response(prompt)

    def process_agent_response(self, prompt):
        try:
            # 1. 사용자 메시지를 대화 기록에 추가
            self.chat_history.append({"role": "user", "content": prompt})

            # 2. 에이전트 호출 (전체 대화 기록 전달)
            result = self.agent.invoke(
                {
                    "messages": self.chat_history # 💡 단일 메시지가 아닌 전체 기록을 보냅니다.
                }
            )
            
            # 3. 에이전트 답변 추출 로직 (기존 유지)
            raw_content = result["messages"][-1].content
            
            if isinstance(raw_content, list):
                final_answer = "".join([part.get('text', '') for part in raw_content if isinstance(part, dict)])
            else:
                final_answer = str(raw_content)

            # 4. AI 답변도 대화 기록에 추가 (다음 대화를 위해 기억)
            self.chat_history.append({"role": "assistant", "content": final_answer})

            # 5. UI 업데이트 (말풍선 표시)
            ai_html = self.format_message("제미나이", final_answer, align="left")
            self.textBrowser.append(ai_html)
            
            # 스크롤 최하단 이동 및 음성 출력
            self.textBrowser.moveCursor(self.textBrowser.textCursor().MoveOperation.End)
            speak(final_answer)

        except Exception as e:
            error_msg = f"❌ 오류 발생: {e}"
            self.textBrowser.append(f"<span style='color:red;'>{error_msg}</span>")
            speak("미안, 오류가 좀 났어.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ChatApp()
    sys.exit(app.exec())