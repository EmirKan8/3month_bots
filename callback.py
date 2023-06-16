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