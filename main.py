#===========================================================================
#=================::ROZWIĄZANE ZADANIA - KEYBOARD RUSH::====================
#===========================================================================

from tkinter import *
from time import sleep
from random import choices
import concurrent.futures
#2.0
from requests import get

# Lista widgetów i prostokątów (przycisków)
widgets = []
rectangles = []

# Okno programu - wywołanie, ustalenie rozdzielczości, ikony
root = Tk()
root.geometry("1200x720+350+100")
root.resizable(False, False)
root.title('Keyboard Rush')
root.iconphoto(False, PhotoImage(file="Images/keyboard.png"))

# Wczytywanie teł
bg = PhotoImage(file="Images/background.png")
endBg = PhotoImage(file='Images/endBackground.png')
menuBg = PhotoImage(file="Images/menuBackground.png")
aboutBg = PhotoImage(file="Images/aboutBackground.png")
errorBg = PhotoImage(file="Images/noinputBackground.png")

# Ustawienia tła
bgCanvas = Canvas(root, width=1200, height=720, highlightthickness=0)
bgCanvas.pack(fill="both", expand=True)

# Wczytywanie plików ze słowami

#==================================================
#=================::ZADANIE 2::====================
#==================================================

####################################################################
source = get('https://www.mit.edu/~ecprice/wordlist.10000').text
easyWords = source.splitlines()
easyWords = [word for word in easyWords if len(word) >= 3 and len(word) <= 7]
####################################################################

with open("mediumFile.txt", "r") as mediumFile:
    wholeText = mediumFile.read()
    mediumWords = list(map(str, wholeText.split()))

with open("hardFile.txt", "r") as hardFile:
    wholeText = hardFile.read()
    hardWords = list(map(str, wholeText.split()))


def menu(*args):
    clearWidgets()
    clearRectangles()

    global stateTimer
    stateTimer = 0

    # Ustawienie tła
    bgCanvas.create_image(0, 0, image=menuBg, anchor="nw")

    # Współrzędne prostokątów (służących jako przyciski)
    easyRect = bgCanvas.create_rectangle((170, 350, 420, 560), fill="", outline="")
    mediumRect = bgCanvas.create_rectangle((470, 350, 720, 560), fill="", outline="")
    hardRect = bgCanvas.create_rectangle((780, 350, 1030, 560), fill="", outline="")
    aboutRect = bgCanvas.create_rectangle((1125, 650, 1190, 710), fill="", outline="")

    # ==================================================
    # =================::ZADANIE 1::====================
    # ==================================================

    # 1.1
    exitRect = bgCanvas.create_rectangle((1125, 10, 1190, 40), fill="", outline="")

    # Przypisanie funkcji dla przycisków
    bgCanvas.tag_bind(easyRect, '<ButtonPress-1>', easyLevel)
    bgCanvas.tag_bind(mediumRect, '<ButtonPress-1>', mediumLevel)
    bgCanvas.tag_bind(hardRect, '<ButtonPress-1>', hardLevel)
    # 1.2
    bgCanvas.tag_bind(exitRect, '<ButtonPress-1>', exit)
    bgCanvas.tag_bind(aboutRect, '<ButtonPress-1>', about)

    # Dodanie przycisków do listy
    rectangles.append(easyRect)
    rectangles.append(mediumRect)
    rectangles.append(hardRect)
    # 1.3
    rectangles.append(exitRect)
    rectangles.append(aboutRect)


def easyLevel(event):
    global chosenWords, level
    level = 1
    # Wczytanie 20 słów do zmiennej
    chosenWords = choices(easyWords, k=20)
    game()


def mediumLevel(event):
    global chosenWords, level
    level = 2
    # Wczytanie 20 słów do zmiennej
    chosenWords = choices(mediumWords, k=20)
    game()


def hardLevel(event):
    global chosenWords, level
    level = 3
    # Wczytanie 20 słów do zmiennej
    chosenWords = choices(hardWords, k=20)
    game()


