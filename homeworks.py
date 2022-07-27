import webbrowser
from threading import Thread
from time import sleep

from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen

import Helper
from Broadcast import Broadcast
from StoysAPI import Stoys

homework_detail_popup = Popup(title="Details")


class HomeworksScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.content_area = None

        self.broadcasting = Broadcast("homeworks", self.load_screen)
        self.loading_window = Helper.popup_loading()

        # Thread(target=self.load_screen, args=(0,)).start()

    def load_screen(self, last_update):
        homework_uis = []
        try:
            self.loading_window.open()
            self.content_area = self.ids["content_area"]

            self.content_area.clear_widgets()
            homeworks_data = Stoys.get_homeworks(Helper.get_auth(), Helper.get_student_id())["result"]
            for homework in homeworks_data:
                title = homework["title"]
                description = homework["description"]
                start_date = homework["start_date"]
                end_date = homework["end_date"]
                content_id = homework["content_id"]

                # Error
                homework_ui = HomeworkCard()
                homework_ui.title = title
                homework_ui.description = Helper.resize_description_text(description)
                homework_ui.start_date = start_date
                homework_ui.end_date = end_date
                homework_ui.content_id = content_id

                homework_uis.append(homework_ui)
                # self.content_area.add_widget(homework_ui)
        except:
            pass


        def s(hui):
            return hui.start_date

        homework_uis.sort(key=s, reverse=True)
        for homework_ui in homework_uis:
            self.content_area.add_widget(homework_ui)


        self.loading_window.dismiss()

class HomeworkDetails(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def close_homework_detail_click(self):
        homework_detail_popup.dismiss()

    def on_download_clicked(self, url):
        webbrowser.open(url)


class HomeworkCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_homework_detail_click(self, content_id):
        hwd = HomeworkDetails()
        homework_data = Stoys.get_homework_details(Helper.get_auth(), Helper.get_student_id(), content_id)["result"][
            "data"]
        hwd.title = homework_data["title"]
        hwd.aciklama = homework_data["aciklama"]
        hwd.start_date = homework_data["start_date"]
        hwd.end_date = homework_data["end_date"]
        hwd.lesson_name = homework_data["lesson_name"]
        hwd.odev_durum_aciklama = homework_data["odev_durum_aciklama"]

        document_link = homework_data["file_url"]
        if not Helper.is_server_data_none(document_link):
            hwd.homework_download_url = document_link
            hwd.ids["download_button"].opacity = 1
        else:
            hwd.ids["download_button"].opacity = 0

        homework_detail_popup.content = hwd
        homework_detail_popup.open()
