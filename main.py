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
        guess.grid()
        
class GuessLevel(tkinter.Frame):
    def __init__(self,master,code:int):
        super().__init__(master)
        self.code = code
        self.text = tkinter.Label(self,text=f"code is {code}")
        self.text.grid()
        


game.setRandomSeed()

root = tkinter.Tk()


frame = GetLevel(root)

frame.grid()









root.mainloop()