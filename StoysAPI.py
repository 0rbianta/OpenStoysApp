import json

import requests

from datetime import datetime


class HTTP:
    def __init__(self):
        pass

    def POST(self, URL, DATA, HEADER={"Content-Type": "application/json"}):
        try:
            request = requests.post(URL, json=DATA, headers=HEADER)
            data = json.loads(request.text)
            return data
        except ConnectionError:
            return None

    def GET(self, URL, HEADER={"Content-Type": "application/json"}):
        request = None
        try:
            request = requests.get(URL, headers=HEADER)
            data = json.loads(request.text)
            return data
        except ConnectionError:
            return ConnectionError
        except json.JSONDecodeError:
            return request


class _Stoys(HTTP):
    class Date:
        class dateFormat2:
            def create_stoys_adapted_date(day, month, year):
                if not (day is None and month is None and year is None):
                    while len(month) < 2:
                        month = "0" + month
                    while len(day) < 2:
                        day = "0" + day
                    return f"{day}.{month}.{year}"
                return "00.00.00"

            def create_stoys_adapted_date_from_milliseconds(ms):
                dt = datetime.fromtimestamp(ms / 1000)
                return f"{dt.day}.{dt.month}.{dt.year}"

            def create_stoys_date_with_current_time(self):
                return datetime.today().strftime("%d.%m.%Y")

        class dateFormat11:
            def create_stoys_adapted_date(day, month, year):
                if not (day is None and month is None and year is None):
                    while len(month) < 2:
                        month = "0" + month
                    while len(day) < 2:
                        day = "0" + day
                    return f"{year}-{month}-{day}"
                return "00-00-00"

            def create_stoys_adapted_date_from_milliseconds(ms):
                dt = datetime.fromtimestamp(ms / 1000)
                return f"{dt.year}-{dt.month}-{dt.day}"

            def create_stoys_date_with_current_time():
                return datetime.today().strftime("%Y-%m-%d")

    def __init__(self):
        super().__init__()

        self.api_client_key = "46-68p9z@_Vm4@SR"
        self.api_client_secret = "U2ubk=pZk6=kX3m_sB8q7!+k9MKgmCHb"
        self.api = "https://api.stoys.co/api/v1/"
        self.login_link = self.api + "mobile/auth/token"
        self.absence_list_link = self.api + "mobile/student/absence/{studentId}"
        self.academic_calendar_link = self.api + "mobile/student/academiccalendar/{studentId}/{userId}"
        self.academic_details_link = self.api + "mobile/student/calendar/{studentId}/{userId}"
        self.announcement_details_link = self.api + "mobile/announcement/announcementdetail/" \
                                                    "{announcementId}/{announcementType}"
        self.announcements_link = self.api + "mobile/announcement/{userId}"
        self.conversation_details_link = self.api + "mobile/message/getconversationmessages/{conversationId}"
        self.conversations_link = self.api + "mobile/message/getconversations/{userId}"
        self.daily_state_link = self.api + "mobile/student/getdailynotes/{studentId}/{date}"
        self.etude_calendar_link = self.api + "mobile/student/etude/{studentId}"
        self.exam_calendar_link = self.api + "mobile/student/calendarexam/{studentId}/{startDate}/{endDate}"
        self.exam_type_link = self.api + "mobile/student/examtypes/{studentId}"
        self.gallery_link = self.api + "mobile/student/getgalery/{studentId}"
        self.class_teacher_link = self.api + "mobile/student/getteachers"
        self.guardian_link = self.api + "mobile/guardian/student"
        self.guidance_link = self.api + "mobile/student/liststudentguidance/{studentId}/{userId}/0"
        self.homework_details_link = self.api + "mobile/student/homeworkdetay/{homeworkId}/{studentId}/0"
        self.homeworks_link = self.api + "mobile/student/homeworklist/{studentId}/0"
        self.last_five_exams_link = self.api + "mobile/student/lastfiveexams/{studentId}/{examTypeId}"
        self.open_exam_details_link = self.api + "mobile/student/getopenexamdetail/{studentId}/{examId}"
        self.open_exam_link = self.api + "mobile/student/openexamlist/{studentId}"
        self.schedule_view_link = self.api + "mobile/student/scheduleview/{studentId}/0"
        self.school_report_link = self.api + "mobile/student/examdetail/{studentId}/{examId}"
        self.student_information_link = self.api + "mobile/student/studentinformation/{studentId}/0"

    def login(self, username, password):
        data = {"username": username, "password": password, "client_key": self.api_client_key,
                "client_secret": self.api_client_secret}
        return self.POST(self.login_link, data)

    def get_absence_list(self, auth, student_id):
        return self.GET(self.absence_list_link.format(studentId=student_id),
                        {"Content-Type": "application/json", "Authorization": auth})

    def get_academic_calendar(self, auth, student_id, user_id):
        return self.GET(self.academic_calendar_link.format(studentId=student_id, userId=user_id),
                        {"Content-Type": "application/json", "Authorization": auth})

    def get_academic_details(self, auth, student_id, user_id):
        return self.GET(self.academic_details_link.format(studentId=student_id, userId=user_id),
                        {"Content-Type": "application/json", "Authorization": auth})

    def get_announcement_details(self, auth, announcement_id, announcement_type):
        return self.GET(
            self.announcement_details_link.format(announcementId=announcement_id, announcementType=announcement_type),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_announcements(self, auth, user_id):
        return self.GET(
            self.announcements_link.format(userId=user_id),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_conversations_details(self, auth, conversation_id):
        return self.GET(
            self.conversation_details_link.format(conversationId=conversation_id),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_conversations(self, auth, user_id):
        return self.GET(
            self.conversations_link.format(userId=user_id),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_daily_state(self, auth, student_id, date):
        return self.GET(
            self.daily_state_link.format(studentId=student_id, date=date),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_etude_calendar(self, auth, student_id):
        return self.GET(
            self.etude_calendar_link.format(studentId=student_id),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_exam_calendar(self, auth, student_id, start_date, end_date):
        return self.GET(
            self.exam_calendar_link.format(studentId=student_id, startDate=start_date, endDate=end_date),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_exam_types(self, auth, student_id):
        return self.GET(
            self.exam_type_link.format(studentId=student_id),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_gallery(self, auth, student_id):
        return self.GET(
            self.gallery_link.format(studentId=student_id),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_teacher(self, auth, sinif_id):
        return self.POST(
            self.class_teacher_link, {"sinif_id": sinif_id},
            {"Content-Type": "application/json", "Authorization": auth})

    def get_guardian(self, auth):
        return self.GET(
            self.guardian_link,
            {"Content-Type": "application/json", "Authorization": auth})

    def get_guidance(self, auth, student_id, user_id):
        return self.GET(
            self.guidance_link.format(studentId=student_id, userId=user_id),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_homework_details(self, auth, student_id, homework_id):
        return self.GET(
            self.homework_details_link.format(studentId=student_id, homeworkId=homework_id),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_homeworks(self, auth, student_id):
        return self.GET(
            self.homeworks_link.format(studentId=student_id),
            {"Content-Type": "application/json", "Authorization": auth})

    # This method is not tested
    def get_last_five_exams(self, auth, student_id, exam_type_id):
        return self.GET(
            self.last_five_exams_link.format(studentId=student_id, examTypeId=exam_type_id),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_open_exam(self, auth, student_id):
        return self.GET(
            self.open_exam_link.format(studentId=student_id),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_schedule_view(self, auth, student_id):
        return self.GET(
            self.schedule_view_link.format(studentId=student_id),
            {"Content-Type": "application/json", "Authorization": auth})

    # This method is not tested
    def get_school_report(self, auth, student_id, exam_id):
        return self.GET(
            self.school_report_link.format(studentId=student_id, examId=exam_id),
            {"Content-Type": "application/json", "Authorization": auth})

    def get_student_information(self, auth, student_id):
        return self.GET(
            self.student_information_link.format(studentId=student_id),
            {"Content-Type": "application/json", "Authorization": auth})


Stoys = _Stoys()
