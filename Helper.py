import base64
from io import BytesIO

import requests
from kivy.core.image import Image
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.label import MDLabel

import home
from StoysAPI import Stoys
from KivyStorage import Storage

screen_manager = ScreenManager()
broadcast = []


def resize_description_text(description, text_size=170):
    if len(description) > text_size:
        return description[:text_size] + "..."

    return description


class popup_loading(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.content = MDLabel(text="Loading...", theme_text_color="Custom", text_color=(1, 1, 1, 1))
        self.size_hint = (None, None)
        self.size = (dp(150), dp(90))
        self.title = ""
        self.auto_dismiss = False

    def m_open(self):
        self.open()

    def m_close(self):
        self.dismiss()


def on_internet_connected():
    if broadcast != []:
        broadcast.append(broadcast[len(broadcast) - 1])


def is_server_data_none(value):
    return value is None or value == "" or value == "null" or value == "nil" or \
           value == "None" or value == b'\x00'


def base64_to_kivy_texture(encoded_image):
    pixels = BytesIO(base64.b64decode(bytes(encoded_image, "utf-8")))
    pixels.seek(0)
    core_image = Image(BytesIO(pixels.read()), ext="png")
    return core_image.texture


def create_signal_load_screen(screen_name):
    broadcast.append(f"reload_required_{screen_name}")


def get_user_id():
    try:
        login_data = Storage.get("login_data")
        return Stoys.login(login_data["username"], login_data["password"])["result"]["user_id"]
    except:
        return None


def get_student_id():
    try:
        login_data = Storage.get("login_data")
        return Stoys.login(login_data["username"], login_data["password"])["result"]["student_id"]
    except:
        return None


def get_auth():
    try:
        login_data = Storage.get("login_data")
        return Stoys.login(login_data["username"], login_data["password"])["result"]["token"]
    except:
        return None


def check_connection():
    try:
        requests.get("https://api.stoys.co")
        return True
    except:
        return False
