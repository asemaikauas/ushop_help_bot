import types

import telebot
import sqlite3

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '6771413468:AAGYVZB1LV5YoGpFPMsq4ooP2uTd-ytSNPI'
bot = telebot.TeleBot(TOKEN)
user_language = {}

ASKING_FOR_PIN, ASKING_FOR_NAME = range(2)
user_data = {}

ASKING_FOR_DEVICE, ASKING_FOR_PROMO = range(2)
user2_data = {}

ASKING_FOR_GOOD = range(1)
user3_data = {}

ASKING_FOR_CORP = range(1)
user4_data = {}

ASKING_FOR_REVIEW = range(1)
user5_data = {}


@bot.message_handler(commands=['start'])
def main(message):
    GROUP_CHAT_ID = message.chat.id
    print(f"Chat ID: {message.chat.id}")

    markup = InlineKeyboardMarkup()
    button_ru = InlineKeyboardButton("RUS", callback_data='ru')
    button_kz = InlineKeyboardButton("KZ", callback_data='kz')

    markup.row(button_kz, button_ru)

    bot.send_message(message.chat.id,
                     '🤖 Сәлеметсіз бе! Мен Shop Market қолдау ботымын. Мен сізге көмектескім келеді! Қай тілде жауап '
                     'беру керек? \n\n 🤖 Здравствуйте! Я бот поддержки Ushop Market. Хочу вам помочь! На каком языке '
                     'отвечать?',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    language = user_language.get(chat_id, 'default')
    if call.data == 'ru':
        # Set the user's language to Russian
        user_language[chat_id] = 'ru'
        bot.answer_callback_query(call.id, "Язык установлен на русский.")
        # Send a confirmation message or continue the conversation in Russian
        send_language_specific_message(chat_id)  # This sends the follow-up message in Kazakh

    elif call.data == 'kz':
        user_language[chat_id] = 'kz'
        bot.answer_callback_query(call.id, "Тіл қазақшаға ауыстырылды.")
        send_language_specific_message(chat_id)  # This sends the follow-up message in Kazakh
    elif call.data == 'when_deliver_ru' or call.data == 'when_deliver_kz':
        send_delivery_type_options(chat_id, language)
    elif call.data == 'pickup_delivery_ru' or call.data == 'pickup_delivery_kz':
        delivery_pickup_info(chat_id, language)
    elif call.data == 'thanks_kz' or call.data == 'thanks_ru':
        any_questions(chat_id, language)
    elif call.data == 'not_received_ru' or call.data == 'not_received_kz':
        start_return_process(chat_id)
    elif call.data == 'courier_delivery_ru' or call.data == 'courier_delivery_kz':
        courier_info(chat_id, language)
    elif call.data == 'change_order_ru' or call.data == 'change_order_kz':
        change_info(chat_id, language)
    elif call.data == 'in_order_g_ru' or call.data == 'in_order_g_kz':
        change_act(chat_id, language)
    elif call.data == 'not_change_ru' or call.data == 'not_change_kz':
        not_change_options(chat_id, language)
    elif call.data == 'cancel_order_ru' or call.data == 'cancel_order_kz':
        cancel_info(chat_id, language)
    elif call.data == 'no_pickup_ru' or call.data == 'no_pickup_kz':
        no_pickup_answer(chat_id, language)
    elif call.data == 'no_longer_needed_ru' or call.data == 'no_longer_needed_kz':
        no_need_answer(chat_id, language)
    elif call.data == 'stay_time_ru' or call.data == 'stay_time_kz':
        time_info(chat_id, language)
    elif call.data == 'pay/return_ru' or call.data == 'pay/return_kz':
        pay_return(chat_id, language)
    elif call.data == 'pay_order_in_ru' or call.data == 'pay_order_in_kz':
        pay_order_in(chat_id, language)
    elif call.data == 'ways_of_pay_ru' or call.data == 'ways_of_pay_kz':
        ways_of_paying(chat_id, language)
    elif call.data == 'bank_pay_ru' or call.data == 'bank_pay_kz':
        bank_pay(chat_id, language)
    elif call.data == 'partial_ru' or call.data == 'partial_kz':
        partial_pay(chat_id, language)
    elif call.data == 'when_receive_ru' or call.data == 'when_receive_kz':
        when_receive_pay(chat_id, language)
    elif call.data == 'issues_pay_ru' or call.data == 'issues_pay_kz':
        issues_pay_info(chat_id, language)
    elif call.data == 'no_transition':
        no_transition_info(chat_id, language)
    elif call.data == 'not_work_ru' or call.data == 'not_work_kz':
        still_not_work(chat_id, language)
    elif call.data == 'not_helped':
        start_device_process(chat_id)
    elif call.data == 'no_promo':
        no_promo_info(chat_id, language)
    elif call.data == 'still_no_promo':
        still_no_promo(chat_id, language)
    elif call.data == 'promo_used':
        promo_used(chat_id, language)
    elif call.data == 'no_active_order':
        start_promo_process(chat_id)
    elif call.data == 'promo_expired':
        promo_expired(chat_id, language)
    elif call.data == 'code_works':
        start_promo_process(chat_id)
    elif call.data == 'other_promo_issue':
        start_device_process(chat_id)
    elif call.data == 'return_goods':
        return_goods_info(chat_id, language)
    elif call.data == 'return_product':
        return_product_info(chat_id, language)
    elif call.data == 'other_return_issue':
        start_return_process(chat_id)
    elif call.data == 'yes_choice':
        if language == 'ru':
            text = 'Подскажите, пожалуйста, у товара указана гарантия?'
            btn1 = InlineKeyboardButton('Да', callback_data='yes_guarantee')
            btn2 = InlineKeyboardButton('Нет', callback_data='no_guarantee')
            btn3 = InlineKeyboardButton('На главную', callback_data='ru')
        else:
            text = 'Тауарда кепілдік уақыты көрсетілген бе?'
            btn1 = InlineKeyboardButton('Иә', callback_data='yes_guarantee')
            btn2 = InlineKeyboardButton('Жоқ', callback_data='no_guarantee')
            btn3 = InlineKeyboardButton('Басты бетке', callback_data='kz')
        markup = InlineKeyboardMarkup()
        markup.row(btn1, btn2)
        markup.row(btn3)

        bot.send_message(chat_id, text, reply_markup=markup)
    elif call.data == 'yes_guarantee' or call.data == 'no_guarantee':
        guarantee_info(chat_id, language, call.data)
    elif call.data == 'no_choice':
        no_choice_info(chat_id, language)
    elif call.data == 'less_than_10':
        less_than_10_info(chat_id, language)
    elif call.data == 'yes_pack':
        yes_pack_info(chat_id, language)
    elif call.data == 'no_pack' or call.data == 'more_than_10':
        no_pack_info(chat_id, language)
    elif call.data == 'contact_seller':
        contact_seller_info(chat_id, language)
    elif call.data == 'return_order_ru' or call.data == 'return_order_kz':
        return_product_info(chat_id, language)
    elif call.data == 'goods_in_ru' or call.data == 'goods_in_kz':
        goods_in_info(chat_id, language)
    elif call.data == 'damaged':
        start_good_process(chat_id, language)
    elif call.data == 'how_to_use':
        how_to_use(chat_id, language)
    elif call.data == 'other_person_ru' or call.data == 'other_person_kz':
        if language == 'ru':
            text = 'Ваш заказ оформлен в рассрочку?'
            btn1 = InlineKeyboardButton('Да', callback_data='yes_other_person')
            btn2 = InlineKeyboardButton('Нет', callback_data='no_other_person')
            btn3 = InlineKeyboardButton('На главную', callback_data='ru')
        else:
            text = 'Сіздің тапсырыңыз бөліп төлеумен рәсімделген бе еді?'
            btn1 = InlineKeyboardButton('Иә', callback_data='yes_other_person')
            btn2 = InlineKeyboardButton('Жоқ', callback_data='no_other_person')
            btn3 = InlineKeyboardButton('Басты бетке', callback_data='kz')
        markup = InlineKeyboardMarkup()
        markup.row(btn1, btn2)
        markup.add(btn3)
        bot.send_message(chat_id, text, reply_markup=markup)
    elif call.data == 'yes_other_person':
        yes_other_person(chat_id, language)
    elif call.data == 'no_other_person':
        no_other_person(chat_id, language)
    elif call.data == 'delivery_items_ru' or call.data == 'delivery_items_kz':
        delivery_info(chat_id, language)
    elif call.data == 'not_find_ru' or call.data == 'not_find_kz':
        not_find_info(chat_id, language)
    elif call.data == 'find_promo':
        find_promo_info(chat_id, language)
    elif call.data == 'cities_ru' or call.data == 'cities_kz':
        cities_info(chat_id, language)
    elif call.data == 'cooperation':
        cooperation_info(chat_id, language)
    elif call.data == 'become_seller':
        become_seller_info(chat_id, language)
    elif call.data == 'seller_question':
        seller_question(chat_id, language)
    elif call.data == 'ushop_vacancies' or call.data == 'marketing_advertising':
        ushop_vacancies_info(chat_id, language)
    elif call.data == 'other_cooperation' or call.data == 'write_to_person':
        start_corp_process(chat_id, language)
    elif call.data == 'reviews':
        reviews_info(chat_id, language)
    elif call.data == 'how_to_review':
        how_to_review_info(chat_id, language)
    elif call.data == 'not_published':
        not_published_info(chat_id, language)
    elif call.data == 'other_review_question':
        start_review_process(chat_id, language)
    bot.answer_callback_query(call.id)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    username1 = message.from_user.username
    print(f"Chat ID: {message.chat.id}")
    chat_id = message.chat.id
    if chat_id in user_data:
        if user_data[chat_id]["state"] == ASKING_FOR_PIN:
            user_data[chat_id]["pin"] = message.text
            user_data[chat_id]["state"] = ASKING_FOR_NAME
            language = user_language.get(chat_id, 'default')
            if language == 'ru':
                text = "На какое имя был оформлен товар?"
            else:
                text = "Тауар кімнің атына жазылған еді?"
            bot.send_message(chat_id, text)

        elif user_data[chat_id]["state"] == ASKING_FOR_NAME:
            user_data[chat_id]["name"] = message.text
            process_return_request(chat_id, user_data[chat_id]["pin"], user_data[chat_id]["name"], username1)
            del user_data[chat_id]
    if chat_id in user2_data:
        if user2_data[chat_id]["state"] == ASKING_FOR_DEVICE:
            user2_data[chat_id]["device"] = message.text
            process_device_request(chat_id, user2_data[chat_id]["device"], username1)
            del user2_data[chat_id]
        elif user2_data[chat_id]["state"] == ASKING_FOR_PROMO:
            user2_data[chat_id]["promo"] = message.text
            process_promo_request(chat_id, user2_data[chat_id]["promo"], username1)
            del user2_data[chat_id]
    if chat_id in user3_data:
        if user3_data[chat_id]["state"] == ASKING_FOR_GOOD:
            user3_data[chat_id]["good_pin"] = message.text
            process_good_request(chat_id, user3_data[chat_id]["good_pin"], username1)
    if chat_id in user4_data:
        user4_data[chat_id]["corp_ask"] = message.text
        process_corp_request(chat_id, user4_data[chat_id]["corp_ask"], username1)
    if chat_id in user5_data:
        user5_data[chat_id]["other_question"] = message.text
        process_review_request(chat_id, user5_data[chat_id]["other_question"], username1)


def send_language_specific_message(chat_id):
    language = user_language.get(chat_id, 'default')

    if language == 'ru':
        text = 'Подскажите, пожалуйста, с чем связан ваш вопрос?\n\nНужно выбрать пункт из меню ниже.'
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton("🚀 Когда будет доставлен мой заказ?", callback_data='when_deliver_ru')
        btn2 = InlineKeyboardButton("🔧 Изменить заказ?", callback_data='change_order_ru')
        btn3 = InlineKeyboardButton("🚫 Отменить заказ", callback_data='cancel_order_ru')
        btn4 = InlineKeyboardButton("⏰ Cрок хранения", callback_data='stay_time_ru')
        btn5 = InlineKeyboardButton("💸 Оплата/возврат", callback_data='pay/return_ru')
        btn6 = InlineKeyboardButton("↩️ Вернуть товар", callback_data='return_order_ru')
        btn7 = InlineKeyboardButton("📦 Товары в заказе", callback_data='goods_in_ru')
        btn8 = InlineKeyboardButton("В каких городах есть Ushop?", callback_data='cities_ru')
        btn9 = InlineKeyboardButton("🤝 Получение заказа другим человеком", callback_data='other_person_ru')
        btn10 = InlineKeyboardButton("🚚 Условия доставки", callback_data='delivery_items_ru')
        btn11 = InlineKeyboardButton("Не нашел(-ла) ответа", callback_data='not_find_ru')

    else:
        text = 'Айтыңызшы, Сіздің сұрағыңыз немен байланысты?\n\nТөмендегі мәзірден элементті таңдау керек.'
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton("🚀 Менің тапсырысым қашан жеткізіледі?", callback_data='when_deliver_kz')
        btn2 = InlineKeyboardButton("🔧 Тапсырысты өзгерту?", callback_data='change_order_kz')
        btn3 = InlineKeyboardButton("🚫 Тапсырысты болдырмау", callback_data='cancel_order_kz')
        btn4 = InlineKeyboardButton("⏰ Сақтау мерзімі", callback_data='stay_time_kz')
        btn5 = InlineKeyboardButton("💸 Төлем/қайтару", callback_data='pay/return_kz')
        btn6 = InlineKeyboardButton("↩️ Тауарды қайтару", callback_data='return_goods_kz')
        btn7 = InlineKeyboardButton("📦 Тапсырыстағы тауарлар", callback_data='goods_in_kz')
        btn8 = InlineKeyboardButton("🏙️ Ushop қандай қалаларда бар?", callback_data='cities_kz')
        btn9 = InlineKeyboardButton("🤝 Тапсырысты басқа адамның алуы", callback_data='other_person_kz')
        btn10 = InlineKeyboardButton("🚚 Жеткізу шарттары", callback_data='delivery_items_kz')
        btn11 = InlineKeyboardButton("❓ Жауап таппадым", callback_data='not_find_kz')

    
    markup.add(btn1)
    if language == 'kz':
        markup.add(btn2)
        markup.add(btn3)
    else:
        markup.row(btn2, btn3)
    markup.row(btn4, btn5)
    markup.row(btn6, btn7)
    markup.add(btn8)
    markup.add(btn9)
    markup.row(btn10, btn11)
    bot.send_message(chat_id, text, reply_markup=markup)


def start_return_process(chat_id):
    language = user_language.get(chat_id, 'default')
    if language == 'ru':
        text = "Напишите, пожалуйста, номер вашего заказа без лишних символов и пробелов."
    else:
        text = "Тапсырыс нөміріңізді жазуыңызды сұраймыз."
    bot.send_message(chat_id, text)
    user_data[chat_id] = {"state": ASKING_FOR_PIN}


def start_device_process(chat_id):
    language = user_language.get(chat_id, 'default')
    if language == 'ru':
        text = ('Хорошо, тогда сейчас подключу техническую поддержку.\n'
                'Напишите, пожалуйста, версию вашего приложения\n\n'
                'Как найти версию приложения:\n\n'
                'Если у вас iOS - то необходимо зайти во вкладку Профиль и сделать свайп вверх.\n'
                'Версия приложения будет в нижней части экрана.\n\n'
                'Если у вас Android - то необходимо зайти во вкладку Кабинет и сделать свайп вверх.\n'
                'Версия приложения будет в нижней части экрана.')
    else:
        text = ('Жақсы, онда қазір техникалық қолдауға қосамын.\n'
                'Өтінемін, қосымшаңыздың нұсқасын жазыңыз\n\n'
                'Қосымша нұсқасын қалай табуға болады:\n\n'
                'Егер сізде iOS болса - Профиль бөліміне кіріп, жоғары қарай свайп жасаңыз.\n'
                'Қосымша нұсқасы экранның төменгі жағында болады.\n\n'
                'Егер сізде Android болса - Кабинет бөліміне кіріп, жоғары қарай свайп жасаңыз.\n'
                'Қосымша нұсқасы экранның төменгі жағында болады.')

    bot.send_message(chat_id, text)
    user2_data[chat_id] = {"state": ASKING_FOR_DEVICE}


def start_good_process(chat_id, language):
    if language == 'ru':
        text = 'Мы обязательно разберемся, как такое могло произойти. Напишите, пожалуйста, номер вашего заказа, без лишних символов и пробелов.'
        btn1 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = 'Біз мұның қалай болғанын міндетті түрде анықтаймыз. Өтінемін, сіздің тапсырысыңыздың нөмірін артық белгілерсіз және бос орынсыз жазыңыз.'
        btn1 = InlineKeyboardButton('Басты бетке', callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    bot.send_message(chat_id, text, reply_markup=markup)
    user3_data[chat_id] = {"state": ASKING_FOR_GOOD}


def start_promo_process(chat_id):
    language = user_language.get(chat_id, 'default')
    if language == 'ru':
        text = 'Напишите, пожалуйста, название промокода, который не получается использовать'
        btn1 = InlineKeyboardButton('На главную', callback_data='ru')
    else:  # Kazakh language
        text = 'Өтінемін, пайдалана алмай жатқан промокодтың атауын жазыңыз'
        btn1 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    bot.send_message(chat_id, text, reply_markup=markup)
    user2_data[chat_id] = {"state": ASKING_FOR_PROMO}


def start_corp_process(chat_id, language):
    if language == 'ru':
        text = 'Напишите, пожалуйста, какой у вас вопрос связанный с сотрудничеством, и я смогу позвать оператора.'
        btn1 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = 'Өтініш, cеріктестікке қатысты қандай сұрағыңыз бар екенін жазыңыз, мен операторды шақыра аламын.'
        btn1 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    bot.send_message(chat_id, text, reply_markup=markup)
    user4_data[chat_id] = {"state": ASKING_FOR_CORP}

def start_review_process(chat_id, language):
    if language == 'ru':
        text = "Напишите, пожалуйста, ваш вопрос и я позову оператора."
        btn1 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        # Kazakh translation (or any other language)
        text = "Өтініш, сұрағыңызды жазыңыз, мен операторды шақырамын."
        btn1 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1]])
    bot.send_message(chat_id, text, reply_markup=markup)
    user5_data[chat_id] = {"state": ASKING_FOR_REVIEW}


