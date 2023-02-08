import requests
import asyncio
import concurrent.futures
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from tkinter import *
from password import password, login
#отправка уведомлений на почту
def https(**args):
              
    msg = MIMEMultipart()
    msg['From'] = login
    msg['To'] = login
    msg['Subject'] = 'Web site monitoring'
    text = f'{args}'
    msg.attach(MIMEText(text, 'plain'))
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.ehlo(login)
    server.login(login, password)
    server.auth_plain()
    server.send_message(msg)
    server.quit()
    
            
#Интервал отправки, асинхронность
def dispatcher():
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    loop = asyncio.get_event_loop()
    callbacks = [ https ] * len(list(showEntries()))
    crontab = [list(tup) for tup in zip(list(showEntries()), list(map(int, showEntries1())), list(F()), callbacks)]
    loop.call_later(60, dispatcher, loop, pool, crontab)
    s = 0
    while True:
        time.sleep(1)
        root.update()
        s += 1  
        for name, interval, value , callback in crontab:
            status11 = name, value
            s1 = 60 * interval
            if s % s1 == 0:
                lbox.insert(0, status11)
                pool.submit(callback, **{name: value})

   
#проверка доступности сайтов
def F():    
    for website in list(showEntries()):
        value0 = requests.get(f'{website}')
        if value0.status_code == 200:
            value1 = f'{value0.status_code}','OK' 
            yield value1
        elif value0.status_code == 404:
            value1 = f'{value0.status_code}','Not found'
            yield value1
        else:
            value1 = f'{value0.status_code}'
            yield value1

#поля ввода
def addBox():
    next_row = len(all_entries_w)
    next_row1 = len(all_entries_t)
   
    ent = Entry(root)
    ent.place(x = 90, y = 60 + 20 * next_row, width = 200)
    ent1 = Entry(root)
    ent1.place(x = 320, y = 60 + 20 * next_row1 , width = 30)

    all_entries_w.append(ent)
    all_entries_t.append(ent1)

#сайты
def showEntries():
    for n, ent in enumerate(all_entries_w):
        yield ent.get()
#интервалы
def showEntries1():
    for n, ent1 in enumerate(all_entries_t):
        yield ent1.get()

#интерфейс
root = Tk()
all_entries_w = []
all_entries_t = []

root.geometry('700x500')
photo = PhotoImage(file='C:\\Users\\Nikito$\\Desktop\\png.png')
root.iconphoto(False, photo)
root.title("Web site monitoring")
root.resizable(False, True)
label1 = Label(root, text = 'Добавить\nсайт:')
label1.place(x = 90, y = 10)
label = Label(root, text = 'Добавить\nинтервал\n(в мин.):')
label.place(x = 320, y = 10)
label2 = Label(root, text = 'Статус\nкод:')
label2.place(x = 400, y = 10)
showButton = Button(root, text='Запуск\nпроверки', command=dispatcher)
showButton.place(x = 10, y = 10)

addboxButton = Button(root, text='Добавить\nполя\nввода', command=addBox)
addboxButton.place(x = 10, y = 60)

lbox = Listbox(root, selectmode=MULTIPLE)
lbox.place(x = 400, y = 60, width = 280, height = 400)
scrollbar = Scrollbar(root)
scrollbar.place(x = 680, y = 50, height = 400) 
lbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = lbox.yview)

root.mainloop()









        











    


    
    
        




