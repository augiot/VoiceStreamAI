import requests
import time
s_time = time.time()
input_audio = "/mnt/user2/workspace/Aug/code/Chat/exp/VoiceStreamAI/zhang-7-0.mp3"
with open(input_audio, 'rb') as f:
    response = requests.post(
        'http://10.20.216.187:8007/transcribe/', 
        files={'file': ('output.mp3', f, 'audio/mp3')})
data = response.json()  # Get the JSON response
text = data['transcription'][1]['text']
e_time = time.time()
print("识别时间：", e_time - s_time)
print("识别结果：", text)
