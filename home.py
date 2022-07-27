from threading import Thread
from time import sleep

from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen

from Broadcast import Broadcast
import Helper
from StoysAPI import Stoys


class ActivityCard(MDCard):
    pass


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.profile_image = None
        self.profile_name_surname = None
        self.profile_no = None
        self.profile_class = None
        self.profile_school = None
        self.content_area = None
        self.broadcasting = Broadcast("home", self.load_screen)
        self.loading_window = Helper.popup_loading()

        Clock.schedule_once(self.load_screen, 1)
        # Thread(target=self.load_screen, args=(0,)).start()

    def load_screen(self, last_update):
        acs = []
        try:
            self.loading_window.open()
            self.profile_image = self.ids["student_card"].ids["profile_image"]
            self.profile_name_surname = self.ids["student_card"].ids["profile_name_surname"]
            self.profile_no = self.ids["student_card"].ids["profile_no"]
            self.profile_class = self.ids["student_card"].ids["profile_class"]
            self.profile_school = self.ids["student_card"].ids["profile_school"]

            user_data = Stoys.get_guardian(Helper.get_auth())["result"][0]
            self.profile_image.texture = Helper.base64_to_kivy_texture(user_data["avatar"])
            self.profile_name_surname.text = user_data["fullname"]
            self.profile_no.text = user_data["student_no"]
            self.profile_class.text = user_data["grade_name"]
            self.profile_school.text = user_data["branch_name"]

            self.content_area = self.ids["content_area"]

            calendar_data = \
                Stoys.get_academic_calendar(Helper.get_auth(), Helper.get_student_id(), Helper.get_user_id())[
                    "result"]

            self.content_area.clear_widgets()

            for idx, activity in enumerate(calendar_data):
                baslangic_tarihi = activity["baslangic_tarihi"]
                bitis_tarihi = activity["bitis_tarihi"]
                baslik = activity["baslik"]
                aciklama = activity["aciklama"]

                ac = ActivityCard()

                if Helper.is_server_data_none(bitis_tarihi):
                    continue

                if not Helper.is_server_data_none(baslik):
                    ac.title = baslik
                if not Helper.is_server_data_none(bitis_tarihi):
                    ac.end_date = bitis_tarihi
                if not Helper.is_server_data_none(aciklama):
                    ac.description = Helper.resize_description_text(aciklama)

                ac.start_date = baslangic_tarihi


                acs.append(ac)
                # self.content_area.add_widget(ac)

                if idx > 10:
                    break
        except:
            pass


        def s(ac):
            return ac.start_date

        acs.sort(key=s, reverse=True)

        for ac in acs:
            self.content_area.add_widget(ac)

        self.loading_window.dismiss()