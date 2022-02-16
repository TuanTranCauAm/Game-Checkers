import tkinter as tk
from PieceOperation import *
from Algorithm import *
from time import time


class COMPUTER (tk.Frame):
    STICKY = tk.N + tk.S + tk.E + tk.W

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.gameStartupDialog()
        self.time1 = 0
        self.time2 = 0
        self.heuristic = 0
        self.namehs = ""

    def gameStartupDialog(self):

        self.start = tk.Frame(self)
        self.start.grid(row=0)

        self.p1Name = tk.StringVar() # Nhập tên người chơi 1(COMPUTER)
        self.p2Name = tk.StringVar() # Nhập tên người chơi 2
        self.heuristic1 = tk.BooleanVar() # Check dùng heuristic 1 không
        self.heuristic2 = tk.BooleanVar() # Check dùng heuristic 2 không
        self.heuristic3 = tk.BooleanVar() # Check dùng heuristic 3 không
        # Tạo giao diện màng hình start

        tk.Label(self.start, text="Choose 1 heuristic in 3 heuristic below to test: ", font=("Helvetica", 18), height=2).grid(
            row=1, column=1)

        self.h1 = tk.Checkbutton(self.start, variable=self.heuristic1)
        self.h1.grid(row = 2, column=0)
        self.h11 = tk.Label(self.start, text="Difference between the number of Pieces\t\t", font=2000)
        self.h11.grid(row = 2, column=1)

        self.h2 = tk.Checkbutton(self.start,variable=self.heuristic2)
        self.h2.grid(row = 3, column=0)
        self.h22 = tk.Label(self.start, text="Number of Pawns and Kings\t\t\t", font=2000)
        self.h22.grid(row = 3, column=1)

        self.h3 = tk.Checkbutton(self.start, variable=self.heuristic3)
        self.h3.grid(row = 4, column=0)
        self.h33 = tk.Label(self.start, text="Difference between value of Pieces\t\t", font=2000)
        self.h33.grid(row = 4, column=1)

        self.h4 = tk.Label(self.start, text=" ", font=2000)
        self.h4.grid(row = 5, column=1)

        self.okButton = tk.Button(self.start, text="START GAME",fg="red", bg="yellow",
                                    border=5,height=1, width=15, font=50,
                                    command=self.beginGame)
        self.okButton.grid(row=6, column = 1)
    
    def draw(self): 
        self.boardCanvas.destroy()
        self.boardCanvas = tk.Canvas(self.game, width=560, height=560)
        self.boardCanvas.grid(row=2, column=0, columnspan=2)
        self.boardCanvas.create_image((280, 280), image=self.backgroundPhoto)
        
        for i in range(8):
            for j in range(8):
                if self.positions[i][j] != None:
                    self.boardCanvas.create_image((35 + 70*i, 35 + 70*j),
                                                  image=self.checkersPieceDict[self.positions[i][j]])
        
        self.boardCanvas.bind("<Button-1>", self.clickBoard)


    def beginGameHelper(self): #Dưới đây là giao diện các phím khi chơi
        self.okButton.grid_forget()
        self.start.grid_forget()

        self.game = tk.Frame(self)
        self.game.grid(row=0)        
        self.clockLabel1 = tk.Label(self.game, text=self.namehs)
        self.clockLabel2 = tk.Label(self.game, text="Choose 1 RED and go\nthen wait, DON'T click the screen !")
        self.clockLabel1.grid(row=1, column=0)
        self.clockLabel2.grid(row=1, column=1)

        self.backgroundPhoto = tk.PhotoImage(file="Image/board.gif")
        self.checkersPieceDict = dict()
        photo = tk.PhotoImage(file = "Image/yellow.gif")
        self.checkersPieceDict[Piece(0)] = photo
        photo = tk.PhotoImage(file = "Image/red.gif")
        self.checkersPieceDict[Piece(1)] = photo

        photo = tk.PhotoImage(file = "Image/yellowKing.gif")
        self.checkersPieceDict[Piece(0, True)] = photo

        photo = tk.PhotoImage(file = "Image/redKing.gif")
        self.checkersPieceDict[Piece(1, True)] = photo


        self.boardCanvas = tk.Canvas(self.game, width=560, height=560)
        self.boardCanvas.grid(row=2, column=0, columnspan=2)
        self.boardCanvas.create_image((280, 280), image=self.backgroundPhoto)
        self.boardCanvas.bind("<Button-1>", self.clickBoard)

        
        self.statusLabel = tk.Label(self.game, text="")
        self.statusLabel.grid(row = 3, column = 0, columnspan =2)

        tk.Button(self.game, text="Resign", command=self.resignGame).grid(
            row=4, column=0)
        self.selected = False



    def beginGame(self): #Hiển thi các turn, thời gian,...
        if self.heuristic1.get() and not self.heuristic2.get() and not self.heuristic3.get():
            self.heuristic = 1
            self.namehs = "Max difference between the number of Pieces"
        elif not self.heuristic1.get() and self.heuristic2.get() and not self.heuristic3.get():
            self.heuristic = 2
            self.namehs = "Max number of Pawns and Kings"
        elif not self.heuristic1.get() and not self.heuristic2.get() and self.heuristic3.get():
            self.heuristic = 3
            self.namehs = "Max difference between value of Pieces"
        else:
            self.heuristic = 0
        if self.heuristic != 0:
            self.beginGameHelper()

            self.positions = initialBoard()
            self.draw()
            if (self.p1Name.get() == ""):
                self.player1Name = "COMPUTER"
            else:
                self.player1Name = self.p1Name.get()

            if (self.p2Name.get() == ""):
                self.player2Name = "GREEDY PEOPLE"
            else:
                self.player2Name = self.p2Name.get()

            self.playerTurnLabel = tk.Label(self.game, text= self.player1Name )
            self.playerTurnLabel.grid(row=0, column=0)
            self.playerTurnLabel2 = tk.Label(self.game, text= "===== " + self.player2Name + " =====")
            self.playerTurnLabel2.grid(row=0, column=1)
            
            self.turn = 1
                


    def clickBoard(self, event): #Hiển thị Kiểm tra khi chọn quân cờ
        self.time1 = time()
        
        if self.turn == 0:
            print("It is not your turn now!")
        else:
            if noMoveDetection(self.positions, self.turn): #Không còn lượt có thể đi
                self.statusLabel["text"] = "No possible moves, you have lost"
                print("no possible moves")
                self.time2 = time()
                self.resignGame()

            else:
                jmpDetectLst = jumpDetection(self.positions, self.turn)

                if self.selected == False: 
                    ptx, pty = pixelToInt(event.x, event.y)

                    if (self.positions[ptx][pty] == None): # Chưa chọn quân
                        self.statusLabel["text"] = "No piece selected"
                        print("no pieces selected")
                    
                    else: #Chọn sai quân, đi sai nước
                        if (self.positions[ptx][pty].color != self.turn):
                            self.statusLabel["text"] = "Wrong color selected" 
                            print("wrong color selected")

                        else:
                            s = set(jmpDetectLst)
                            if len(jmpDetectLst) != 0 and ((ptx, pty) not in s):
                                print("incorrect selection")
                                self.statusLabel["text"] = "Incorrect selection. You have to jump"
                            else:
                                self.selected = True
                                self.selectedPt = (ptx, pty)
                                print("selected")
                                self.statusLabel["text"] = str(self.selectedPt) +  " selected"
                            
                else: # Di chuyển
                    ptx, pty = pixelToInt(event.x, event.y)
                    self.move(ptx, pty)
    


    def setPlayer1(self): # Khúc này implement các phím, tg của người chơi 1
        
        self.playerTurnLabel["text"] = "===== "+ self.player1Name + " ====="
        self.playerTurnLabel2["text"] = self.player2Name
        self.selected = False
        self.statusLabel["text"] = ""
        self.turn = 0


    def setPlayer2(self): # Khúc này implement các phím, tg của người chơi 2

        self.playerTurnLabel["text"] = self.player1Name
        self.playerTurnLabel2["text"] = "===== " + self.player2Name + " ====="
        self.selected = False
        self.statusLabel["text"] = ""
        self.turn = 1


    def computer(self): #Bot di chuyển
        if self.turn == 0:
            print("COMPUTER turn...")
            if noMoveDetection(self.positions, self.turn): #Không còn lượt có thể đi
                self.statusLabel["text"] = "No possible moves, COMPUTER have lost"
                print("no possible moves")
                self.time2 = time()
                self.resignGame()
            else:
                x1, y1, x2, y2 = Go(self.positions, 0, self.heuristic)
                self.selectedPt = (x1, y1)
                self.move(x2, y2)
    
    def people(self):   #Người giả định di chuyển
        if self.turn == 1:
            print("PEOPLE turn...")
            if noMoveDetection(self.positions, self.turn): #Không còn lượt có thể đi
                self.statusLabel["text"] = "No possible moves, PEOPLE have lost"
                print("no possible moves")
                self.time2 = time()
                self.resignGame()
            else:
                x1, y1, x2, y2 = Go(self.positions, 1, 1)
                self.selectedPt = (x1, y1)
                self.move(x2, y2)

    def move(self, x2, y2): #Hiển thị các trạng thái khi di chuyển của người chơi
        ptx, pty = self.selectedPt
        jmplst = jumpPositions(self.positions[ptx][pty], ptx, pty, self.positions)
        mvlst = movePositions(self.positions[ptx][pty], ptx, pty, self.positions)
        
        if len(jmplst) != 0: #kiểm tra xem có nhảy và ăn quân được không
            s = set(jmplst)
            if ((x2, y2) not in s):
                self.statusLabel["text"] = str(self.selectedPt) +  " selected, you have to take the jump"
                return
            else:
                delX = int((x2+ptx)/2.0)
                delY = int((y2+pty)/2.0)
                self.positions[delX][delY] = None
                self.positions[x2][y2] = self.positions[ptx][pty]
                self.positions[ptx][pty] = None

                convertToKing(self.positions)
                self.draw()

                jmplst2 = jumpPositions(self.positions[x2][y2], x2, y2, self.positions)
                
                if len(jmplst2) != 0 and self.turn == 0:
                    self.computer()
                    print("COMPUTER turn...")
                
                elif len(jmplst2) != 0 and self.turn == 1:
                    self.people()
                    print("PEOPLE turn...")

                else:
                    if (noOpponentPieceDetection(self.positions, self.turn)):
                        self.time2 = time()
                        self.winGame()
                        print ("won game")

                    else:
                        if self.turn == 0:
                            self.setPlayer2()
                            self.people()
                        else:
                            self.setPlayer1()
                            self.computer()
        else:
            s = set(mvlst)
            if ((x2, y2) not in s):
                self.statusLabel["text"] = "Invalid move. Select a piece and try again"
                self.selected = False
                return
            else:
                self.positions[x2][y2] = self.positions[ptx][pty]
                self.positions[ptx][pty] = None
                
                convertToKing(self.positions)
                self.draw()

                if self.turn == 0:
                    self.setPlayer2()
                    self.people()
                else:
                    self.setPlayer1()
                    self.computer()
                

    def endGame(self): # Thể hiện màng hình khi game kết thúc
        self.game.destroy()

        self.endFrame = tk.Frame(self)
        self.endFrame.grid(row = 0)
        self.endGameResult = tk.Label(self.endFrame, text= "", height=5, width=50, font=50)
        self.endGameResult.grid(row=0)
        tk.Button(self.endFrame, text="New Game",fg="blue",
                                    border=5,height=3, width=20, font=50,
                                    command=self.endGameNew).grid(row=1)
        tk.Button(self.endFrame, text="Exit", fg="red",
                                    border=5,height=3, width=20, font=50,
                                    command=self.quit).grid(row=2)
    
    def endGameNew(self): # Destructor
        self.endFrame.destroy()
        self.okButton.destroy()
        self.start.destroy()
        
        self.gameStartupDialog()

    def resignGame(self): #Người chơi chủ động kết thúc
        self.endGame()

        if self.turn == 0:
            winner = self.player2Name
            loser = self.player1Name
            
        else:
            winner = self.player1Name
            loser = self.player2Name

        self.endGameResult["text"] = winner + " won!\n" + loser + " lost!\n " + "After: " + str(self.time2 - self.time1)[0:5] + " seconds\n"
        
    def winGame(self): # 1 trong 2 chiến thắng
        self.endGame()

        if self.turn == 0:
            winner = self.player1Name
            loser = self.player2Name
            
        else:
            winner = self.player2Name
            loser = self.player1Name

        self.endGameResult["text"] = winner + " won!\n" + loser + " lost!\n " + "After: " + str(self.time2 - self.time1)[0:5] + " seconds\n"



def pixelToInt(x, y): # Chuyển tọa độ dạng pixel sang (x,y) trên bàng cờ trả về tọa độ trên bàn cờ
    retx = 0
    retx_tot = 70
    
    rety = 0
    rety_tot = 70
    
    while (x > retx_tot and retx < 7):
        retx = retx + 1
        retx_tot = retx_tot + 70
        
    while (y > rety_tot and rety < 7):
        rety = rety + 1
        rety_tot = rety_tot + 70
        
    return (retx, rety)
    
def main1():
    root = tk.Tk()
    root.geometry("562x750")
    img = tk.PhotoImage(file="Image/background.png")
    label1 = tk.Label( root, image = img)
    label1.place(x = 0, y = 0)
    app = COMPUTER(master=root)
    app.mainloop()

main1()