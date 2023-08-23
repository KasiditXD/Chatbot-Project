from tkinter import *
from tkinter import messagebox
import math
import random
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from PIL import ImageTk, Image
import time
import re
import fractions
import enchant     
window = Tk()
window.title("Chatbot")
window.attributes("-fullscreen", True)
window.configure(background="Blue")
Y = 10
letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",",","!","."," ","",
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
           ]
userlog_background = "cyan"
userlog_foreground = "darkcyan"
botlog_background = "lightgreen"
botlog_foreground = "darkgreen"
def configletters(x):
        sentence = x
        for each in x:
            if not (each in letters):
                sentence = sentence.replace(each, "")
        return sentence
def get_source(url):
    try:
        headers = {"Accept-Language": "en-US,en;q=0.5"}
        session = HTMLSession()
        response = session.get(url, headers=headers)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
def scrape_google(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)
    links = list(response.html.absolute_links)
    google_app = (
        "https://www.google.",
        "https://google.",
        "https://webcache.googleusercontent.",
        "http://webcache.googleusercontent.",
        "https://policies.google.",
        "https://support.google.",
        "https://maps.google.",
    )
    for url in links[:]:
        if url.startswith(google_app):
            links.remove(url)
    return links
def get_results(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.th/search?q=" + query)
    return response
def parse_results(response):
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"
    results = response.html.find(css_identifier_result)
    if results:
        result = results[0]
        item = {
            "title": result.find(css_identifier_title, first=True).text,
            "link": result.find(css_identifier_link, first=True).attrs["href"],
            "text": result.find(css_identifier_text, first=True).text,
        }
        return item
    else:
        return None
def google_search(query):
    try:
        response = get_results(query)
        result = parse_results(response)
        print(result)
        if result:
            return result
        else:
            return None
    except:
        return None
def scrape(x):
        lowercase = x.lower()
        result = google_search(lowercase)
        if result:
            if configletters(result["text"]):
                return configletters(result["text"])
            else:
                return "Sorry, I don't have information on this."
        else:
            return "Sorry, I don't have information on this."
class mechanic:
    def evaluate_math_expression(this,expression):
        print("expression: "+expression)
        try:
            expression = re.sub(r"([^\d)])\s*/\s*([^\d(])", r"\1/\2", expression)
            expression = expression.replace("/", "+fractions.Fraction(")
            expression = expression.replace("!", "math.factorial")
            expression = expression.replace("log", "math.log10")
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos")
            expression = expression.replace("tan", "math.tan")
            expression = expression.replace("asin", "math.asin")
            expression = expression.replace("acos", "math.acos")
            expression = expression.replace("atan", "math.atan")
            expression = expression.replace("sqrt", "math.sqrt")
            result = eval(expression)
            return str(result)
        except Exception:
            return None
    def removenonenglish(this,x):
        try:
            checker = enchant.Dict("en_US")
            keys = []
            word = ""
            arr = list(x+"#")
            sentence = x
            for each in arr:
                if each == " " or each == "#":
                    keys.append(word) 
                    word = ""
                else:
                    word = word + each
            print(keys)
            for each in keys:
                print(each)
                try:
                    if checker.check(each) == False: 
                        sentence = sentence.replace(each,"")
                except Exception: 
                    sentence = sentence
            return sentence
        except Exception:
            return sentence
    def printtxt(this,text):
        this.createlog(text, Y)
    def generate(this,arr):
        return arr[random.randrange(0, len(arr))]
    def join(this,s):
        strx = " ".join(map(str, s))
        return strx
    def tryeval(this,str):
        try:
            eval(str)
            return True
        except:
            return False
    def display(this,msg):
        sentence = msg.capitalize()
        if not ("." in msg):
            sentence = sentence + "."
        this.printtxt("Coconutz: " + sentence)
    def displayanswer(this,answer):
        this.printtxt("Bot: " + "The answer is " + str(answer))
    def __init__(this,Y,activate):
        this.Y = Y
        this.activate = activate
        this.keywords = ["evaluate", "calculate", "solve"]
        this.greetings = ["hello","hi","how are you","glad to see you","wassup","hi there!","yes?"]
        this.intro = ["This is coconuZ version 1.5, a chatbot program created by Kaow, please don't hesitate to ask because I'm ready to help"]
        this.errorscrape= ["earn more", "see more", "definition"]
    def onsending(this,exceed, lengthstr, img, text, bgframecolor, fgtextcolor, bgtextcolor):
        global Y
        logframe = Frame(main, bg=bgframecolor)
        logframe.place(x=0, y=Y, width=1000, height=30)
        # initial x60 y10
        image1 = Image.open(img).resize((20, 20))
        test = ImageTk.PhotoImage(image1)
        CoconutImageLabel = Label(logframe, image=test)
        CoconutImageLabel.image = test
        CoconutImageLabel.place(x=5, y=4)
        label2 = Label(logframe, fg=fgtextcolor, bg=bgtextcolor, text=text[:exceed])
        label2.config(font=("Comic Sans MS", 10))
        label2.place(x=40, y=5)
        if lengthstr <= exceed:
            Y = Y + 40
        else:
            label2.config(text=text[:exceed] + "-")
            Y = Y + 30
    def exceedmessagefixing(this,exceed, oncutstr, lengthstr, modifiedstr, bgframecolor, fgtextcolor, bgtextcolor):
        global Y
        print("exceed" + str(lengthstr))
        extendpart = modifiedstr[oncutstr:]
        print("At length " + str(oncutstr) + " : " + extendpart)
        logframe = Frame(main, bg=bgframecolor)
        logframe.place(x=40, y=Y, width=1000, height=30)
        label2 = Label(logframe, fg=fgtextcolor, bg=bgtextcolor, text=extendpart[:exceed])
        label2.config(font=("Comic Sans MS", 10))
        label2.place(x=10, y=5)
        if lengthstr <= exceed:
            Y = Y + 40
        else:
            label2.config(text=extendpart[:exceed] + "-")
            Y = Y + 30
    def createlog(this,text, y):
        lengthstr = len(text)
        print("before" + str(lengthstr))
        oncutstr = 0
        modifiedstr = text
        exceed = 130
        foregroundtextcolor = "white"
        global botlog_background
        global botlog_foreground
        global Y
        this.onsending(exceed,lengthstr,"img/R.png",text,botlog_background,foregroundtextcolor,botlog_foreground,)
        while lengthstr > exceed:
            lengthstr -= exceed
            oncutstr += exceed
            this.exceedmessagefixing(exceed,oncutstr,lengthstr,modifiedstr,botlog_background,foregroundtextcolor,botlog_foreground,)
        if Y > 570:
            print("bot exceed")
            Y = 0
            for each in main.winfo_children():
                each.destroy()
            this.onsending(exceed,lengthstr,"img/R.png",text,botlog_background,foregroundtextcolor,botlog_foreground,)
    def createUserLog(this,text, y):
        lengthstr = len(text)
        oncutstr = 0
        modifiedstr = text
        exceed = 130
        global userlog_background
        global userlog_foreground 
        foregroundtextcolor = "white"
        global Y
        this.onsending(exceed,lengthstr,"img/person.png",text,userlog_background,foregroundtextcolor,userlog_foreground)
        while lengthstr > exceed:
            lengthstr -= exceed
            oncutstr += exceed
            this.exceedmessagefixing(exceed,oncutstr,lengthstr,modifiedstr,userlog_background,foregroundtextcolor,userlog_foreground)
        if Y > 530:
            print("user exceed")
            Y = 0
            for each in main.winfo_children():
                each.destroy()
            this.onsending(exceed,lengthstr,"img/person.png",text,userlog_background,foregroundtextcolor,userlog_foreground)
    def removedoublespace(this,x):
        sentence = str(x)
    def submit(this):
        Y = this.Y
        x = var.get()
        print(x)
        this.createUserLog("User: " + x, Y)
        x += "."
        arr = list(x)
        char_count = 0
        strf = ""
        keys = []
        name = ""
        for char in arr:
            char_count += 1
            strf += char
            find = False
            if char == " ":
                strf = strf.replace(" ", "")
                if strf in this.keywords:
                    if this.activate == False:
                        this.activate = True
                        strf = ""
                    else:
                        keys.append(strf)
                        strf = ""
            if char == ".":
                strf = strf.replace(".", "")
                print(strf)
                keys.append(strf)
                if "s" in strf and this.activate == False:
                    if "is" in keys:
                        strf = strf
                    else:
                        strf = strf.replace("s", "")
                if this.activate == True:
                    this.activate = False
                    this.display("The answer is "+str(this.evaluate_math_expression(strf)))
                else:
                    if strf in this.greetings:
                        print("yes")
                        this.display(this.generate(this.greetings)+ " "+ this.generate(this.intro))
                    else:
                        result = scrape(x.replace(".", "").lower()).strip()
                        for each in this.errorscrape:
                                if each in result:
                                    result = result.replace(each, "")
                        if "." in result:
                            result = result.replace(".", "") + "."
                        if result[0] == " ":
                                result = result[0:]
                        if "  " in result:
                            result = result.replace("  ", ", ")
                        elif "   " in result:
                            result = result.replace("   ", ", ")
                        elif "    " in result:
                            result = result.replace("    ", ", ")      
                        this.display(result.capitalize())
class frame:
    def __init__(this,parent,background,width,height,x,y,isRel=False):
        main = Canvas(parent, background=background, width=width, height=height)
        main.pack(expand=True, fill=BOTH)
        if isRel == True:
            main.place(relx=x, rely=y)
        else:
            main.place(x=x, y=y)
class label:
    def __init__(this,parent,text,background,foreground,size,x,y,font="Comic Sans MS",isRel=False):
        Title = Label(parent, text=text)
        Title.configure(font=(font,size), background=background, foreground=foreground)
        if isRel == True:
               Title.place(relx=x, rely=y)
        else:
            Title.place(x=x, y=y)
var = StringVar()
class entry:
    def __init__(this,width,x,y,isRel):
        this.width = width
        this.x = x
        this.y = y
        this.isRel = isRel
        msgbox = Entry(window,textvariable=var,width=this.width,font=("Comic Sans MS", 25, "bold"),background="#00569F",foreground="White")
        if this.isRel == True:
            msgbox.place(relx=this.x, rely=this.y)
        else:
            msgbox.place(x=this.x, y=this.y)
class textbutton:
    def __init__(this,location,command,background,foreground,text,x,y,font,isRel=False):
        button = Button(location,text=text,command=command,background=background,foreground=foreground,font=font)
        button.configure(font=font)
        if isRel == True:button.place(relx=x, rely=y)
        else:button.place(x=x, y=y)
def userlog_backgroundchanger(x):
        global userlog_background 
        userlog_background = x 
def botlog_backgroundchanger(x):
        global botlog_background 
        botlog_background = x
def userlog_foregroundchanger(x):
        global userlog_foreground 
        userlog_foreground = x 
def botlog_foregroundchanger(x):
        global botlog_foreground 
        botlog_foreground = x
class setting:
    #Background Settings: 
    def __init__(this,width,height):
        this.width = width
        this.height = height
        this.background = "#090041"
        this.row1colors = ["blue","green","red","black"]
        this.row2colors = ["violet","grey","white","orange"]
        this.row3colors = ["green","violet","cyan","orange"]
    def select(this,pos,ColorSettingFrame):
        if (this.columnrow1 == pos):
            currentbackground = this.row1colors[this.columnrow1]
            currentbackground2 = this.row2colors[this.columnrow1]
            currentbackground3 = this.row3colors[this.columnrow1]
            colorlabel = label(ColorSettingFrame,currentbackground,this.background,currentbackground,12,this.startPosX+10,this.startPosY-40)
            colorlabe2 = label(ColorSettingFrame,currentbackground2,this.background,currentbackground2,12,this.startPosX+10,this.startPosY+50)
            colorbtn1 = textbutton(ColorSettingFrame,lambda: main.configure(background=currentbackground),currentbackground,"black",currentbackground,this.startPosX, this.startPosY,("Comic Sans MS", 12, "bold"))
            colorbtn2 = textbutton(ColorSettingFrame,lambda: main.configure(background=currentbackground2),currentbackground2,"black",currentbackground2,this.startPosX, this.startPosY+90,("Comic Sans MS", 12, "bold"))
            colorbtn3 = textbutton(ColorSettingFrame,lambda: userlog_backgroundchanger(currentbackground3),currentbackground3,"black",currentbackground3,this.startPosX, this.startPosY+170,("Comic Sans MS", 12, "bold"))
            colorbtn4 = textbutton(ColorSettingFrame,lambda: botlog_backgroundchanger(currentbackground3),currentbackground3,"black",currentbackground3,this.startPosX, this.startPosY+230,("Comic Sans MS", 12, "bold"))
            colorbtn5 = textbutton(ColorSettingFrame,lambda: userlog_foregroundchanger(currentbackground3),currentbackground3,"black",currentbackground3,this.startPosX, this.startPosY+290,("Comic Sans MS", 12, "bold"))
            colorbtn6 = textbutton(ColorSettingFrame,lambda: botlog_foregroundchanger(currentbackground3),currentbackground3,"black",currentbackground3,this.startPosX, this.startPosY+350,("Comic Sans MS", 12, "bold"))
    def create(this):
        this.startPosX = 240
        this.startPosY = 130
        this.columnrow1 = 0
        ColorSettingFrame = Canvas(window, background=this.background, width=600, height=600)
        ColorSettingFrame.place(x=0,y=0)
        Setting_title = Label(ColorSettingFrame, text="Setting")
        Setting_title.configure(font=("Comic Sans MS", 40, "bold"), background="#2A0061", foreground="#FF5353")
        Setting_title.place(x=40, y=10)
        bg_label = label(ColorSettingFrame,"Background -> ","#2A0061","#FF8686",15,40,130)
        user_log = label(ColorSettingFrame,"User Log -> ","#2A0061","#FF8686",15,40,300)
        bot_log = label(ColorSettingFrame,"Bot Log -> ","#2A0061","#FF8686",15,40,360)
        user_text = label(ColorSettingFrame,"User Text -> ","#2A0061","#FF8686",15,40,420)
        bot_text = label(ColorSettingFrame,"Bot Text -> ","#2A0061","#FF8686",15,40,480)
        while this.columnrow1 <= 3:
            this.select(this.columnrow1,ColorSettingFrame) 
            this.startPosX += 90
            this.columnrow1 += 1
        this.columnrow1 = 0
        this.startPosX = 240
        this.startPosY = 130
        exitbtn = textbutton(ColorSettingFrame,lambda: ColorSettingFrame.destroy(),"#D30000","white","Exit",545, 0,("Comic Sans MS", 15, "bold"))
def popupinfo():
    messagebox.showinfo("showinfo", "This is chatbot, name is CoconutZ, version 1.0, created by Kaow.")
chatbotmecha = mechanic(10,False)
settingsystem = setting(600,600)         
main = Frame(window, background="#261F8C", width=1080, height=670)
main.pack(expand=True, fill=BOTH)
main.place(x=410, y=0)
frame2 = frame(window,"#005194",345,870,30,0,False)
frame3 = frame(window,"#090041",1080,225,410,649,False)
titlebot = label(window,"CHATBOT","blue","white",35,60,35)
subtitle = label(window,"Experimental version 1.0","green","#FDCFFF",15,55,120,"Courier New bold")
entrychat = entry(30,0.35,0.92,True)
framemenu = frame(window,"purple",150,500,0.05,0.25,True)
labelmenu = label(window,"Menu","indigo","white",25,0.07,0.3,"Helvetica 25 underline",True) 
image = Image.open("img/exitgui.png").resize((105, 100))
imagetk = ImageTk.PhotoImage(image)
buttonexits = Button(window,command=quit,background="purple",border=0,foreground="White",image=imagetk)
buttonexits.place(relx=0.065, rely=0.4)
imagesetting = Image.open("img/settinggui.png").resize((100, 100))
imagesettingtk = ImageTk.PhotoImage(imagesetting)
buttonsetting = Button(window, command=lambda:settingsystem.create(), image=imagesettingtk, border=0, background="purple")
buttonsetting.place(relx=0.07, rely=0.6)
imageinfo = Image.open("img/info.png").resize((100, 100))
imageinfotk = ImageTk.PhotoImage(imageinfo)
buttoninfo = Button(window, command=lambda: popupinfo(), image=imageinfotk, border=0, background="purple")
buttoninfo.place(relx=0.07, rely=0.8)
buttonsend = textbutton(window,lambda:chatbotmecha.submit(),"#FF7900","white","Submit",0.85, 0.92,("Comic Sans MS", 15, "bold"),True)
window.mainloop()
