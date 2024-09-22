import sqlite3


class Database:
    connected = False
    connection = None
    cursor = None

    classes_dict = {}
    lessons_dict = {}
    rooms_id = {}

    tables_dictionaries_names = ['classes', 'lessons', 'rooms']
    tables_dictionaries = [classes_dict, lessons_dict, rooms_id]

    def connect(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        self.connected = True

    def disconnect(self):
        self.connection.commit()
        self.connection.close()
        self.connected = False

    def get_id(self, table):
        self.cursor.execute(f'SELECT MAX(id) FROM timetable')
        last_id = self.cursor.fetchall()[0][0]
        if last_id is None:
            last_id = -1
        return last_id

    def get_dictionaries(self):
        for i in range(len(self.tables_dictionaries)):
            self.cursor.execute(f'SELECT COUNT(*) FROM {self.tables_dictionaries_names[i]}')
            if self.cursor.fetchall() is not [(0,)]:
                self.cursor.execute(f'SELECT * FROM {self.tables_dictionaries_names[i]}')
                temp_data = self.cursor.fetchall()
                temp_dict = {}

                for id, title in temp_data:
                    temp_dict[id] = title

                self.tables_dictionaries[i].update(temp_dict)

    def insert_data_into_timetable(self, data_for_sql):  # this function is used to insert data into timetable only
        for i in data_for_sql:
            self.cursor.execute(f'INSERT INTO timetable VALUES{tuple(i)}')

    def insert_changes_into_dictionaries(self, data):
        for i in range(len(data)):
            for j in data[i]:
                self.cursor.execute(f'INSERT INTO {self.tables_dictionaries_names[i]} VALUES {j}')

    def get_information_from_timetable(self, class_name, date):
        if class_name is not None:
            self.cursor.execute(f'SELECT * FROM timetable WHERE class_id={class_name} AND date=\'{date}\';')
            data = self.cursor.fetchall()
            if not data:
                data = 'error_no_data'
        else:
            data = 'error_no_data'
        return data
