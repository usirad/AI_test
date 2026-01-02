import pyttsx3

def speak(text: str):
    """텍스트를 음성으로 출력합니다. (매 호출 시 엔진 초기화)"""
    try:
        # 1. 호출될 때마다 엔진 인스턴스를 새로 생성합니다.
        # 이렇게 하면 이전 대화의 엔진 상태가 꼬이는 것을 방지할 수 있습니다.
        engine = pyttsx3.init()
        
        # 2. 한국어 목소리 설정 (기존 로직 유지)
        voices = engine.getProperty('voices')
        korean_voice_id = None
        for voice in voices:
            if 'korean' in voice.name.lower() or 'ko-kr' in voice.id.lower():
                korean_voice_id = voice.id
                break
        
        if korean_voice_id:
            engine.setProperty('voice', korean_voice_id)
        
        # 속도 조절 (너무 빠르면 말을 씹을 수 있음)
        engine.setProperty('rate', 180) 

        # 3. 재생 및 대기
        engine.say(text)
        engine.runAndWait()
        
        # 4. 사용 후 명시적으로 정지 및 삭제
        engine.stop()
        del engine
        print("✅ 음성 재생 종료.")
        
    except Exception as e:
        print(f"❌ TTS 오류 발생: {e}")