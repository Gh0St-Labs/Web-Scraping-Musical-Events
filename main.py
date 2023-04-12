import time

import requests
import selectorlib
import smtplib
import ssl
import sqlite3


url = 'http://programmer100.pythonanywhere.com/tours/'
connect = sqlite3.connect('app_database.db')


def scrape(URL):
    response = requests.get(URL)
    page_source = response.text
    return page_source

def extract(page_source_or_url):
    extractor = selectorlib.Extractor.from_yaml_file('source.yaml')
    value = extractor.extract(page_source_or_url)['tours']
    return value

def store_db(extracted_data):
    split_content = extracted_data.split(',')
    split_content = [item.strip() for item in split_content]
    cursor = connect.cursor()
    cursor.execute('INSERT INTO events VALUES (?,?,?)', split_content)
    connect.commit()


def read_db(extracted_content):
    split_content = extracted_content.split(',')
    split_items = [item.strip() for item in split_content]
    band, city, date = split_items
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM events WHERE Band_Name=? AND City_Name=? AND Date=?', (band, city, date))
    data = cursor.fetchall()
    return tuple(data)

def send_email(msg):
    host = 'smtp.gmail.com'
    port = 465

    username = 'syondukeabraham@gmail.com'
    password = 'zrokenbhrussjhrq'


    reciever = 'kordan.goat@gmail.com'
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, reciever, msg)

if __name__ == '__main__':
    while True:
        scraped = scrape(url)
        extracted = extract(scraped)
        print(extracted)
        if extracted != 'No upcoming tours':
            datas = read_db(extracted)
            datas = tuple(datas)
            if not datas:
                store_db(extracted)
                send_email(msg='Hey! New Event Tour has been found!')
                print('Email was sent')

        time.sleep(3)