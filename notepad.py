from tkinter import *
from tkinter import font
from pickle import dump, load
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askokcancel, showinfo, showwarning
import tkinter.colorchooser as colorchooser
from datetime import datetime
from os import path as os_path
# import tkinter.simpledialog as simpledialog
# import tkinter.ttk as ttk

# Initial variables
np_background_color = "#fff"
np_title = "Untitled - NotepadX"
np_font_family = "Lucida Console"
np_font_size = 10
np_font_style = "normal"
np_theme = "light"
np_text_background = "#fff"
np_text_foreground = "#000"
np_database_file = "npx_files/data.notepadx"

def writeDatabase(key, value):
    theFile = open(np_database_file, "rb")
    dataFile = load(theFile)
    theFile.close()
    dataFile[key] = value
    with open(np_database_file, "wb") as f:
        dump(dataFile, f)

def readDatabase(key):
    theFile = open(np_database_file, "rb")
    dataFile = load(theFile)
    theFile.close()
    return dataFile[key]


def changeFont(font):
    writeDatabase("font_family", font)
    textarea.config(font=(readDatabase("font_family"), readDatabase("font_size"), readDatabase("font_style")))

def changeStyle(font):
    writeDatabase("font_style", font)
    textarea.config(font=(readDatabase("font_family"), readDatabase("font_size"), readDatabase("font_style")))


def changeSize(font):
    writeDatabase("font_size", font)
    textarea.config(font=(readDatabase("font_family"), readDatabase("font_size"), readDatabase("font_style")))

def resetSize(element):
    writeDatabase("font_size", "10")
    textarea.config(font=(readDatabase("font_family"), readDatabase("font_size"), readDatabase("font_style")))
    element.set(10)

def textHighlighter(stringToFind):
    global textarea
    idx = "1.0"
    if stringToFind.get() != "":
        while 1:
            idx = textarea.search(stringToFind.get(), idx, nocase=1, stopindex=END)
            if not idx: break
            lastidx = '%s+%dc' % (idx, len(stringToFind.get()))
            textarea.tag_add('found', idx, lastidx)
            idx = lastidx

        textarea.tag_config('found', foreground="black", background="yellow")

def textReplacer(text, replace):
    global textarea, fileSaved
    idx = "1.0"
    # print(text.get(), replace.get())
    if text.get() != "":
        while 1:
            idx = textarea.search(text.get(), idx, nocase=1, stopindex=END)
            if not idx: break
            lastidx = '%s+%dc' % (idx, len(text.get()))
            # textarea.tag_add('found', idx, lastidx)
            textarea.replace(idx, lastidx, replace.get())
            idx = lastidx
    fileSaved = False
    now_title = notepad.title()
    if not notepad.title().startswith("*"):
        notepad.title("*" + now_title)

    # textarea.tag_config('found', foreground="black", background="yellow")

def quitNewWindow(givenWindow):
    global textarea
    textarea.tag_delete('found')
    givenWindow.destroy()
    

def findText():
    newWindow = Toplevel(notepad)
    newWindow.title("Find text")
    newWindow.config(background="#f8f8f8")
    newWindow.geometry("200x92")
    newWindow.resizable(0, 0)
    newWindow.attributes('-toolwindow', True)
    stringToFind = StringVar()
    userInput = Entry(newWindow, textvariable=stringToFind)
    userInput.pack(pady=10, padx=10, fill=X)
    userInput.focus_set()

    Button(newWindow, text="Find", command=lambda: textHighlighter(stringToFind)).pack()
    newWindow.protocol("WM_DELETE_WINDOW", lambda: quitNewWindow(newWindow))


def replaceText():
    replacerWindow = Toplevel(notepad)
    replacerWindow.attributes("-toolwindow", True)
    replacerWindow.title("Replace text")
    replacerWindow.geometry("230x120")
    replacerWindow.resizable(0, 0)
    textVar = StringVar()
    replaceVar = StringVar()
    Label(replacerWindow, text="Find what:").grid(row=1, column=1, pady=10)
    textEntry = Entry(replacerWindow, textvariable=textVar)
    textEntry.grid(row=1, column=2)
    textEntry.focus_set()

    Label(replacerWindow, text="Replace with:").grid(row=2, column=1)
    Entry(replacerWindow, textvariable=replaceVar).grid(row=2, column=2)
    Button(replacerWindow, text="Replace All", command=lambda: textReplacer(textVar, replaceVar)).grid(row=4, column=1, pady=20, padx=10)
    






