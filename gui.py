from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as box
from assembly import *

fileptr = [False, 0]

class MainWIndow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background='#eed')
        self.parent = parent
        self.initUI()
        self.initQuitButton()
        self.initFileButton()
        self.initInputText()
        self.initOutputText()
        self.initLabels()
        self.initAssembleButton()
        self.initInfoLabel()

    def initUI(self):
        self.parent.title('Pass-1 Assembler')
        self.pack(fill=BOTH, expand=1)
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        self.parent.geometry('800x600+%d+%d' % ((sw - 800) / 2, (sh - 600) / 2))

    def initQuitButton(self):
        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.place(relx=0.8, rely=0.9, relwidth=0.1)

    def initAssembleButton(self):
        genButton = Button(self, text="Assemble", command=self.invokeAssemble)
        genButton.place(relx=0.32, rely=0.9, relwidth=0.2)

    def initFileButton(self):
        fileButton = Button(self, text="Select Input", command=self.onOpen)
        fileButton.place(relx=0.1, rely=0.9, relwidth=0.2)

    def initInputText(self, textParam=''):
        self.inputText = Text(self)
        self.inputText.place(relx=0.1, rely=0.07, relwidth=0.52, relheight=0.35)
        self.inputText.insert(index=INSERT, chars=textParam)

    def initLabels(self):
        l1 = Label(self, text="Input Assembly Source", background='#eed')
        l2 = Label(self, text="Output Machine Code", background='#eed')
        l1.place(relx=0.2, rely=0.02, relwidth=0.3)
        l2.place(relx=0.2, rely=0.45, relwidth=0.3)

    def initInfoLabel(self, textParam="Information: ", flag=1):
        if flag is 1:
            l3 = Label(self, text=textParam, background='#2ed')
        else:
            l3 = Label(self, text=textParam, background='#a77')
        l3.place(relx=0.65, rely=0.07, relwidth=0.32)

    def initOutputText(self, textParam=''):
        self.outputText = Text(self)
        self.outputText.place(relx=0.1, rely=0.5, relwidth=0.52, relheight=0.35)
        self.outputText.insert(index=INSERT, chars=textParam)

    def onOpen(self):
        filename = filedialog.askopenfilename()
        if filename is '':
            box.showinfo("Info", "You did not select a file.")
        else:
            global fileptr
            fileptr[0] = True
            fileptr[1] = filename
            f = open(fileptr[1], 'r')
            self.text = f.read()
            self.text = self.text.split('\n')
            displayText = ''
            for i in range(len(self.text)):
                displayText += (str(i + 1) + ' ' + self.text[i] + '\n')
            self.initInputText(displayText)

    def invokeAssemble(self):
        # call to assembly code module
        ## print("Call") #testing #success
        lineNo, assembledCode, errorList, errorFlag = assemble(
            self.inputText.get('0.0', END))  # someTuple returns the information which is passed onto initInfoLabel()
        if errorFlag is False:
            outputText = ''
            # print('assembledCode:', assembledCode)
            for i in range(len(assembledCode)):
                outputText += (str(i + 1) + ' ' + assembledCode[i] + '\n')
                # print('outputText:', outputText)
            self.initOutputText(outputText)
            infoString = 'Success!\n0 Errors!\nThere are\n' + str(
                lineNo) + ' lines in the machine code.\nMachine code size is ' + str(
                lineNo * 16) + 'bits.'  # someTuple is processed and converted to a string
            self.initInfoLabel(infoString, flag=1)
        else:
            infoString = str(len(errorList)) + ' Errors.\n'
            for i in errorList:
                ##print(i)
                infoString += ('Error at line: ' + str(i.get('lineNo')) + '\nType: ' + str(i.get('type')) + '\n\n')
            self.initInfoLabel(infoString, flag=0)


def main():
    root = Tk()
    app = MainWIndow(root)
    root.mainloop()


main()
