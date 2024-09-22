import os

from additional_processors import date_worker
from img_to_text.get_text_from_file import *
from data_processing.data_processor import *
from data_base.database import *
from dotenv import load_dotenv

from source import texts


class GeneralController:
    textGetter = None
    dataProcessor = DataProcessor()
    database = Database()

    def __init__(self):
        load_dotenv()

    @staticmethod
    def get_user_bot_token():
        return os.getenv("USER_BOT_TOKEN")

    @staticmethod
    def get_admin_bot_token():
        return os.getenv("ADMIN_BOT_TOKEN")

    @staticmethod
    def get_path_to_cat():
        return os.getenv("PATH_TO_CAT")

    @staticmethod
    def get_path_to_temp_file():
        return os.getenv("PATH_TO_TEMP_FILE")

    @staticmethod
    def get_path_to_data_base():
        return os.getenv("PATH_TO_DATABASE")

    def get_data_from_pdf(self):
        data = []
        space = 0.1
        for page_num in range(3):
            for n in range(1, 12):  # 1, 12
                pre = self.textGetter.extract_table(page_num, (
                    ((1.07 + (0.95 * (n - 1)) - space) * 72, 0.25 * 72, (1.07 + (0.95 * n) + space) * 72, 8.26 * 72)))
                if pre is not None:
                    data.append(self.dataProcessor.main_process_data(pre))
        return data

    def init_dictionaries(self):
        self.database.get_dictionaries()
        dictionaries = self.database.tables_dictionaries
        self.dataProcessor.set_dictionaries(dictionaries)

    def put_data_into_database(self, schedule_pdf, date_code):
        self.textGetter = TextGetter(schedule_pdf)
        data = self.get_data_from_pdf()
        self.dataProcessor.last_id = self.database.get_id('id')
        for i in range(len(data)):
            data_for_sql = self.dataProcessor.database_process_data(data[i],
                                                                    date_worker.get_date_from_datecode(date_code))
            changes = self.dataProcessor.get_changes_in_dictionaries()
            self.database.insert_changes_into_dictionaries(changes)
            self.database.insert_data_into_timetable(data_for_sql)

    def get_schedule_from_database(self, class_id, chat_id):
        data_from_sql = self.database.get_information_from_timetable(class_id, date_worker.get_date(chat_id))
        decoded = self.dataProcessor.decode_data_from_sql(data_from_sql)
        return decoded

    def connect_to_database(self, database):
        self.database.connect(database)

    def disconnect_from_database(self):
        self.database.disconnect()

    def get_schedule_for_exact_class(self, class_name, chat_id):
        self.connect_to_database(self.get_path_to_data_base())
        self.init_dictionaries()
        key = self.dataProcessor.get_key(class_name.lower(), 0)
        schedule_list = self.get_schedule_from_database(key, chat_id)
        schedule = ''
        if schedule_list != 'error_no_data':
            for i in schedule_list:
                schedule += i + '\n'
        else:
            schedule = texts.there_is_no_schedule_for + date_worker.get_date(chat_id)
        self.database.disconnect()
        return schedule
