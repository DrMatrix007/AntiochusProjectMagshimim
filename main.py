from ctypes import c_bool
from os import system
import compile_c_code
import tkinter
import re


# #to hide the console window in production
# win32gui.ShowWindow(win32gui.GetForegroundWindow(),win32con.SW_HIDE)

#import the c binaries
game = compile_c_code.compile_c_file("./game.c")

#setting up the return type of the functions, the defulat is c_int, but if its not, then we get a "garbage" value.
game.checkIfAllAllowedDigitsRepeatAtLeastOnce.restype = c_bool 
game.getDoesShowGuessesLeft.restype = c_bool

class GetLevel(tkinter.Frame):
    def __init__(self,master):
        super().__init__(master,padx=20,pady=20)
        #set the layout
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        self.grid_columnconfigure(3,weight=1)

        #create the code
        self.final_code = game.generateCode()
        
        #the widgets
        self.easyButton = tkinter.Button(self,text="Easy",padx=10,command=lambda:self.next(1))
        self.mediumButton = tkinter.Button(self,text="Medium",padx=10,command=lambda:self.next(2))
        self.hardButton = tkinter.Button(self,text="Hard",padx=10,command=lambda:self.next(3))
        self.crazyButton = tkinter.Button(self,text="Crazy",padx=10,command=lambda:self.next(4))
        

        self.showCodeVar = tkinter.BooleanVar()
        self.showCodeCheckBox = tkinter.Checkbutton(self,text="show code?",variable=self.showCodeVar,)


        self.welcomeLabel = tkinter.Label(self,text = '''The Game Was Created By:\n
Ofri Haviv also known as DrMatrix in 2022 ©


A secret password was chosen to protect the credit card of Pancratius,
the descendant of Antiochus.

Your mission is to stop Pancratius by revealing his secret password.
The rules are as follows:

1. In each round you try to guess the secret password (4 distinct digits)
2. After every guess you'll receive two hints about the password
    HITS:   The number of digits in your guess which were exactly right.
    MISSES: The number of digits in your guess which belongs to
   the password but were miss-placed.
3. If you'll fail to guess the password after a certain number of rounds 
Pancratius will buy all the gifts for Hanukkah!!!
''',justify="left")

        self.welcomeLabel.grid(row=0,column=0,columnspan=4)
        self.easyButton .grid(row=1,column=0)
        self.mediumButton.grid(row=1,column=1)
        self.hardButton .grid(row=1,column=2)
        self.crazyButton .grid(row=1,column=3)

        self.showCodeCheckBox.grid(row=2,columnspan=4,sticky="nsew")
        
        #definitely not a rick roll
        self.definitelyNotARickRollButton = tkinter.Button(self,text="secret feature",command=lambda: system("explorer \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\""))
        self.definitelyNotARickRollButton.grid(row=3,columnspan=4)

    def next(self,value:int):
        #destroy this widget, and adding the next
        self.destroy()
        for i in range(1,5):
            print(game.getAmountOfGuesses(i))
        GuessLevel(self.master,game.generateCode(),game.getAmountOfGuesses(value),game.getDoesShowGuessesLeft(value),self.showCodeVar.get()).grid(sticky="nsew")

