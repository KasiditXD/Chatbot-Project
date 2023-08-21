from tkinter import *
import tkinter as tk
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

window = tk.Tk()
window.title("Chatbot")
window.attributes("-fullscreen", True)
window.configure(background="Blue")

width = 1000


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

        if result:
            return result
        else:
            display("I dont understand the question")
            return None
    except:
        display("Sorry, I don't have information on this.")


def checkifinknowledge(keys, arr):
    try:
        word = []
        nos = None
        for each in keys:
            if "s" in each:
                nos = each.replace("s", "")

            if each in arr:
                word.append(each)
            elif (nos) in arr:
                word.append(nos)

        if word:
            return word
        else:
            return None
    except:
        return None


def printtxt(text):
    createlog(text, Y)


def generate(keys, arr):
    return keys[arr][random.randrange(0, len(knowledge[arr]))]


def join(s):
    strx = " ".join(map(str, s))
    return strx


def mathconfig(strf, func):
    try:
        x = strf.replace(func, "")
        if ("(" in x) or (")" in x):
            x = x.replace("(", "")
            x = x.replace(")", "")
        if "pow" in strf:
            if func == ("pow" or "power" or "^"):
                a = list(x)
                for each in a:
                    if each == ",":
                        a.remove(",")
                return math.pow(int(a[0]), int(a[1]))
        else:
            z = int(x)
            if func == "sin":
                return math.sin(z)
            elif func == "cos":
                return math.cos(z)
            elif func == "tan":
                return math.tan(z)
            elif func == "sqrt":
                return math.sqrt(z)
    except:
        return (
            "I cannot solve this problem, if I know better, I may be able to help you."
        )


def tryeval(str):
    try:
        eval(str)
        return True
    except:
        return False


def display(msg):
    sentence = msg.capitalize()
    if not ("." in msg):
        sentence = sentence + "."
    printtxt("Coconutz: " + sentence)


def answerwithrespecttoterms(terms):
    sentence = ""
    x = 0
    for each in terms:
        x += 1
        subject = each

        definition = knowledge[subject][random.randrange(0, len(knowledge[subject]))]
        sentence = sentence + subject + " is " + definition
        if len(terms) > 1 and x != len(terms):
            sentence = sentence + ", and "
    display(
        knowledge["knowing"][random.randrange(0, len(knowledge["knowing"]))]
        + " "
        + sentence
    )


def displayanswer(answer):
    printtxt("Bot: " + "The answer is " + str(answer))


def recognition(keys, pseudo):
    pos = -1
    definition = []
    o = []
    for i in keys:
        pos += 1
        if "is" == i:
            for each in keys:
                o.append(each)
            for i in range(pos + 1):
                o.remove(keys[i])
            stro = " ".join(map(str, o))
            pseudo[keys[pos - 1]] = [str(stro)]
            subject = [keys[pos - 1], str(stro)]
            return (
                subject[0] + " " + str(grammar["verbtobe"][0]) + " " + str(subject[1])
            )


def configletters(x):
    sentence = x
    for each in x:
        if not (each in letters):
            sentence = sentence.replace(each, "")
    return sentence


def scrape(x):
    lowercase = x.lower()
    result = google_search(lowercase)

    if result:
        return configletters(result["text"])


recognize = False
answered = False
pending = False
onPendingName = None
onpendingAnswer = False
onexit = False

