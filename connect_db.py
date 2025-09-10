import json

import psycopg2
from fuzzywuzzy import fuzz
from config import all_schedule

from fuzzywuzzy import process
from json import loads
def con_data_base():
    global con
    con = psycopg2.connect(
    user='postgres',
    password='nasty18',
    host='localhost',
    port='5432'
    )


#база данных для FAQ
def create_db_faq():
    print('FAQ created')
    cur = con.cursor()
    cur.execute('''CREATE TABLE FAQ  
         (ID serial primary key,
          QUESTOIN jsonb,
          ANSWER jsonb);''')
    con.commit()
def insert_table_FAQ(que, answ):
    a = (que,answ)
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO FAQ (QUESTOIN,ANSWER) VALUES {a} "
    )
    con.commit()
def delete_table_FAQ():
    cur = con.cursor()
    cur.execute("DELETE FROM FAQ;")


#база данных для пользователей
def create_db_user():
    print('users created')
    cur = con.cursor()
    cur.execute('''CREATE TABLE USERS  
         (ID serial primary key,
          USER_ID text,
          LANGUAGE text);''')
    con.commit()

def insert_table_user(id_user,lang):
    a = (id_user,lang)
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO USERS (USER_ID,LANGUAGE) VALUES {a} "
    )
    con.commit()


#база данных для расписание
def create_db_schedule():
    print('schedule created')
    cur = con.cursor()

    cur.execute('''CREATE TABLE SCHEDULE  
         (ID serial primary key,
         GROUPS text, 
         SCHEDULE_INFO jsonb
           );''')
    con.commit()
def insert_table_schedule(group,schedule_info):
    a = (group,schedule_info)
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO SCHEDULE (GROUPS,SCHEDULE_INFO) VALUES {a} "
    )
    con.commit()

#база данных для навигации
def create_db_navig():
    print('navig created')
    cur = con.cursor()
    cur.execute('''CREATE TABLE NAVIG  
         (ID serial primary key,
          LANG text,
          BUILDING text,
          ADDRES text, 
          PHOTO text
          );''')
    con.commit()
def insert_table_navig(building,addres,photo,lang):
    a = (lang,building, addres, photo)
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO NAVIG (LANG,BUILDING,ADDRES,PHOTO) VALUES {a} "
    )
    con.commit()
def delete_table_navig():
    cur = con.cursor()
    cur.execute("DELETE FROM NAVIG;")

#поиск по вопросам общим
def answer_learn_general (question, user_id, users):
    answer = []
    language_us = users[user_id]
    cur = con.cursor()
    cur.execute("SELECT QUESTOIN,ANSWER from FAQ")
    rows = cur.fetchall()
    for row in rows:
        que_list = row[0]
        ans_list = row[1]
        for a in que_list:
            if language_us == a:
                x = fuzz.token_sort_ratio(question, que_list[a])
                if x == 100:
                    answer.clear()
                    answer.append([que_list[a], ans_list, x])
                    return answer
                elif x >= 57:
                    if len(answer) != 0 and answer[0][2] < x:
                        answer.remove(answer[0])
                    if len(answer) != 3:
                        answer.append([que_list[a], ans_list, x])
                        answer.sort()
    #answer.reverse()
    return answer

#запосинание пользователей и языков
def recover_user():
    us = {}
    cur = con.cursor()
    cur.execute("SELECT USER_ID,LANGUAGE from USERS")
    rows = cur.fetchall()
    for x in rows:
        #print(x)
        us[x[0]]=x[1]
    return us

#сохраниние расписания
def save_schedule():
    print("begin save")
    cur = con.cursor()
    cur.execute("DELETE FROM SCHEDULE;")
    for group in all_schedule:
        full_answer = json.dumps(all_schedule[group], ensure_ascii=False)
        print(full_answer)
        insert_table_schedule(group,full_answer)
    print("end save")

#поиск нужного расписания
async def pull_schedule():
    print("pull_schedule")
    cur = con.cursor()
    cur.execute("SELECT GROUPS,SCHEDULE_INFO from SCHEDULE")
    rows = cur.fetchall()
    for x in rows:
        all_schedule[x[0]] = x[1]


#поиск нужного корпуса
def find_navig(home,lang):
    answer = []
    cur = con.cursor()
    cur.execute("SELECT LANG,BUILDING,ADDRES,PHOTO from NAVIG")
    rows = cur.fetchall()
    for y in rows:
        if y[0] != lang:
            continue
        ssss = y[1]
        x = fuzz.token_sort_ratio(home, ssss)
        answ_ocn = [y[2],y[3]]
        if x == 100:
            answer.clear()
            answer.append([ssss, answ_ocn, x])
            return answer
        if x >= 60 :
            if len(answer) != 0 and answer[0][2] < x:
                answer.remove(answer[0])
            if len(answer) != 3:
                answer.append([ssss, answ_ocn, x])
                answer.sort()
    answer.reverse()
    return answer