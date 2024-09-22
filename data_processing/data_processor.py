class DataProcessor:

    possible_words = {
        'русскийязык': 'Русский язык',
        'роднойязык': 'Родной язык',
        'родной': 'Родной ',
        'ангязанг 1': 'Английский язык',
        'ангязанг 2': 'Английский язык',
        'ангязанг 1и': 'Английский язык',
        'ангязанг 2и': 'Английский язык',
        'ангязанг 1о': 'Английский язык',
        'ангязанг 2о': 'Английский язык',
        'вероятность истатистика': 'Вероятность и статистика',
        'инфинф 1': 'Информатика',
        'инфинф 2': 'Информатика',
        'инфинф 1а': 'Информатика',
        'инфинф 2а': 'Информатика',
        'инфинф 1о': 'Информатика',
        'инфинф 2о': 'Информатика',
        'опдопд 1': 'ОПД',
        'опдопд 2': 'ОПД',
        'опдопд 1а': 'ОПД',
        'опдопд 2а': 'ОПД',
        'опдопд 1и': 'ОПД',
        'опдопд 2и': 'ОПД',
        'аалаал 1': 'ААЛ',
        'аалаал 2': 'ААЛ',
        'физ-раф-ра 1': 'Физкультура',
        'физ-раф-ра 2': 'Физкультура',
        'немязнем': 'Немецкий язык',
        'фрязфра': 'Французский язык',
        'естествознание(био)': 'Естествознание (Био)',
        'естествознание(физ)': 'Естествознание (Физ)',
        'информационнаябезопасность': 'Информационная безопасность',
        'предметныепробы': 'Предметные пробы',
        'разговорыо важном': 'Разговоры о важном',
        'основыстроительной деятельности': 'Основы строительной деятельности',
        'техтех 1': 'Технология*',
        'техтех 2': 'Технология*'
    }

    dictionaries = []  # 0 - classes, 1 - lessons, 2 - rooms
    changes_in_dictionaries = [{}, {}, {}]  # 0 - classes, 1 - lessons, 2 - rooms
    last_id = -1

    def main_process_data(self, data):
        for i in range(len(data)):
            if None in data[i]:
                data[i].remove(None)
            for j in range(len(data[i])):
                if '\n' in data[i][j]:
                    data[i][j] = data[i][j].split('\n')

            line = ''
            temp = ''

            for j in range(len(data[i])):
                if type(data[i][j]) == list:
                    for x in range(len(data[i][j])):
                        if self.possible_words.get(temp.lower()) is not None:
                            temp = self.possible_words.get(temp.lower())

                        if data[i][j][x].isdigit():
                            temp += ' ' + data[i][j][x]
                        else:
                            temp += data[i][j][x]

                    if len(data[i]) != 1 and j != 0:
                        line += ' ' + temp
                    else:
                        line += temp

                    temp = ''
                else:
                    if data[i][j] == '' and len(data[i]) == 1:
                        line = '-'
                    elif data[i][j] == '' and len(data[i]) != 1:
                        line += ' /'
                    else:
                        line = data[i][j]
            data[i] = line
        for i in range(len(data) - 1, 0, -1):
            if data[i] != '-':
                break
            else:
                data.pop(i)

        if len(data[0]) > 3:
            data[0] = data[0][len(data[0]) - 3:]

        if not data[0][0].isdigit() or (data[0][1].isdigit() and data[0][0] != '1'):
            data[0] = data[0][1:]

        # solving problem with technology lesson that has long cell
        temp_data = data.copy()

        for i in range(len(temp_data)):
            if temp_data[i][:10] == 'Технология':
                line = ''
                split = temp_data[i].split(' ')
                split_len = len(split)
                for j in range(split_len):
                    if split[j][:10] == 'Технология' and split[j][:11] != 'Технология*' and split_len == 2:
                        data.insert(i, data[i])
                        line = data[i]
                        break
                    elif split[j][:11] == 'Технология*':
                        line += 'Технология '
                    elif split[j].isdigit():
                        if j + 1 < split_len:
                            line += split[j] + ' '
                        else:
                            line += split[j]
                data[i] = line

        return data

    def set_dictionaries(self, dictionaries):
        self.dictionaries = dictionaries

    def get_key(self, value, dictionary_number):
        dictionary = self.dictionaries[dictionary_number]

        keys = list(dictionary.keys())
        values = list(dictionary.values())
        if value in values:
            index = values.index(value)
            return keys[index]
        else:
            return None

    def get_changes_in_dictionaries(self):
        changes_in_dictionaries = self.changes_in_dictionaries
        for i in range(len(changes_in_dictionaries)):
            changes_in_dictionaries[i] = list(self.changes_in_dictionaries[i].items())
        self.changes_in_dictionaries = [{}, {}, {}]
        return changes_in_dictionaries

    def get_last_id_from_dictionary(self, dictionary_number):
        all_ids = list(self.dictionaries[dictionary_number].keys())
        if not(all_ids == []):
            return max(all_ids)
        else:
            return -1

    def analyze_data_names(self, data, is_class):
        for i in data:
            dictionary_number = None
            if i.isdigit() is False and is_class:
                dictionary_number = 0
            elif i.isdigit() is False and is_class is False:
                dictionary_number = 1
            elif i.isdigit() and is_class is False:
                dictionary_number = 2

            if self.get_key(i, dictionary_number) is None:
                id = self.get_last_id_from_dictionary(dictionary_number) + 1
                self.dictionaries[dictionary_number][id] = i
                self.changes_in_dictionaries[dictionary_number][id] = i

    @staticmethod
    def get_divided(data):
        divided = []
        current = ''
        amount_of_lessons = 0
        needs_to_be_appended = False

        if data == '-':
            divided = None
        else:
            needs_to_be_appended = True
            for j in data.split(' '):
                if not j.isdigit():
                    if current == '':
                        current += j
                    else:
                        current += ' ' + j
                else:
                    divided.append(current)
                    divided.append(j)
                    current = ''
                    amount_of_lessons += 1
                    needs_to_be_appended = False

            if needs_to_be_appended:
                divided.append(current)
                divided.append('0')
                amount_of_lessons += 1

        return divided, amount_of_lessons

    def database_process_data(self, data, date):
        class_name = data.pop(0)
        data_for_sql = []  # final data that is ready for sql
        pre_data_for_sql = []  # almost ready, but needs tp have additional lists removed
        self.analyze_data_names([class_name], True)

        for i in range(len(data)):
            current = data[i]
            divided, amount_of_lessons = self.get_divided(current)

            if divided is None and amount_of_lessons == 0:
                pass
            else:
                self.last_id += 1
                line = [self.last_id, self.get_key(class_name, 0)]
                self.analyze_data_names(divided, False)
                for j in range(2):
                    if j % 2 == 0:
                        line.append(self.get_key(divided[j], 1))
                    else:
                        line.append(self.get_key(divided[j], 2))

                line.append(i + 1)
                line.append(date)
                line = [line]

                if len(divided) == 4:
                    self.last_id += 1
                    additional_line = [self.last_id, self.get_key(class_name, 0)]
                    divided = divided.copy()[2:]

                    for j in range(2):
                        if j % 2 == 0:
                            additional_line.append(self.get_key(divided[j], 1))
                        else:
                            additional_line.append(self.get_key(divided[j], 2))

                    additional_line.append(i + 1)
                    additional_line.append(date)
                    line.append(additional_line)

                pre_data_for_sql.append(line)

        for i in pre_data_for_sql:
            for j in i:
                data_for_sql.append(j)

        return data_for_sql

    def decode_data_from_sql(self, data):  # table structure: id, class_id, lesson_id, room_id, lesson_nr, date
        if data != 'error_no_data':
            decoded = [self.dictionaries[0][data[0][1]]]  # schedule for the whole day
            pre_decoded = []  # schedule before final processing
            for i in range(len(data)):
                lesson_name = self.dictionaries[1][data[i][2]]
                room = self.dictionaries[2][data[i][3]]
                lesson_nr = data[i][4]
                pre_decoded.append([lesson_nr, f'{lesson_name} {room}'])

            was_connected = False
            for i in range(len(pre_decoded)):
                if was_connected:
                    was_connected = False
                    continue

                if i == (len(pre_decoded) - 1):
                    decoded.append(f'{pre_decoded[i][0]}: {pre_decoded[i][1]}')
                elif pre_decoded[i][0] == pre_decoded[i + 1][0]:
                    decoded.append(f'{pre_decoded[i][0]}: {pre_decoded[i][1]} / {pre_decoded[i + 1][1]}')
                    was_connected = True
                else:
                    decoded.append(f'{pre_decoded[i][0]}: {pre_decoded[i][1]}')
            return decoded
        else:
            return data
