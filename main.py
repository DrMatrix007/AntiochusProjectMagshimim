from ctypes import c_bool, c_float
from typing import Text
import compile_c_code
import tkinter
import re

game = compile_c_code.compile_c_file("./game.c")

game.checkIfAllAllowedDigitsRepeatAtLeastOnce.restype = c_bool 
game.getDoesShowGuessesLeft.restype = c_bool

class GetLevel(tkinter.Frame):
    def __init__(self,master):
        super().__init__(master,padx=20,pady=20)
        
        self.final_code = game.generateCode()
        # self.b = tkinter.Button(self,text="press this",command=self.next)
        # self.b.grid()

        self.easyButton = tkinter.Button(self,text="Easy",padx=10,command=lambda:self.next(1))
        self.mediumButton = tkinter.Button(self,text="Medium",padx=10,command=lambda:self.next(2))
        self.hardButton = tkinter.Button(self,text="Hard",padx=10,command=lambda:self.next(3))
        self.crazyButton = tkinter.Button(self,text="Crazy",padx=10,command=lambda:self.next(4))

        self.easyButton .grid(row=0,column=0)
        self.mediumButton.grid(row=0,column=1)
        self.hardButton .grid(row=0,column=2)
        self.crazyButton .grid(row=0,column=3)

    def next(self,value:int):
        self.destroy()
        GuessLevel(self.master,game.generateCode(),game.getAmountOfGuesses(value),game.getDoesShowGuessesLeft(value),True).grid(sticky="nsew")


        
class GuessLevel(tkinter.Frame):
    def __init__(self,master,code:int,amountOfGuesses:bool,showGuessesLeft:bool,doesShowCode:bool):
        super().__init__(master,padx=20,pady=20,bg="lightblue")
        
        self.guessesLeft = amountOfGuesses
        self.maxGuesses = amountOfGuesses
        self.showCode = doesShowCode
        self.showGuessesLeft = showGuessesLeft

        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(2,weight=1)
        # self.grid_rowconfigure(2,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(2,weight=1)
        


        self.code = code
        self.codeText = tkinter.StringVar()
        
        self.codeText.set((f"code is {self.code};" if self.showCode else "") + (f"Guesses remain: {self.guessesLeft}" if self.showGuessesLeft else "") )


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

        self.listGuesses = tkinter.Listbox(self)
        self.listGuesses.grid(column=2,row=0,rowspan=1,columnspan=1,sticky="nsew")
    def check_input(self) -> tuple[bool,int]:

        value = self.inputArea.get()
        if(bool(re.fullmatch("[1-6]{4}", value))):
            if(game.checkIfAllAllowedDigitsRepeatAtLeastOnce(int(value))):
                return True,int(value)

        return False,0
    def analyze_data(self):
        isGood,guess = self.check_input()
        if(isGood):
            hits = game.countHits(self.code,guess)
            misses = game.countMiss(self.code,guess)
            self.guessesLeft-=1
            if(hits == 4):
                self.next(True)
            self.responseInputVar.set("")
            self.guessText.set(f"Guess:\nthere are {hits} hits;\nthere are {misses} misses")
            self.listGuesses.insert(self.listGuesses.size(),f"{guess.__str__()}: Hits: {hits}, Misses: {misses}")
            self.codeText.set((f"code is {self.code};" if self.showCode else "") + (f"Guesses remain: {self.guessesLeft}" if self.showGuessesLeft else "") )
            if(self.guessesLeft<=0):
                self.next(False)
        else:
            self.responseInputVar.set("You need to write a 4 digit number,\nwith different digits that are 1-6!")
            self.guessText.set("Guess:")
    def next(self,isSucces:bool):
        self.destroy()
        Ending(self.master,self.code,isSucces,self.guessesLeft,self.maxGuesses).grid(sticky="nsew")


class Ending(tkinter.Frame):
    def __init__(self,master,code:int,isSucces:bool,guessesLeft:int,maxGuesses:int):
        super().__init__(master,padx=20,pady=20)

        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.text = (f"Well done, you found the code!!!!\nThe code: {code}\nYou found it in {guessesLeft} out of {maxGuesses}!" if isSucces 
        else f"Oh no, you didn't found the Code!!!\nThe code was {code}\nYou had {maxGuesses} and didn't found it, better luck next time!!!")
        self.textLabel = tkinter.Label(self,text=self.text)

        self.textLabel.grid(sticky="nsew")

game.setRandomSeed()

root = tkinter.Tk()

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)






frame = GetLevel(root)

frame.grid(sticky="nsew")





root.mainloop()