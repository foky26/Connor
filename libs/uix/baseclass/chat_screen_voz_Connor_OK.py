from kivy.animation import Animation
from kivy.properties import DictProperty, ListProperty, StringProperty
from components.boxlayout import PBoxLayout
from components.dialog import PDialog
from components.screen import PScreen
from components.toast import toast
from characterai import PyCAI
import re
import threading
from elevenlabs import generate, play, set_api_key, voices, Models
import pygame
import os
import requests


class ChatScreen(PScreen):

    user = DictProperty()
    title = StringProperty()
    chat_logs = ListProperty()
    token = '75f9f46ba4e6796e9169c40902334062c78936a6'
    character = StringProperty()
    client = PyCAI(token)
    habla=""


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        d = threading.Thread(target=self.daemon, daemon=True)
        d.start()

    def daemon(self):
        while True:
              if self.habla!="":
                  eleven_api_key = '2e427e0d0c8aeb4bb82d252ff09d03dc'
                  set_api_key(eleven_api_key)
                  voice_list = voices()
                  selected_voice_id = voice_list[10].voice_id
                  pygame.mixer.init()
                  fichero = "output.mp3"
                  nm=0
                  CHUNK_SIZE = 1024
                  url = "https://api.elevenlabs.io/v1/text-to-speech/" + selected_voice_id
                  headers = {
                          "Accept": "audio/mpeg",
                          "Content-Type": "application/json",
                          "xi-api-key": eleven_api_key
                      }
                  data = {
                          "text": self.habla,
                          "model_id": "eleven_multilingual_v1",
                          "voice_settings": {
                              "stability": 0.4,
                              "similarity_boost": 1.0
                          }
                      }
                  try:
                        response = requests.post(url, json=data, headers=headers)
                        f = open(fichero, 'wb')
                        with f:
                            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                              if chunk:
                                  f.write(chunk)
                        f.close()
                        pygame.mixer.music.load(fichero)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            nm = nm
                  except:
                        pass

                  self.habla = ""
                  pygame.mixer.quit()
                  try:
                     os.remove(fichero)
                  except:
                      self.habla = ""



    def send(self, text):
        if not text:
            toast("Escribe algo!")
            return

        salida= {"name":self.title,"text": text, "send_by_user": True, "pos_hint": {"right": 1}}
        self.chat_logs.append(salida)
        self.manager.get_screen("home").conversacion.append(salida)
        self.scroll_to_bottom()



    def receive(self, text):
        while self.habla!="":
            a=0
        if text:
            self.ids.field.text = ""
            try:
                respuesta = self.client.chat.send_message(self.character, text, wait=True)
                texto = respuesta['replies'][0]['text']
                texto = texto.replace("\n", " ")
                texto = re.sub("\*.*?\*", "", texto)
                texto = texto.replace("\"", "")
                texto = texto.replace(". ", ".\n")
                texto = texto.replace("? ", "?\n")
                texto = texto.replace("! ", "!\n")
            except:
                texto=""

            salida={"name":self.title,
            "text": texto,
            "send_by_user": False,
             }

            self.chat_logs.append(salida)
            self.manager.get_screen("home").conversacion.append(salida)

            self.habla=texto

            self.scroll_to_bottom()








    def show_user_info(self):
        PDialog(
            content=UserInfoDialogContent(
                title=self.user["name"],
                image=self.user["image"],
                about=self.user["about"],
            )
        ).open()

    def scroll_to_bottom(self):
        rv = self.ids.chat_rv
        box = self.ids.box
        if rv.height < box.height:
            Animation.cancel_all(rv, "scroll_y")
            Animation(scroll_y=0, t="out_quad", d=0.5).start(rv)



class UserInfoDialogContent(PBoxLayout):
    title = StringProperty()
    image = StringProperty()
    about = StringProperty()

