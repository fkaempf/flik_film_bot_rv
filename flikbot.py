# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 22:41:04 2020

@author: Florian Kämpf
"""

import datetime
import pandas as pd 

import time
import numpy as np
import telegram
import os
import sys

import webbrowser
import requests
from bs4 import BeautifulSoup

from urllib.request import urlopen



sp=None
activelist="flik-liste"
forcequit=False
neu_text=None
 

def randfilm(inet=True,output=False,tele=False):
            film_number=np.random.randint(1,len(list(flik.index)))
            film_text=str(flik.iloc[film_number,0]) + " \nLink: " + str(flik.loc[film_number,"URL"])            
           
            
            global last_film_text
            
            global sp
            
            if sp == True:
                film_number=51
                film_text='Scott Pilgrim vs. the World (2010) \nLink: www.letterboxd.com/film/scott-pilgrim-vs-the-world/'
            
            if inet==True:
                webbrowser.open(flik.iloc[film_number,2])
            
            print("")
            print(film_text)
            if tele ==True:
                
                if film_text != last_film_text or film_text == 'Scott Pilgrim vs. the World (2010) \nLink: www.letterboxd.com/film/scott-pilgrim-vs-the-world/':
                    id_chat=bot.get_updates()[-1].message.chat_id
                    bot.send_message(chat_id=id_chat, text=film_text)
                    last_film_text=film_text
                else:
                    film_number=np.random.randint(1,len(list(flik.index)))
                    film_text=str(flik.iloc[film_number,0]) + " (" + str(flik.iloc[film_number,1]) + ") \nLink: " + str(flik.iloc[film_number,2])
                    id_chat=bot.get_updates()[-1].message.chat_id
                    bot.send_message(chat_id=id_chat, text=film_text)
                    last_film_text=film_text
                
            if output==True:
                return film_number
            

def updatemessage():
    return bot.get_updates()[-1].message.text.lower()

def newmessageid():
    return bot.get_updates()[-1].message.message_id

def resetmid():
    
    global oldmessageid
    oldmessageid = newmessageid()
    


def list_getter(url="https://letterboxd.com/flik_memes/list/flik-liste/page/"):
    
    link =[]
    name =[]
    page = 0
    goon = True
    
    while goon == True:
        
            page += 1
            film_url_mod = url + str(page)
            response = requests.get(film_url_mod)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            
            wrapper = soup.find_all('div',class_="poster film-poster really-lazy-load")
            
            
            
            for index,item in enumerate(list(wrapper)):
            
                link.append("letterboxd.com"+str(wrapper[index]["data-target-link"])) 
                name.append(wrapper[index].find_all(True)[0]["alt"])
                
            if wrapper == []:
                goon = False
    film_df = pd.DataFrame({"Name":name,"URL":link})
    film_df.to_csv("lists\\" + url.split("/")[-3] + ".csv",index=False)
    return film_df

now = datetime.datetime.now()
print(str(now.strftime("%H:%M %d.%m.%Y")))
print("")
print("Running...")

flik=pd.read_csv("lists\FLIK-Liste.csv")
flik_unver=pd.read_csv("lists\FLIK-Liste.csv")

#ab hier bot teil

bot = telegram.Bot(token='1174845563:AAF-tTzmvMuZB2wWC07EeZHKP9tq-_97w6A')

# flofight_test_bot = '1095591214:AAGLAHVYwEhZ9vOTMLUUckArORNjUfCkBiw'
# flik_film_bot = '1174845563:AAF-tTzmvMuZB2wWC07EeZHKP9tq-_97w6A'

neu_lange=None


while(True):
    try:
        inet=False
            
        while bot.get_updates()==[] or bot.get_updates()[-1].message.text==None:
                time.sleep(5)
                
        while bot.get_updates()[-1].message==None:
            time.sleep(1)
            
        resetmid()
        
        
        oldmessageid=newmessageid()
        neu_text=updatemessage()
    
        neu_lange=len(bot.get_updates())
        alt_text=neu_text
        alt_lange=neu_lange
        last_c_message="0"
        last_film_text="0"
        sp=False
        
        while (True):
            inet=False

       
            now2 = datetime.datetime.now()
            
            #time 5 stunden
            
            if int(str(now2-now).replace(":","")[0]) >= 3:
                
                
                os.system(r"start flikbot.py")
                forcequit=True
                
                quit()
            
            while bot.get_updates()[-1].message  ==None:
                       time.sleep(1) 
                
            while bot.get_updates()==[] or bot.get_updates()[-1].message.text==None:
                        time.sleep(2)
               
            if oldmessageid != newmessageid():
                    print("")
                    print(newmessageid())
            
            try:
                       
               neu_text=updatemessage()
               
                
               if len(bot.get_updates()) == 100: 
                   bot.get_updates(offset=-1)
               if type(updatemessage())==str:
                    
                     
                    #go
                    
                    if oldmessageid != newmessageid() and updatemessage() == "go":
                        time.sleep(0.1)
                        if updatemessage() == "go": 
                            randfilm(inet=False,tele=True)
                            alt_lange=int(neu_lange)
                    
                        resetmid()
                    
                    #runtime
                    
                    if oldmessageid != newmessageid() and updatemessage()== "runtime": 
                   
                        now2 = datetime.datetime.now()
                        bot.send_message(chat_id=595203046, text="Runtime: "+str(now2-now))
                    
                        resetmid()
                    
                    #stop
                    
                    if oldmessageid != newmessageid() and updatemessage() == "stop":
                        if bot.get_updates()[-1].message.chat_id == 595203046:
                            import sys
                            sys.exit()
                            
                    #pc    
                    if oldmessageid != newmessageid() and updatemessage() == "pc":
                        if bot.get_updates()[-1].message.chat_id == 595203046:
                            randfilm(inet=True)
                    
                        resetmid()
                    
                    #help
                    
                    if oldmessageid != newmessageid() and updatemessage() == "help":
                        
                        if bot.get_updates()[-1].message.chat_id != 595203046:
                            helpmessage = "go - gives you a random movie from the FLIK-List\ncheck [FILMNAME] - checks if a certain film is in the FLIK-List\nsuggest [FILMNAME] - suggests a film for the FLIK-List"
                            bot.send_message(chat_id=bot.get_updates()[-1].message.chat_id,text=helpmessage)
                            resetmid()
                        else:
                            helpmessage = "go - gives you a random movie from the FLIK-List                                  \
                                           check [FILMNAME] - checks if a film is contained in the FLIK-List                 \
                                               suggest [FILMNAME] - suggests a film for the FLIK-List                        \
                                                   check suggs - displays the suggestion list                                \
                                                       clear suggs - clear suggestion list                                   \
                                                           sp on - activates Scott Pilgrim Mode                              \
                                                               sp off - deactivates Scott Pilgrim Mode                       \
                                                                   stop - shuts the bot down                                 \
                                                                       pc - opens a random film from the FLIK-List on the pc \
                                                                           runtime - displays runtime of the bot               \
                                                                             update flik - updates the flik-list\
                                                                               new list [LINK TO LIST] - adds new list to folder\
                                                                                   show list - shows available lists\
                                                                                       active list - displays active list\
                                                                                       change list [LISTNAME] - changes active list"
                                                                                       
                            bot.send_message(chat_id=bot.get_updates()[-1].message.chat_id,text=helpmessage)
                    
                            resetmid()
                    #update flik
                    
                    if bot.get_updates()[-1].message.chat_id == 595203046:
                        if oldmessageid != newmessageid() and updatemessage() == "update flik":
                            time.sleep(0.5)
                            bot.send_message(chat_id=595203046, text="Update gestartet!")  
                            flik=list_getter()
                            bot.send_message(chat_id=595203046, text="FLIK-Liste wurde geupdatet.")  
                            
                            resetmid()
                    # add new list
                    if bot.get_updates()[-1].message.chat_id == 595203046:
                        if oldmessageid != newmessageid() and updatemessage()[:8] == "new list":
                            resetmid()
                            try:
                                list_getter(updatemessage()[8:].lstrip())
                                bot.send_message(chat_id=595203046, text="Liste wurde dem Verzeichnis hinzugefügt.")  
                                
                                resetmid()
                            except: 
                                  bot.send_message(chat_id=595203046, text="Ungültiger Link!")    
                    #show lists
                        
                    if bot.get_updates()[-1].message.chat_id == 595203046:
                        if oldmessageid != newmessageid() and updatemessage() == "show lists":
                            all_lists=os.listdir("lists\\")
                            all_lists_message=""
                    
                                    
                            for index,x in enumerate(all_lists):
                                    if x[-4:]==".csv":
                                        x=x.replace(".csv","")
                                        all_lists_message+= str(index+1) + " "+ str(x) + str("\n")
                                
                            bot.send_message(chat_id=595203046, text=all_lists_message)    
                            resetmid()
                            
                    #active list
                    if bot.get_updates()[-1].message.chat_id == 595203046:
                        if oldmessageid != newmessageid() and updatemessage() == "active list":  
                           bot.send_message(chat_id=595203046, text=activelist) 
                           resetmid()   
                                 
                    #change list [input]
                    if bot.get_updates()[-1].message.chat_id == 595203046:
                        if oldmessageid != newmessageid() and updatemessage()[:11] == "change list":
                            resetmid()
                            all_lists=[x.lower().replace(x[-4:],"") for x in os.listdir("lists\\")]
                            all_lists_message=""
                            try:
                                try:
                                    index_select = int(updatemessage()[11:].lstrip()) -1
                                    flik = pd.read_csv("lists\\"+ all_lists[index_select] + ".csv")
                                    bot.send_message(chat_id=595203046, text="Die aktive Liste wurde zu '"+all_lists[index_select]+"' geändert.")  
                                    activelist=all_lists[index_select]
                                except:
                                    int(updatemessage()[11:].lstrip())
                                    bot.send_message(chat_id=595203046, text="Dieser Index existiert im Verzeichnis nicht.")  
                           
                            except:                                       
                            
                                if updatemessage()[11:].lstrip().lower() in all_lists:
                                    
                                    flik = pd.read_csv("lists\\"+ updatemessage()[11:].lstrip().lower() + ".csv")
                                    activelist=updatemessage()[11:].lstrip().lower()
                                    bot.send_message(chat_id=595203046, text="Die aktive Liste wurde zu '"+updatemessage()[11:]+"' geändert.")  
                                
                                else:
                                    
                                    for index,x in enumerate(all_lists):
                                       
                                            x=x.replace(".csv","")
                                            all_lists_message+= str(index+1) + " "+ str(x) + str("\n")
                                    
                                    bot.send_message(chat_id=595203046, text="Diese Liste befindet sich nicht im Listernverzeichnis. Folgende Listen sind verfügbar.")  
                                    bot.send_message(chat_id=595203046, text=all_lists_message)          
                            
                            
       
                    #check
                    
                    if oldmessageid != newmessageid() and updatemessage().lower()[0:5] == "check":
                        if updatemessage().lower()[6:] != "suggs" and len(updatemessage().lower())>5:
                            
                            
                            if updatemessage().lower()[6:] in [x.lower() for x in list(flik_unver.iloc[:,0])]:
                                c_message=str('"' + updatemessage().lower()[6:] + '"' + " befindet sich in der FLIK-Liste")
                            
                            if updatemessage().lower()[6:] not in [x.lower() for x in list(flik_unver.iloc[:,0])]:
                                c_message=str('"' + updatemessage().lower()[6:] + '"' + " befindet sich nicht in der FLIK-Liste")
                            
                           # if last_c_message != c_message:
                            bot.send_message(chat_id=bot.get_updates()[-1].message.chat_id, text=c_message)
                            
                            last_c_message=c_message
                                
                            
                            alt_lange=int(neu_lange)
                            
                            resetmid()
                        #check suggs
                        
                        else:
                            if bot.get_updates()[-1].message.chat_id == 595203046:
                                try:
                                    file=open("suggestions.txt","r")
                                    allsuggs=file.read()                  
                                    file.close()
                                   
                                    bot.send_message(chat_id=595203046, text=allsuggs)
                                    resetmid()
                                    
                                except:
                                    bot.send_message(chat_id=595203046, text="No suggestions")    
                                    resetmid()
                            
                    #sp     
                            
                    if oldmessageid != newmessageid() and updatemessage().lower()[0:2] == "sp":
                        
                        if bot.get_updates()[-1].message.chat_id == 595203046 and len(updatemessage().lower())>4:
                            
                            if updatemessage().lower()[3:5] == "on":
                                sp = True
                                bot.send_message(chat_id=595203046, text="Scott Pilgrim Modus angeschaltet.")
                                
                            if updatemessage().lower()[3:6] == "off":
                                sp = False
                                bot.send_message(chat_id=595203046, text="Scott Pilgrim Modus ausgeschaltet.")
                            resetmid()
    
                    
                    #clear
                        
                    if oldmessageid != newmessageid() and updatemessage().lower() == "clear suggs":
                        os.remove("suggestions.txt")
                        bot.send_message(chat_id=595203046, text="Suggestions cleared")
                    
                        resetmid()
                    
                    #suggest
                    
                    if oldmessageid != newmessageid() and updatemessage().lower()[0:7] == "suggest":
                        
                        if len(updatemessage().lower())>8:
                            
                            if updatemessage().lower()[8:] in [x.lower() for x in list(flik_unver.iloc[:,0])]:
                                
                                bot.send_message(chat_id=bot.get_updates()[-1].message.chat_id, text=str('"' + updatemessage().lower()[8:] + '"' + " befindet sich bereits in der FLIK-Liste."))
                            
                            
                            
                            else:
                               
                                file=open("suggestions.txt","a+")
                                sugg_film=updatemessage().lower()[8:] + " [" + bot.get_updates()[-1].message.from_user.first_name + "]\n"
                                file.write(sugg_film)
                                file.close()
                                
                                bot.send_message(chat_id=bot.get_updates()[-1].message.chat_id, text=updatemessage().lower()[8:] + " wurde auf die Vorschlagsliste gesetzt.")
                        
                        resetmid()
          
            except:

               if oldmessageid != newmessageid() and updatemessage() =="stop":
                   import sys
                   sys.exit()
            

               print("")
               print("Error")
               bot.send_message(chat_id=595203046, text="Error")
               resetmid()
               

    except:
        if neu_text =="stop":
           
            
            sys.exit()
        if forcequit==True:
            quit()
        
        try:
              time.sleep(4)
              urlopen("https://www.google.de")
              print("Error")
              bot.send_message(chat_id=595203046, text="Error")
              if forcequit==True:
                  quit()
                  exit()
        except:
                 print("Kein Internet")
                
    
    
    #Offline modus wenn telegram skript nicht funktioniert
    
#alternativ skript    
if neu_lange==None:
        eingabe=None
        
        print("")
        print("Telegram Skript funktioniert nicht")
         
        randfilm(inet=False)
        
        
        
        while (True):
            eingabe=input()
            if eingabe == "stop":
                import sys
                sys.exit()
            if type(eingabe)==str:
                
                randfilm(inet=False)
                
                eingabe=None
    
    #stop durch telegram
    
if oldmessageid != newmessageid() and neu_text == "stop":
                    import sys
                    sys.exit()
  
