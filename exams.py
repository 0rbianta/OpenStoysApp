from threading import Thread
from time import sleep

from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen

import Helper
from Broadcast import Broadcast
from StoysAPI import Stoys


class ExamsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.content_area = None

        self.broadcasting = Broadcast("exams", self.load_screen)
        self.loading_window = Helper.popup_loading()

        # Thread(target=self.load_screen, args=(0,)).start()

    def load_screen(self, last_update):
        try:
            self.loading_window.open()
            self.content_area = self.ids["content_area"]

            self.content_area.clear_widgets()

            exams_data = Stoys.get_exam_calendar(Helper.get_auth(), Helper.get_student_id(),
                                                 Stoys.Date.dateFormat11.create_stoys_adapted_date("0", "0", "0"),
                                                 Stoys.Date.dateFormat11.create_stoys_date_with_current_time())["result"]

            ecs = []
            for exam in exams_data:
                baslik = exam["baslik"]
                baslangic_tarihi = exam["baslangic_tarihi"]

                ec = ExamCard()
                ec.baslik = baslik
                ec.baslangic_tarihi = baslangic_tarihi

                ecs.append(ec)
                # self.content_area.add_widget(ec)
        except:
            pass

        def s(ec):
            return ec.baslangic_tarihi

        ecs.sort(key=s, reverse=True)
        for ec in ecs:
            self.content_area.add_widget(ec)

        self.loading_window.dismiss()

class ExamCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
