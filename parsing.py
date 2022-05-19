import time
from config import all_schedule
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
all_parsing_sites =[
    "https://ruz.spbstu.ru/faculty/120/groups",
    "https://ruz.spbstu.ru/faculty/122/groups",
    "https://ruz.spbstu.ru/faculty/92/groups",
    "https://ruz.spbstu.ru/faculty/121/groups",
    "https://ruz.spbstu.ru/faculty/95/groups",
    "https://ruz.spbstu.ru/faculty/99/groups",
    "https://ruz.spbstu.ru/faculty/94/groups",
    "https://ruz.spbstu.ru/faculty/124/groups",
    "https://ruz.spbstu.ru/faculty/111/groups",
    "https://ruz.spbstu.ru/faculty/101/groups",
    "https://ruz.spbstu.ru/faculty/123/groups",
    "https://ruz.spbstu.ru/faculty/119/groups",
    "https://ruz.spbstu.ru/faculty/93/groups",
    "https://ruz.spbstu.ru/faculty/100/groups"
]

#делаем словарь {номер_группы:{день_недели:расписание}}
async def pars(all_parsing,driver):
    for site in all_parsing:
        type_of_time = [0]
        type_of_training = []
        gr = []
        find_oc1 = 0
        find_oc2 = 0
        find_gr1 = 0
        find_gr2 = 0
        driver.get(site)
        while 1 :
            if len(type_of_time) == 0:
                break  # для while

            news_elements = driver.find_elements(By.CLASS_NAME, "page")
            while len(news_elements) == 0:
                news_elements = driver.find_elements(By.CLASS_NAME, "page")

            page_c = news_elements[0].find_elements(By.ID, "rootPageContainer")
            while len(page_c) == 0:
                page_c = news_elements[0].find_elements(By.ID, "rootPageContainer")

            page_app = page_c[0].find_elements(By.CLASS_NAME, "app")
            while len(page_app) == 0:
                page_app = page_c[0].find_elements(By.CLASS_NAME, "app")

            page_faculty = page_app[0].find_elements(By.CLASS_NAME, "faculty")
            while len(page_faculty) == 0:
                page_faculty = page_app[0].find_elements(By.CLASS_NAME, "faculty")

            page_tabs = page_faculty[0].find_elements(By.CLASS_NAME, "tabs-area")
            while len(page_tabs) == 0:
                page_tabs = page_faculty[0].find_elements(By.CLASS_NAME, "tabs-area")

            page_types = page_tabs[0].find_elements(By.CLASS_NAME, "tabbed-area__tabs")  # определеление очки и типа
            while len(page_types) == 0:
                page_types = page_tabs[0].find_elements(By.CLASS_NAME, "tabbed-area__tabs")  # определеление очки и типа

            if find_oc1 == 0:
                type_of_time = page_types[0].text.split('\n')  # как учатся очно или заочно
                find_oc1 = 1

            if find_oc2 == 0:
                type_of_training = page_types[1].text.split('\n')  # типы обучения
                find_oc2 = 1

            if find_gr1 == 0:#перелистывание по очке или заочке
                checkbox = page_types[0].find_elements(By.LINK_TEXT, type_of_time[0])
                while len(checkbox) == 0:
                    checkbox = page_types[0].find_elements(By.LINK_TEXT, type_of_time[0])
                checkbox[0].click()
                find_gr1 = 1

            if find_gr2 == 0:#перелистывание по типу
                checkbox_tp = page_types[1].find_elements(By.LINK_TEXT, type_of_training[0])
                while len(checkbox_tp) == 0:
                    checkbox_tp = page_types[1].find_elements(By.LINK_TEXT, type_of_training[0])
                checkbox_tp[0].click()
                page_group = page_tabs[0].find_elements(By.CLASS_NAME, "tabbed-area__pane")  # считывание самих групп
                while len(page_group) == 0:
                    page_group = page_tabs[0].find_elements(By.CLASS_NAME, "tabbed-area__pane")  # считывание самих групп

                gr1 = page_group[0].text.split('\n')
                if gr1[0] == 'Группы не найдены':
                    type_of_training.remove(type_of_training[0])
                    if len(type_of_training) == 0:
                        type_of_time.remove(type_of_time[0])
                        find_gr2 = 0
                        find_gr1 = 0
                        find_oc2 = 0
                    continue
                find_gr2 = 1
                for x in gr1:
                    if (x != 'Группы не найдены') and (('курс' in x) != True):
                        gr.append(x)
            elem = gr[0]
            checkbox_groups = page_tabs[0].find_elements(By.LINK_TEXT, elem)
            while len(checkbox_groups) == 0:
                checkbox_groups = page_tabs[0].find_elements(By.LINK_TEXT, elem)

            checkbox_groups[0].click()
            time.sleep(0.5)
            await find_schedule(driver, elem)
            driver.back()
            time.sleep(0.35)
            gr.remove(elem)
            if len(gr) == 0:
                if len(type_of_training) != 0:
                    type_of_training.remove(type_of_training[0])
                    find_gr2 = 0
                else:
                    type_of_time.remove(type_of_time[0])
                    find_gr2 = 0
                    find_gr1 = 0
                    find_oc2 = 0
        #break