knowledge = {
    "self": ["Chat bot"],
    "you": ["ok", "fine"],
    "yourself": ["happy"],
    "coconut": ["A type of fruit"],
    "strawberry": ["A tropical fruit that is sweet and sourly"],
    "friend": ["Pan", "Shokun", "Mart", "Pic"],
    "questions": ["what", "when", "where", "why", "how"],
    "command": ["define"],
    "calculates": ["evaluate", "calculate", "solve"],
    "answernoidea": [
        "I don't know",
        "what?",
        "I don't know what this means",
        "I have no idea",
    ],
    "greetings": [
        "hello",
        "hi",
        "how are you",
        "glad to see you",
        "wassup",
        "hi there!",
        "yes?",
    ],
    "symbol": ["+", "-", "*", "/"],
    "trigonometry": ["sin", "cos", "tan"],
    "mathfunc": ["pow", "sqrt", "^"],
    "knowing": ["i know what it is,", "It can be defined as", ""],
    "intro": [
        "This is coconuZ version 1.5, a chatbot program created by Kaow, please don't hesitate to ask because I'm ready to help"
    ],
}
errorscrape = {"earn more", "see more", "definition"}
grammar = {
    "personal": ["my", "myself", "self", "yourself", "yourselves", "I"],
    "verbtobe": ["is", "am", "are"],
    "userself": ["your"],
    "userpoint": ["you"],
    "refuse": ["wrong", "no", "not", "incorrect", "mistaken"],
}
letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",",","!","."," ",]


def onsending(exceed, lengthstr, img, text, bgframecolor, fgtextcolor, bgtextcolor):
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


def exceedmessagefixing(
    exceed, oncutstr, lengthstr, modifiedstr, bgframecolor, fgtextcolor, bgtextcolor
):
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


def createlog(text, y):
    lengthstr = len(text)
    print("before" + str(lengthstr))
    oncutstr = 0
    modifiedstr = text
    exceed = 130
    
    foregroundtextcolor = "white"
    global botlog_background
    global botlog_foreground
    

    global Y
    onsending(
        exceed,
        lengthstr,
        "img/R.png",
        text,
        botlog_background,
        foregroundtextcolor,
        botlog_foreground,
    )
    while lengthstr > exceed:
        lengthstr -= exceed
        oncutstr += exceed
        exceedmessagefixing(
            exceed,
            oncutstr,
            lengthstr,
            modifiedstr,
            botlog_background,
            foregroundtextcolor,
            botlog_foreground,
        )

    if Y > 570:
        print("bot exceed")
        Y = 0
        for each in main.winfo_children():
            each.destroy()
        onsending(
            exceed,
            lengthstr,
            "img/R.png",
            text,
            botlog_background,
            foregroundtextcolor,
            botlog_foreground,
        )


def createUserLog(text, y):
    lengthstr = len(text)
    oncutstr = 0
    modifiedstr = text
    exceed = 130
    global userlog_background
    global userlog_foreground 




    
    foregroundtextcolor = "white"
    
    global Y

    onsending(exceed,lengthstr,"img/person.png",text,userlog_background,foregroundtextcolor,userlog_foreground)

    while lengthstr > exceed:
        lengthstr -= exceed
        oncutstr += exceed
        exceedmessagefixing(
            exceed,
            oncutstr,
            lengthstr,
            modifiedstr,
            userlog_background,
            foregroundtextcolor,
            userlog_foreground,
        )

    if Y > 530:
        print("user exceed")
        Y = 0
        for each in main.winfo_children():
            each.destroy()
        onsending(
            exceed,
            lengthstr,
            "img/person.png",
            text,
            userlog_background,
            foregroundtextcolor,
            userlog_foreground,
        )


def removedoublespace(x):
    sentence = str(x)
    
    
  
        
    """
    strarray = list(sentence)
    for each in strarray:
        position += 1
        if each == "#":
            sentence = sentence.replace("#"," ")
    """
    return sentence


Y = 10

def evaluate_math_expression(expression):
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
def removenonenglish(x):
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
   
        

