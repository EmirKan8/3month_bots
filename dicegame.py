from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot, dp






async def bot_dice(message: types.Message):
        #bot
        await bot.send_message(message.chat.id, f"Погнали  {message.from_user.full_name}\n"
                                                f"Бот кидает кубик --> ")

        bot1= await  message.answer_dice()
        print (bot1)

        await bot.send_message(message.chat.id, f"очко : {bot1.dice.value}\n"
                                                f"Теперь ваша очередь  --> \n")


        #user
        await bot.send_message(message.chat.id, f" {message.from_user.full_name}\n"
                                            f"  ваш бросок--> ")

        user = await  message.answer_dice()
        print(user)

        await bot.send_message(message.chat.id, f"очко : {user.dice.value}\n"
                                            f"резултат  --> \n")
        #result

        if bot1.dice.value == user.dice.value:
               await bot.send_message(message.chat.id, f"ничья")

        elif bot1.dice.value < user.dice.value:
               await bot.send_message(message.chat.id, f"победитель -> {message.from_user.full_name}")

        elif bot1.dice.value > user.dice.value:
               await bot.send_message(message.chat.id, f"победитель -> BOT" )
        else:
              await bot.send_message(message.chat.id, f"победитель -> BOT")

def register_handlers_1commands(dp: Dispatcher):
    dp.register_message_handler(bot_dice,commands=['dice'])