def process_return_request(chat_id, pin_number, name, username1):
    managers_group_id = '-1001833169106'
    bot.send_message(managers_group_id, f"Return Request:\nPIN: {pin_number}\nName: {name}\nUsername: {username1}")
    language = user_language.get(chat_id, 'default')
    if language == 'ru':
        text = "Ваш заказ передан первому свободному менеджеру, и скоро с Вами свяжутся."
        btn14 = InlineKeyboardButton("На главную", callback_data='ru')
    else:
        text = "Сіздің тапсырысыңыз бос алғашқы менеджерге жіберілді, жақын арада Сізбен хабарласады."
        btn14 = InlineKeyboardButton("Басты бетке", callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn14)
    bot.send_message(chat_id, text, reply_markup=markup)


def process_promo_request(chat_id, promo, username1):
    managers_group_id = '-1001833169106'
    bot.send_message(managers_group_id, f"Promo code issue: {promo}\nUsername: {username1}")

    language = user_language.get(chat_id, 'default')
    if language == 'ru':
        text = "Ваш промокод передан первому свободному менеджеру, и скоро с Вами свяжутся."
        btn14 = InlineKeyboardButton("На главную", callback_data='ru')
    else:
        text = "Сіздің промокодыңыз бос алғашқы менеджерге жіберілді, жақын арада Сізбен хабарласады."
        btn14 = InlineKeyboardButton("Басты бетке", callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn14)
    bot.send_message(chat_id, text, reply_markup=markup)


