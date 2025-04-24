import requests
import selectorlib
import os
import smtplib as smt
import ssl

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}
url = "http://programmer100.pythonanywhere.com/tours/"

password = os.getenv("WEBSCRAPING")
sender = "pythonprojectstc@gmail.com"
receiver = "pythonprojectstc@gmail.com"


def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()
    with smt.SMTP_SSL(host, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)