import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os
import random
def send_message(message,subject):
    message = str(message)
    messagemail = """From: Notify v2.0 <notifycompany913@gmail.com>
To: You <mailidsample@gmail.com>
Subject: """

    messagemail=messagemail+subject+ """

""" + message
    message = "'" + message + "'"
    #command = "notify-send " + message
    #os.system(command)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("your_sending_mail", "password")     s.sendmail("your_sending_mail", "reciever_mail", messagemail)
    s.quit() 
def poll():
    cred_file = open("Credentials.txt","r")
    content = cred_file.readlines()
    line1 = content[0].rstrip()
    cred_file.close()

    ctr_file = open("Counter.txt","r")
    counter = ctr_file.readlines()[0].rstrip()
    counter = int(counter)
    ctr_file.close()

    username = line1.split(",")[0]
    password = line1.split(",")[1]
    login_data = {}
    login_data["username"] = username
    login_data["password"] = password

    with requests.Session() as sess:
        url = "https://online.iitg.ac.in/tnp/Main.jsp"

        try:
            r = sess.post(url,login_data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            send_message("Check Internet Connection!!")
            return
        except requests.exceptions.ConnectionError as err:
            send_message("Check Internet Connection!!")
            return

        jobs = sess.get("https://online.iitg.ac.in/tnp/student/job_eligible_list.jsp")
        soup =  BeautifulSoup(jobs.text,"html5lib")

        tables = soup.select('table')
        
        if len(tables) == 0:
            send_message("Incorrect Credentials!!")
            return

        table = tables[0]
        rows = table.select('tr')

        ctr = 0
        for row in rows:
            if len(row.select('td')) > 0:
                ctr += 1
        defaul = str(rows[1])
        fn = defaul.find('No job matches')
        sn = defaul.find('Dummy')
        if fn!=-1 or sn!=-1 :
            ctr -= 1
        print(ctr)
        if ctr > counter:
            ctr_file = open("Counter.txt","w")
            ctr_file.write(str(ctr))
            ctr_file.close()
            change=ctr-counter
            message_string =str(change)+ " New Companies on portal\n"+ "now total = "+str(ctr)+"\n"
            subject=(str(rows[1].select('td')[1]).split(">")[1]).split("<")[0]
            message_string += "\n\n\n Script Now handles all exceptions for guaranteed notification  ;)"
            send_message(message_string,subject)
        if ctr < counter:
            ctr_file = open("Counter.txt","w")
            ctr_file.write(str(ctr))
            ctr_file.close()
            change=ctr-counter
            message_string =str(-change)+ " Companies removed from portal\n"+ "now total = "+str(ctr)+"\n"
            subject = "Company removed"

            send_message(message_string,subject)
#oll()
send_message("...","signing off")
doNothing=1