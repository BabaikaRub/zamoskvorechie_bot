from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot
from keyboards import inline_selector, pay_buttons, direction_buttons, inline_menu_back, inline_menu_enroll
from db import get_data

class FSMClient(StatesGroup):
    payment = State()
    direction = State()


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет! Я бот, введи команду /sign_up', reply_markup=ReplyKeyboardRemove())


async def command_sign(message: types.Message):
    await bot.send_message(message.from_user.id, 'Есть две категории занятий, выбери одну ниже', reply_markup=inline_selector)


@dp.callback_query_handler(text='button_free', state=None)
async def free_list(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Выберите форму обучения', reply_markup=pay_buttons)

    await FSMClient.payment.set()
    await callback.answer()


@dp.message_handler(Text(equals='Платно'), state=FSMClient.payment)
@dp.message_handler(Text(equals='Бесплатно'), state=FSMClient.payment)
async def select_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Платно':
            data['payment'] = 'Нет'
            
        elif message.text == 'Бесплатно':
            data['payment'] = 'Да'
          
    await FSMClient.next()
    await bot.send_message(message.from_user.id, 'Выберите направление:', reply_markup=direction_buttons)


@dp.message_handler(Text(equals='Техническая направленность'), state=FSMClient.direction)
@dp.message_handler(Text(equals='Физкультурно-спортивная направленность'), state=FSMClient.direction)
@dp.message_handler(Text(equals='Социально-гуманитарная направленность'), state=FSMClient.direction)
@dp.message_handler(Text(equals='Туристско-краеведческая направленность'), state=FSMClient.direction)
@dp.message_handler(Text(equals='Художественная направленность'), state=FSMClient.direction)
async def select_data(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text

    async with state.proxy() as data:
        result = await get_data(data)
    
    await bot.send_message(message.from_user.id, 'Список доступных занятий:', reply_markup=ReplyKeyboardRemove())

    if not result:
        await bot.send_message(message.from_user.id, 'Кружков по такому запросу не найдено!!!')

    else:
        for item in result:
            await bot.send_message(message.from_user.id, f'*Название кружка:* {item[2]}\n*Название группы:* {item[3]}\n*Возраст:* {item[5]}\n*Свободные места:* {item[9]}\n*Код на mos.ru:* {item[10]}', parse_mode="Markdown", reply_markup=inline_menu_enroll)

    await bot.send_message(message.from_user.id, 'Для выбора другого направления нажмите кнопку "Назад"', reply_markup=inline_menu_back)
    await state.finish()


@dp.callback_query_handler(text='button_back')
async def get_back(callback: types.CallbackQuery):
    await free_list(callback)

    await callback.answer()


# @dp.message_handler(Text(equals='Назад'))
# async def get_menu(message: types.Message):
#     await command_sign(message)


@dp.callback_query_handler(text='button_busy')
async def busy_list(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'В данных момент запись на данные кружки не ведется\nВы можете записаться в список ожидания, чтобы попасть на выбраное вами направление в дальнейшем', reply_markup=ReplyKeyboardRemove())

    file = open('files/Busy.xlsx', 'rb')
    await bot.send_document(callback.from_user.id, file)

    await callback.answer()


def registration_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_sign, commands=['sign_up'])
