from threading import Thread
from time import sleep

from kivy.clock import Clock
from kivymd.uix.screen import MDScreen

import Helper
from Broadcast import Broadcast
from KivyStorage import Storage
from StoysAPI import Stoys


class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.profile_name_surname = None
        self.profile_info = None
        self.profile_image = None

        self.broadcasting = Broadcast("profile", self.load_screen)
        self.loading_window = Helper.popup_loading()

        # Clock.schedule_once(self.load_screen, 1)

        # Thread(target=self.load_screen, args=(0,)).start()

    def load_screen(self, last_update):
        try:
            self.loading_window.open()
            self.profile_name_surname = self.ids["profile_name_surname"]
            self.profile_info = self.ids["profile_info"]
            self.profile_image = self.ids["profile_image"]

            self.profile_info.text = ""

            self.profile_info.text += "\n\n\n\n"

            # keys: ['ogrencibilgi', 'ogrenciadres', 'ogrenciresim', 'aile']
            student_data = Stoys.get_student_information(Helper.get_auth(), Helper.get_student_id())["result"]
            ogrencibilgi = student_data["ogrencibilgi"]
            ogrenciadres = student_data["ogrenciadres"]
            ogrenciresim = student_data["ogrenciresim"]
            aile = student_data["aile"]

            adi_soyadi = ogrencibilgi["adi_soyadi"]
            tc_kimlik_no = ogrencibilgi["tc_kimlik_no"]
            ogrenci_no = ogrencibilgi["ogrenci_no"]
            sinif_adi = ogrencibilgi["sinif_adi"]
            # Returns E or possibly K
            cinsiyeti = ogrencibilgi["cinsiyeti"]
            dogum_tarihi = ogrencibilgi["dogum_tarihi"]
            # None value
            ev_tel = ogrencibilgi["ev_tel"]
            # None value
            cep_tel = ogrencibilgi["cep_tel"]
            eposta = ogrencibilgi["eposta"]

            self.profile_name_surname.text = adi_soyadi

            if not Helper.is_server_data_none(tc_kimlik_no):
                self.profile_info.text += "T.C. kimlik no: " + tc_kimlik_no + "\n"
            if not Helper.is_server_data_none(ogrenci_no):
                self.profile_info.text += "Öğrenci no: " + ogrenci_no + "\n"
            if not Helper.is_server_data_none(sinif_adi):
                self.profile_info.text += "Sınıf adı: " + sinif_adi + "\n"
            if not Helper.is_server_data_none(cinsiyeti):
                self.profile_info.text += "Cinsiyet: " + cinsiyeti + "\n"
            if not Helper.is_server_data_none(dogum_tarihi):
                self.profile_info.text += "Doğum tarihi: " + dogum_tarihi + "\n"
            if not Helper.is_server_data_none(ev_tel):
                self.profile_info.text += "Ev Telefonu: " + ev_tel + "\n"
            if not Helper.is_server_data_none(cep_tel):
                self.profile_info.text += "Cep Telefonu: " + cep_tel + "\n"
            if not Helper.is_server_data_none(eposta):
                self.profile_info.text += "E-posta: " + eposta + "\n"

            # ------

            acik_adres = ogrenciadres["acik_adres"]

            if not Helper.is_server_data_none(acik_adres):
                self.profile_info.text += "Açık adres: " + acik_adres + "\n"

            # ------

            self.profile_image.texture = Helper.base64_to_kivy_texture(ogrenciresim)

            # ------

            self.profile_info.text += "Family Information:" + "\n"

            for idx, person in enumerate(aile):
                if idx > 3:
                    break
                person_info = ""
                cep_tel = person["cep_tel"]
                # None value
                ev_tel = person["ev_tel"]
                eposta = person["eposta"]
                # Veli, Kardeş vs.
                yakinlik_tanim = person["yakinlik_tanim"]

                if not Helper.is_server_data_none(cep_tel):
                    person_info += cep_tel + " "
                if not Helper.is_server_data_none(ev_tel):
                    person_info += ev_tel + " "
                if not Helper.is_server_data_none(eposta):
                    person_info += eposta + " "
                if not Helper.is_server_data_none(yakinlik_tanim):
                    person_info += yakinlik_tanim + " "

                if person_info != "":
                    self.profile_info.text += person_info + "\n"



        except KeyError:
            pass
        except:
            pass
        self.loading_window.dismiss()

    def on_logout_clicked(self):
        Storage.delete("login_data")
        Helper.screen_manager.current = "login_screen"
