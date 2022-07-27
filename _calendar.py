import datetime
from threading import Thread
from time import sleep

from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.screen import MDScreen

import Helper
from Broadcast import Broadcast
from StoysAPI import Stoys


class CalendarScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.today = datetime.datetime.today()
        self.date_picker = MDDatePicker(self.today.year, self.today.month, self.today.day)
        self.date_picker.bind(on_save=self.on_date_picker_choose)

        self.content_area = None
        self.selected_date_info = None
        self.current_selected_date = self.today.strftime("%Y-%m-%d")
        self.broadcasting = Broadcast("calendar", self.load_screen)
        self.loading_window = Helper.popup_loading()

        # Thread(target=self.load_screen, args=(0,)).start()
        # Clock.schedule_once(self.load_screen, 2)
        # Thread(target=self.load_screen, args=(0,)).start()

    def load_screen(self, last_update):
        try:
            self.loading_window.open()
            self.content_area = self.ids["content_area"]
            self.selected_date_info = self.ids["selected_date_info"]
            self.today = datetime.datetime.today()

            self.selected_date_info.text = "Showing activities for " + self.current_selected_date

            calendar_data = \
                Stoys.get_academic_calendar(Helper.get_auth(), Helper.get_student_id(), Helper.get_user_id())[
                    "result"]

            calendar_data.reverse()

            self.content_area.clear_widgets()

            added_count = 0

            for activity in calendar_data:
                baslangic_tarihi = activity["baslangic_tarihi"]
                bitis_tarihi = activity["bitis_tarihi"]
                baslik = activity["baslik"]
                aciklama = activity["aciklama"]

                cac = CalendarActivityCard()

                if Helper.is_server_data_none(bitis_tarihi):
                    continue

                if int(bitis_tarihi.replace("-", "")) >= int(self.current_selected_date.replace("-", "")):
                    if not Helper.is_server_data_none(baslik):
                        cac.title = baslik
                    if not Helper.is_server_data_none(bitis_tarihi):
                        cac.end_date = bitis_tarihi
                    if not Helper.is_server_data_none(aciklama):
                        cac.description = Helper.resize_description_text(aciklama)

                    cac.start_date = baslangic_tarihi

                    self.content_area.add_widget(cac)
                    added_count += 1

                if added_count >= 5:
                    break

        except:
            pass
        self.loading_window.dismiss()

    def on_choose_date_clicked(self):
        self.date_picker.open()

    def on_date_picker_choose(self, date_picker, date, _):
        date = str(date)
        self.selected_date_info.text = "Showing activities for " + date
        self.current_selected_date = str(date)
        Thread(target=self.load_screen, args=(0,)).start()


class CalendarActivityCard(MDCard):
    pass
