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


