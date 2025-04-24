import requests
import selectorlib
from emailing import send_email
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}
url = "http://programmer100.pythonanywhere.com/tours/"



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
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


def read(extracted):
    with open("data.txt", "r")as file:
        return file.read()


if __name__=="__main__":
    while True:
        scraped = scrape(url)
        extracted = extract(scraped)
        print(extracted)

        content = read(extracted)
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                message = ("Subject: New show!\n\n"
                           f"New show: {extracted} available!\n"
                           "Visit here to book:http://programmer100.pythonanywhere.com/tours/")
                send_email(message)
                print("Email sent!")
        time.sleep(2)