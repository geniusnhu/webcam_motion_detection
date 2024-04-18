import base64


def get_base64_encoded_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        audio_encoded = base64.b64encode(audio_file.read()).decode('utf-8')
    return f"data:audio/x-wav;base64,{audio_encoded}"
