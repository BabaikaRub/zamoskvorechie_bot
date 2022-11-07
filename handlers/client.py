from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot
from keyboards.client_kb import inline_selector, pay_buttons, direction_buttons, inline_menu_back, inline_menu_enroll, inline_menu_wait_list
from keyboards.age_kb import *
from db import get_data


class FSMClient(StatesGroup):
    payment = State()
    direction = State()
    age = State()


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет! Я бот, введи команду /sign_up', reply_markup=ReplyKeyboardRemove())


async def command_sign(message: types.Message):
    await bot.send_message(message.from_user.id, 'Есть две категории занятий, выбери одну ниже', reply_markup=inline_selector)


@dp.callback_query_handler(text='button_free', state=None)
async def free_list(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Выберите форму обучения', reply_markup=pay_buttons)

    # Вот здесь добавить какой-то дополнительный триггер
    await FSMClient.payment.set()
    await callback.answer()


@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def command_cancel(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await bot.send_message(message.from_user.id, 'Действие отменено', reply_markup=types.ReplyKeyboardRemove())


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
async def select_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
        payment, direction = data['payment'], message.text

    if payment == 'Да':
        if direction == 'Техническая направленность':
            await bot.send_message(message.from_user.id, 'Выберите возраст:', reply_markup=tech_dirc_free)
            await FSMClient.next()

        elif direction == 'Социально-гуманитарная направленность':
            await bot.send_message(message.from_user.id, 'Выберите возраст:', reply_markup=social_dirc_free)
            await FSMClient.next()

        elif direction == 'Туристско-краеведческая направленность':
            await bot.send_message(message.from_user.id, 'Выберите возраст:', reply_markup=turist_dirc_free)
            await FSMClient.next()
        
        elif direction == 'Художественная направленность':
            await bot.send_message(message.from_user.id, 'Выберите возраст:', reply_markup=paint_dirc_free)
            await FSMClient.next()
        
        # Заглушка
        else:
            await bot.send_message(message.from_user.id, 'В кружки по данному напралению сейчас запись не идет', reply_markup=types.ReplyKeyboardRemove())
            await state.finish()

    elif payment == 'Нет':
        if direction == 'Техническая направленность':
            await bot.send_message(message.from_user.id, 'Выберите возраст:', reply_markup=tech_dirc_pay)
            await FSMClient.next()

        elif direction == 'Социально-гуманитарная направленность':
            await bot.send_message(message.from_user.id, 'Выберите возраст:', reply_markup=social_dirc_pay)
            await FSMClient.next()

        elif direction == 'Физкультурно-спортивная направленность':
            await bot.send_message(message.from_user.id, 'Выберите возраст:', reply_markup=phys_dirc_pay)
            await FSMClient.next()
        
        # Решить как выводить список возрастов для худ. направленности 
        elif direction == 'Художественная направленность':
            await bot.send_message(message.from_user.id, 'Выберите категорию:', reply_markup=paint_dirc_pay)
            await FSMClient.next()
        
        # Заглушка
        else:
            await bot.send_message(message.from_user.id, 'В кружки по данному напралению сейчас запись не идет', reply_markup=types.ReplyKeyboardRemove())
            await state.finish()


@dp.message_handler(state=FSMClient.age)
async def select_data(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg = message.text
        data['age'] = ' '.join(msg.split()[:2])

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
    await bot.send_message(callback.from_user.id, 'В данных момент запись на данные кружки не ведется\nВы можете записаться в список ожидания, чтобы попасть на выбраное вами направление в дальнейшем', reply_markup=inline_menu_wait_list)

    file = open('files/Busy.xlsx', 'rb')
    await bot.send_document(callback.from_user.id, file)

    await callback.answer()


def registration_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_sign, commands=['sign_up'])
    dp.register_message_handler(command_cancel, state='*', commands=['cancel'])
