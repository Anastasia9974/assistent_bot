import asyncio
import logging
from aiogram import Bot,Dispatcher,executor,types
import json

from config import TOKEN
from config import key_language
from config import key_ru, key_eng
from config import key_admin
from config import users
from config import key_schedule_ru, key_schedule_eng
from config import all_schedule
from config import navigation_keys_ru, navigation_keys_eng

from created_key import list_key
from created_key import list_questions
from created_key import list_markup
from created_key import one_day_schedule

from connect_db import create_db_user,create_db_schedule,create_db_faq,create_db_navig
from connect_db import con_data_base
from connect_db import answer_learn_general
from connect_db import insert_table_user
from connect_db import recover_user
from connect_db import save_schedule,pull_schedule
from connect_db import find_navig
from connect_db import delete_table_navig, delete_table_FAQ

from work_with_files import add_in_arr

from work_str import form_answer

from parsing import start_pars
from google_tbl import find_googl_table_ru, find_googl_table_eng
user_call = {}
answer_user = {}
schedule_user = {}
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Хэндлер на команду /start
@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    await bot.send_sticker(message.chat.id,r"CAACAgIAAxkBAAEEwtdihVLeKhOAN9gGHUIguNqdTLsqVgACVAADQbVWDGq3-McIjQH6JAQ")
    await list_key(message, 0, key_language)

@dp.callback_query_handler()
#выбор кнопок для языка и темы
async def callback_worker(call: types.CallbackQuery):
    user_id = str(call.message.chat.id)
    #print(call.data)
    user_call[user_id] = call.data
    if call.data == "ru":
        users[user_id] = call.data
        insert_table_user(user_id,call.data)
        await list_key(0, call, key_ru)
        await list_markup(user_id, call, 0, users)
    elif call.data == "eng":
        users[user_id] = call.data
        insert_table_user(user_id,call.data)
        await list_key(0,call, key_eng)
        await list_markup(user_id, call, 0, users)

    elif call.data == "schedule":
        if users[user_id] == 'ru':
            await call.message.answer("Введите номер группы (через '/' или '.')")
        else:
            await call.message.answer("Enter the group number (via '/' or '.')")

    elif call.data == "navig":
        if users[user_id] == 'ru':
            await list_key(0, call, navigation_keys_ru)
        else:
            await list_key(0,call, navigation_keys_eng)


    elif call.data == "process":
        if users[user_id] == 'ru':
            await call.message.answer("Задайте вопрос в строке")
        else:
            await call.message.answer( "Ask a question in the line")

    elif call.data == "feedback":
        if users[user_id] == 'ru':
            await call.message.answer("Вы можете написать свои вопросы/жалобы в анкете по ссылке:"+"\n\r"+"https://forms.gle/45NnAHFfB1uRD15B6")
        else:
            await call.message.answer("You can write any questions/complaints in the questionnaire by the link:"+"\n\r"+"https://forms.gle/RPHX81LXej3DUve49")
    elif call.data == 'language':
        await list_key(0, call, key_language)
    else:
        await navig_worker(call,user_id)
        await admin_worker(call)
        if call.data == '1' or call.data == '2' or call.data == '3':
            await answer_worker(call,user_id)
        await schedule_worker(call,user_id)
#выбор кнопок для администратора
async def admin_worker(call: types.CallbackQuery):
    #print('vfvfvf')
    if call.data == "adm":
        await list_key(0,call,key_admin)
    elif call.data == "adm1":
        await call.message.answer( "Какую именно(навигация,FAQ,расписание,user)?")
    elif call.data == "adm2":
        await call.message.answer("Введите название файла в вопросами:")
    elif call.data == 'adm3':
        await call.message.answer("Введите название файла в вопросами(навигация):")
    elif call.data == 'adm4':
        print('delete FAQ')
        delete_table_FAQ()
    elif call.data == 'adm5':
        print('delete navig')
        delete_table_navig()
