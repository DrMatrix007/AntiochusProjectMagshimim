from ctypes import c_float
from typing import Text
import compile_c_code
import tkinter

game = compile_c_code.compile_c_file("./game.c")




class GetLevel(tkinter.Frame):
    def __init__(self,master):
        super().__init__(master,padx=20,pady=20)
        
        self.final_code = game.generateCode()
        self.b = tkinter.Button(self,text="press this",command=self.next)
        self.b.grid()
    def next(self):
        self.destroy()
        guess = GuessLevel(self.master,game.generateCode())
        guess.grid(sticky="nsew")

        
class GuessLevel(tkinter.Frame):
    def __init__(self,master,code:int):
        super().__init__(master,padx=20,pady=20,bg="lightblue")
        
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)


        self.code = code
        self.text = tkinter.Label(self,text=f"code is {code}")
        self.text.grid(sticky="nsew")
        
        
        self.inputArea = tkinter.Entry(self)
        self.inputArea.grid(column=0,row=1,sticky="nsew")


        self.responseInputVar = tkinter.StringVar()
        self.responseInput = tkinter.Label(self,textvariable=self.responseInputVar)
        self.responseInput.grid(column=1,row=1,sticky="nsew")

        self.submitInputButton = tkinter.Button(self,text="submit",command=self.check_input)
        self.submitInputButton.grid(column=0,row=2,sticky="nsew")
        
        self.guessText = tkinter.StringVar()
        self.guessText.set("Guess: ")
        self.guessLabel = tkinter.Label(self,textvariable=self.guessText)
        self.guessLabel.grid(column=0,row=3,sticky="nsew")
    def check_input(self):
        if(re.match("[1-6]{4}", self.inputArea.get())):
            self.responseInputVar.set("")
        else:
            self.responseInputVar.set("badddd")
            


game.setRandomSeed()

root = tkinter.Tk()

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)






frame = GetLevel(root)

frame.grid(sticky="nsew")





root.mainloop()