def submit():
    global Y
    global recognize
    global answered
    global pending
    global onPendingName
    global onpendingAnswer
    global onexit
    x = var.get()
    createUserLog("User: " + x, Y)

    x += "."
    arr = list(x)
    char_count = 0
    strf = ""
    keys = []
    calc_activate = False
    name = ""
    command_activate = False
    for char in arr:
        char_count += 1
        strf += char
        find = False
        if char == " ":
            strf = strf.replace(" ", "")
            for question_word in knowledge["questions"]:
                if strf == question_word:
                    keys.append(strf)
                    strf = ""
                    break

                else:
                    if strf in knowledge["calculates"]:
                        if calc_activate == False:
                            calc_activate = True
                        strf = ""
                        break
                    else:
                        keys.append(strf)
                        strf = ""
                        break

            for uself in grammar["userself"]:
                if strf == uself:
                    keys.append(strf)
                    strf = ""
                    display("you talk about my self")
                    break
        if char == ".":
            strf = strf.replace(".", "")
            keys.append(strf)
            if "s" in strf and calc_activate == False:
                if "is" in keys:
                    strf = strf
                else:
                    strf = strf.replace("s", "")

            if (
                (strf in knowledge) or command_activate == True
            ) and onpendingAnswer == False:
                term = checkifinknowledge(keys, knowledge)
                answerwithrespecttoterms(term)
                # display(knowledge["knowing"][random.randrange(0,len(knowledge["knowing"]))]+" "+knowledge[term][random.randrange(0,len(knowledge[term]))])

            else:
                if strf in knowledge["greetings"]:
                    display(generate(knowledge, "greetings")+ " "+ generate(knowledge, "intro"))
                    answered = True

                else:
                    isAnswered = False
                    if "no" in keys:
                        display("no?" + " what's wrong?")
                        onpendingAnswer = True

                    if calc_activate == True:
                        calc_activate = False
                        display("The answer is "+str(evaluate_math_expression(strf)))
                    else:
                        if "is" in keys and (not "what" in keys):
                            display("Remembered, " + recognition(keys, knowledge))
                        else:
                            if onpendingAnswer == False:
                                result = removenonenglish(scrape(x.replace(".", "").lower() + "meaning")).strip()
                                
                                for each in errorscrape:
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
                                elif "he" in result:
                                    result = result.replace("he",", ")

                                 
                                
                                display(result.capitalize())

def popupinfo():
    messagebox.showinfo("showinfo", "This is chatbot, name is CoconutZ, version 1.0, created by Kaow.")
    
userlog_background = "cyan"
userlog_foreground = "darkcyan"
botlog_background = "lightgreen"
botlog_foreground = "darkgreen"


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
    
    
def setting():
    
    
    


    ColorSettingFrame = Canvas(window, background="#090041", width=600, height=600)
    ColorSettingFrame.place(x=0,y=0)
    Setting_title = tk.Label(ColorSettingFrame, text="Setting")
    Setting_title.configure(font=("Comic Sans MS", 40, "bold"), background="#2A0061", foreground="#FF5353")
    Setting_title.place(x=40, y=10)
    
    bg = tk.Label(ColorSettingFrame, text="Background → ")
    bg.configure(font=("Comic Sans MS", 15, "bold"), background="#2A0061", foreground="#FF8686")
    bg.place(x=40, y=130)
