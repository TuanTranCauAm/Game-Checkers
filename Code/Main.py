import tkinter as tk
from PieceOperation import *
from PlayerVsBot import *
from PlayerVsPlayer import *

class Game (tk.Frame):
    STICKY = tk.N + tk.S + tk.E + tk.W

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.gameStartupDialog()


    def vsCOM(self):
        self.label1.grid_forget()
        self.label2.grid_forget()
        self.okButton1.grid_forget()
        self.okButton2.grid_forget()
        self.okButton3.grid_forget()
        app = COMPUTER(master=self)
        app.mainloop()
    
    def vsPLAYER(self):
        self.label1.grid_forget()
        self.label2.grid_forget()
        self.okButton1.grid_forget()
        self.okButton2.grid_forget()
        self.okButton3.grid_forget()
        app = PLAYER(master=self)
        app.mainloop()


    def gameStartupDialog(self):

        self.start = tk.Frame(self)
        self.start.grid(row=0)

    
        self.label1 = tk.Label(self, text="\n\t\t\tGAME CHECKERS\t\t\t\t\n", font=2000)
        self.label1.grid(row=1, column=0)

        #self.label1 = tk.Label(self.start, text="\n\t\tGAME CHECKERS           \n", font=2000)
        
        self.okButton1 = tk.Button(self, text="Vs COMPUTER", fg="green", 
                                    border=10,height=5, width=30, font=50,
                                    command=self.vsCOM)
        self.okButton1.grid(row=3, column = 0)
        self.okButton2 = tk.Button(self, text="Vs PLAYER", fg="blue", 
                                    border=10,height=5, width=30, font=50,
                                    command=self.vsPLAYER)
        self.okButton2.grid(row=4, column = 0)
        self.okButton3 = tk.Button(self, text="QUIT GAME", fg="red", 
                                    border=10,height=5, width=30, font=50,
                                    command=self.quit)
        self.okButton3.grid(row=5, column = 0)
        self.label2 = tk.Label(text="\t\t", font=2000)
        self.label2.grid(row=5, column=0)
        

    
def main():
    root = tk.Tk()
    root.geometry("562x750")
    img = tk.PhotoImage(file="Image/background.png")
    label1 = tk.Label( root, image = img)
    label1.place(x = 0, y = 0)
    app = Game(master=root)
    app.mainloop()

main()