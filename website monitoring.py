import requests
import asyncio
import concurrent.futures
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import re
#отправка уведомления на почту
def https(**args):
              
    msg = MIMEMultipart()
    msg['From'] = 'TeSt1284211@yandex.ru'
    msg['To'] = 'TeSt1284211@yandex.ru'
    msg['Subject'] = 'Web site monitoring'
    text = f'{args}'
    msg.attach(MIMEText(text, 'plain'))
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.ehlo('TeSt1284211@yandex.ru')
    server.login('TeSt1284211@yandex.ru', '2133145qW')
    server.auth_plain()
    server.send_message(msg)
    server.quit()
    
            
#Интервал отправки
def dispatcher(loop, pool, crontab):
             
    time_seconds = time.time()
    delay_seconds = (((time_seconds//60)+ 1)  - time_seconds // 60) * 60
    loop.call_later(delay_seconds, dispatcher, loop, pool, crontab)
    s = 0
    while True:
        time.sleep(1)
        s += 1  
        for name, interval, value , callback in crontab: 
            s1 = 60 * interval
            if s % s1 == 0:
                pool.submit(callback, **{name: value})
      
#список сайтов и их интервалы
def get_crontab():
    print('Web site monitoring')
    print('Каждый сайт(интервал) вводите через пробел')
    vvod = input('Введите сайты: ')
    times = list(map(int,input('Введите интервалы для каждого сайта(в мин): ').split()))
    websites = re.split(' ', vvod)
    fnc = ['https'] * len(websites)
    status0 = ['статус код:'] * len(websites)
    status = [list(tup) for tup in zip(status0, list(F(websites)))]
    crontab = [list(tup) for tup in zip(websites, times, status, fnc)]
    for key in crontab:
        key[3] = globals()[key[3]]                                                         
    return crontab

#проверка доступности сайтов
def F(websites):
    for website in websites:
        value0 = requests.get(f'{website}')
        if value0.status_code == 200:
            value1 = {'OK', f'{value0.status_code}'}
            yield value1
        elif value0.status_code == 404:
            value1 = {'Not found', f'{value0.status_code}'}
            yield value1
        else:
            value1 = {'-', f'{value0.status_code}'}
            yield value1

  
            
#асинхронность
pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
loop = asyncio.get_event_loop()
dispatcher(loop, pool, get_crontab())
loop.run_forever()






    









        











    


    
    
        




