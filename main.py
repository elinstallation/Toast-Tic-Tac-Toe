import pygame
import sys
import time

pygame.font.init()
pygame.init()
screen_HEIGHT = 500
screen_WIDTH = 500

screen = pygame.display.set_mode((screen_WIDTH, screen_HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

font = pygame.font.SysFont('arialblack', 48)

BOARD = pygame.image.load("assets/board_toast.png")

X_PIECE = pygame.image.load("assets/strawberry.png")
X_PIECE = pygame.transform.scale(X_PIECE, (120, 120))

O_PIECE = pygame.image.load("assets/blueberry.png")
O_PIECE = pygame.transform.scale(O_PIECE, (120, 120))

X_WIN = pygame.image.load("assets/x_win.png")
X_WIN = pygame.transform.scale(X_WIN, (300, 150))

O_WIN = pygame.image.load("assets/o_win.png")
O_WIN = pygame.transform.scale(O_WIN, (300, 150))

board = [['', '', ''], ['', '', ''], ['', '', '']]
graphical_board = [[[None, None] for _ in range(3)] for _ in range(3)]

to_move = 'X'
game_finished = False
win_image = None
message_time = 0

BG_COLOUR = (240, 240, 240)
HIGHLIGHT_COLOUR = (200, 50, 50)

def render_board(board, x_img, o_img):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                graphical_board[i][j][0] = x_img
                graphical_board[i][j][1] = x_img.get_rect(center=(j*(screen_WIDTH//3)+(screen_WIDTH//6), 
                                                                 i*(screen_HEIGHT//3)+(screen_HEIGHT//6)))
            elif board[i][j] == 'O':
                graphical_board[i][j][0] = o_img
                graphical_board[i][j][1] = o_img.get_rect(center=(j*(screen_WIDTH//3)+(screen_WIDTH//6), 
                                                                i*(screen_HEIGHT//3)+(screen_HEIGHT//6)))
            
            if graphical_board[i][j][0] is not None:
                screen.blit(graphical_board[i][j][0], graphical_board[i][j][1])

def add_XO(board, graphical_board, to_move):
    current_pos = pygame.mouse.get_pos()
    converted_x = current_pos[0] // (screen_WIDTH // 3) 
    converted_y = current_pos[1] // (screen_HEIGHT // 3)
    
    if 0 <= converted_x < 3 and 0 <= converted_y < 3 and board[converted_y][converted_x] == '':
        board[converted_y][converted_x] = to_move
        return board, 'O' if to_move == 'X' else 'X'
    
    return board, to_move

def check_win(board):
    # rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != '':
            return board[row][0]
    
    # columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
            return board[0][col]
    
    #  diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return board[0][2]
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                return None  
    
    return "DRAW"

def reset_game():
    global board, graphical_board, to_move, game_finished, win_image, message_time
    board = [['', '', ''], ['', '', ''], ['', '', '']]
    graphical_board = [[[None, None] for _ in range(3)] for _ in range(3)]
    to_move = 'X'
    game_finished = False
    win_image = None
    message_time = 0

run = True

while run:
    screen.fill(BG_COLOUR)
    screen.blit(BOARD, (0, 0))
    render_board(board, X_PIECE, O_PIECE)
    
    if win_image:
        overlay = pygame.Surface((screen_WIDTH, screen_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  
        screen.blit(overlay, (0, 0))
        
        win_rect = win_image.get_rect(center=(screen_WIDTH//2, screen_HEIGHT//2))
        screen.blit(win_image, win_rect)
        
        if time.time() - message_time > 2:
            reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_finished and not win_image:
            board, to_move = add_XO(board, graphical_board, to_move)
            result = check_win(board)
            
            if result:
                game_finished = True
                if result == "DRAW":
                    win_image = font.render("It's a Draw!", True, HIGHLIGHT_COLOUR)
                elif result == "X":
                    win_image = X_WIN
                else:
                    win_image = O_WIN
                message_time = time.time()

    pygame.display.update()

pygame.quit()
sys.exit()