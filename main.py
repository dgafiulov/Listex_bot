from general_controller import *

# Warning: This file is used for testing only. So there is no practical usage of this code
# and during work it is never used

generalController = GeneralController()
'''classes = ['5А', '5Б', '5В', '5Г', '6А', '6Б', '6В', '6Г', '7А', '7Б', '7В', '7Г', '8А', '8Б', '8В', '8Г', '9А', '9Б', '9В', '9Г', '10А', '10Б', '10В', '10Г', '10Д', '10Е', '11А', '11Б', '11В', '11Г', '11Д', '11Е', '11Ж']

generalController.connect_to_database('source/test7.db')
generalController.init_dictionaries()
generalController.put_data_into_database('D:/хрень/работы/python/расписание/source/sUN.pdf', 1)
generalController.disconnect_from_database()

for i in classes:
    schedule = generalController.get_schedule_for_exact_class(i)
    print(schedule)'''


def get_data_from_pdf():
    data = []
    space = 0.1
    for page_num in range(3, 4):
        for n in range(1, 9):  # 1, 12
            pre = textGetter.extract_table(page_num, ((0.88 + (1.76 * (n - 1)) - 0.04) * 72, 1 * 72, (0.88 + (1.76 * n) + 0.04) * 72, 7.3 * 72))
            print(pre)
            if pre is not None:
                data.append(dataProcessor.main_process_data(pre))
    return data


textGetter = TextGetter('path')
dataProcessor = DataProcessor()
data = get_data_from_pdf()
for i in data:
    print(i)