def process_device_request(chat_id, device, username1):
    managers_group_id = '-1001833169106'
    bot.send_message(managers_group_id, f"App version: {device}\nUsername: {username1}")

    language = user_language.get(chat_id, 'default')
    if language == 'ru':
        text = "Ваш заказ передан первому свободному менеджеру, и скоро с Вами свяжутся."
        btn14 = InlineKeyboardButton("На главную", callback_data='ru')
    else:
        text = "Сіздің тапсырысыңыз бос алғашқы менеджерге жіберілді, жақын арада Сізбен хабарласады."
        btn14 = InlineKeyboardButton("Басты бетке", callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn14)
    bot.send_message(chat_id, text, reply_markup=markup)


def process_good_request(chat_id, good_pin, username1):
    managers_group_id = '-1001833169106'
    bot.send_message(managers_group_id, f"Damaged/missed good REPORTED! \nPIN: {good_pin}\nUsername: {username1}")

    language = user_language.get(chat_id, 'default')
    if language == 'ru':
        text = "Ваш вопрос был передан первому свободному менеджеру, и скоро с Вами свяжутся."
        btn14 = InlineKeyboardButton("На главную", callback_data='ru')
    else:
        text = "Сіздің сұрағыңыз бос алғашқы менеджерге жіберілді, жақын арада Сізбен хабарласады."
        btn14 = InlineKeyboardButton("Басты бетке", callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn14)
    bot.send_message(chat_id, text, reply_markup=markup)


def process_corp_request(chat_id, corp_question, username1):
    managers_group_id = '-1001833169106'
    bot.send_message(managers_group_id, f"Cooperation request \nDescription: {corp_question}\nUsername: {username1}")

    language = user_language.get(chat_id, 'default')
    if language == 'ru':
        text = "Ваш вопрос был передан первому свободному менеджеру, и скоро с Вами свяжутся."
        btn14 = InlineKeyboardButton("На главную", callback_data='ru')
    else:
        text = "Сіздің сұрағыңыз бос алғашқы менеджерге жіберілді, жақын арада Сізбен хабарласады."
        btn14 = InlineKeyboardButton("Басты бетке", callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn14)
    bot.send_message(chat_id, text, reply_markup=markup)


def process_review_request(chat_id, other_question, username1):
    managers_group_id = '-1001833169106'
    bot.send_message(managers_group_id, f"Review request \nDescription: {other_question}\nUsername: {username1}")

    language = user_language.get(chat_id, 'default')
    if language == 'ru':
        text = "Ваш вопрос был передан первому свободному менеджеру, и скоро с Вами свяжутся."
        btn14 = InlineKeyboardButton("На главную", callback_data='ru')
    else:
        text = "Сіздің сұрағыңыз бос алғашқы менеджерге жіберілді, жақын арада Сізбен хабарласады."
        btn14 = InlineKeyboardButton("Басты бетке", callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn14)
    bot.send_message(chat_id, text, reply_markup=markup)


def send_delivery_type_options(chat_id, language):
    if language == 'ru':
        text = "Хорошо. Подскажите, пожалуйста, какой тип доставки у вас?"
        btn12 = InlineKeyboardButton("Доставка до пункта выдачи", callback_data='pickup_delivery_ru')
        btn13 = InlineKeyboardButton("Курьерская доставка", callback_data='courier_delivery_ru')
        btn14 = InlineKeyboardButton("На главную", callback_data='ru')
    else:  # Assuming the other language is Kazakh
        text = "Жақсы. Өтінемін, Сіздің жеткізу түріңіз қандай?"
        btn12 = InlineKeyboardButton("Шығару пунктіне жеткізу", callback_data='pickup_delivery_kz')
        btn13 = InlineKeyboardButton("Курьерлік жеткізу", callback_data='courier_delivery_kz')
        btn14 = InlineKeyboardButton("Басты бетке", callback_data='ru')
    markup = InlineKeyboardMarkup()
    markup.add(btn12)
    markup.add(btn13)
    markup.add(btn14)
    bot.send_message(chat_id, text, reply_markup=markup)


