from config import ip_table_ru, ip_table_eng
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from googleapiclient.discovery import build
import os
import smtplib
import asyncio
from email.mime.text import MIMEText
from email.header import Header

async def send_email(data):
    ans = """"""
    i = 0
    mas = data['values']
    recipients_emails = "vamp.be.live@gmail.com"
    login = 'Assistant.bot.Student@gmail.com'
    for x in mas[0]:
        if i != 0 and x != '':
            if i == 1:
                ans += """Институт: """+ x
            elif i == 2:
                ans += """, Направление: """+ x
            elif i == 3:
                ans += """, Группа: """ + x
            elif i == 4:
                ans += """, Имя и Фамилия: """+ x
            elif i == 5:
                ans += """, Вопрос/Жалоба: """+ x
            elif i == 6:
                ans += """, Электронная почта: """+ x
        i += 1

    msg = MIMEText(ans, 'plain', 'utf-8')
    msg['Subject'] = Header('Ассистент бот(вопросы/жалобы)', 'utf-8')
    msg['From'] = login
    msg['To'] = recipients_emails
    #text = bs(ans, "html.parser").text
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('Assistant.bot.Student@gmail.com', 'Assistant.bot.Student2022')
    smtpObj.sendmail("assistant.bot.student@gmail.com", "vamp.be.live@gmail.com", msg.as_string())
    print("SEND")

async def find_googl_table_ru():
    global ru_num
    ru_num = 5
    while True:
        await asyncio.sleep(20)
        creds = ServiceAccountCredentials.from_json_keyfile_name( os.path.dirname(__file__)+'/bot-ru-350508-b124631d0011.json', scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']).authorize(httplib2.Http())
        server = build('sheets','v4', creds)
        sheet = server.spreadsheets()
        resp = sheet.values().get(spreadsheetId = ip_table_ru,range = f"list1!A{ru_num}:G{ru_num}").execute()
        ind =0
        for x in resp:
            if x =='values':
                ind = 1
        if ind == 1:
            await send_email(resp)
            ru_num += 1
        else:
            print("not_ru")
        pass

async def find_googl_table_eng():
    global eng_num
    eng_num = 2
    while True:
        await asyncio.sleep(20)
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.dirname(__file__) + '/bot-ru-350508-b124631d0011.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']).authorize(
            httplib2.Http())
        server = build('sheets', 'v4', creds)
        sheet = server.spreadsheets()
        resp = sheet.values().get(spreadsheetId=ip_table_ru, range=f"list2!A{eng_num}:G{eng_num}").execute()
        ind = 0
        for x in resp:
            if x == 'values':
                ind = 1
        if ind == 1:
            await send_email(resp)
            eng_num += 1
        else:
            print("not_eng")
        pass
