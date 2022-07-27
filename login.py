from threading import Thread

import requests.exceptions
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

import Helper
from StoysAPI import Stoys
from KivyStorage import Storage


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def login_check(self, username, password):
        try:
            res = Stoys.login(username, password)

            if res["error"]["err"] == 0:
                Storage.put("login_data", username=username, password=password)
                Helper.screen_manager.current = "main_screen"
                Helper.create_signal_load_screen("home")
            else:
                Snackbar(text="These credentials do not match our records.").open()
        except requests.exceptions.ConnectionError:
            Snackbar(text="Please check your connection.").open()
        except KeyError:
            Snackbar(text="These credentials do not match our records.").open()
        except:
            Snackbar(text="An error acquired.").open()

    def login_button_clicked(self, username, password):
        Thread(target=self.login_check, args=(username, password,)).start()
