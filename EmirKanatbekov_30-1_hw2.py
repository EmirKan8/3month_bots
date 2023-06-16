import logging
import random
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config

TOKEN = config("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, f"Добро пожаловать в EmirKan bot, {message.from_user.full_name}!\n"
                                            f"В этом боте есть:\n"
                                            f"викторина -> /quiz\n"
                                            f"смешные картинки mem -> /mem\n"
                                            f"и другие команды!")

@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    options = [
        types.InlineKeyboardButton(text='Ответ 1', callback_data='answer_1'),
        types.InlineKeyboardButton(text='Ответ 2', callback_data='answer_2'),
        types.InlineKeyboardButton(text='Ответ 3', callback_data='answer_3'),
    ]
    markup.add(*options)
    next_button = InlineKeyboardButton("NEXT", callback_data="next_button_1")
    markup.add(next_button)

    question = "Кто создал Chatgpt?"
    answers = [
        "James Cameron",
        "Sam Altman",
        "Elon Musk",
        "Batman",
        "Spongebob",
    ]

    await message.answer_poll(
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        reply_markup=markup
    )


@dp.callback_query_handler(text="next_button_1")
async def quiz_2(callback: types.CallbackQuery):
    question = "В каком году был основан Geeks?"
    answers = ['2005', '2010', '2018', 'Я не знаю']

    await callback.message.answer_poll(
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2
    )


@dp.callback_query_handler(lambda c: c.data.startswith('answer_'))
async def process_quiz_answer(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вы выбрали ответ ' + callback_query.data[7:])


@dp.message_handler(commands=['mem'])
async def get_mem(message: types.Message):
    pass


@dp.message_handler(commands=['pin'])
async def pin_message(message: types.Message):
    if message.reply_to_message:
        await message.reply_to_message.pin()


@dp.message_handler(commands=['game'])
async def send_random_emoji(message: types.Message):
    emojis = ["⚽", "🏀", "🎲", "🎳", "🎰", "🎯"]
    random_emoji = random.choice(emojis)
    await message.answer(random_emoji)

    @dp.message_handler(commands=['dice'])
    async def bot_dice(message: types.Message):
        # bot
        await bot.send_message(message.chat.id, f"Погнали  {message.from_user.full_name}\n"
                                                f"Бот кидает кубик --> ")

        bot1 = await  message.answer_dice()
        print(bot1)

        await bot.send_message(message.chat.id, f"очко : {bot1.dice.value}\n"
                                                f"Теперь ваша очередь  --> \n")

        # user
        await bot.send_message(message.chat.id, f" {message.from_user.full_name}\n"
                                                f"  ваш бросок--> ")

        user = await  message.answer_dice()
        print(user)

        await bot.send_message(message.chat.id, f"очко : {user.dice.value}\n"
                                                f"резултат  --> \n")
        # result

        if bot1.dice.value == user.dice.value:
            await bot.send_message(message.chat.id, f"ничья")

        elif bot1.dice.value < user.dice.value:
            await bot.send_message(message.chat.id, f"победитель -> {message.from_user.full_name}")

        elif bot1.dice.value > user.dice.value:
            await bot.send_message(message.chat.id, f"победитель -> BOT")
        else:
            await bot.send_message(message.chat.id, f"победитель -> BOT")


def register_handlers_1commands(dp: Dispatcher):
    dp.register_message_handler(bot_dice, commands=['dice'])


@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo_message_or_square_number(message: types.Message):
    if message.text.isdigit():
        square = int(message.text) ** 2
        await message.answer(f"Квадрат числа: {square}")
    else:
        await message.answer(message.text)


@dp.message_handler(content_types=types.ContentType.ANY)
async def unknown_message(message: types.Message):
    await message.answer("Неизвестная команда или сообщение.")


@dp.message_handler(content_types=types.ContentType.ANY, is_chat_admin=True)
async def admin_commands(message: types.Message):
    if message.text == '!pin' and message.reply_to_message:
        await message.reply_to_message.pin()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)