#Background Settings: 
    blue = tk.Label(ColorSettingFrame, text="blue")
    blue .configure(font=("Comic Sans MS", 12, "bold"), background="#2A0061", foreground="#48A6FF")
    blue.place(x=250, y=90)

    blue_color = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#48A6FF", command = lambda: main.configure(background='blue'))
    blue_color.place(x=240, y=130)

    green = tk.Label(ColorSettingFrame, text="green")
    green.configure(font=("Comic Sans MS", 12, "bold"), background="#2A0061", foreground="#0EB800")
    green.place(x=335, y=90)

    green_color = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#0EB800", command = lambda: main.configure(background='green'))
    green_color.place(x=330, y=130)

    red = tk.Label(ColorSettingFrame, text="red")
    red.configure(font=("Comic Sans MS", 12, "bold"), background="#2A0061", foreground="red")
    red.place(x=430, y=90)

    red_color = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1,background="red", foreground="#0EB800", command = lambda: main.configure(background='red'))
    red_color.place(x=420, y=130)

    black = tk.Label(ColorSettingFrame, text="Black")
    black.configure(font=("Comic Sans MS", 12, "bold"), background="#2A0061", foreground="#060606")
    black.place(x=515, y=90)

    black_color = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="black",foreground="#0EB800", command = lambda: main.configure(background='black'))
    black_color.place(x=510, y=130)

    violet = tk.Label(ColorSettingFrame, text="violet")
    violet.configure(font=("Comic Sans MS", 12, "bold"), background="#2A0061", foreground="#C800CB")
    violet.place(x=245, y=180)

    violet_color = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#C800CB",foreground="#0EB800", command = lambda: main.configure(background='violet'))
    violet_color.place(x=238, y=210)

    gray = tk.Label(ColorSettingFrame, text="gray")
    gray.configure(font=("Comic Sans MS", 12, "bold"), background="#2A0061", foreground="#878787")
    gray.place(x=340, y=180)

    gray_color = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#878787",foreground="#0EB800", command = lambda: main.configure(background='gray'))
    gray_color.place(x=330, y=210)

    white = tk.Label(ColorSettingFrame, text="white")
    white.configure(font=("Comic Sans MS", 12, "bold"), background="#2A0061", foreground="White")
    white.place(x=425, y=180)

    white_color = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="white", foreground="#0EB800", command = lambda: main.configure(background='white'))
    white_color.place(x=420, y=210)

    orange = tk.Label(ColorSettingFrame, text="orange")
    orange.configure(font=("Comic Sans MS", 12, "bold"), background="#2A0061", foreground="#FF7400")
    orange.place(x=510, y=180)

    orange_color = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#FF7400", foreground="#0EB800", command = lambda: main.configure(background='orange'))
    orange_color.place(x=510, y=210)

# User log color
    user_log= tk.Label(ColorSettingFrame, text="User Log → ")
    user_log.configure(font=("Comic Sans MS", 15, "bold"), background="#2A0061", foreground="#FF8686")
    user_log.place(x=40, y=300)

    user_green = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#0EB800", command = lambda: userlog_backgroundchanger("green"))
    user_green.place(x=235, y=300)

    user_purple = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#8500CB", command = lambda: userlog_backgroundchanger("purple"))
    user_purple.place(x=330, y=300)

    user_lightblue = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#00D4FF",command = lambda: userlog_backgroundchanger("lightblue"))
    user_lightblue.place(x=420, y=300)

    user_orange = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#FF7400", command = lambda: userlog_backgroundchanger("orange"))
    user_orange.place(x=510, y=300)

# Bot log color
    user_log= tk.Label(ColorSettingFrame, text="Bot Log → ")
    user_log.configure(font=("Comic Sans MS", 15, "bold"), background="#2A0061", foreground="#FF8686")
    user_log.place(x=40, y=370)

    bot_green = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#0EB800", command = lambda: botlog_backgroundchanger("green"))
    bot_green.place(x=235, y=370)

    bot_purple = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#8500CB", command = lambda: botlog_backgroundchanger("purple"))
    bot_purple.place(x=330, y=370)

    bot_lightblue = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#00D4FF", command = lambda: botlog_backgroundchanger("lightblue"))
    bot_lightblue.place(x=420, y=370)

    bot_orange = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#FF7400", command = lambda: botlog_backgroundchanger("orange"))
    bot_orange.place(x=510, y=370)

# Text User
    text_user= tk.Label(ColorSettingFrame, text="Text User → ")
    text_user.configure(font=("Comic Sans MS", 15, "bold"), background="#2A0061", foreground="#FF8686")
    text_user.place(x=40, y=440)

    text_user_green = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#0EB800", command = lambda: userlog_foregroundchanger("green"))
    text_user_green.place(x=235, y=440)

    text_user_purple = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#8500CB", command = lambda: userlog_foregroundchanger("purple"))
    text_user_purple.place(x=330, y=440)

    text_user_lightblue = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#00D4FF", command = lambda: userlog_foregroundchanger("lightblue"))
    text_user_lightblue.place(x=420, y=440)

    text_user_orange = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#FF7400", command = lambda: userlog_foregroundchanger("orange"))
    text_user_orange.place(x=510, y=440)

