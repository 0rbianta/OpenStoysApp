from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

import Helper
import login
import home
import homeworks
import exams
import profile
import _calendar
from KivyStorage import Storage


class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class App(MDApp):

    def __init__(self, **kwargs):
        super(App, self).__init__(**kwargs)

        Builder.load_file("./Screens/home.kv")
        Builder.load_file("./Screens/homeworks.kv")
        Builder.load_file("./Screens/exams.kv")
        Builder.load_file("./Screens/profile.kv")
        Builder.load_file("./Screens/calendar.kv")

        Helper.screen_manager.add_widget(Builder.load_file("./Screens/login.kv"))
        Helper.screen_manager.add_widget(Builder.load_file("./Screens/main.kv"))
        Helper.screen_manager.add_widget(Builder.load_file("./Screens/no_connection.kv"))

        Helper.screen_manager.current = "login_screen"

        self.screen_before_no_connection = None

        try:
            login_data = Storage.get("login_data")
            if not (login_data["username"] is None and login_data["password"] is None):
                Helper.screen_manager.current = "main_screen"
        except KeyError:
            pass
        except:
            pass

        Clock.schedule_interval(self.internet_checker, 4)

    def internet_checker(self, _):
        if not Helper.check_connection():
            if self.screen_before_no_connection is None:
                self.screen_before_no_connection = Helper.screen_manager.current
            Helper.screen_manager.current = "no_connection"
        elif Helper.screen_manager.current == "no_connection":
            Helper.on_internet_connected()
            Helper.screen_manager.current = self.screen_before_no_connection
            self.screen_before_no_connection = None

    def build(self):
        return Helper.screen_manager

    def on_pause(self):
        pass


if __name__ == "__main__":
    App().run()