def colorChooser():
    chosenColor = colorchooser.askcolor()
    writeDatabase("font_color", chosenColor[1])
    textarea.config(fg=chosenColor[1])



def fontChooser():
    fontChooser = Toplevel(notepad)
    fontChooser.title("Choose font")
    fontChooser.config(background="#f8f8f8")
    fontChooser.geometry("160x250")
    fontChooser.attributes('-toolwindow', True)
    fontChooser.resizable(0, 0)
    Label(fontChooser, text="Font Family:").pack()
    font_families = list(font.families())
    font_families.sort()
    lbx = Listbox(fontChooser, selectmode=BROWSE)
    lbx.pack()
    for i in font_families:
        lbx.insert(END, i)
    # lbx.bind("<ListboxSelect>", command=lambda: changeFont(lbx.get(ACTIVE)))
    Button(fontChooser, text="Ok", command=lambda: changeFont(lbx.get(ACTIVE)), padx=12).pack(side=RIGHT, padx=20)


def styleChooser():
    fontChooser = Toplevel(notepad)
    fontChooser.title("Choose style")
    fontChooser.config(background="#f8f8f8")
    fontChooser.geometry("160x250")
    fontChooser.resizable(0, 0)
    fontChooser.attributes('-toolwindow', True)
    Label(fontChooser, text="Font Style:").pack()
    font_styles = ["normal", "bold", "italic", "underline"]
    # font_styles.sort()
    lbx = Listbox(fontChooser, selectmode=BROWSE)
    lbx.pack()
    for i in font_styles:
        lbx.insert(END, i)
    # lbx.bind("<ListboxSelect>", command=lambda: changeFont(lbx.get(ACTIVE)))
    Button(fontChooser, text="Ok", command=lambda: changeStyle(lbx.get(ACTIVE)), padx=12).pack(side=RIGHT, padx=20)

def sizeChooser():
    fontChooser = Toplevel(notepad)
    fontChooser.title("Choose size")
    fontChooser.config(background="#eee")
    fontChooser.geometry("150x120")
    fontChooser.resizable(0, 0)
    fontChooser.attributes('-toolwindow', True)
    Label(fontChooser, text="Font Size:").pack()
    slider = Scale(fontChooser, orient=HORIZONTAL, from_=5, to=120)
    slider.set(int(readDatabase("font_size")))
    slider.pack()
    # for i in range(5, 100):
    #     lbx.insert(END, i)
    # lbx.bind("<ListboxSelect>", command=lambda: changeFont(lbx.get(ACTIVE)))
    Button(fontChooser, text="Ok", command=lambda: changeSize(slider.get()), padx=12).pack(side=RIGHT, padx=10)
    Button(fontChooser, text="Reset", command=lambda: resetSize(slider), padx=12).pack(side=RIGHT, padx=10)

def aboutNotepadX():
    showinfo(title="About NotepadX", message="Welcome to NotepadX. This is an open source Note application by Pritam. You can view, edit, save files through NotepadX.")

def warningNotepadX():
    showwarning(title="Warning!", message="This Note application uses some additional files from the 'npx_files' folder. Please don't remove anything from the folder.")


def cutText():
    textarea.event_generate("<<Cut>>")

def copyText():
    textarea.event_generate("<<Copy>>")

def pasteText():
    textarea.event_generate("<<Paste>>")



def wordWrap():
    global horizontalScrollbar
    if readDatabase("word_wrap") == "none":
        writeDatabase("word_wrap", "word")
        textarea.config(wrap="word")
        horizontalScrollbar.pack_forget()
    else:
        writeDatabase("word_wrap", "none")
        textarea.config(wrap="none")
        horizontalScrollbar.pack(fill=X, side=BOTTOM)


def insertDateTime():
    global textarea, fileSaved
    date = datetime.now()
    currentDate = date.strftime("%I:%M %p %d/%m/%Y")
    textarea.insert(END, currentDate)
    fileSaved = False
    currentTitle = notepad.title()
    if currentTitle.startswith("*"):
        return False
    elif not currentTitle.startswith("*"):
        notepad.title("*" + currentTitle)


fileSaved = True
def writtenText(event):
    global textarea, fileSaved
    kc = event.keycode
    if kc not in [16, 17, 18, 19, 20, 27, 33, 34, 34, 35, 36, 37, 38, 39, 40, 44, 25, 91, 92, 93]:
        starredNotepadTitle = "*" + notepad.title()
        if notepad.title().startswith("*"):
            return False
        elif textarea.get(1.1, END) != readDatabase("written_text"):
            notepad.title(starredNotepadTitle)
            fileSaved = False



        