# Text bot
    text_bot = tk.Label(ColorSettingFrame, text="Text Bot → ")
    text_bot.configure(font=("Comic Sans MS", 15, "bold"), background="#2A0061", foreground="#FF8686")
    text_bot.place(x=40, y=510)

    text_bot_green = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#0EB800", command = lambda: botlog_foregroundchanger("green"))
    text_bot_green.place(x=235, y=510)
    text_bot_purple = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#8500CB", command = lambda: userlog_foregroundchanger("purple"))
    text_bot_purple.place(x=330, y=510)

    text_bot_lightblue = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#00D4FF", command = lambda: userlog_foregroundchanger("lightblue"))
    text_bot_lightblue.place(x=420, y=510)

    text_bot_orange = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), width=5, height=1, background="#FF7400", command = lambda: userlog_foregroundchanger("orange"))
    text_bot_orange.place(x=510, y=510)

# Exit button
    buttonexits = tk.Button(ColorSettingFrame, font=("Comic Sans MS", 12, "bold"), text="X", width=5, height=1, command = lambda: ColorSettingFrame.destroy(), background="#D30000", foreground="White")
    buttonexits.place(x=540, y=0)



    
# Create a frame
main = tk.Frame(window, background="#261F8C", width=1080, height=670)
main.pack(expand=True, fill=tk.BOTH)
main.place(x=410, y=0)

frame2 = tk.Frame(window, background="#005194", width=345, height=870)
frame2.place(x=30, y=0)

frame3 = tk.Frame(window, background="#090041", width=1080, height=225)
frame3.place(x=410, y=649)

# The chatbot title
Title = tk.Label(frame2, text="CHATBOT")
Title.configure(
    font=("Comic Sans MS", 35, "bold"), background="#005194", foreground="#FDCFFF"
)
Title.place(x=60, y=35)

Title2 = tk.Label(frame2, text="(experimental version 1.0)")
Title2.configure(
    font=("Courier New", 15, "bold"), background="#005194", foreground="#FDCFFF"
)
Title2.place(x=17, y=100)


# The entry box
message1 = tk.Label(frame3, text="Send a message: ")
message1.configure(
    font=("Comic Sans MS", 18, "bold"), background="#000048", foreground="#FDCFFF"
)
message1.place(x=20, y=68)


var = StringVar()
msgbox = Entry(
    window,
    textvariable=var,
    width=30,
    font=("Comic Sans MS", 25, "bold"),
    background="#00569F",
    foreground="White",
)
msgbox.place(relx=0.35, rely=0.92)

menucanvas = Canvas(window, width=150, height=500, background="purple")
menucanvas.place(relx=0.05, rely=0.25)
labelmenu = Label(window, text="Menu", font=("Helvetica 25 underline"))
labelmenu.config(background="indigo", foreground="white")
labelmenu.place(relx=0.07, rely=0.3)

imageexit = Image.open("img/exitgui.png").resize((105, 100))
imageexittk = ImageTk.PhotoImage(imageexit)
# Exit button
buttonexits = tk.Button(
    window,
    command=quit,
    background="purple",
    border=0,
    foreground="White",
    image=imageexittk,
)

buttonexits.place(relx=0.065, rely=0.4)

imagesetting = Image.open("img/settinggui.png").resize((100, 100))
imagesettingtk = ImageTk.PhotoImage(imagesetting)
# Setting button
buttonexits = tk.Button(
    window, command=setting, image=imagesettingtk, border=0, background="purple"
)
buttonexits.place(relx=0.07, rely=0.6)

# info button
imageinfo = Image.open("img/info.png").resize((100, 100))
imageinfotk = ImageTk.PhotoImage(imageinfo)
buttonexits = tk.Button(
    window, command=lambda: popupinfo(), image=imageinfotk, border=0, background="purple"
)
buttonexits.place(relx=0.07, rely=0.8)

# Sending button
button = tk.Button(
    window,
    text="Submit",
    command=submit,
    font=("Comic Sans MS", 15, "bold"),
    background="#FF7900",
    foreground="white",
)
button.config()
button.place(relx=0.8, rely=0.92)


window.mainloop()
