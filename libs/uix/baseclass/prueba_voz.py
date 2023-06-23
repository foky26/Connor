import io
import json
from elevenlabslib.helpers import *
from elevenlabslib import *

eleven_api_key = '2e427e0d0c8aeb4bb82d252ff09d03dc'
user = ElevenLabsUser(eleven_api_key)
voice=user.get_available_voices()[10]
print(voice.voiceID)
print(voice.get_name())

voice.generate_and_stream_audio("Hola soy Connor", model_id = 'eleven_multilingual_v1')

