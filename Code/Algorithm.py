from copy import deepcopy
import math
from PieceOperation import *
import random

def heuristic(board, hs):           # Hàm đánh giá các heuristic
    if hs == 1:                     # Số quân cờ mình - Số quân cờ đối thủ
        heuris = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] != None and board[x][y].color == 0:
                    heuris += 1
                if board[x][y] != None and board[x][y].color == 1:
                    heuris -= 1
        return heuris
    if hs == 2:                 # Giá trị đội mình đang có (thường + vua x 3) 
        heuris = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] != None and board[x][y].color == 0:
                    heuris += 1
                    if board[x][y].king == True:
                        heuris += 2
        return heuris  
    if hs == 3:                         # Giá trị đội mình - Giá trị đội đối thủ
        heuris = 0                      # Giá trị đội = (thường + hàng nó đứng đối với phe) + vua x 10
        for x in range(8):
            for y in range(8):
                if board[x][y] != None and board[x][y].color == 0 and board[x][y].king == False:
                    heuris += (1 + x)
                if board[x][y] != None and board[x][y].color == 0 and board[x][y].king == True:
                    heuris += 10
                if board[x][y] != None and board[x][y].color == 1 and board[x][y].king == False:
                    heuris -= (1 + 7 - x)
                if board[x][y] != None and board[x][y].color == 1 and board[x][y].king == True:
                    heuris -= 10
        return heuris


def getChild(board, who):           # Trả về các trường hợp có thể đi của một trạng thái
    currentBoard = deepcopy(board)
    child = []
    if who == True:
        child = boardDetection(currentBoard, 0)  # Nước đi của bot
    else:    
        child = boardDetection(currentBoard, 1)  # Nước đi của player
    return child
 

def MiniMax(board, depth, alpha, beta, maximizing, hs): # Trả về value của trạng thái hiện tại khi nhìn xa n bước
    if(depth == 0):                                     # Trả về value của trạng thái đó
        return heuristic(board, hs)
    currentBoard = deepcopy(board)      
    if maximizing == True:                              # Trạng thái tốt nhất
        maxEval = -math.inf
        for child in getChild(currentBoard, True):      # Tìm tất cả các trạng thái của ta
            Eval = MiniMax(child, depth-1, alpha, beta, False, hs)
            maxEval = max(maxEval, Eval)
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        return maxEval
    else:   
        minEval = math.inf
        for child in getChild(currentBoard, False):     # Tìm con của player
            Eval = MiniMax(child, depth-1, alpha, beta, True, hs)
            minEval = min(minEval, Eval)
            beta = min(beta, minEval)
            if beta <= alpha:
                break
        return minEval


def MoreJump(board, turn):      # Trả về trạng thái cuối khi đi bước tiếp theo (vì luật nhảy liên tục)
    ret = []                    # Lưu [[bảng tạo thành, quân cờ, bước đi đầu tiên của quân cờ để được bản đó],...]
    for x in range(8):
        for y in range(8):
            if board[x][y] != None and board[x][y].color == turn:
                b = jumpPositions(board[x][y], x, y, board)
                if len(b) != 0:
                    for m in b:
                        child = deepcopy(board)
                        child[m[0]][m[1]] = board[x][y]
                        x1 = int((m[0]+x)/2.0)
                        y1 = int((m[1]+y)/2.0)
                        child[x1][y1] = None
                        child[x][y] = None
                        ret1 = boardJumpDetection(child, turn)
                        if len(ret1) != 0:
                            for z in ret1:
                                ret.append([z, x, y, m[0], m[1]])
                        else:
                            ret.append([child, x, y, m[0], m[1]])
    return ret


def Go(board, turn, hs):    # (Trạng thái, turn, cách đánh giá heuristic). Trả về quân cờ và nước đi của quân cờ đó
    xPiece = -1
    yPiece = 0
    xGo = 0
    yGo = 0
    compare1 = -math.inf
    compare2 = math.inf
    a = MoreJump(board, turn)
    People = []
    if len(a) != 0:
        for i in a:
            child = i[0]
            if turn == 0:
                p = MiniMax(child, 3, -math.inf, math.inf, False, hs)
                if p > compare1:
                    compare1 = p
                    xPiece = i[1]
                    yPiece = i[2]
                    xGo = i[3]
                    yGo = i[4]
            else:
                p = MiniMax(child, 1, -math.inf, math.inf, True, 1)
                if p < compare2:
                    compare2 = p
                    xPiece = i[1]
                    yPiece = i[2]
                    xGo = i[3]
                    yGo = i[4]
    if xPiece == -1:
        for x in range(8):
            for y in range(8):
                if board[x][y] != None and board[x][y].color == turn:
                    a = movePositions(board[x][y], x, y, board)
                    if len(a) != 0:
                        for m in a:
                            child = deepcopy(board)
                            child[m[0]][m[1]] = board[x][y]
                            child[x][y] = None
                            if turn == 0:
                                p = MiniMax(child, 3, -math.inf, math.inf, False, hs)
                                if p > compare1:
                                    compare1 = p
                                    xPiece = x
                                    yPiece = y
                                    xGo = m[0]
                                    yGo = m[1]
                            else:
                                p = MiniMax(child, 1, -math.inf, math.inf, True, 1)
                                if p <= compare2:
                                    compare1 = p
                                    People.append([x,y,m[0],m[1]])
        if turn == 1:
            if len(People) > 0:
                c = random.choice(People)
                xPiece = c[0]
                yPiece = c[1]
                xGo = c[2]
                yGo = c[3]
    return (xPiece, yPiece, xGo, yGo)
    