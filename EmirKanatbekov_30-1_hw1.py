from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton , InputFile
from decouple import config
import logging


TOKEN = config("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    await bot.send_message(message.chat.id, f"Добро пожаловать в EmirKan bot  {message.from_user.full_name}\n"
                                            f"В этом боте есть \n"
                                            f"викторина -> /quiz \n"
                                            f"смешные картинки mem  -> /mem\n ")



@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message) -> None:
    markup = InlineKeyboardMarkup()
    next_button = InlineKeyboardButton("NEXT", callback_data="next_button_1")
    markup.add(next_button)

    quiestion = "Кто создал Chatgpt?"
    answers = [
        "James Cameron",
        "Sam Altman",
        "Elon Musk",
        "Batman",
        "Spongebob",

    ]


    await message.answer_poll(
        question=quiestion,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        reply_markup=markup
    )


@dp.callback_query_handler(text="next_button_1")
async def quiz_2(callback: types.CallbackQuery):
    quiestion = "В каком году был основан Geeks? "
    answers = ['2005',
               '2010 ',
               '2018',
               'Я не знаю']


    await callback.message.answer_poll(
        question=quiestion,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,

    )
@dp.message_handler(commands=['mem'])
async def get_mem(message: types.Message):
    photo = open (r"C:\Users\EMIR\Downloads\www\src\img\scale_1200.webp",'rb')
    await bot.send_photo(message.chat.id, photo=photo)

@dp.message_handler(content_types=['text'])
async def echo(message: types.Message) -> None:
    await bot.send_sticker(message.chat.id,f"[{message.text}]"  )

@dp.message_handler(content_types=['text'])
async def echo(message: types.Message) -> None:
    await bot.send_sticker(message.chat.id, f"[{message.text}]")


async def echo_message_or_square_number(message: types.Message):
    if message.text.isdigit():
        square = int(message.text) ** 2
        await bot.send_message(message.chat.id, f"Квадрат числа: {square}")
    else:
        await bot.send_message(message.chat.id, f"[{message.text}]")
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=False)