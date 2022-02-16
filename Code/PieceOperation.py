from copy import deepcopy


def boundsCheck(f):             # Kiểm tra giới hạn bàn cờ
    
    def retfunc(*args):
        xlst = f(*args)
        
        y = []
        for x in xlst:
            x1, x2 = x
            if x1 < 8 and x1 >= 0 and x2 < 8 and x2 >= 0:
                y.append(x)
        
        return y
        
    return retfunc

# Kể từ đây, kí hiệu piece là một quân cờ (có 2 attribute: màu, check có phải vua không)
@boundsCheck
def surroundings(piece, x, y, board):   # Các ô có thể ĐI của quân cờ (có thể chứ chưa chắc đi được)
    ret = []
    if piece != None:
        if (piece.king):                        # Nếu quân cờ là vua
            ret.append((x - 1, y - 1))
            ret.append((x + 1, y + 1))
            ret.append((x + 1, y - 1))
            ret.append((x - 1, y + 1))
            return ret
        
        else:
            if (piece.color == 0):              # Nếu là lính phe trên
                ret.append((x + 1, y + 1))
                ret.append((x - 1, y + 1))
                return ret
            else:                               # Nếu là lính phe dưới
                ret.append((x - 1, y - 1))
                ret.append((x + 1, y - 1))
                return ret 


@boundsCheck
def possibleJumps(piece, x, y, board):      # Kiểm tra các bước có thể NHẢY của quân cờ (có thể chứ chưa chắc nhảy được)
    positions = surroundings(piece, x, y, board)    # Lấy vùng lận cận
    
    ret = []
    
    for p in positions:                             # Xét các ô lân cận
        i, j = p
        if board[i][j] != None:
            if board[i][j].color != piece.color:    # Nếu có ô khác màu thì nhảy ra sau được
                ret.append((x+2*(i - x), y + 2*(j - y)))
    
    return ret


def jumpPositions(piece, x, y, board):      # Kiểm tra quân cờ NHẢY có được không
    positions = possibleJumps(piece, x, y, board)   # Lấy các bước có thể NHẢY
    
    ret = []
    
    for p in positions:
        i, j = p

        if board[i][j] == None:                     # Nếu ô có thể nhảy không có quân cờ thì nhảy được
            ret.append((i, j))

    return ret

def movePositions(piece, x, y, board):      # Kiểm tra quân cờ có ĐI được không
    positions = surroundings(piece, x, y, board)

    ret = []

    for p in positions:
        i, j = p
        
        if board[i][j] == None:                 # Nếu trong ô có thể đi mà trống thì có thể đi ô đó
            ret.append((i, j))

    return ret


@boundsCheck
def pieceDetection(board, turn):     # Kiểm tra các quân có thể đi
    ret = []
    for x in range(8):
        for y in range(8):
            if board[x][y] != None and board[x][y].color == turn:
                a = movePositions(board[x][y], x, y, board)
                b = jumpPositions(board[x][y], x, y, board)
                if len(a) == 0 and len(b) == 0:
                    pass
                else:
                    ret.append((x, y))
    return ret

def boardJumpDetection(board, turn):     # Kiểm tra các quân có thể nhảy
    ret = []
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
                            ret = ret + ret1
                        else:
                            ret.append(child)
    return ret

def boardDetection(board, turn):     # Kiểm tra các quân có thể đi
    ret = boardJumpDetection(board, turn)
    if len(ret) == 0:
        for x in range(8):
            for y in range(8):
                if board[x][y] != None and board[x][y].color == turn:
                    a = movePositions(board[x][y], x, y, board)
                    if len(a) != 0:
                        for m in a:
                            child = deepcopy(board)
                            child[m[0]][m[1]] = board[x][y]
                            child[x][y] = None
                            ret.append(child)
    return ret


def initialBoard():         # Khởi tạo bàn cờ
    ret = []
    
    for i in range(8):          # Khởi tạo các ô bàn cờ
        ith_row = []
        ret.append(ith_row)
        
        for j in range(8):
            ret[i].append(None)

    
    for i in range(0, 4, 2):    # Khởi tạo các quân cờ
        for j in range(0, 7, 2):
            ret[j][i] = Piece(0)
            ret[1+j][7-i] = Piece(1)
    

    for j in range(0, 7, 2):
        ret[1+j][1] = Piece(0)
        ret[j][6] = Piece(1)

#    0 1 2 3 4 5 6 7
#0   0   0   0   0
#1     0   0   0   0
#2   0   0   0   0
#3
#4
#5     1   1   1   1
#6   1   1   1   1
#7     1   1   1   1
    return ret


def convertToKing(board):   # Quân cờ biến thành vua
    for j in range(8):
        if board[j][0] != None:     # Nếu quân cờ màu 1 ở trên cùng
            if board[j][0].color == 1 and board[j][0].king != True: # Nếu không là vua thì biến thành vua
                board[j][0].king = True
                
        if board[j][7] != None:     # Nếu quân cờ màu 0 ở dưới cùng
            if board[j][7].color == 0 and board[j][7].king != True: # Nếu không là vua thì biến thành vua
                board[j][7].king = True
                
    return

def noMoveDetection(board, colorTurn):   # Kiểm tra xem đến lượt người chơi có bị hết đường hay không (thua)
    ret = True

    for x in range(8):
        for y in range(8):
            if board[x][y] != None and board[x][y].color == colorTurn:  # Kiểm tra tất cả các quân cờ hiện có
                mvLst = movePositions(board[x][y], x, y, board)
                jmpLst = jumpPositions(board[x][y], x, y, board)
                
                if len(mvLst) == 0 and len(jmpLst) == 0:
                    pass
                else:
                    ret = False                                         # Nếu tồn tại quân còn đường thì ok
    return ret


def noOpponentPieceDetection(board, turn):  # Kiểm tra xem đã ăn hết quân của đối thủ chưa
    ret = True
    
    if turn == 0:                           
        opponent = 1
    else:
        opponent = 0

    for x in range(8):
        for y in range(8):
            if board[x][y] != None and board[x][y].color == opponent:
                ret = False

    return ret

def jumpDetection(board, turn):     # Nếu có cơ hội nhảy thì bắt buộc phải nhảy
    ret = []

    for x in range(8):
        for y in range(8):
            if board[x][y] != None and board[x][y].color == turn:
                jmpLst = jumpPositions(board[x][y], x, y, board)
                
                if len(jmpLst) == 0:
                    pass
                else:
                    ret.append((x, y))
    return ret


class Piece:            # Khởi tạo quân cờ
    def __init__(self, color, king = False):    # Khởi tạo
        self.color = color
        self.king = king
    
    def __eq__(self, other):    # So sánh bằng
        if isinstance(other, Piece):
            return (self.color == other.color) and (self.king == other.king)
        else:
            return False

    def __ne__(self, other):    # So sánh khác
        return not self.__eq__(other)    


    def __hash__(self):         # Băm giá trị để dễ dàng add vào set()
        return hash((self.color, self.king))