def game():
    clearRectangles()

    global inputbox, timerbox, textbox, stateTimer, inputWordlist, chosenWords, correctWords, incorrectWords, counter, startIndex, characters

    counter = 0
    startIndex = 0
    stateTimer = 0
    correctWords = 0
    incorrectWords = 0
    characters = 0
    inputWordlist = []

    bgCanvas.create_image(0, 0, image=bg, anchor="nw")

    returnRect = bgCanvas.create_rectangle((1125, 650, 1190, 710), fill="", outline="")
    rectangles.append(returnRect)
    bgCanvas.tag_bind(returnRect, '<ButtonPress-1>', menu)

    root.bind('<Key>', keyPressed)

    # Timer, ustawienia
    timerFrame = Frame(bgCanvas, height=50, width=100, bg='lavender blush', highlightbackground="plum2",
                       highlightcolor="plum2",
                       highlightthickness=2)
    timerFrame.place(x=550, y=250)
    timerbox = Message(timerFrame, bg='lavender blush', fg='gray49', font="Corbel 18", text='{:02d}:00'.format(1),
                       width=100)
    timerbox.place(relheight=1, relwidth=1)

    # Frame ze słowami do przepisania
    textFrame = Frame(bgCanvas, height=150, width=460, bg='lavender blush', highlightbackground="plum2",
                      highlightcolor="plum2",
                      highlightthickness=2)
    textFrame.place(x=380, y=340)
    textbox = Text(textFrame, bg='lavender blush', fg='snow4', bd='0.8', font="Corbel 18", width=455, borderwidth="0",
                   wrap='word')
    textbox.insert(INSERT, chosenWords)
    textbox['state'] = 'disabled'

    # Wyśrodkowanie tekstu w oknie (ale nie działa:--D)
    textbox.tag_configure("center", justify="center")
    textbox.insert("1.0", "")
    textbox.tag_add("center", "1.0", "end")
    textbox.pack()
    textbox.place(relwidth=1, relheight=1)

    # Frame do wpisywania słów
    inputFrame = Frame(bgCanvas, height=35, width=400, bg='green', highlightbackground="light blue",
                       highlightcolor="light blue", highlightthickness=2)
    inputFrame.place(x=410, y=520)
    inputbox = Text(inputFrame, font="Corbel 18", fg='gray68', height=35, width=400, bg='gray99', borderwidth="0")
    inputbox.tag_configure("center", justify="center")
    inputbox.insert("1.0", "")
    inputbox.tag_add("center", "1.0", "end")
    inputbox.pack()
    inputbox.place(relheight=1, relwidth=1)

    # Wrzucenie powyższych frameów do listy widgets
    widgets.append(textFrame)
    widgets.append(timerFrame)
    widgets.append(timerbox)
    widgets.append(textbox)
    widgets.append(inputFrame)
    widgets.append(inputbox)


def keyPressed(key):
    global chosenWords, stateTimer, startIndex, correctWords, counter, incorrectWords, characters

    # Obsługa wątku
    concurrent.futures.ThreadPoolExecutor().submit(timer, stateTimer, 60)
    stateTimer = 1

    if key.keysym == 'space' and not (inputbox.get('1.0', 'end-1c').isspace()):

        characters += len(chosenWords[0])
        endIndex = startIndex + len(chosenWords[0])
        inputWordlist.insert(0, inputbox.get('1.0', 'end-1c').strip())
        inputbox.delete('1.0', END)
        textbox.tag_add('highlight_correct_' + str(counter), '1.' + str(startIndex), '1.' + str(endIndex))
        textbox.tag_add('highlight_wrong_' + str(counter), '1.' + str(startIndex), '1.' + str(endIndex))

        try:
            if inputWordlist[0] == chosenWords[chosenWords.index(inputWordlist[0])]:
                correctWords += 1
                textbox.tag_config('highlight_correct_' + str(counter), foreground='CadetBlue3')
        except:
            textbox.tag_config('highlight_wrong_' + str(counter), foreground='pale violet red')
            incorrectWords += 1

        startIndex = startIndex + len(chosenWords[0]) + 1
        chosenWords.pop(0)
        counter += 1

        if len(inputWordlist) == 20:
            inputWordlist.clear()
            textbox['state'] = 'normal'
            textbox.delete('1.0', END)

            if (level == 1):
                chosenWords = choices(easyWords, k=20)
            elif (level == 2):
                chosenWords = choices(mediumWords, k=20)
            else:
                chosenWords = choices(hardWords, k=20)

            textbox.insert(INSERT, chosenWords)
            textbox['state'] = 'disabled'
            startIndex = 0