class GuessLevel(tkinter.Frame):
    def __init__(self,master,code:int,amountOfGuesses:bool,showGuessesLeft:bool,doesShowCode:bool):
        super().__init__(master,padx=20,pady=20,bg="lightblue")


        #setting up the ui, with the correct functions

        self.guessesLeft = amountOfGuesses
        self.maxGuesses = amountOfGuesses
        self.showCode = doesShowCode
        self.showGuessesLeft = showGuessesLeft

        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(2,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(2,weight=1)
        


        self.code = code
        self.codeText = tkinter.StringVar()
        
        self.codeText.set((f"code is {self.code}\n" if self.showCode else "") + (f"Guesses remain: {self.guessesLeft}" if self.showGuessesLeft else "") )


        self.codeLabel = tkinter.Label(self,textvariable=self.codeText)
        self.codeLabel.grid(sticky="nsew")
        
        
        self.inputArea = tkinter.Entry(self)
        self.inputArea.grid(column=0,row=1,sticky="nsew")


        self.responseInputVar = tkinter.StringVar()
        self.responseInput = tkinter.Label(self,textvariable=self.responseInputVar)
        self.responseInput.grid(column=1,row=1,sticky="nsew")

        self.submitInputButton = tkinter.Button(self,text="submit",command=self.analyze_data)
        self.submitInputButton.grid(column=0,row=2,sticky="nsew")
        
        self.guessText = tkinter.StringVar()
        self.guessText.set("Guess: ")
        self.guessLabel = tkinter.Label(self,textvariable=self.guessText)
        self.guessLabel.grid(column=0,row=3,sticky="nsew")


        self.listGuesses = tkinter.Variable(value= [])
        self.listGuessesBox = tkinter.Listbox(self,listvariable=self.listGuesses)
        self.listGuessesBox.grid(column=2,row=0,rowspan=1,columnspan=1,sticky="nsew")
    def check_input(self) -> tuple[bool,int]:
        #checking for the input for validation
        value = self.inputArea.get()
        if(bool(re.fullmatch("[1-6]{4}", value))):
            if(game.checkIfAllAllowedDigitsRepeatAtLeastOnce(int(value))):
                return True,int(value)

        return False,0
    def analyze_data(self):
        isGood,guess = self.check_input()
        if(isGood):
            #if the input good
            hits = game.countHits(self.code,guess)
            misses = game.countMiss(self.code,guess)
            self.guessesLeft-=1

            self.responseInputVar.set("")
            self.guessText.set(f"Guess:\nthere are {hits} hits\nthere are {misses} misses")
            self.listGuessesBox.insert(self.listGuessesBox.size(),f"{guess.__str__()}: Hits: {hits}, Misses: {misses}")
            self.codeText.set((f"code is {self.code}\n" if self.showCode else "") + (f"Guesses remain: {self.guessesLeft}" if self.showGuessesLeft else "") )
            if(hits == 4):
                self.next(True)
          
            if(self.guessesLeft<=0):
                self.next(False)
        else:
            #if the input ins't valid
            self.responseInputVar.set("You need to write a 4 digit number,\nwith different digits that are 1-6!")
            self.guessText.set("Guess:")
    def next(self,isSucces:bool):
        self.destroy()
        Ending(self.master,self.code,isSucces,self.guessesLeft,self.maxGuesses,self.listGuesses.get()).grid(sticky="nsew")


class Ending(tkinter.Frame):
    def __init__(self,master,code:int,isSucces:bool,guessesLeft:int,maxGuesses:int,guessList:list):
        super().__init__(master,padx=20,pady=20)
        #show the user the code, and extra info about this game.
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.text = (f"Well done, you found the code!!!!\nThe code: {code}\nYou found it in {maxGuesses-guessesLeft} out of {maxGuesses}!" if isSucces 
        else f"Oh no, you didn't found the Code!!!\nThe code was {code}\nYou had {maxGuesses} and didn't found it, better luck next time!!!")
        self.textLabel = tkinter.Label(self,text=self.text)


        self.listbox = tkinter.Listbox(self)
        for i in guessList:
            self.listbox.insert(self.listbox.size(),i)

        self.returnButton = tkinter.Button(self, text="start again",command=lambda:self.restart_game())


        self.textLabel.grid(sticky="nsew")
        self.listbox.grid(column=1,row=0,sticky="nsew")
        self.returnButton.grid(column=0,row=1)
    def restart_game(self):
        self.destroy()
        GetLevel(self.master).grid(sticky="nsew")
        
if __name__ == "__main__":
    game.setRandomSeed()

    root = tkinter.Tk()

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)


    frame = GetLevel(root)

    frame.grid(sticky="nsew")





    root.mainloop()