#выбор кнопок для ответа
async def answer_worker(call: types.CallbackQuery,user):
    if answer_user[user][0][0] != 'navig':
        if call.data == '1':
            await call.message.answer(form_answer(answer_user[user][0][0],answer_user[user][0][1]))
        elif call.data == '2':
            await call.message.answer(form_answer(answer_user[user][1][0], answer_user[user][1][1]))
        elif call.data == '3':
            await call.message.answer(form_answer(answer_user[user][2][0], answer_user[user][2][1]))
    else:
        if call.data == '1':
            await call.message.answer(answer_user[user][1][0])
            if answer_user[user][1][1] != '0':
                if users[str(call.message.chat.id)] == 'ru':
                    await call.message.answer("Вид здания:")
                else:
                    await call.message.answer("The building looks like:")
                await call.message.answer_photo(answer_user[user][1][1])
        elif call.data == '2':
            await call.message.answer(answer_user[user][2][0])
            if answer_user[user][2][1] != '0':
                if users[str(call.message.chat.id)] == 'ru':
                    await call.message.answer("Вид здания:")
                else:
                    await call.message.answer("The building looks like:")
                await call.message.answer_photo(answer_user[user][2][1])
        elif call.data == '3':
            await call.message.answer(answer_user[user][3][0])
            if answer_user[user][3][1] != '0':
                if users[str(call.message.chat.id)] == 'ru':
                    await call.message.answer("Вид здания:")
                else:
                    await call.message.answer("The building looks like:")
                await call.message.answer_photo(answer_user[user][3][1])

#выбор кнопок для расписания
async def schedule_worker(call: types.CallbackQuery,user):
    await pull_schedule()
    if call.data == "schedule1":
        await one_day_schedule(all_schedule, call,user, schedule_user, 'monday', 'Понедельник')
        await one_day_schedule(all_schedule, call, user, schedule_user, 'tuesday', 'Вторник')
        await one_day_schedule(all_schedule, call, user, schedule_user, 'wednesday','Среда')
        await one_day_schedule(all_schedule, call, user, schedule_user, 'thursday','Четверг')
        await one_day_schedule(all_schedule, call, user, schedule_user, 'friday','Пятница')
        await one_day_schedule(all_schedule, call, user, schedule_user, 'saturday','Суббота')
        all_schedule.clear()
    elif call.data == "schedule2":
        await one_day_schedule(all_schedule, call,user, schedule_user, 'monday', 'Понедельник')
        all_schedule.clear()
    elif call.data == "schedule3":
        await one_day_schedule(all_schedule, call, user, schedule_user, 'tuesday', 'Вторник')
        all_schedule.clear()
    elif call.data == "schedule4":
        await one_day_schedule(all_schedule, call, user, schedule_user, 'wednesday','Среда')
        all_schedule.clear()
    elif call.data == "schedule5":
        await one_day_schedule(all_schedule, call, user, schedule_user, 'thursday','Четверг')
        all_schedule.clear()
    elif call.data == "schedule6":
        await one_day_schedule(all_schedule, call, user, schedule_user, 'friday','Пятница')
        all_schedule.clear()
    elif call.data == "schedule7":
        await one_day_schedule(all_schedule, call, user, schedule_user, 'saturday','Суббота')
        all_schedule.clear()

#выбор кнопок для навигации
async def navig_worker(call: types.CallbackQuery,user):
    if call.data == 'building':
        if users[user] == 'ru':
            await call.message.answer("Необходимо ввести полное название корпуса (если присутствуют числительные, то они вводятся цифрами):")
            await call.message.answer("Пример: 1 учебный корпус")
            await call.message.answer("Введите название корпуса, до которого хотите добраться:")
        else:
            await call.message.answer("It is necessary to enter the full name of the building (if numerals are present, then they are entered in words):")
            await call.message.answer("Example: 1 educational building")
            await call.message.answer("Enter the name of the building you want to reach:")
    elif call.data == 'dormitory':
        if users[user] == 'ru':
            await call.message.answer("Введите номер общежития (цифрой), до которого хотите добраться:")
        else:
            await call.message.answer("Enter the number of the hostel (digit) you want to get to:")