def delivery_pickup_info(chat_id, language):
    if language == 'ru':
        text = "В период распродажи заказы доставляются в течение следующего дня, после оформления заказа😊 \n\nКак только заказ поступит, вам придет смс-уведомление, пожалуйста, дождитесь его до посещения пункта выдачи.\n\nУвы, точное время доставки подсказать не получится."
        btn1 = InlineKeyboardButton("Спасибо", callback_data='thanks_ru')
        btn2 = InlineKeyboardButton("Не получил заказ на следующий день", callback_data='not_received_ru')
        btn3 = InlineKeyboardButton("На главную", callback_data='ru')
    else:  # Assuming the other language is Kazakh
        text: str = "Опцияны таңдаңыз:"
        btn1 = InlineKeyboardButton("Рахмет", callback_data='thanks_kz')
        btn2 = InlineKeyboardButton("Келесі күні тапсырысты алмадым", callback_data='not_received_kz')
        btn3 = InlineKeyboardButton("Басты бетке", callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(chat_id, text, reply_markup=markup)


def any_questions(chat_id, language):
    if language == 'ru':
        text = "Если вдруг будут еще вопросы, просто нажмите на кнопку."
        btn1 = InlineKeyboardButton("У меня еще вопрос!", callback_data='ru')
    else:
        text = "Егер тағы да сұрақтарыңыз болса, батырманы басыңыз."
        btn1 = InlineKeyboardButton("Менде тағы сұрақ бар!", callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    bot.send_message(chat_id, text, reply_markup=markup)


def id_number(chat_id, language):
    if language == 'ru':
        text = "Напишите, пожалуйста, номер вашего заказа."
        btn = InlineKeyboardButton("На главную⬅️", callback_data='ru')
    else:
        text = "Тапсырыс нөміріңізді жазып жіберуіңізді өтінеміз."
        btn = InlineKeyboardButton("Басты бетке⬅️", callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.add(btn)
    bot.send_message(chat_id, text, reply_markup=markup)


def courier_info(chat_id, language):
    if language == 'ru':
        text = 'Заказы доставляются в интервале с 10:00 до 22:00. К сожалению, точного времени мы не можем вам подсказать😔 Курьер свяжется с вами в день доставки за 30 минут до приезда! Будьте, пожалуйста, на связи.'
        btn1 = InlineKeyboardButton("Спасибо", callback_data='thanks_ru')
        btn2 = InlineKeyboardButton("Не получил заказ в срок", callback_data='not_received_ru')
        btn3 = InlineKeyboardButton("На главную⬅️", callback_data='ru')
    else:
        text = "Тапсырыстар сағат 10:00-ден 22:00-ге дейін жеткізіледі. Өкінішке орай, нақты уақытты сізге айта алмаймыз😔 Курьер жеткізу күні келгенге дейін 30 минут бұрын сізбен байланысқа шығады! Өтінемін, байланыста болыңыз."
        btn1 = InlineKeyboardButton("Рахмет", callback_data='thanks_kz')
        btn2 = InlineKeyboardButton("Тапсырысты уақытылы алмадым", callback_data='not_received_kz')
        btn3 = InlineKeyboardButton("Басты бетке⬅️", callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(chat_id, text, reply_markup=markup)


def change_info(chat_id, language):
    if language == 'ru':
        text = 'Хорошо, подскажите пожалуйста, что именно Вы хотели бы изменить?'
        btn2 = InlineKeyboardButton("Товары в заказе⬅️", callback_data='in_order_g_ru')
        btn3 = InlineKeyboardButton("На главную⬅️", callback_data='ru')
    else:  # Assuming the other language is Kazakh
        text = 'Жақсы, өтінемін, нақты нені өзгерткіңіз келеді?'
        btn2 = InlineKeyboardButton("Тапсырыстағы тауарлар⬅️", callback_data='in_order_g_kz')
        btn3 = InlineKeyboardButton("Басты бетке⬅️", callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(chat_id, text, reply_markup=markup)


def change_act(chat_id, language):
    if language == 'ru':
        text = 'Подскажите, пожалуйста, что именно вы хотели бы изменить?'
        btn1 = InlineKeyboardButton("Добавить товар", callback_data='not_change_ru')
        btn2 = InlineKeyboardButton("Убрать товар", callback_data='not_change_ru')
        btn3 = InlineKeyboardButton("На главную", callback_data='ru')
    else:  # Assuming the other language is Kazakh
        text = 'Өтінемін, нақты нені өзгерткіңіз келеді?'
        btn1 = InlineKeyboardButton("Тауар қосу", callback_data='not_change_kz')
        btn2 = InlineKeyboardButton("Тауар алып тастау", callback_data='not_change_kz')
        btn3 = InlineKeyboardButton("Басты бетке", callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(chat_id, text, reply_markup=markup)


def not_change_options(chat_id, language):
    if language == 'ru':
        text = (
            'Увы, внести изменения в оформленный заказ не получится, вы можете отказаться от любого товара при получении. \n\n'
            'Если заказ оформлен в рассрочку, отказаться можно только от всего заказа😔\n\n'
            'Наши заказы собираются очень быстро, и мы просто не можем технически вмешаться в процесс и изменить что-либо в заказе.\n'
            'В будущем, постараемся добавить такую возможность, на сегодняшний день, к сожалению, её нет.')
        btn1 = InlineKeyboardButton("Хорошо, понимаю", callback_data='thanks_ru')
        btn2 = InlineKeyboardButton("Отменить заказ", callback_data='not_received_ru')
        btn3 = InlineKeyboardButton("На главную", callback_data='ru')
    else:  # Assuming the other language is Kazakh
        text = (
            'Өкінішке орай, рәсімделген тапсырыста өзгерістер енгізу мүмкін емес, тауарды алған кезде кез келген тауардан бас тарта аласыз. \n\n'
            'Егер тапсырыс жайлы төлеммен рәсімделген болса, тек бүкіл тапсырыстан бас тартуға болады😔\n\n'
            'Біздің тапсырыстар өте жылдам жиналады, және біз техникалық тұрғыдан процеске араласып, тапсырыста бірдеңе өзгерте алмаймыз.\n'
            'Болашақта, мұндай мүмкіндікті қосуға тырысамыз, бүгінгі таңда, өкінішке орай, мұндай мүмкіндік жоқ.')
        btn1 = InlineKeyboardButton("Жақсы, түсінемін", callback_data='thanks_kz')
        btn2 = InlineKeyboardButton("Тапсырысты болдырмау", callback_data='not_received_kz')
        btn3 = InlineKeyboardButton("Басты бетке", callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(chat_id, text, reply_markup=markup)


def cancel_info(chat_id, language):
    if language == 'ru':
        text = 'Скажите, пожалуйста, по какой причине вы хотели бы отменить заказ?'
        btn1 = InlineKeyboardButton("Не успею забрать с пункта выдачи", callback_data='no_pickup_ru')
        btn2 = InlineKeyboardButton("Заказ мне больше не нужен", callback_data='no_longer_needed_ru')
        btn3 = InlineKeyboardButton("На главную⬅️", callback_data='main_menu_ru')
    else:  # Assuming the other language is Kazakh
        text = 'Өтінемін, қандай себептен тапсырысты болдырмақшысыз?'
        btn1 = InlineKeyboardButton("Шығару орнынан уақытында ала алмаймын", callback_data='no_pickup_kz')
        btn2 = InlineKeyboardButton("Тапсырыс маған қажет емес", callback_data='no_longer_needed_kz')
        btn3 = InlineKeyboardButton("Басты бетке⬅️", callback_data='main_menu_kz')
    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(chat_id, text, reply_markup=markup)


def no_pickup_answer(chat_id, language):
    if language == 'ru':
        text = ('В случае, если вы не успеваете забрать заказ с пункта выдачи в течение 5 дней с момента его доставки, '
                'то мы можем продлить срок хранения заказа на 14 дней. \n\nПродлим?')
        btn1 = InlineKeyboardButton("Да, давайте", callback_data='not_received_ru')
        btn2 = InlineKeyboardButton("Нет, продление заказа не поможет", callback_data='not_received_ru')
        btn3 = InlineKeyboardButton("Успеваю забрать, не нужно", callback_data='thanks_ru')
        btn4 = InlineKeyboardButton("На главную⬅️", callback_data='ru')
    else:  # Assuming the other language is Kazakh
        text = ('Егер Сіз тапсырысты оның жеткізілген сәтінен бастап 5 күн ішінде шығару пунктінен ала алмасаңыз, '
                'онда біз тапсырысты сақтау мерзімін 14 күнге ұзарта аламыз. \n\nҰзартайық па?')
        btn1 = InlineKeyboardButton("Иә, жасайық", callback_data='not_received_kz')
        btn2 = InlineKeyboardButton("Жоқ, тапсырысты ұзарту көмектеспейді", callback_data='not_received_kz')
        btn3 = InlineKeyboardButton("Уақытында алып кетуге үлгеремін, қажет емес", callback_data='thanks_kz')
        btn4 = InlineKeyboardButton("Басты бетке⬅️", callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    bot.send_message(chat_id, text, reply_markup=markup)


def no_need_answer(chat_id, language):
    if language == 'ru':
        text = 'Подскажите, пожалуйста, почему вы решили отменить заказ?'
        btn1 = InlineKeyboardButton("Нашел(-ла) дешевле", callback_data='not_received_ru')
        btn2 = InlineKeyboardButton("Долгая доставка", callback_data='not_received_ru')
        btn3 = InlineKeyboardButton("Перезаказал (-ла) другие товары", callback_data='not_received_ru')
        btn4 = InlineKeyboardButton("Другая", callback_data='not_received_ru')
        btn5 = InlineKeyboardButton("На главную", callback_data='ru')
    else:  # Assuming the other language is Kazakh
        text = 'Өтінемін, тапсырысты неге болдырмақшысыз?'
        btn1 = InlineKeyboardButton("Арзанырақ таптым", callback_data='not_received_kz')
        btn2 = InlineKeyboardButton("Жеткізу ұзақ уақыт алады", callback_data='not_received_kz')
        btn3 = InlineKeyboardButton("Басқа тауарларға қайта тапсырыс бердім", callback_data='not_received_kz')
        btn4 = InlineKeyboardButton("Басқа себеп", callback_data='not_received_kz')
        btn5 = InlineKeyboardButton("Басты бетке", callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.row(btn4, btn5)
    bot.send_message(chat_id, text, reply_markup=markup)


def time_info(chat_id, language):
    if language == 'ru':
        text = 'Срок хранения заказов на пункте выдачи 5 дней с момента их доставки.\nУспеваете забрать или продлим? 😊'
        btn1 = InlineKeyboardButton("Успеваю, спасибо", callback_data='thanks_ru')
        btn2 = InlineKeyboardButton("Хочу продлить срок хранения", callback_data='not_received_ru')
        btn3 = InlineKeyboardButton("На главную", callback_data='ru')
    else:  # Assuming the other language is Kazakh
        text = 'Тапсырыстарды шығару орнында сақтау мерзімі олардың жеткізілген сәтінен бастап 5 күн.\nУақытында алып кетуге үлгересіз бе, әлде мерзімін ұзартамыз ба? 😊'
        btn1 = InlineKeyboardButton("Үлгеремін, рахмет", callback_data='thanks_kz')
        btn2 = InlineKeyboardButton("Сақтау мерзімін ұзартқым келеді", callback_data='not_received_kz')
        btn3 = InlineKeyboardButton("Басты бетке", callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(chat_id, text, reply_markup=markup)


def pay_return(chat_id, language):
    if language == 'ru':
        text = 'Подскажите, пожалуйста, с чем связан ваш вопрос?'
        btn2 = InlineKeyboardButton("Оплата заказа", callback_data='pay_order_in_ru')
        btn3 = InlineKeyboardButton("Возврат средств", callback_data='return_goods')
        btn4 = InlineKeyboardButton("На главную⬅️", callback_data='ru')
    else:  # Assuming the other language is Kazakh
        text = 'Жақсы, өтінемін, нақты нені өзгерткіңіз келеді?'
        btn2 = InlineKeyboardButton("Тапсырыс төлемі", callback_data='pay_order_in_kz')
        btn3 = InlineKeyboardButton("Қаражатты қайтару", callback_data='return_goods')
        btn4 = InlineKeyboardButton("Басты бетке⬅️", callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    bot.send_message(chat_id, text, reply_markup=markup)


def pay_order_in(chat_id, language):
    if language == 'ru':
        text = 'Подскажите, пожалуйста, какой у вас вопрос связанный с оплатой заказа?'
        btn2 = InlineKeyboardButton("Какие есть способы оплаты?", callback_data='ways_of_pay_ru')
        btn3 = InlineKeyboardButton("Проблемы при оплате", callback_data='issues_pay_ru')
        btn4 = InlineKeyboardButton("На главную⬅️", callback_data='ru')
    else:  # Assuming the other language is Kazakh
        text = 'Жақсы, өтінемін, нақты нені өзгерткіңіз келеді?'
        btn2 = InlineKeyboardButton("Қандай төлем әдістері бар?", callback_data='ways_of_pay_kz')
        btn3 = InlineKeyboardButton("Төлем кезіндегі мәселелер", callback_data='issues_pay_kz')
        btn4 = InlineKeyboardButton("Басты бетке⬅️", callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    bot.send_message(chat_id, text, reply_markup=markup)


def ways_of_paying(chat_id, language):
    if language == 'ru':
        text = 'Оплата заказов возможна как онлайн, рассрочкой, так и во время получения заказа.'
        btn1 = InlineKeyboardButton("Банковские карты", callback_data='bank_pay_ru')
        btn2 = InlineKeyboardButton("Рассрочка", callback_data='partial_ru')
        btn3 = InlineKeyboardButton("При получении", callback_data='when_receive_ru')
        btn4 = InlineKeyboardButton("На главную⬅️", callback_data='ru')
    else:  # Assuming the other language is Kazakh
        text = 'Жақсы, өтінемін, нақты нені өзгерткіңіз келеді?'
        btn1 = InlineKeyboardButton("Банк карталары", callback_data='bank_pay_kz')
        btn2 = InlineKeyboardButton("Несиелеу", callback_data='partial_kz')
        btn3 = InlineKeyboardButton("Тауар келген кезде", callback_data='when_receive_kz')
        btn4 = InlineKeyboardButton("Басты бетке⬅️", callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    bot.send_message(chat_id, text, reply_markup=markup)


def bank_pay(chat_id, language):
    if language == 'ru':
        text = 'Онлайн вы можете оплатить картой Kaspi.kz или Halyk.'
        btn1 = InlineKeyboardButton("Хорошо", callback_data='thanks_ru')
        btn4 = InlineKeyboardButton("На главную⬅️", callback_data='ru')
    else:  # Assuming the other language is Kazakh
        text = 'Жақсы, өтінемін, нақты нені өзгерткіңіз келеді?'
        btn1 = InlineKeyboardButton("Жақсы", callback_data='thanks_kz')
        btn4 = InlineKeyboardButton("Басты бетке⬅️", callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn4)
    bot.send_message(chat_id, text, reply_markup=markup)


def partial_pay(chat_id, language):
    pass


def when_receive_pay(chat_id, language):
    if language == 'ru':
        text = 'Во время получения заказа вы можете оплатить наличными, либо картой Kaspi.kz, Halyk. Доступные платежные системы при оплате после получения заказа: MasterCard, Visa.'
        btn1 = InlineKeyboardButton("Хорошо", callback_data='thanks_ru')
        btn4 = InlineKeyboardButton("На главную⬅️", callback_data='ru')
    else:  # Assuming the other language is Kazakh
        text = 'Тапсырысты алған кезде сіз ақшамен немесе Kaspi.kz, Halyk карталарымен төлей аласыз. Тапсырысты алғаннан кейін төлеу үшін қол жетімді төлем жүйелері: MasterCard, Visa.'
        btn1 = InlineKeyboardButton("Жақсы", callback_data='thanks_kz')
        btn4 = InlineKeyboardButton("Басты бетке⬅️", callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn4)
    bot.send_message(chat_id, text, reply_markup=markup)


def issues_pay_info(chat_id, language):
    if language == 'ru':
        text = 'Подскажите, пожалуйста, с чем связана техническая ошибка?'
        btn1 = InlineKeyboardButton("Не переходит к оплате", callback_data='no_transition')
        btn2 = InlineKeyboardButton("Не получается ввести промокод", callback_data='no_promo')
        btn3 = InlineKeyboardButton("Другое", callback_data='other_promo_issue')
        btn4 = InlineKeyboardButton("На главную", callback_data='ru')
    else:
        text = 'Техникалық қате немен байланысты екенін айтып беріңізші?'
        btn1 = InlineKeyboardButton("Төлемге өту мүмкін емес", callback_data='no_transition')
        btn2 = InlineKeyboardButton("Промокод енгізе алмаймын", callback_data='no_promo')
        btn3 = InlineKeyboardButton("Басқа", callback_data='other_promo_issue')
        btn4 = InlineKeyboardButton("Басты бетке", callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3, btn4)
    bot.send_message(chat_id, text, reply_markup=markup)


def no_transition_info(chat_id, language):
    if language == 'ru':
        text = 'Часто, техническая ошибка связана с тем, что пользователи неправильно или не до конца вводят свои данные для оформления заказа. Пожалуйста, проверьте вводимые данные на наличие лишних пробелов и заполненных всех строк.'
        btn1 = InlineKeyboardButton("Помогло, спасибо", callback_data='thanks_ru')
        btn2 = InlineKeyboardButton("Ознакомились, но все равно не получается", callback_data='not_work_ru')
        btn3 = InlineKeyboardButton("На главную", callback_data='ru')
    else:  # Kazakh language
        text = 'Жиі, техникалық қате пайдаланушылар тапсырыс рәсімдеу үшін өз деректерін дұрыс немесе толық енгізбеген кезде пайда болады. Енгізілген деректерді артық бос орындар мен барлық жолдар толтырылғанына тексеріп көріңіз.'
        btn1 = InlineKeyboardButton("Көмектесті, рахмет", callback_data='thanks_kz')
        btn2 = InlineKeyboardButton("Таныстым, бірақ бәрібір істемейді", callback_data='not_work_kz')
        btn3 = InlineKeyboardButton("Басты бетке", callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn1)  # First button in its own row
    markup.add(btn2)  # Second button in its own row
    markup.add(btn3)  # Third button in its own row

    bot.send_message(chat_id, text, reply_markup=markup)


def still_not_work(chat_id, language):
    if language == 'ru':
        text = 'Так как наше приложение очень часто обновляется, порой наши разработчики могут за чем-то не уследить. Поэтому рекомендуем вам переустановить приложение. Тем самым вы очистите кэш памяти и ошибка может пропасть. Не переживайте, все товары находящиеся в корзине сохранятся.'
        btn1 = InlineKeyboardButton("Ошибка пропала, спасибо", callback_data='thanks_ru')
        btn2 = InlineKeyboardButton("Нет, не помогло", callback_data='not_helped')
        btn3 = InlineKeyboardButton("На главную", callback_data='ru')
    else:  # Kazakh language
        text = 'Біздің қосымша жиі жаңартылатындықтан, кейде біздің әзірлеушілер бір нәрсені байқамауы мүмкін. Сондықтан қосымшаны қайта орнатуды ұсынамыз. Бұл арқылы сіз кэш жадын тазалайсыз және қате жоғалуы мүмкін. Алаңдамаңыз, себетте барлық тауарлар сақталады.'
        btn1 = InlineKeyboardButton("Қате жоғалды, рахмет", callback_data='thanks_kz')
        btn2 = InlineKeyboardButton("Жоқ, көмектеспеді", callback_data='not_helped')
        btn3 = InlineKeyboardButton("Басты бетке", callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.row(btn1)  # First button in its own row
    markup.row(btn2)  # Second button in its own row
    markup.row(btn3)  # Third button in its own row

    bot.send_message(chat_id, text, reply_markup=markup)


def no_promo_info(chat_id, language):
    if language == 'ru':
        text = 'Технические проблемы связанные с вводом промокода возникают крайне редко.\n\n' \
               'Рекомендуем вам проверить, заполнили ли вы все данные для оформления заказа, ' \
               'имя, способ доставки, телефон, адрес доставки.\n' \
               'После повторить попытку.\n\n' \
               'Также обращаем внимание, что в промокоде не должно быть пробелов и лишних символов.'
        btn1 = InlineKeyboardButton('Cпасибо, помогло', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('Все заполнил(-а), пробелов нет', callback_data='still_no_promo')
        btn3 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = 'Промокод енгізгенде техникалық ақаулар өте сирек кездеседі.\n\n' \
               'Тапсырысты рәсімдеу үшін барлық деректерді дұрыс толтырғаныңызды тексеруіңізді ұсынамыз: ' \
               'атыңыз, жеткізу тәсілі, телефон, жеткізу мекен-жайы.\n' \
               'Содан кейін қайта байқап көріңіз.\n\n' \
               'Сонымен қатар, промокодта артық бос орындар мен лишние символдар болмауы тиіс екенін ескертеміз.'

        btn1 = InlineKeyboardButton('Рахмет, көмектесті', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Барлығын толтырдым, бос орындар жоқ', callback_data='still_no_promo')
        btn3 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.row(btn1)  # First button in its own row
    markup.row(btn2)  # Second button in its own row
    markup.row(btn3)  # Third button in its own row

    bot.send_message(chat_id, text, reply_markup=markup)

    # Add the code to send the message with the button here


def still_no_promo(chat_id, language):
    if language == 'ru':
        text = 'Подскажите, пожалуйста, какая ошибка возникает при вводе промокода?'
        btn1 = InlineKeyboardButton('Промокод уже использован', callback_data='promo_used')
        btn2 = InlineKeyboardButton('Срок действия промокода истек', callback_data='promo_expired')
        btn3 = InlineKeyboardButton('Другая', callback_data='other_promo_issue')
        btn4 = InlineKeyboardButton('На главную', callback_data='ru')
    else:  # Kazakh language
        text = 'Өтінемін, промокод енгізгенде қандай қате пайда болады?'
        btn1 = InlineKeyboardButton('Промокод қолданылған', callback_data='promo_used')
        btn2 = InlineKeyboardButton('Промокодтың әрекет ету мерзімі өтіп кеткен', callback_data='promo_expired')
        btn3 = InlineKeyboardButton('Басқа', callback_data='other_promo_issue')
        btn4 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    bot.send_message(chat_id, text, reply_markup=markup)


def promo_used(chat_id, language):
    if language == 'ru':
        text = ('Возможно, вы уже использовали промокод в другом неоформленном заказе. Поэтому система не дает вам '
                'применить промокод повторно. Проверьте, пожалуйста, раздел "Мои Заказы" на наличие активных заказов.\n'
                'Если таковые имеются, вы можете продолжить оформление старого заказа или отменить его.\n'
                'После отмены промокод вновь станет доступным.\n\n'
                'Раздел Мои Заказы можно найти так:\n'
                'iOS - Профиль - Мои заказы - Активные\n'
                'Android - Кабинет - Мои заказы - Активные\n'
                'Сайт - Правый верхний угол, Мои заказы - Активные.')

        btn1 = InlineKeyboardButton('Спасибо помогло', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('Активных заказов нет, не помогло', callback_data='no_active_order')
        btn3 = InlineKeyboardButton('На главную', callback_data='ru')
    else:  # Kazakh language
        text = (
            'Мүмкін, сіз промокодты басқа жасалмаған тапсырыста қолданған боларсыз. Сондықтан жүйе сізге промокодты '
            'қайта қолдануға мүмкіндік бермейді. Өтінемін, "Менің Тапсырыстарым" бөлімін тексеріңіз, онда белсенді '
            'тапсырыстар бар ма екенін.\n'
            'Егер олай болса, сіз ескі тапсырысты рәсімдеуді жалғастыра аласыз немесе оны болдырмауыңызға болады.\n'
            'Болдырмағаннан кейін промокод қайтадан қолжетімді болады.\n\n'
            '"Менің Тапсырыстарым" бөлімін мұнда табуға болады:\n'
            'iOS - Профиль - Менің тапсырыстарым - Белсенді\n'
            'Android - Кабинет - Менің тапсырыстарым - Белсенді\n'
            'Сайт - Оң жоғарғы бұрыш, Менің тапсырыстарым - Белсенді.')

        btn1 = InlineKeyboardButton('Рахмет, көмектесті', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Белсенді тапсырыстар жоқ, көмектеспеді', callback_data='no_active_order')
        btn3 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    bot.send_message(chat_id, text, reply_markup=markup)


def promo_expired(chat_id, language):
    if language == 'ru':
        text = (
            'Дело в том, что все промокоды на Ushop Market имеют срок жизни, в случае, если вы получили данную ошибку - '
            'промокод уже не активен.\n'
            'Но не спешите огорчаться - мы часто отправляем новые, чтобы вы могли приобретать товары с большей выгодой. '
            'Следите за обновлениями в приложении Ushop Market и наших социальных сетях 🙂')

        btn1 = InlineKeyboardButton('Хорошо, понимаю', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('Уверен (-а), код еще работает', callback_data='code_works')
        btn3 = InlineKeyboardButton('На главную', callback_data='ru')
    else:  # Kazakh language
        text = ('Ushop Market-тегі барлық промокодтардың өмір сүру мерзімі бар, егер сіз бұл қатені алсаңыз - '
                'промокод артық белсенді емес.\n'
                'Бірақ қапаланбаңыз - біз жиі жаңа промокодтар жібереміз, сіз тауарларды одан да үлкен пайдамен сатып ала '
                'аласыз. Ushop Market қосымшасында және біздің әлеуметтік желілерімізде жаңартуларды қадағалаңыз 🙂')

        btn1 = InlineKeyboardButton('Жақсы, түсінемін', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('Сенімдімін, код әлі жұмыс істейді', callback_data='code_works')
        btn3 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    bot.send_message(chat_id, text, reply_markup=markup)


def return_goods_info(chat_id, language):
    if language == 'ru':
        text = 'Подскажите, пожалуйста, какой у вас вопрос связанный с возвратом заказа?'
        btn1 = InlineKeyboardButton('Мне не вернулись деньги', callback_data='not_received_ru')
        btn2 = InlineKeyboardButton('Хочу вернуть товар', callback_data='return_product')
        btn4 = InlineKeyboardButton('Другой', callback_data='other_return_issue')
        btn5 = InlineKeyboardButton('На главную', callback_data='ru')
    else:  # Kazakh language
        text = 'Өтінемін, тапсырысты қайтаруға байланысты қандай сұрағыңыз бар?'
        btn1 = InlineKeyboardButton('Ақшам қайтарылмады', callback_data='not_received_kz')
        btn2 = InlineKeyboardButton('Тауарды қайтарғым келеді', callback_data='return_product')
        btn4 = InlineKeyboardButton('Басқа', callback_data='other_return_issue')
        btn5 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn4, btn5)

    bot.send_message(chat_id, text, reply_markup=markup)


def return_product_info(chat_id, language):
    if language == 'ru':
        text = 'Подскажите, пожалуйста, у вас есть претензии к качеству товара?'
        btn1 = InlineKeyboardButton('Есть', callback_data='yes_choice')
        btn2 = InlineKeyboardButton('Нет', callback_data='no_choice')
    else:
        text = 'Тауар сапасына қатысты шағымдарыңыз бар ма?'
        btn1 = InlineKeyboardButton('Бар', callback_data='yes_choice')
        btn2 = InlineKeyboardButton('Жоқ', callback_data='no_choice')
    markup = InlineKeyboardMarkup()
    markup.row(btn1, btn2)
    bot.send_message(chat_id, text, reply_markup=markup)


def guarantee_info(chat_id, language, state):
    if state == 'yes_guarantee':
        if language == 'ru':
            text = (
                "В данном случае бракованный товар в сохранившейся комплектации вы можете принести в течение срока гарантии, "
                "в любой удобный пункт выдачи.\n\n"
                "Администратор проверит отсутствие следов эксплуатации, которые могли привести к поломке и в случае их "
                "отсутствия мы оформим вам возврат.\n\n"
                "Обращаем внимание, товар может быть принят на диагностику для подтверждения наличия заводского дефекта. "
                "Срок проверки регламентируется статьями закона о защите прав потребителей."
            )
            btn1 = InlineKeyboardButton('Хорошо', callback_data='thanks_ru')
            btn2 = InlineKeyboardButton('На главную', callback_data='ru')
        else:
            text = (
                "Осы жағдайда, ақаулы тауарды сақталған жиынтығымен кепілдік мерзімі ішінде кез келген ыңғайлы тарату орнына әкелуге болады.\n\n"
                "Әкімші пайдалану іздерінің болмауын тексереді, олар бұзылуға әкелуі мүмкін, және олардың болмауы жағдайында біз сізге қайтарымды ресімдейміз.\n\n"
                "Назар аударыңыз, тауар зауыттық ақау болуын растау үшін диагностикаға қабылдануы мүмкін. Тексеру мерзімі тұтынушылар құқығын қорғау туралы заңның мақалаларымен реттеледі."
            )
            btn1 = InlineKeyboardButton('Жақсы', callback_data='thanks_kz')
            btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')
    else:
        if language == 'ru':
            text = (
                "В данном случае бракованный товар в сохранившейся комплектации вы можете принести в любой удобный пункт выдачи.\n\n"
                "Администратор проверит отсутствие следов эксплуатации, которые могли привести к поломке и в случае их "
                "отсутствия мы оформим вам возврат.\n\n"
                "Обращаем внимание, товар может быть принят на диагностику для подтверждения наличия заводского дефекта. "
                "Срок проверки регламентируется статьями закона о защите прав потребителей."
            )
            btn1 = InlineKeyboardButton('Хорошо', callback_data='thanks_ru')
            btn2 = InlineKeyboardButton('На главную', callback_data='ru')
        else:
            text = (
                "Осы жағдайда, ақаулы тауарды сақталған жиынтығымен кез келген ыңғайлы тарату орнына әкелуге болады.\n\n"
                "Әкімші пайдалану іздерінің болмауын тексереді, олар бұзылуға әкелуі мүмкін, және олардың болмауы жағдайында біз сізге қайтарымды ресімдейміз.\n\n"
                "Назар аударыңыз, тауар зауыттық ақау болуын растау үшін диагностикаға қабылдануы мүмкін. Тексеру мерзімі тұтынушылар құқығын қорғау туралы заңның мақалаларымен реттеледі."
            )
            btn1 = InlineKeyboardButton('Жақсы', callback_data='thanks_kz')
            btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.row(btn1, btn2)
    bot.send_message(chat_id, text, reply_markup=markup)


def no_choice_info(chat_id, language):
    if language == 'ru':
        text = "Подскажите, пожалуйста, сколько дней прошло с даты, когда вы забрали заказ?"
        btn1 = InlineKeyboardButton('10 или менее дней', callback_data='less_than_10')
        btn2 = InlineKeyboardButton('Прошло более 10 дней', callback_data='more_than_10')
        btn3 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = "Өтінемін, айтыңызшы, тапсырысты алған күннен бастап неше күн өтті?"
        btn1 = InlineKeyboardButton('10 күн немесе одан аз', callback_data='less_than_10')
        btn2 = InlineKeyboardButton('10 күннен астам уақыт өтті', callback_data='more_than_10')
        btn3 = InlineKeyboardButton('Басты бетке', callback_data='kz')
    markup = InlineKeyboardMarkup()
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    bot.send_message(chat_id, text, reply_markup=markup)


def less_than_10_info(chat_id, language):
    if language == 'ru':
        text = "Подскажите, пожалуйста, товар сохранил свою упаковку и не был использован в быту?"
        btn1 = InlineKeyboardButton('Да, верно', callback_data='yes_pack')
        btn2 = InlineKeyboardButton('Нет', callback_data='no_pack')
        btn3 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        # Here you can put the text and buttons for another language if needed
        # For example, a Kazakh version
        text = "Өтінемін, айтыңызшы, тауар өз қаптамасын сақтады ма және тұрмыста пайдаланылған жоқ па?"
        btn1 = InlineKeyboardButton('Иә, дұрыс', callback_data='yes_pack')
        btn2 = InlineKeyboardButton('Жоқ', callback_data='no_pack')
        btn3 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    bot.send_message(chat_id, text, reply_markup=markup)


def yes_pack_info(chat_id, language):
    if language == 'ru':
        text = (
            "Вы можете принести товар в пункт выдачи в течение 10 дней с момента получения заказа, администратор "
            "проверит отсутствие следов эксплуатации и в случае их отсутствия мы оформим вам возврат.\n\n"
            "Если ваш товар входит в перечень невозвратных, к сожалению, возврат не может быть проведен. "
            "Перечень невозвратных товаров указан на нашем сайте: "
        )
        btn1 = InlineKeyboardButton('Хорошо', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = (
            "Сіз тапсырыс алғаннан кейінгі 10 күн ішінде тауарды тарату пунктіне әкеле аласыз, әкімшілік пайдалану іздерінің "
            "жоқтығын тексереді және олардың болмаған жағдайда біз сізге қайтарымды ресімдейміз.\n\n"
            "Егер сіздің тауарыңыз қайтарылмайтын тауарлар тізіміне кірсе, өкінішке орай, қайтару мүмкін емес. Қайтарылмайтын "
            "тауарлар тізімі біздің веб-сайтымызда көрсетілген: "
        )
        btn1 = InlineKeyboardButton('Жақсы', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.row(btn1)
    markup.row(btn2)
    bot.send_message(chat_id, text, reply_markup=markup)


def no_pack_info(chat_id, language):
    if language == 'ru':
        text = (
            "Увы, в таком случае, мы не сможем принять подобный товар на возврат 😞\n\n"
            "Но вы можете написать продавцу для согласования подобного возврата, возможно, он сможет разрешить вам "
            "вернуть товар, даже если прошло более 7 дней или товар уже был использован в быту."
        )
        btn1 = InlineKeyboardButton('Хорошо, понимаю', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('Как можно написать продавцу?', callback_data='contact_seller')
        btn3 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = (
            "Өкінішке орай, осындай жағдайда біз мұндай тауарды қайтаруға қабылдай алмаймыз 😞\n\n"
            "Дегенмен, сіз сатушыға осындай қайтаруды келісу үшін жаза аласыз, мүмкін ол сізге тауарды қайтаруға "
            "рухсат бере алады, тіпті 7 күннен астам уақыт өтсе немесе тауар тұрмыста қолданылған болса."
        )
        btn1 = InlineKeyboardButton('Жақсы, түсіндім', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Сатушыға қалай жазуға болады?', callback_data='contact_seller')
        btn3 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(chat_id, text, reply_markup=markup)


def contact_seller_info(chat_id, language):
    if language == 'ru':
        text = (
            "Для этого зайдите в мобильное приложение Ushop Market, выберите товар, который вы хотите вернуть, "
            "пролистайте ниже и нажмите кнопку “Задать вопрос продавцу”.\n\n"
            "Если продавец не выйдет на связь в течение двух суток- оповестите, пожалуйста, нас через кнопку "
            "“🧑‍💻Написать человеку” в главном меню бота - мы постараемся ускорить время реакции представителя магазина."
        )
        btn1 = InlineKeyboardButton('Хорошо, понимаю', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        # Kazakh translation (or any other language)
        text = (
            "Бұл үшін Ushop Market мобильді қосымшасына кіріңіз, қайтарғыңыз келетін тауарды таңдаңыз, "
            "төменге айналдырыңыз да “Сатушыға сұрақ қою” түймесін басыңыз.\n\n"
            "Егер сатушы екі тәулік ішінде хабарласпаса, өтінемін, боттың басты мәзіріндегі “🧑‍💻Адамға жазу” түймесі арқылы "
            "бізге хабарлаңыз - біз дүкен өкілінің жауап беру уақытын жылдамдатуға тырысамыз."
        )
        btn1 = InlineKeyboardButton('Жақсы, түсінемін', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup()
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(chat_id, text, reply_markup=markup)


def goods_in_info(chat_id, language):
    if language == 'ru':
        text = "Подскажите, пожалуйста, какой у вас вопрос связанный с товаром?"
        btn1 = InlineKeyboardButton('Получил(-а) не тот/битый/не весь товар', callback_data='damaged')
        btn2 = InlineKeyboardButton('Как пользоваться товаром?', callback_data='how_to_use')
        btn3 = InlineKeyboardButton('В моем заказе не хватает товара', callback_data='damaged')
        btn4 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        # Kazakh translation (or any other language)
        text = "Өтінемін, айтыңызшы, сіздің тауарға қатысты қандай сұрағыңыз бар?"
        btn1 = InlineKeyboardButton('Басқа/сынған/толық емес тауар алдым', callback_data='damaged')
        btn2 = InlineKeyboardButton('Тауарды қалай пайдалану керек?', callback_data='how_to_use')
        btn3 = InlineKeyboardButton('Менің тапсырысымда тауар жетіспейді', callback_data='damaged')
        btn4 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2], [btn3], [btn4]])
    bot.send_message(chat_id, text, reply_markup=markup)


def how_to_use(chat_id, language):
    if language == 'ru':
        text = (
            "О характеристиках и нюансах товара, а также о том, как правильно его использовать, вы можете прочесть "
            "в описании товара или уточнить информацию у продавца.\n\n"
            "Для этого в мобильном приложении Ushop Market выберите товар, который интересует, пролистайте ниже "
            "и нажмите кнопку “Задать вопрос продавцу”.\n\n"
            "Если продавец не выйдет на связь в течение суток - оповестите, пожалуйста, нас - через кнопку "
            "“🧑‍💻Написать человеку” в главном меню бота. Мы постараемся ускорить время реакции представителя магазина."
        )
        btn1 = InlineKeyboardButton('Хорошо, понимаю', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        # Kazakh translation (or any other language)
        text = (
            "Тауардың сипаттамалары мен нюанстары туралы, сондай-ақ оны қалай дұрыс пайдалану керектігі туралы ақпаратты "
            "тауар сипаттамасынан оқи аласыз немесе сатушыдан анықтауға болады.\n\n"
            "Бұл үшін Ushop Market мобильді қосымшасында қызықтыратын тауарды таңдап, төменге айналдырып, “Сатушыға сұрақ қою” "
            "түймесін басыңыз.\n\n"
            "Егер сатушы бір тәулік ішінде хабарласпаса, өтінемін, бізге хабарлаңыз - боттың басты мәзіріндегі “🧑‍💻Адамға жазу” "
            "түймесі арқылы. Біз дүкен өкілінің жауап беру уақытын жылдамдатуға тырысамыз."
        )
        btn1 = InlineKeyboardButton('Жақсы, түсіндім', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2]])
    bot.send_message(chat_id, text, reply_markup=markup)


def yes_other_person(chat_id, language):
    if language == 'ru':
        text = (
            "К сожалению, ваш заказ не может забрать другой человек, так как он оформлен в рассрочку. "
            "Заказ с рассрочкой может получить только оформитель рассрочки. Вам нужно будет подойти с паспортом, "
            "чтобы оформить договор рассрочки."
        )
        btn1 = InlineKeyboardButton('Хорошо, понимаю', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        # Kazakh translation (or any other language)
        text = (
            "Өкінішке орай, сіздің тапсырысыңызды басқа адам ала алмайды, өйткені ол бөліп төлеумен рәсімделген. "
            "Бөліп төлеумен рәсімделген тапсырысты тек бөліп төлеуді рәсімдеген адам ала алады. Сізге паспортпен келіп, "
            "бөліп төлеу шартын рәсімдеу қажет болады."
        )
        btn1 = InlineKeyboardButton('Жақсы, түсіндім', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2]])
    bot.send_message(chat_id, text, reply_markup=markup)


def no_other_person(chat_id, language):
    if language == 'ru':
        text = (
            "Другой человек может забрать заказ, для этого необходимо передать ему номер заказа и код для получения. "
            "Код поступает в push уведомлении, если вы пропустили уведомление - его можно найти в разделе 'Мои Заказы', "
            "вкладка 'Текущие' внутри заказа присутствует кнопка 'Получить заказ' код находится там 😇\n\n"
            "Также фактический получатель должен иметь при себе документ подтверждающий личность."
        )
        btn1 = InlineKeyboardButton('Хорошо', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        # Kazakh translation (or any other language)
        text = (
            "Басқа адам тапсырысты ала алады, ол үшін тапсырыс нөмірі мен алу кодын беру қажет. "
            "Код push хабарламасында келеді, егер сіз хабарламаны өткізіп алсаңыз - оны 'Менің Тапсырыстарым' бөлімінен, "
            "'Ағымдағы' қойындысында, тапсырыс ішінде 'Тапсырысты алу' түймесі бар, код сол жерде 😇\n\n"
            "Сонымен қатар, нақты алушының өзіндіктігін растайтын құжаты болуы тиіс."
        )
        btn1 = InlineKeyboardButton('Жақсы', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2]])
    bot.send_message(chat_id, text, reply_markup=markup)


def delivery_info(chat_id, language):
    if language == 'ru':
        text = (
            "Доставка до пункта выдачи Ushop Market бесплатна.\n\n"
            "Доставка курьером стоит 1 500 тенге, но если сумма заказа будет выше 35 000 тенге, заказ привезут "
            "бесплатно в любую доступную точку города, в котором открыт наш пункт выдачи.\n\n"
            "С удовольствием доставим ваши заказы!🍇"
        )
        btn1 = InlineKeyboardButton('Хорошо', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        # Kazakh translation (or any other language)
        text = (
            "Ushop Market тарату пунктіне дейін жеткізу тегін.\n\n"
            "Курьер арқылы жеткізу 1 500 теңге тұрады, бірақ егер тапсырыс сомасы 35 000 теңгеден жоғары болса, "
            "тапсырыс кез келген қаланың қолжетімді нүктесіне тегін жеткізіледі, онда біздің тарату пунктіміз ашық.\n\n"
            "Тапсырыстарыңызды жеткізуден қуаныштымыз!🍇"
        )
        btn1 = InlineKeyboardButton('Жақсы', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2]])
    bot.send_message(chat_id, text, reply_markup=markup)


def not_find_info(chat_id, language):
    if language == 'ru':
        text = (
            "Возможно, ваш вопрос связан с одной из этих тем?\n\n"
            "Выберите подходящую тему вопроса или обратитесь к сотруднику поддержки."
        )
        btn1 = InlineKeyboardButton('Где найти промокоды', callback_data='find_promo')
        btn2 = InlineKeyboardButton('Сотрудничество', callback_data='cooperation')
        btn3 = InlineKeyboardButton('Отзывы', callback_data='reviews')
        btn4 = InlineKeyboardButton('Написать сотруднику', callback_data='write_to_person')
        btn5 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        # Kazakh translation (or any other language)
        text = (
            "Мүмкін, сіздің сұрағыңыз осы тақырыптардың бірімен байланысты шығар?\n\n"
            "Сұрақтың сізге лайық тақырыбын таңдаңыз немесе қолдау қызметкеріне жүгініңіз."
        )
        btn1 = InlineKeyboardButton('Промокодты қайдан табуға болады', callback_data='find_promo')
        btn2 = InlineKeyboardButton('Серіктестік', callback_data='cooperation')
        btn3 = InlineKeyboardButton('Пікірлер', callback_data='reviews')
        btn4 = InlineKeyboardButton('Қызметкерге жазу', callback_data='write_to_person')
        btn5 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2], [btn3], [btn4], [btn5]])
    bot.send_message(chat_id, text, reply_markup=markup)


def find_promo_info(chat_id, language):
    if language == 'ru':
        text = (
            "Активные промокоды появляются на нашем сайте или в социальных сетях. Также мы их публикуем в личном "
            "кабинете, об этом клиентам поступают уведомления. Поэтому рекомендуем вам включить уведомления от "
            "приложения Ushop Market - как только появятся новые предложения, вы узнаете одним из первых 😊\n\n"
            "Instagram:\n"
            "Telegram канал:\n"
            "Будем рады вашей подписке 😍"
        )
        btn1 = InlineKeyboardButton('Хорошо, поскорее бы.', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        # Kazakh translation (or any other language)
        text = (
            "Белсенді промокодтар біздің веб-сайтымызда немесе әлеуметтік желілерде пайда болады. Сондай-ақ, біз оларды "
            "жеке кабинетте жариялаймыз, бұл туралы клиенттерге хабарламалар келеді. Сондықтан Ushop Market қосымшасынан "
            "хабарламаларды қосуға кеңес береміз - жаңа ұсыныстар пайда бола салысымен, сіз біріншілерден болып білесіз 😊\n\n"
            "Instagram:\n"
            "Telegram арнасы:\n"
            "Жазылуыңызды қуана қабылдаймыз 😍"
        )
        btn1 = InlineKeyboardButton('Жақсы, тезірек болсын.', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2]])
    bot.send_message(chat_id, text, reply_markup=markup)


def cities_info(chat_id, language):
    if language == 'ru':
        text = (
            "Мы уже успели открыться в городе Алматы, Шымкент, и Астана! Будем дальше расширять свои горизонты и будем "
            "искренне рады видеть вас в числе наших клиентов 😇Следите за нашими обновлениями✨Все наши старания - для вас!💜\n\n"
            "Адреса пунктов выдачи по ссылке:\n"
            "У каждого пункта выдачи прописан адрес и указан график работы✨"
        )
        btn1 = InlineKeyboardButton('Хорошо', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = (
            "Біз Алматы, Шымкент және Астана қалаларында ашылдық! Өз шеңберімізді кеңейтуді жалғастыратын боламыз және сізді "
            "біздің клиенттеріміздің арасында көргенімізге шын жүректен қуанамыз 😇Біздің жаңалықтарымызды бақылаңыз✨Барлық "
            "енгізілген өзгерістер - сіз үшін!💜\n\n"
            "Тарату пункттерінің мекен-жайлары сілтеме бойынша көрсетілген:\n"
            "Әрбір тарату пунктінің мекен-жайы жазылған және жұмыс кестесі көрсетілген✨"
        )
        btn1 = InlineKeyboardButton('Жақсы', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2]])
    bot.send_message(chat_id, text, reply_markup=markup)


def cooperation_info(chat_id, language):
    if language == 'ru':
        text = 'Мы всегда рады сотрудничеству☺️. Подскажите, с чем связан ваш вопрос?'
        btn1 = InlineKeyboardButton('Хочу стать продавцом', callback_data='become_seller')
        btn2 = InlineKeyboardButton('Я продавец и у меня вопрос', callback_data='seller_question')
        btn3 = InlineKeyboardButton('Вакансии Ushop Market', callback_data='ushop_vacancies')
        btn4 = InlineKeyboardButton('Маркетинг/Реклама', callback_data='marketing_advertising')
        btn5 = InlineKeyboardButton('Другое', callback_data='other_cooperation')
        btn6 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = 'Біз әрқашан серіктестікке қуаныштымыз☺️. Сұрағыңыз қандай мәселе бойынша?'
        btn1 = InlineKeyboardButton('Сатушы болғым келеді', callback_data='become_seller')
        btn2 = InlineKeyboardButton('Мен сатушымын және сұрағым бар', callback_data='seller_question')
        btn3 = InlineKeyboardButton('Ushop Market бос орындары', callback_data='ushop_vacancies')
        btn4 = InlineKeyboardButton('Маркетинг/Жарнама', callback_data='marketing_advertising')
        btn5 = InlineKeyboardButton('Басқа', callback_data='other_cooperation')
        btn6 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2], [btn3], [btn4], [btn5], [btn6]])
    bot.send_message(chat_id, text, reply_markup=markup)


def become_seller_info(chat_id, language):
    if language == 'ru':
        text = (
            "Подробнее об условиях сотрудничества вы можете почитать на нашем сайте для партнеров: __________ "
            "Мы готовы начать с вами работать уже завтра, если вам подходит сотрудничество по системе фулфилмент: партнеры "
            "отправляют товар на наш склад, после чего получают прибыль с его реализации.Вопросы вы можете задать менеджеру "
            "в телеграм @______ или начать чат с поддержкой в личном кабинете после регистрации. Будем рады дальнейшему "
            "сотрудничеству 🍇🙌"
        )
        btn1 = InlineKeyboardButton('Понятно', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = (
            "Әріптестік шарттары туралы толығырақ біздің серіктестер сайтынан оқи аласыз: __________ "
            "Егер сізге фулфилмент жүйесі бойынша ынтымақтастық жағдайы ұнайтын болса, ертеңнен бастап сізбен жұмыс істеуге дайынбыз: "
            "әріптестер біздің қоймаға тауар жібереді, содан кейін оның сатылуынан табыс алады. Сұрақтарыңызды телеграмдағы менеджерге "
            "@______ немесе тіркелгеннен кейін жеке кабинетте қолдау қызметімен чат арқылы қоя аласыз. Одан әрі ынтымақтастықты жалғастыруға "
            "қуаныштымыз 🍇🙌"
        )
        btn1 = InlineKeyboardButton('Түсінікті', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2]])
    bot.send_message(chat_id, text, reply_markup=markup)


def seller_question(chat_id, language):
    if language == 'ru':
        text = (
            "Для создания обращения в вашем личном кабинете есть удобный чат с поддержкой. Для того, чтобы написать "
            "сообщение, нажмите на красный значок в нижнем правом углу личного кабинета.\n"
            "Если телеграм вам удобнее - напишите боту @___________, и обращение будет передано менеджеру "
            "поддержки в чате.\n\n"
            "Почти все интересующие вас ответы есть здесь: ________________"
        )
        btn1 = InlineKeyboardButton('Хорошо', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = (
            "Жеке кабинетіңізде қолдау қызметімен сөйлесу үшін ыңғайлы чат бар. Хабар жазу үшін жеке кабинеттің төменгі "
            "оң жақ бұрышындағы қызыл белгішені басыңыз.\n"
            "Егер телеграм сізге ыңғайлы болса - @___________ ботына жазыңыз, және сіздің өтінішіңіз қолдау "
            "менеджерінің чатына жіберіледі.\n\n"
            "Сізді қызықтыратын көптеген жауаптар мұнда бар: ________________"
        )
        btn1 = InlineKeyboardButton('Жақсы', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2]])
    bot.send_message(chat_id, text, reply_markup=markup)


def ushop_vacancies_info(chat_id, language):
    if language == 'ru':
        text = (
            "Вы можете предложить свою кандидатуру, позвонив на нашу горячую линию: +7 _______________, "
            "выберите консультацию с HR-отделом в будни с 9:00 до 18:00 😊\n"
            "В выходные, к сожалению, отдел не работает.\n\n"
            "Либо, вы можете просмотреть вакансии на hh.kz, и откликнуться на подходящею: _________________\n"
            "Будем рады видеть вас в наших рядах❤️"
        )
        btn1 = InlineKeyboardButton('Круто, пойду посмотрю', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = (
            "Сіз өз үміткерлігіңізді ұсыну үшін біздің жедел желімізге қоңырау шалуыңызға болады: +7 _______________, "
            "дүйсенбіден жұмаға дейін 9:00-ден 18:00-ге дейін HR бөлімімен кеңесу қызметін таңдаңыз 😊\n"
            "Демалыс күндері бөлім жұмыс істемейді.\n\n"
            "Немесе, hh.kz сайтынан бос орындарға қарап, сәйкес келетініне жауап бере аласыз: _________________\n"
            "Сізді біздің қатарымызда көргенімізге қуаныштымыз❤️"
        )
        btn1 = InlineKeyboardButton('Керемет, қарап көремін', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2]])
    bot.send_message(chat_id, text, reply_markup=markup)


def reviews_info(chat_id, language):
    if language == 'ru':
        text = "Подскажите, пожалуйста, какой у вас вопрос связанный с отзывами?"
        btn1 = InlineKeyboardButton('Как оставить отзыв?', callback_data='how_to_review')
        btn2 = InlineKeyboardButton('Почему отзыв не публикуется сразу?', callback_data='not_published')
        btn3 = InlineKeyboardButton('У меня другой вопрос с отзывом', callback_data='other_review_question')
        btn4 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = "Өтінемін, пікірлермен байланысты қандай сұрағыңыз бар екенін айтыңызшы?"
        btn1 = InlineKeyboardButton('Пікірді қалай қалдыруға болады?', callback_data='how_to_review')
        btn2 = InlineKeyboardButton('Неге пікір бірден жарияланбайды?', callback_data='not_published')
        btn3 = InlineKeyboardButton('Пікірлер бойынша басқа сұрағым бар', callback_data='other_review_question')
        btn4 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2], [btn3], [btn4]])
    bot.send_message(chat_id, text, reply_markup=markup)


def how_to_review_info(chat_id, language):
    if language == 'ru':
        text = (
            "Чтобы оставить отзыв к товару, необходимо:\n"
            "– открыть Личный кабинет;\n"
            "– перейти в раздел «Мои заказы»;\n"
            "– открыть на нужный заказ.\n"
            "Напротив каждого товара появится строка “Оставить отзыв”. Вам необходимо кликнуть на нее и оставить отзыв.\n"
            "После того, как отзыв пройдет модерацию, он будет опубликован."
        )
        btn1 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = (
            "Тауарға пікір қалдыру үшін:\n"
            "– Жеке кабинетті ашу қажет;\n"
            "– «Менің тапсырыстарым» бөліміне өту;\n"
            "– Қажетті тапсырысты ашу керек.\n"
            "Әрбір тауардың қасында “Пікір қалдыру” деген жол пайда болады. Оған басып, пікіріңізді қалдыруыңыз қажет.\n"
            "Пікір модерациядан өткен соң, ол жарияланады."
        )
        btn1 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1]])
    bot.send_message(chat_id, text, reply_markup=markup)


def not_published_info(chat_id, language):
    if language == 'ru':
        text = (
            "У вашего заказа статус всё ещё доставляется, потому отзыв отправить пока невозможно. Дело в том, что на "
            "обновление информации в базе требуется некоторое время. В ближайшее время статус будет обновлен, и при "
            "желании вы сможете оставить отзыв на заказанный вами товар."
        )
        btn1 = InlineKeyboardButton('Хорошо', callback_data='thanks_ru')
        btn2 = InlineKeyboardButton('На главную', callback_data='ru')
    else:
        text = (
            "Сіздің тапсырысыңыздың мәртебесі әлі де жеткізілуде, сондықтан әлі пікір жіберу мүмкін емес. Ақпараттың "
            "базада жаңартылуына біраз уақыт қажет. Жақын арада мәртебе жаңартылады, және қалауыңыз бойынша сіз тапсырылған "
            "тауарыңызға пікір қалдыра аласыз."
        )
        btn1 = InlineKeyboardButton('Жақсы', callback_data='thanks_kz')
        btn2 = InlineKeyboardButton('Басты бетке', callback_data='kz')

    markup = InlineKeyboardMarkup([[btn1], [btn2]])
    bot.send_message(chat_id, text, reply_markup=markup)



bot.polling(non_stop=True)
