from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


button_1 = KeyboardButton('От 1 года')
button_3 = KeyboardButton('От 3 лет')
button_4 = KeyboardButton('От 4 лет')
button_5 = KeyboardButton('От 5 лет')
button_6 = KeyboardButton('От 6 лет')
button_7 = KeyboardButton('От 7 лет')
button_8 = KeyboardButton('От 8 лет')
button_9 = KeyboardButton('От 9 лет')
button_10 = KeyboardButton('От 10 лет')
button_11 = KeyboardButton('От 11 лет')
button_12 = KeyboardButton('От 12 лет')
button_14 = KeyboardButton('От 14 лет')
button_18 = KeyboardButton('От 18 лет')
button_20 = KeyboardButton('От 20 лет')

tech_dirc_free = ReplyKeyboardMarkup(row_width=1).add(button_6).add(button_8).add(button_10)
social_dirc_free = ReplyKeyboardMarkup(row_width=1).add(button_10)
turist_dirc_free = ReplyKeyboardMarkup(row_width=1).row(button_8, button_12)
paint_dirc_free = ReplyKeyboardMarkup(row_width=1).add(button_7).add(button_8).add(button_12)

tech_dirc_pay = ReplyKeyboardMarkup(row_width=1).add(button_8).add(button_10).add(button_11)
social_dirc_pay = ReplyKeyboardMarkup(row_width=1).add(button_1).add(button_3).add(button_12)
phys_dirc_pay = ReplyKeyboardMarkup(row_width=1).row(button_4, button_6).row(button_8, button_9).row(button_11, button_18)
paint_dirc_pay = ReplyKeyboardMarkup(row_width=1).row(button_3, button_4).row(button_5, button_6).row(button_7, button_8).row(button_12, button_14, button_20)
