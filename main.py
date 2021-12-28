from ctypes import c_float
import compile_c_code
import tkinter as tk




game = compile_c_code.compile_c_file("./game.c")

root = tk.Tk()


frame = tk.Frame(root,padx=10,pady=10)

frame.grid()

tk.Button(frame,text="nice", command=frame.destroy).grid(column=0,row=0)


game.test()

print(10)

root.mainloop()