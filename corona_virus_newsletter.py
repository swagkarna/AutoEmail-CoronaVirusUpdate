from bs4 import BeautifulSoup
import requests
import smtplib
import time

bd_coronainfo_list=[]
world_coronainfo_list = []

worldometer_page_link = "https://www.worldometers.info/coronavirus/"
IEDCR_bangladesh_page_link = "http://iedcr.gov.bd/"
source = requests.get(worldometer_page_link).text
source_bd = requests.get(IEDCR_bangladesh_page_link).text
soup = BeautifulSoup(source,"lxml")
soupbd = BeautifulSoup(source_bd,"lxml")

def bangladesh_corona_update():
    table_data = soupbd.find('table',class_="table table-hover").find('tbody')
    for data in table_data.findAll('tr') :
        for info in data.findAll('td') :
            bd_coronainfo_list.append(info.text)


    for data in soupbd.findAll('div',class_="col-sm-3"):
        bd_coronainfo_list.append(data.h3.text)




def world_corona_update() :
    for data in soup.findAll('div',{"id" :"maincounter-wrap"}):
        #cases2,cases3 are temporary variables that holds the address
        tabledata = data.find('div',class_="maincounter-number")
        final_value= tabledata.find('span').text
        world_coronainfo_list.append(final_value)

    #Printing on Console
    print(f"Total CoronaVirus Cases (World): {world_coronainfo_list[0]}")
    print(f"Total Death : {world_coronainfo_list[1]}")
    print(f"Total Recovered : {world_coronainfo_list[2]}")
    print()
    print()


world_corona_update()


def send_email() :
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('iamakifislam@gmail.com','<your password from google>') #I kept this hidden for privacy
    body = f'''
Assalamu Alaykum,

I am Akif's BOT,not Akif. This is a program generated mail. I collect the latest data from the trusted sources and send you this email with information.
In last 24 hours in Bangladesh, {bd_coronainfo_list[-2]} people died and among {bd_coronainfo_list[3]} tests, {bd_coronainfo_list[11]} newly found as Corona virus positive.


*** Have a Look in Details *** 

*** Total Results in the World : 
- Total Corona Virus Cases : {world_coronainfo_list[0]}
- Total Death along the world : {world_coronainfo_list[1]}
- Total Recovered : {world_coronainfo_list[2]}
Source : WorldoMeter 
Link : (https://www.worldometers.info/coronavirus)


*** Last 24 Hours in Bangladesh : 
- COVID-19 test conducted in last 24 hours : {bd_coronainfo_list[3]} 
    Test Conducted at IEDCR : {bd_coronainfo_list[1]}, 
    Test Conducted at Other's Lab : {bd_coronainfo_list[2]}
    (These are the number of total tests)


- COVID-19 positive cases in last 24 hours : {bd_coronainfo_list[11]} 
    Found at IEDCR : {bd_coronainfo_list[9]} 
    Found at Other's Lab : {bd_coronainfo_list[10]}

    Recovered in last 24 hours : {bd_coronainfo_list[-4]}
    Death in last 24 hours : {bd_coronainfo_list[-2]}


*** Total Results in Bangladesh : 
    -Total COVID-19 test conducted : {bd_coronainfo_list[7]}
    -COVID-19 Total Positive (+) cases : {bd_coronainfo_list[15]}
    -Total Recovered : {bd_coronainfo_list[-3]}
    -Total Death in Bangladesh : {bd_coronainfo_list[-1]}

Source: IEDCR, Bangladesh
Link : (http://iedcr.gov.bd)


N.B : This mail has been sent by Akif's Automation BOT. If you see any bugs,errors or wrong information on this email, please share with me, I will fix that.This is a test mail.I am not responsible for any mistakes of any of these data. 

Keep praying for the world. May Allah help us from this devastating pandemic.

Sincerely,
A ROBOT
Created by Akif Islam
'''
    subject = 'Corona Virus NewsLetter -(By Akif''s Automation Program)'

    message = f"Subject: {subject}\n\n{body}"

    #To Akif (MySelf)
    
    server.sendmail(
        'iamakifislam@gmail.com',
        'iamakifislam@gmail.com',
        message
    )

    print("EMAIL SENT ! ! ")
    server.quit()

while(True) :
    world_corona_update()
    bangladesh_corona_update()
    send_email()
    time.sleep(3600*12) #Time in seconds.
    #It will email in every 12 hours with latest updates.