@dp.message_handler(content_types = ["text"])
async def learn_process(message:types.Message):
    user_id = str(message.chat.id)
    if message.text == 'Continue' or message.text == 'Продолжить':
        await cont_process(message)
        return

    if user_call[user_id] == 'process':
        answer = answer_learn_general(message.text, user_id,users)
        a = []
        #print(answer)
        if len(answer) >= 3:
            a.append(answer[0][1])
            a.append(answer[1][1])
            a.append(answer[2][1])
        elif len(answer) >= 2:
            a.append(answer[0][1])
            a.append(answer[1][1])
        elif len(answer) >= 1:
            a.append(answer[0][1])
        answer_user[user_id] = a
        await list_questions(message, answer,user_call[user_id],users[user_id])

    elif user_call[user_id] == "building":
        answer = find_navig(message.text,users[user_id])
        a = [["navig"]]
        if len(answer) >= 3:
            a.append(answer[0][1])
            a.append(answer[1][1])
            a.append(answer[2][1])
        elif len(answer) >= 2:
            a.append(answer[0][1])
            a.append(answer[1][1])
        elif len(answer) >= 1:
            a.append(answer[0][1])
        answer_user[user_id] = a
        await list_questions(message, answer,user_call[user_id],users[user_id])
    elif user_call[user_id] == "dormitory":
        if users[user_id] == 'ru':
            answer = answer_learn_general('общежитие '+message.text, user_id,users)
        else:
            answer = answer_learn_general('dorm '+message.text, user_id,users)
        a = [["navig"]]
        if len(answer) >= 3:
            a.append(answer[0][1])
            a.append(answer[1][1])
            a.append(answer[2][1])
        elif len(answer) >= 2:
            a.append(answer[0][1])
            a.append(answer[1][1])
        elif len(answer) >= 1:
            a.append(answer[0][1])
        answer_user[user_id] = a
        await list_questions(message, answer, user_call[user_id],users[user_id])

    elif user_call[user_id] == "schedule":

        await pull_schedule()
        rit = 0
        for x in all_schedule:
            if x == message.text.replace('.', '/'):
                rit = 1
                break
        if rit == 0:
            await message.answer("Номер группы введён неправильно")
            all_schedule.clear()
            return

        schedule_user[user_id] = message.text
        if users[user_id] == 'ru':
            await list_key(message, 0, key_schedule_ru)
        else:
            await list_key(message, 0, key_schedule_eng)

    await adm_process(message)

async def adm_process(message:types.Message):
    user_id = str(message.chat.id)
    if user_call[user_id] == 'adm1':
        if message.text == 'FAQ':
            create_db_faq()
        elif message.text == 'навигация':
            create_db_navig()
        elif message.text == 'расписание':
            create_db_schedule()
        elif message.text == 'user':
            create_db_user()
    elif user_call[user_id] == 'adm2':
        add_in_arr(message.text,'process')
    elif user_call[user_id] == 'adm3':
        add_in_arr(message.text,'navig')
    return

async def cont_process(message:types.Message):
    user_id = str(message.chat.id)
    if users[user_id] == 'ru':
        await list_key(message, 0, key_ru)
    else:
        await list_key(message, 0, key_eng)
    return

async def pars_schedule():
    global sled_begin
    while True:
        await asyncio.sleep(100000)
        print(sled_begin)
        await start_pars(sled_begin)
        sled_begin += 1
        if sled_begin == 8:
            save_schedule()
            sled_begin = 1
        pass

if __name__ == "__main__":
    sled_begin = 1
    con_data_base()
    users = recover_user()
    loop = asyncio.get_event_loop()
    loop.create_task(pars_schedule())
    loop.create_task(find_googl_table_eng())
    loop.create_task(find_googl_table_ru())
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)