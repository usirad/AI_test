import pyttsx3

_tts_engine = pyttsx3.init()

# 💡 한국어 목소리 설정 함수 (옵션)
def _set_korean_voice(engine):
    """사용 가능한 한국어 목소리를 찾아 설정합니다."""
    voices = engine.getProperty('voices')
    for voice in voices:
        # 시스템에 따라 한국어 목소리 이름이 다를 수 있습니다.
        if 'korean' in voice.name.lower() or 'ko-kr' in voice.id.lower():
            engine.setProperty('voice', voice.id)
            print(f"🎤 TTS 목소리 설정 완료: {voice.name}")
            return
    print("⚠️ 한국어 목소리를 찾을 수 없습니다. 기본 목소리로 진행합니다.")

_set_korean_voice(_tts_engine)

def speak(text: str):
    """텍스트를 음성으로 출력합니다."""
    _tts_engine.say(text)
    _tts_engine.runAndWait()
    print("✅ 음성 재생 종료.")