# Usuwanie widgetów
def clearWidgets():
    for widget in widgets:
        widget.destroy()
    widgets.clear()


# Usuwanie buttonów (prostokątów)
def clearRectangles():
    for rectangle in rectangles:
        bgCanvas.delete(rectangle)


def end():
    clearWidgets()

    bgCanvas.create_image(0, 0, image=endBg, anchor="nw")

    cpmBox = bgCanvas.create_text(492, 350, text='', font="Helvetica 30 bold", fill='PaleTurquoise4')
    wpmBox = bgCanvas.create_text(710, 350, text='', font="Helvetica 30 bold", fill='PaleTurquoise4')
    accBox = bgCanvas.create_text(603, 474, text='', font="Helvetica 30 bold", fill='PaleTurquoise4')

    # Tworzenie i obsługa przycisków
    rerunRect = bgCanvas.create_rectangle((442, 665, 512, 590), fill="", outline="")
    homeRect = bgCanvas.create_rectangle((552, 674, 645, 580), fill="", outline="")
    exitRect = bgCanvas.create_rectangle((682, 665, 749, 590), fill="", outline="")

    bgCanvas.tag_bind(rerunRect, '<ButtonPress-1>', easyLevel)
    bgCanvas.tag_bind(homeRect, '<ButtonPress-1>', menu)
    bgCanvas.tag_bind(exitRect, '<ButtonPress-1>', exit)

    # Wyliczanie i wypisanie statystyk
    wpm = characters / 5
    total = correctWords + incorrectWords

    if characters != 0:
        acc = (correctWords / total) * 100
        cpmBox = bgCanvas.create_text(492, 350, text=f'{characters}', font="Helvetica 30 bold", fill='PaleTurquoise4')
        wpmBox = bgCanvas.create_text(710, 350, text=f'{round(wpm)}', font="Helvetica 30 bold", fill='PaleTurquoise4')
        accBox = bgCanvas.create_text(603, 474, text=f'{round(acc)}%', font="Helvetica 30 bold", fill='PaleTurquoise4')
    else:
        bgCanvas.create_image(0, 0, image=errorBg, anchor="nw")
        cpmBox.delete()
        wpmBox.delete()
        accBox.delete()

    # Uzależnienie przycisku rerun od poziomu trudności
    if (level == 1):
        bgCanvas.tag_bind(rerunRect, '<ButtonPress-1>', easyLevel)
    elif (level == 2):
        bgCanvas.tag_bind(rerunRect, '<ButtonPress-1>', mediumLevel)
    else:
        bgCanvas.tag_bind(rerunRect, '<ButtonPress-1>', hardLevel)

    # Wpisanie obiektów do listy
    rectangles.append(wpmBox)
    rectangles.append(cpmBox)
    rectangles.append(accBox)
    rectangles.append(rerunRect)
    rectangles.append(homeRect)
    rectangles.append(exitRect)


def timer(state, t):
    if state != 1:
        while t:
            mins, secs = divmod(t, 60)
            timerbox['text'] = '{:02d}:{:02d}'.format(mins, secs)
            sleep(1)
            t -= 1
        end()

# Funkcja exit, potrzebna do Zadania 1
def exit(event):
    root.quit()


def about(event):
    clearRectangles()
    bgCanvas.create_image(0, 0, image=aboutBg, anchor="nw")
    returnRect = bgCanvas.create_rectangle((1125, 650, 1190, 710), fill="", outline="")
    rectangles.append(returnRect)
    bgCanvas.tag_bind(returnRect, '<ButtonPress-1>', menu)


menu()
root.mainloop()