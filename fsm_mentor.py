from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import tutor_admin, teacher_admin, admins
from handlers.keyboards import start_markup, cancel_markup, submit_markup


class FSMMentor(StatesGroup):
    name = State()
    direction = State()
    age = State()
    group = State()
    submit = State()

async def start_mentor_creation(message: types.Message, state: FSMContext):
    if message.from_user.id not in teacher_admin and tutor_admin and admins:
        await message.answer("Ты не мой босс!")
    else:
        if message.chat.type == 'private':

             await FSMMentor.name.set()
             await message.answer("имя ментора ", reply_markup= cancel_markup)
        else:
              await message.reply("Пиши в личке!")




async def enter_name(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer("Пиши буквами!")
    else:

       async with state.proxy() as data:
        data['name'] = message.text
        await FSMMentor.next()
        await message.answer("Введите направление менторства:", reply_markup= cancel_markup)

async def enter_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await FSMMentor.next()
    await message.answer("Введите возраст ментора:", reply_markup= cancel_markup)

async def enter_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пиши числа!")
    else:
     async with state.proxy() as data:
        data['age'] = message.text
        await FSMMentor.next()
        await message.answer("Введите группу ментора:", reply_markup= cancel_markup)

async def enter_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await message.answer(f"Имя: {data['name']}\n"
                         f"Возраст: {data['age']}\n"
                         f"Группа: {data['group']}\n"
                         f"Направление: {data['direction']}\n")
    await FSMMentor.next()
    await message.answer("Все верно", reply_markup= submit_markup)

async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        # TODO: Запись в БД
        await state.finish()
        await message.answer("Записал в БД!")
    elif message.text.lower() == 'заново':
        await message.answer("пиши команду -> /reg")
        await state.finish()
    elif message.text.lower() == 'cancel':
        await state.finish()
        await message.answer('Отменено!')
    else:
        await message.answer("Используй кнопки!")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await message.answer(" пока ", reply_markup=start_markup)

    await state.finish()

def register_handlers_fsm_mentor(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, commands=['cancel'], state='*')
    dp.register_message_handler(cancel_reg, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(start_mentor_creation, commands=['/reg'])
    dp.register_message_handler(enter_name, state=FSMMentor.name)
    dp.register_message_handler(enter_direction, state=FSMMentor.direction)
    dp.register_message_handler(enter_age, state=FSMMentor.age)
    dp.register_message_handler(enter_group, state=FSMMentor.group)