def saveFile():
    global textarea, fileSaved
    replacedTitle = notepad.title().replace("*", "")
    writeDatabase("written_text", textarea.get(1.0, END))
    filePath = readDatabase("working_file_path")
    if filePath == "none" or filePath == "":
        filePath = asksaveasfilename(initialfile="*.txt", defaultextension=".txt", filetypes=(('text files', 'txt'),))
        writeDatabase("working_file_path", filePath)

    with open(filePath, "w") as f:
        f.write(textarea.get(1.0, END))

    notepad.title(replacedTitle)
    fileSaved = True
    notepad.title(os_path.basename(filePath) + " - NotepadX")

def saveFileAs():
    global textarea, fileSaved

    filePath = asksaveasfilename(initialfile="*.txt", defaultextension=".txt", filetypes=(('text files', 'txt'),))
    if filePath:
        with open(filePath, "w") as f:
            f.write(textarea.get(1.0, END))

        writeDatabase("working_file_path", filePath)
        newNotePadTitle = os_path.basename(filePath) + " - NotepadX"
        notepad.title(newNotePadTitle)
        fileSaved = True



def openFile():
    global textarea, fileSaved
    filePath = askopenfilename(defaultextension=".txt")
    # print(filePath)

    with open(filePath, "r") as f:
        textarea.delete(1.0, END)
        textData = f.read()
        textarea.insert(END, textData)
        writeDatabase("written_text", textData)


    writeDatabase("working_file_path", os_path.basename(filePath))
    notepad.title(os_path.basename(filePath) + " - NotepadX")
    fileSaved = True



def newFile():
    global textarea, fileSaved
    if not fileSaved:
        a = askokcancel(title="New file", message="Create new file? All the changes may not be saved.")
    if fileSaved or a:
        writeDatabase("written_text", "")
        textarea.delete(1.0, END)
        replacedTitle = notepad.title().replace("*", "")
        notepad.title(replacedTitle)
        fileSaved = True
        writeDatabase("working_file_path", "none")
        notepad.title(np_title)

def quitApp():
    if fileSaved:
        notepad.destroy()
    else:
        if askokcancel(title="Quit NotepadX?", message="Changes you made may not be saved"):
            notepad.destroy()
    
def resetApp():
    warn = askokcancel(title="Reset NotepadX?", message="Do you want to reset the application? All the customizations will be erased.")
    # print(warn)
    if warn:
        data = {
            "working_file_path": "none",
            "font_family": "Lucida Console",
            "font_size": 10,
            "font_style": "normal",
            "written_text": "",
            "font_color": "#000",
            "word_wrap": "word"
        }
        with open(np_database_file, "wb") as f:
            dump(data, f)
        showinfo(title="NodepadX", message="The application has been reset successfully.")
        notepad.destroy()

def keyboardShortcuts():
    showinfo(title="Keyboard Shortcuts", message='''
    Keyboard Shortcuts for NotepadX:\n
    1. Ctrl+N: New File
    2. Ctrl+O: Open File
    3. Ctrl+S: Save File
    4. Ctrl+Shift+S: Save as new file
    5. Ctrl+F: Find
    6. Ctrl+H: Replace
    7. Ctrl+Alt+T: Insert Date/Time
    8. Ctrl+Alt+W: Toggle Word Wrap
    9. Ctrl+Alt+C: Change Text Color
    10. Ctrl+Alt+F: Change Font Family
    11. Ctrl+Alt+Z: Change Font Size
    12. Ctrl+Alt+Y: Change Font Style
    13. Ctrl+K: Open Keyboard Shortcuts
    14. Ctrl+Alt+R: Reset NotepadX
    ''')

def ctrlS(event):
    saveFile()

def ctrlShiftS(event):
    saveFileAs()

def ctrlN(event):
    newFile()

def ctrlO(event):
    openFile()

def ctrlF(event):
    findText()

def ctrlH(event):
    replaceText()

def ctrlAltT(event):
    insertDateTime()

def ctrlAltC(event):
    colorChooser()

def ctrlAltW(event):
    wordWrap()

def ctrlAltF(event):
    fontChooser()

def ctrlAltZ(event):
    sizeChooser()

def ctrlAltY(event):
    styleChooser()

def ctrlK(event):
    keyboardShortcuts()

def ctrlAltR(event):
    resetApp()

# def ctrl




notepad = Tk()
ab_title = readDatabase("working_file_path")
if ab_title== "none" or ab_title == "":
    notepad.title(np_title)
