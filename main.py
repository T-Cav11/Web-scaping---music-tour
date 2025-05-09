import requests
import selectorlib
from emailing import send_email
import time
import sqlite3


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}
url = "http://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("events.db", timeout=10)



"""Scrape the page source from the URL"""
def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()



def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band,city,date))
    rows = cursor.fetchall()
    return rows

if __name__=="__main__":
    while True:
        scraped = scrape(url)
        extracted = extract(scraped)
        print(extracted)


        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                message = ("Subject: New show!\n\n"
                           f"New show: {extracted} available!\n"
                           "Visit here to book:http://programmer100.pythonanywhere.com/tours/")
                send_email(message)
                print("Email sent!")
        time.sleep(1)