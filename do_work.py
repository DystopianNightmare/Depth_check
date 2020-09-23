import smtplib
from array import array

from bs4 import BeautifulSoup
from urllib.request import urlopen
from smtplib import SMTP
from email.message import EmailMessage

url = "https://mwstest.mdu.com/esb/admin/monitoring/queuestatus"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
i = 1
arr = []
for row in soup.findAll('tr'):
    for cell in row.findAll('td'):

        if i % 5 == 2:
            string = str(cell)
            j = int(string.find(">"))
            t = int(string.find("/"))
            string = string[j + 1:t - 1]
            arr.append(string)

        if i % 5 == 1:
            string = str(cell)
            j = int(string.find(">"))
            t = int(string.find("/"))
            string = string[4:-5]
            arr.append(string)
        i = i + 1

j = 0
over = []
for q in arr:
    if j % 2 == 1:
        if int(arr[j]) > 25:
            this = arr[j - 1] + " has a last check depth of " + str(arr[j])
            print(this)
            over.append(this)
    j = j + 1

if len(over) != 0:
    FROM = "ipsentry@mdu.com"
    TO = "joshua.gandolfo@mduresources.com"
    k = 0
    message = EmailMessage()
    message['From'] = FROM
    message['To'] = TO
    message['Subject'] = str(len(over)) + ' queue(s) over 25'
    msg = 'There is ' + str(len(over)) + ' queue(s) over 25\n\n'
    for j in over:
        msg = msg + (str(over[k]) + "\n")
        k = k + 1
    message.set_content(msg)
    s = smtplib.SMTP('smtp.mdu.com')
    s.send_message(message)