else:
    notepad.title(os_path.basename(ab_title) + " - NotepadX")
notepad.geometry("878x488")
notepad.configure(background="#fff")
notepad.wm_iconbitmap("npx_files/npx.ico")

# Creating the menu
mainMenu = Menu(notepad)

# File menu
fileMenu = Menu(mainMenu, tearoff=False)
fileMenu.add_command(label="New", command=newFile)
fileMenu.add_command(label="Open", command=openFile)
fileMenu.add_command(label="Save", command=saveFile)
fileMenu.add_command(label="Save as..", command=saveFileAs)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=quitApp)
mainMenu.add_cascade(label="File", menu=fileMenu)

# Edit menu
editMenu = Menu(mainMenu, tearoff=False)
editMenu.add_command(label="Cut", command=cutText)
editMenu.add_command(label="Copy", command=copyText)
editMenu.add_command(label="Paste", command=pasteText)
editMenu.add_separator()
editMenu.add_command(label="Find", command=findText)
editMenu.add_command(label="Replace", command=replaceText)
editMenu.add_separator()
editMenu.add_command(label="Time/Date", command=insertDateTime)
mainMenu.add_cascade(label="Edit", menu=editMenu)


# Format menu
formatMenu = Menu(notepad, tearoff=False)
formatMenu.add_command(label="Word wrap", command=wordWrap)
formatMenu.add_separator()
formatMenu.add_command(label="Text Color", command=colorChooser)
formatMenu.add_command(label="Font Family", command=fontChooser)
formatMenu.add_command(label="Font Size", command=sizeChooser)
formatMenu.add_command(label="Font Style", command=styleChooser)
mainMenu.add_cascade(label="Format", menu=formatMenu)


# Help menu
helpMenu = Menu(notepad, tearoff=False)
helpMenu.add_command(label="About", command=aboutNotepadX)
helpMenu.add_command(label="Warning", command=warningNotepadX)
helpMenu.add_command(label="Keyboard Shortcuts", command=keyboardShortcuts)
helpMenu.add_command(label="Reset the app", command=resetApp)

mainMenu.add_cascade(label="Help", menu=helpMenu)

notepad.config(menu=mainMenu)


# textarea = scrolledText.ScrolledText(notepad, width=878, height=488, wrap=NONE, borderwidth=0)
# textarea.pack()

textarea = Text(notepad, undo=True, maxundo=-1, font=(readDatabase("font_family"), readDatabase("font_size"), readDatabase("font_style")), wrap=readDatabase("word_wrap"),
                borderwidth=0, background=np_text_background, fg=readDatabase("font_color"))

textarea.pack(fill=BOTH, expand=True)
textarea.insert(END, readDatabase("written_text"))
textarea.focus_set()
textarea.bind("<KeyPress>", writtenText)
textarea.bind("<Control-s>", ctrlS)
textarea.bind("<Control-Shift-S>", ctrlShiftS)
textarea.bind("<Control-n>", ctrlN)
textarea.bind("<Control-o>", ctrlO)
textarea.bind("<Control-f>", ctrlF)
textarea.bind("<Control-h>", ctrlH)
textarea.bind("<Control-Alt-t>", ctrlAltT)
textarea.bind("<Control-Alt-c>", ctrlAltC)
textarea.bind("<Control-Alt-w>", ctrlAltW)
textarea.bind("<Control-Alt-f>", ctrlAltF)
textarea.bind("<Control-Alt-z>", ctrlAltZ)
textarea.bind("<Control-Alt-y>", ctrlAltY)
textarea.bind("<Control-k>", ctrlK)
textarea.bind("<Control-Alt-r>", ctrlAltR)

# textarea.config(wrap=NONE) # Word wrap disabled


# Adding vertical scrollbar
verticalScrollbar = Scrollbar(textarea, cursor="arrow")
verticalScrollbar.config(command=textarea.yview)
textarea.config(yscrollcommand=verticalScrollbar.set)
verticalScrollbar.pack(fill=Y, side=RIGHT)

# Adding horizontal scrollbar
horizontalScrollbar = Scrollbar(textarea, cursor="arrow", orient="horizontal")
horizontalScrollbar.config(command=textarea.xview)
textarea.config(xscrollcommand=horizontalScrollbar.set)
if readDatabase("word_wrap") != "word":
    horizontalScrollbar.pack(fill=X, side=BOTTOM)

notepad.protocol("WM_DELETE_WINDOW", quitApp)
notepad.mainloop()
