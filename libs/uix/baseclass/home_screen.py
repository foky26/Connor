import json
from kivy.properties import ListProperty

from components.boxlayout import PBoxLayout
from components.dialog import PDialog
from components.screen import PScreen
import datetime



class HomeScreen(PScreen):



    chats = ListProperty()
    conversacion=ListProperty()
    conv_chateo = ListProperty()

    hora_actual = datetime.datetime.now()
    hora_formateada = hora_actual.strftime('%H:%M')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conversacion = []
        self.conv_chateo=[]
        with open("assets/users.json") as f:
            self.data = json.load(f)

        for i in self.data:
            user_data = {
                "text": i,
                "secondary_text": self.data[i]["message"],
                "time": self.hora_formateada,
                "image": self.data[i]["image"],
                "char": self.data[i]["char"],
                "unread_messages": self.data[i]["unread_messages"],
                "on_release": lambda x={
                    "name": i,
                    **self.data[i],
                }: self.goto_chat_screen(x),
            }
            self.chats.append(user_data)
            self.conversacion.append({"name":i,"text":self.data[i]["message"],"send_by_user":False,})
            self.conv_chateo.append({"name": i, "role": "system","content": "Tienes que contestar y comportate como si fueras el androide Connor de Detroit Become Human. Da respuestas no muy largas.", })

    def goto_chat_screen(self, user):
        self.manager.set_current("chat")
        chat_screen = self.manager.get_screen("chat")
        chat_screen.user = user
        chat_screen.character=user["char"]
        chat_screen.habla=""
        chat_screen.chat_logs = []
        chat_screen.chateo=[]
        try:
            for item in self.conversacion:
             for i in item:
                if item[i]==user["name"]:
                    chat_screen.chat_logs.append(item)

        except:
             pass

        try:
            for item in self.conv_chateo:
                    for i in item:
                          if item[i] == user["name"]:
                              chat_screen.chateo.append({"role":"user", "content":item['content']})
        except:
             pass


        chat_screen.title = user["name"]


    def show_menu(self):
        PDialog(content=MenuDialogContent()).open()


class MenuDialogContent(PBoxLayout):
    pass
