import json

from aiogram import Bot,Dispatcher,executor,types
from connect_db import pull_schedule
async def list_key(message: types.Message,call, name_key):
    #FAQ = []
    keyboard = types.InlineKeyboardMarkup()
    if call == 0:
        user_id = str(message.chat.id)
    else:
        user_id = str(call.message.chat.id)
    for x in name_key:
        if x != 'que' and x != 'adm':
            key_a = types.InlineKeyboardButton(text=name_key[x], callback_data=x)
            keyboard.add(key_a)
        elif x == 'que':
            question = name_key[x]
        elif x == 'adm' and user_id == "1317942159":
            key_a = types.InlineKeyboardButton(text=name_key[x], callback_data=x)
            keyboard.add(key_a)
    if call != 0:
        await call.message.answer(question, reply_markup = keyboard)
    else:
        await message.answer(question, reply_markup = keyboard)

async def list_questions(message: types.Message, answer, chapter,lang):
    #print(answer)
    if len(answer) > 0:
        num = 1
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        for x in answer:
            key_a = types.InlineKeyboardButton(text=x[0], callback_data=str(num))
            num = num + 1
            #anw.append(x)
            keyboard.add(key_a)
        answer.clear()
        if lang == 'ru':
            if chapter == 'process':
                question = 'Выберите нужный вопрос'
            else:
                question = 'Выберите нужный вариант'
        else:
            if chapter == 'process':
                question = 'Select the desired question'
            else:
                question = 'Select the suitable option'
        await message.answer(question, reply_markup=keyboard)
    else:
        if lang == 'ru':
            if chapter == 'process':
                await message.answer( "Такого вопроса в базе нет(((")
            else:
                await message.answer( "Такого корпуса в базе нет(((")
            await message.answer( "Если хотите, чтобы его добавили, перейдите в раздел “Обратная связь”")
        else:
            if chapter == 'process':
                await message.answer( "There is no such question in the database (((")
            else:
                await message.answer( "There is no such a building in the database (((")
            await message.answer( "If you want it to be added, switch to “Feedback” section")

async def list_markup(user_id, call, message, users):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if users[user_id] == 'eng':
        button = types.KeyboardButton('Continue')
    else:
        button = types.KeyboardButton('Продолжить')
    markup.add(button)
    if users[user_id] == 'ru':
      await  call.message.answer(text='Кнопкой "Продолжить" вызывается главное меню', reply_markup=markup)
    else:
      await  call.message.answer( text='The "Continue" button calls the main menu', reply_markup=markup)

async def one_day_schedule(all_schedule,call,user,schedule_user,what_day, write_what_day):
    work = all_schedule[schedule_user[user].replace('.', '/')]
    schedul_answ = ''

    for x in work:
        if x == what_day:
            for y in work[x]:
                if y[2] == ":" or y[1] == ":":
                    schedul_answ += '\n\r'
                schedul_answ += y
                schedul_answ += '\n\r'
            break
    if schedul_answ != ('Нет занятий\n\r'):
        await call.message.answer(schedul_answ)
    else:
        await call.message.answer(write_what_day +'\n\r'+schedul_answ)