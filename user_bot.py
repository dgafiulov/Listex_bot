from telebot import *
from general_controller import *

generalController = GeneralController()
bot = telebot.TeleBot(generalController.get_user_bot_token())
btn_date = types.KeyboardButton(texts.change_date)
btn_menu = types.KeyboardButton(texts.menu)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn_menu, btn_date)
    bot.send_message(message.from_user.id,
                     texts.greetings,
                     reply_markup=markup)


@bot.message_handler(commands=['terms_of_use'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn_menu, btn_date)
    bot.send_message(message.from_user.id,
                     texts.terms_of_use,
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == texts.menu:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn5 = types.KeyboardButton('5')
        btn6 = types.KeyboardButton('6')
        btn7 = types.KeyboardButton('7')
        btn8 = types.KeyboardButton('8')
        btn9 = types.KeyboardButton('9')
        btn10 = types.KeyboardButton('10')
        btn11 = types.KeyboardButton('11')
        markup.row(btn_date).add(btn5, btn6, btn7, btn8, btn9, btn10, btn11)
        bot.send_message(message.from_user.id, texts.choose_parallel, reply_markup=markup)

    elif message.text == texts.change_date:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(texts.yesterday)
        btn2 = types.KeyboardButton(texts.today)
        btn3 = types.KeyboardButton(texts.tomorrow)
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, texts.change_date, reply_markup=markup)

    elif message.text == '5':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('5А')
        btn2 = types.KeyboardButton('5Б')
        btn3 = types.KeyboardButton('5В')
        btn4 = types.KeyboardButton('5Г')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, texts.choose_class, reply_markup=markup)

    elif message.text == '6':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('6А')
        btn2 = types.KeyboardButton('6Б')
        btn3 = types.KeyboardButton('6В')
        btn4 = types.KeyboardButton('6Г')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, texts.choose_class, reply_markup=markup)

    elif message.text == '7':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('7А')
        btn2 = types.KeyboardButton('7Б')
        btn3 = types.KeyboardButton('7В')
        btn4 = types.KeyboardButton('7Г')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, texts.choose_class, reply_markup=markup)

    elif message.text == '8':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('8А')
        btn2 = types.KeyboardButton('8Б')
        btn3 = types.KeyboardButton('8В')
        btn4 = types.KeyboardButton('8Г')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, texts.choose_class, reply_markup=markup)

    elif message.text == '9':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('9А')
        btn2 = types.KeyboardButton('9Б')
        btn3 = types.KeyboardButton('9В')
        btn4 = types.KeyboardButton('9Г')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, texts.choose_class, reply_markup=markup)

    elif message.text == '10':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('10А')
        btn2 = types.KeyboardButton('10Б')
        btn3 = types.KeyboardButton('10В')
        btn4 = types.KeyboardButton('10Г')
        btn5 = types.KeyboardButton('10Д')
        btn6 = types.KeyboardButton('10Е')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.from_user.id, texts.choose_class, reply_markup=markup)

    elif message.text == '11':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('11А')
        btn2 = types.KeyboardButton('11Б')
        btn3 = types.KeyboardButton('11В')
        btn4 = types.KeyboardButton('11Г')
        btn5 = types.KeyboardButton('11Д')
        btn6 = types.KeyboardButton('11Е')
        btn7 = types.KeyboardButton('11Ж')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
        bot.send_message(message.from_user.id, texts.choose_class, reply_markup=markup)

    elif message.text in texts.list_of_all_classes:
        if date_worker.get_date(message.chat.id) == '2024-03-21':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(btn_menu)
            img = open(generalController.get_path_to_cat(), 'rb')
            bot.send_photo(message.chat.id, img)
            bot.send_message(message.from_user.id, texts.trouble_text, reply_markup=markup)
        else:
            schedule = generalController.get_schedule_for_exact_class(message.text, message.from_user.id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(btn_menu)
            bot.send_message(message.from_user.id, schedule, reply_markup=markup)

    elif message.text == texts.yesterday:
        date_worker.set_date_code(message.from_user.id, -1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_menu)
        bot.send_message(message.from_user.id, texts.date_changed_to + date_worker.get_date(message.from_user.id),
                         reply_markup=markup)

    elif message.text == texts.today:
        date_worker.set_date_code(message.from_user.id, 0)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_menu)
        bot.send_message(message.from_user.id, texts.date_changed_to + date_worker.get_date(message.from_user.id),
                         reply_markup=markup)

    elif message.text == texts.tomorrow:
        date_worker.set_date_code(message.from_user.id, 1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_menu)
        bot.send_message(message.from_user.id, texts.date_changed_to + date_worker.get_date(message.from_user.id),
                         reply_markup=markup)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_menu)
        bot.send_message(message.from_user.id, texts.i_dont_understand, reply_markup=markup)


bot.polling(none_stop=True, interval=0)
