import json
from connect_db import insert_table_FAQ, insert_table_navig
def add_question_file(question, answer, data,language):
    if language == 'en':
        language ='eng'
    full_answer = json.dumps([answer, data],ensure_ascii=False)
    full_que = json.dumps({language: question},ensure_ascii=False)
    print(full_que,full_answer)
    insert_table_FAQ(full_que,full_answer)
def add_in_arr (name, tema):
    with open(name, 'r', encoding='UTF-8') as question_file:
        que = ''
        ans = ''
        data = ''
        lang = ''
        for x in question_file:
            if x[:2] == 'q:':
                que += x[2:].lstrip().lower().replace('\n', ' ').replace('\t', ' ').replace("'","`")
            if x[:2] == 'a:':
                if len(x[2:].lstrip()) != 0:
                    ans += x[2:].lstrip().replace('\n', ' ').replace('\t', ' ')
                else:
                    ans += '\r\n'
            if x[:2] == 'd:':
                data = x[2:].lstrip().replace('\n', ' ')
            if x[:2] == 'l:':
                lang = x[2:].strip().lower().replace('\n', ' ')
                if tema == 'process':
                    add_question_file(que.strip(), ans.strip(), data.strip(), lang.strip())
                else:
                    print(que.strip(), ans.strip(), data.strip())
                    insert_table_navig(que.strip(), ans.strip(), data.strip(),lang.strip())
                que = ''
                ans = ''
                data = ''
                lang = ''