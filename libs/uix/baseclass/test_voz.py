import pyttsx3 as voz

engine = voz.init()
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)
engine.runAndWait()
for voice in voices:
   engine.setProperty('voice', voice.id)
   print(voice.id)
   engine.say('Hola me llamo Connor y soy el androide enviado por CyberLife.')
   engine.runAndWait()