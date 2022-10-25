from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


inline_button_free = InlineKeyboardButton('Есть записи', callback_data='button_free')
inline_button_busy = InlineKeyboardButton('Нет записей', callback_data='button_busy')

button_budget = KeyboardButton('Платно')
button_pay = KeyboardButton('Бесплатно')
button_back = KeyboardButton('Назад')

button_tech = KeyboardButton('Техническая направленность')
button_sport = KeyboardButton('Физкультурно-спортивная направленность')
button_social = KeyboardButton('Социально-гуманитарная направленность')
button_turist = KeyboardButton('Туристско-краеведческая направленность')
button_paint = KeyboardButton('Художественная направленность')

inline_back = InlineKeyboardButton('Назад', callback_data='button_back')
inline_enroll = InlineKeyboardButton('Записаться', url='https://www.mos.ru/pgu/ru/app/dogm/077060701/#step_1')

inline_menu_enroll = InlineKeyboardMarkup(row_width=1)
inline_menu_enroll.add(inline_enroll)

inline_menu_back = InlineKeyboardMarkup(row_width=1)
inline_menu_back.add(inline_back)

direction_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
direction_buttons.add(button_tech).add(button_sport).add(button_social).add(button_turist).add(button_paint)

inline_selector = InlineKeyboardMarkup(row_width=1)
inline_selector.row(inline_button_free, inline_button_busy)

pay_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
pay_buttons.row(button_budget, button_pay)