async def find_schedule (driver, elem):
    gr_page = driver.find_elements(By.CLASS_NAME, "page")
    while len(gr_page) == 0:
        gr_page = driver.find_elements(By.CLASS_NAME, "page")

    gr_c = gr_page[0].find_elements(By.ID, "rootPageContainer")
    while len(gr_c) == 0:
        gr_c = gr_page[0].find_elements(By.ID, "rootPageContainer")

    gr_app = gr_c[0].find_elements(By.CLASS_NAME, "app")
    while len(gr_app) == 0:
        gr_app = gr_c[0].find_elements(By.CLASS_NAME, "app")

    gr_faculty = gr_app[0].find_elements(By.CLASS_NAME, "schedule-page")
    while len(gr_faculty) == 0:
        gr_faculty = gr_app[0].find_elements(By.CLASS_NAME, "schedule-page")

    gr_schedule = gr_faculty[0].find_elements(By.CLASS_NAME, "schedule")
    while len(gr_schedule) == 0:
        gr_schedule = gr_faculty[0].find_elements(By.CLASS_NAME, "schedule")
    schedule_list = gr_schedule[0].text.replace('"','`').split('\n')
    y = 0
    day_schedule = {'monday': ['Нет занятий'], 'tuesday': ['Нет занятий'], 'wednesday': ['Нет занятий'],
                    'thursday': ['Нет занятий'], 'friday': ['Нет занятий'], 'saturday': ['Нет занятий']}

    if schedule_list[0] == "На эту неделю занятия не поставлены":
        all_schedule[elem] = day_schedule
        return

    if y<len(schedule_list) and ((', пн' in schedule_list[y]) == True):
        mond = []
        while (y<len(schedule_list) and (', вт' in schedule_list[y]) == False) and ((', ср' in schedule_list[y]) == False) and ((', чт' in schedule_list[y]) == False) and ((', пт' in schedule_list[y]) == False) and ((', сб' in schedule_list[y]) == False):
            if schedule_list[y] != 'Потокпоказать группы':
                mond.append(schedule_list[y])
            else:
                mond.append('Группы всего потока')
            y+=1
        day_schedule['monday'] = mond
    if y<len(schedule_list) and ((', вт' in schedule_list[y]) == True):
        tuesd = []
        while (y<len(schedule_list) and (', ср' in schedule_list[y]) == False) and ((', чт' in schedule_list[y]) == False) and ((', пт' in schedule_list[y]) == False) and ((', сб' in schedule_list[y]) == False):
            if schedule_list[y] != 'Потокпоказать группы':
                tuesd.append(schedule_list[y])
            else:
                tuesd.append('Группы всего потока')
            y+=1
        day_schedule['tuesday'] = tuesd
    if y<len(schedule_list) and ((', ср' in schedule_list[y]) == True) == True:
        wednesd = []
        while (y<len(schedule_list) and (', чт' in schedule_list[y]) == False) and ((', пт' in schedule_list[y]) == False) and ((', сб' in schedule_list[y]) == False):
            if schedule_list[y] != 'Потокпоказать группы':
                wednesd.append(schedule_list[y])
            else:
                wednesd.append('Группы всего потока')

            y += 1
        day_schedule['wednesday'] = wednesd
    if y<len(schedule_list) and ((', чт' in schedule_list[y]) == True):
        thursd = []
        while (y<len(schedule_list) and (', пт' in schedule_list[y]) == False) and ((', сб' in schedule_list[y]) == False):
            if schedule_list[y] != 'Потокпоказать группы':
                thursd.append(schedule_list[y])
            else:
                thursd.append('Группы всего потока')
            y += 1
        day_schedule['thursday'] = thursd
    if y<len(schedule_list) and ((', пт' in schedule_list[y]) == True):
        frid = []
        while (y<len(schedule_list) and (', сб' in schedule_list[y]) == False):
            if schedule_list[y] != 'Потокпоказать группы':
                frid.append(schedule_list[y])
            else:
                frid.append('Группы всего потока')
            y += 1
        day_schedule['friday'] = frid
    if y<len(schedule_list) and ((', сб' in schedule_list[y]) == True):
        saturd = []
        while (y<len(schedule_list)):
            if schedule_list[y] != 'Потокпоказать группы':
                saturd.append(schedule_list[y])
            else:
                saturd.append('Группы всего потока')
            y += 1
        day_schedule['saturday'] = saturd
    all_schedule[elem] = day_schedule
    #print(day_schedule)
    #print(schedule_list)

async def start_pars (begin):
    driver = Chrome(executable_path="./chromedriver.exe")
    driver.minimize_window()
    if begin == 1:
        print("НАЧАЛОСЬ")
        await pars(all_parsing_sites[:2],driver)
    if begin == 2:
        print("НАЧАЛОСЬ2")
        await pars(all_parsing_sites[2:4],driver)
    if begin == 3:
        print("НАЧАЛОСЬ3")
        await pars(all_parsing_sites[4:6],driver)
    if begin == 4:
        print("НАЧАЛОСЬ4")
        await pars(all_parsing_sites[6:8],driver)
    if begin == 5:
        print("НАЧАЛОСЬ5")
        await pars(all_parsing_sites[8:10],driver)
    if begin == 6:
        print("НАЧАЛОСЬ6")
        await pars(all_parsing_sites[10:12],driver)
    if begin == 7:
        print("НАЧАЛОСЬ7")
        await pars(all_parsing_sites[12:],driver)
    print("ОНО СПАРСИЛОСЬ")
    driver.quit()


