import datetime

Yekaterinburg_tz = datetime.timezone(datetime.timedelta(hours=5))
users_timecodes = {} # -1 - yesterday, 0 - today, 1 - tomorrow


def set_date_code(chat_id, new_date_code):
    global users_timecodes
    users_timecodes[chat_id] = new_date_code


def get_date(chat_id):  # 0 - today, -1 - yesterday, 1 - tomorrow and so on
    global users_timecodes
    if chat_id in users_timecodes:
        date = users_timecodes[chat_id]
    else:
        date = 0
    return str((datetime.datetime.now(Yekaterinburg_tz) + datetime.timedelta(days=date)).date())


def get_date_from_datecode(code=None):  # 0 - today, -1 - yesterday, 1 - tomorrow and so on
    datecode = code if code is not None else 0
    return str((datetime.datetime.now(Yekaterinburg_tz) + datetime.timedelta(days=datecode)).date())
