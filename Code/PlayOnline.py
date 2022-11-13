import tkinter as tk
from PieceOperation import *
from _thread import *
from network import Network
import datetime as dt
import pickle
import json
import os

class PLAYONLINE(tk.Frame):
    STICKY = tk.N + tk.S + tk.E + tk.W

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.network = Network()
        self.idOnline = int(self.network.getP())
        self.lastMove = None
        self.turn = 0
        self.beginGame()           


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
        #self.boardCanvas.bind("<Button-1>", self.waiting)
        if self.turn != self.idOnline:
            start_new_thread(self.waiting, ())


    def waiting(self):
        while self.turn != self.idOnline:
            game = self.network.send("wait")
            if game.data != None and self.lastMove != game.data:
                self.selected = True
                self.selectedPt = (game.data[0], game.data[1])
                self.move(game.data[2], game.data[3])
                print("Nhận: " + str(game.data[0]) + " " + str(game.data[1]) + " " + str(game.data[2]) + " " + str(game.data[3]))
                self.lastMove = game.data


    def beginGameHelper(self): #Dưới đây là giao diện các phím khi chơi
        self.game = tk.Frame(self)
        self.game.grid(row=0)        

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

        self.selected = False


    def beginGame(self): #Hiển thi các turn, thời gian,...
        self.beginGameHelper()

        self.positions = initialBoard()
        self.draw()

        self.p1Name = tk.StringVar(value="YOU") if self.idOnline == 0 else tk.StringVar(value="ENERMY")
        self.p2Name = tk.StringVar(value="ENERMY") if self.idOnline == 0 else tk.StringVar(value="YOU")

        self.player1Name = self.p1Name.get()

        self.player2Name = self.p2Name.get()
        
        run = True
        while run:
            game = self.network.send("get")
            if game.ready:
                self.turn = 0
                run = False
                
        self.playerTurnLabel = tk.Label(self.game, text= "===== "+ self.player1Name + " =====")
        self.playerTurnLabel.grid(row=0, column=0)
        self.playerTurnLabel2 = tk.Label(self.game, text=self.player2Name)
        self.playerTurnLabel2.grid(row=0, column=1)
                
                
    def clickBoard(self, event): #Hiển thị Kiểm tra khi chọn quân cờ
        
        if noMoveDetection(self.positions, self.turn): #Không còn lượt có thể đi
            self.statusLabel["text"] = "No possible moves, you have lost"
            #print("no possible moves")
            self.resignGame()

        else:
            jmpDetectLst = jumpDetection(self.positions, self.turn)

            if self.selected == False: 
                ptx, pty = pixelToInt(event.x, event.y)

                if (self.positions[ptx][pty] == None): # Chưa chọn quân
                    self.statusLabel["text"] = "No piece selected"
                    #print("no pieces selected")
                
                elif(self.positions[ptx][pty].color == self.idOnline):      #Chọn sai quân, đi sai nước
                    if (self.positions[ptx][pty].color != self.turn):
                        self.statusLabel["text"] = "Wrong color selected" 
                        #print("wrong color selected")

                    else:
                        s = set(jmpDetectLst)
                        if len(jmpDetectLst) != 0 and ((ptx, pty) not in s):
                            #print("incorrect selection")
                            self.statusLabel["text"] = "Incorrect selection. You have to jump"
                        else:
                            self.selected = True
                            self.selectedPt = (ptx, pty)
                            #print("selected")
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
                self.selected = True
                self.selectedPt = (x2, y2)
                
                if self.turn == self.idOnline:
                    print("Gửi: " + str(ptx) + " " + str(pty) + " " + str(x2) + " " + str(y2))
                    self.lastMove = [ptx, pty, x2, y2]
                    self.network.send(str(ptx) + " " + str(pty) + " " + str(x2) + " " + str(y2))

                convertToKing(self.positions)

                if (noOpponentPieceDetection(self.positions, self.turn)):
                        self.winGame()
                        print ("won game")
                        return

                else:
                        if self.turn == 0:
                            self.setPlayer2()
                        else:
                            self.setPlayer1()
                            
                self.draw()
                
        else:
            s = set(mvlst)
            if ((x2, y2) not in s):
                self.statusLabel["text"] = "Invalid move. Select a piece and try again"
                self.selected = False
                return
            else:
                self.positions[x2][y2] = self.positions[ptx][pty]
                self.positions[ptx][pty] = None
                
                if self.turn == self.idOnline:
                    print("Gửi: " + str(ptx) + " " + str(pty) + " " + str(x2) + " " + str(y2))
                    self.lastMove = [ptx, pty, x2, y2]
                    self.network.send(str(ptx) + " " + str(pty) + " " + str(x2) + " " + str(y2))

                convertToKing(self.positions)

                if self.turn == 0:
                    self.setPlayer2()
                else:
                    self.setPlayer1()    
                    
                self.draw()


    def endGame(self): # Thể hiện màng hình khi game kết thúc
        self.game.destroy()

        self.endFrame = tk.Frame(self)
        self.endFrame.grid(row = 0)
        self.endGameResult = tk.Label(self.endFrame, text= "", height=5, width=50, font=50)
        self.endGameResult.grid(row=0)
        tk.Button(self.endFrame, text="Exit", fg="red", 
                                    border=5,height=3, width=20, font=50,
                                    command=self.quit).grid(row=2)

    
    def endGameNew(self): # Destructor
        self.endFrame.destroy()
        self.loadButton.destroy()
        self.okButton.destroy()
        self.timerFrame.destroy()
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

        self.endGameResult["text"] = winner + " won!\n" + loser + " lost!\n"

        
    def winGame(self): # 1 trong 2 chiến thắng
        self.endGame()

        if self.turn == 0:
            winner = self.player1Name
            loser = self.player2Name
            
        else:
            winner = self.player2Name
            loser = self.player1Name

        self.endGameResult["text"] = winner + " won!\n" + loser + " lost!\n"


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
    
def main2():
    root = tk.Tk()
    app = PLAYONLINE(master=root)
    app.mainloop()

#main2()