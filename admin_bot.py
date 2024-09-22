from telebot import *
from general_controller import GeneralController
from source import texts

general_controller = GeneralController()
bot = telebot.TeleBot(general_controller.get_admin_bot_token())
btn_add = types.KeyboardButton(texts.add_schedule)
btn_date_codeM1 = types.KeyboardButton('-1')
btn_date_code0 = types.KeyboardButton('0')
btn_date_code1 = types.KeyboardButton('1')

hello_init = False
date_code = None


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn_add)
    bot.send_message(message.from_user.id,
                     texts.Listex_admin_panel,
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global hello_init
    global date_code
    if message.text == texts.add_schedule:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_date_codeM1, btn_date_code0, btn_date_code1)
        bot.send_message(message.from_user.id,
                         texts.code_instructions,
                         reply_markup=markup)
        hello_init = True

    if message.text in ['-1', '0', '1'] and hello_init:
        bot.send_message(message.from_user.id, texts.send_file, reply_markup=types.ReplyKeyboardRemove())
        hello_init = False
        date_code = message.text


@bot.message_handler(content_types=['document'])
def get_file(message):
    global date_code, general_controller
    if date_code is not None:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(general_controller.get_path_to_temp_file(), 'wb') as new_file:
            new_file.write(downloaded_file)
        general_controller.connect_to_database(general_controller.get_path_to_data_base())
        general_controller.init_dictionaries()
        general_controller.put_data_into_database(general_controller.get_path_to_temp_file(), int(date_code))
        general_controller.disconnect_from_database()
        bot.send_message(message.from_user.id, texts.success)


bot.polling(none_stop=True, interval=0)
