import requests
import selectorlib
import smtplib
import ssl
import os


url = 'http://programmer100.pythonanywhere.com/tours/'

def scrape(URL):
    response = requests.get(URL)
    page_source = response.text
    return page_source

def extract(page_source_or_url):
    extractor = selectorlib.Extractor.from_yaml_file('source.yaml')
    value = extractor.extract(page_source_or_url)['tours']
    return value

def store(extracted_data):
    with open('data.txt', 'a') as file:
        file.write(extracted_data + "\n")

def read(extracted_content):
    with open('data.txt', 'r') as file:
        return file.read()

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
    scraped = scrape(url)
    extracted = extract(scraped)
    print(extracted)

    content = read(extracted)
    if extracted != 'No upcoming tours':
        if extracted not in content:
            store(extracted)
            send_email(msg='Hey! New Event Tour has been found!')