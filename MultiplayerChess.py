# ChessProject.py

import pygame
import socket
import time

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '1000,50'


pygame.init()
screen = pygame.display.set_mode((800, 800))  
clock = pygame.time.Clock()


selection_box = pygame.image.load("selection_box.png")


WHITE = (255, 255, 255)
GREEN = (0, 255, 0)






piece_map = ["BR","BH","BB","BQ","BK","BB","BH","BR",
             "BP","BP","BP","BP","BP","BP","BP","BP",
             "  ","  ","  ","  ","  ","  ","  ","  ",
             "  ","  ","  ","  ","  ","  ","  ","  ",
             "  ","  ","  ","  ","  ","  ","  ","  ",
             "  ","  ","  ","  ","  ","  ","  ","  ",
             "WP","WP","WP","WP","WP","WP","WP","WP",
             "WR","WH","WB","WQ","WK","WB","WH","WR"]
def xy_to_index(x,y):
    return y*8 + x

def draw_black(x,y):
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                # Flip the column calculation: (7-col) instead of col
                pygame.draw.rect(screen, WHITE, ((7-col) * 100, (7-row) * 100, 100, 100))
            else:
                pygame.draw.rect(screen, GREEN, ((7-col) * 100, (7-row) * 100, 100, 100))   

    for row in range(64):
        piece = piece_map[row]
        if piece != "  ":
            image = pygame.image.load(f"{piece}.png")
            scaled_image = pygame.transform.scale(image, (100, 100))
            # Flip both row and column calculations
            screen.blit(scaled_image, ((7 - (row % 8)) * 100, (7 - (row // 8)) * 100))
    
    screen.blit(selection_box, (x, y))


def draw_white(x,y):
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, WHITE, (col * 100, row * 100, 100, 100))
            else:
                pygame.draw.rect(screen, GREEN, (col * 100, row * 100, 100, 100))   


    
    for row in range(64):
        piece = piece_map[row]
        if piece != "  ":
            image = pygame.image.load(f"{piece}.png")
            scaled_image = pygame.transform.scale(image, (100, 100))
            screen.blit(scaled_image, ((row % 8) * 100, (row // 8) * 100))
            screen.blit(selection_box,(x,y))

    draw_check()



def pawn_moves(color, index, piece_map):
    could_move = []
    direction = -8 if color == "W" else 8
    start_row = [48,49,50,51,52,53,54,55] if color == "W" else [8,9,10,11,12,13,14,15]
    forward = index + direction
    
    

    if piece_map[forward][0] != color and piece_map[forward] != "  ":
        pass 
    else:
        #if white is on starting row it can go forward once or twice 
        if index in start_row and color == 'W':
            could_move.append(forward)
            could_move.append(forward - 8)
        
        else: # white can only move forward since not on starter row 
            could_move.append(forward)
    
        if index in start_row and color == 'B':
            could_move.append(forward + 8)
            could_move.append(forward)
        else : 
            could_move.append(forward)
        
    diagoal_left = index + direction - 1
    diagoal_right = index + direction + 1
    
    if piece_map[diagoal_left] != "  " and piece_map[diagoal_left][0] != color: 
        could_move.append(diagoal_left)
    if piece_map[diagoal_right] != "  " and piece_map[diagoal_right][0] != color: 
        could_move.append(diagoal_right)


    return could_move

def knight_moves(color, index, piece_map):
    could_move = []
    knight_moves = [15, 17, 10, 6, -15, -17, -10, -6]
    
    for move in knight_moves:
        new_index = index + move
        # the new index needs to be without bounds otherwise it'll throw an error 
        if 0 <= new_index < 64 and piece_map[new_index][0] != color:
            could_move.append(new_index)
    
    return could_move

def bishop_moves(color, index, piece_map):
    could_move = [] 
    directions = [9, 7, -9, -7]  # Diagonal directions- top-left, top-right, bottom-left, bottom-right

    for direction in directions:
        new_index = index + direction
        #The while loop continues until out of bounds or encounters a piece 
        while 0 <= new_index < 64:
            if piece_map[new_index] == "  ":  # Empty square
                could_move.append(new_index)
            elif piece_map[new_index][0] != color:  # Opponent's piece
                could_move.append(new_index)
                break
            else:  # Own piece
                break
            
            new_index += direction
            
    return could_move

def rook_moves(color, index, piece_map):
    could_move = []
    rook_directions = [-8,-1,1,8]
    
    for direction in rook_directions:
        new_index = index + direction
        
        while 0 <= new_index < 64:
            if direction == -1 and new_index % 8 == 7:  #Prevents wrapping if rook is on edge of board 
                break
            if direction == 1 and new_index % 8 == 0:   #Prevents wrapping if rook is on edge of board 
                break
            if piece_map[new_index] == "  ": #Empty space
                could_move.append(new_index)
            elif piece_map[new_index][0] != color:
                could_move.append(new_index)
                break
            else:
                break
            new_index += direction
    return could_move
def queen_moves(color, index, piece_map):
    could_move = []
    Rmoves = rook_moves(color,index,piece_map)
    Bmoves = bishop_moves(color,index,piece_map)
    for move in Rmoves:
        could_move.append(move)
    for move in Bmoves:
        could_move.append(move)
         
    return could_move

def king_moves(color,index,piece_map):
    could_move = []
    directions = [-9,-8,-7,-1,1,7,8,9]
    
    for move in directions:
        new_index = move + index
        
        if 0 <= new_index < 64:
            if (move == -1 or move == 7 or move == -9) and new_index % 8 == 7:  #Prevents wrapping if rook is on edge of board 
                continue
            if (move == 1 or move == -7 or move == 9) and new_index % 8 == 0:   #Prevents wrapping if rook is on edge of board 
                continue
        
            if piece_map[new_index] == "  ": #Empty space
                could_move.append(new_index)
            elif piece_map[new_index][0] != color:
                could_move.append(new_index)
          
    return could_move
        

     

def eligible_moves(piece_to_move, index):
    could_move = []
    color = piece_to_move[0]
    piece = piece_to_move[1]

    if piece == 'P':
        could_move = pawn_moves(color , index, piece_map)
    elif piece == 'H':
        could_move = knight_moves(color , index, piece_map)
    elif piece == 'B':
        could_move = bishop_moves(color , index, piece_map)
    elif piece == 'R':
        could_move = rook_moves(color,index,piece_map)
    elif piece == 'Q':
        could_move = queen_moves(color,index,piece_map)
    elif piece == 'K':
        could_move = king_moves(color,index,piece_map)

    

    return could_move


    
def attacking_squares(color,piece_map):
    attacking = []

    for i in range(64):

        if piece_map[i][0] == color:
            piece = piece_map[i][1]

            if piece == 'P':
                pawnmove = pawn_moves(color , i, piece_map)
                for move in pawnmove:
                    attacking.append(move)
            elif piece == 'H':
                knightmove = knight_moves(color , i, piece_map)
                for move in knightmove:
                    attacking.append(move)
            elif piece == 'B':
                bishopmove = bishop_moves(color , i, piece_map)
                for move in bishopmove:
                    attacking.append(move)
            elif piece == 'R':
                rookmoves = rook_moves(color,i,piece_map)
                for move in rookmoves:
                    attacking.append(move)
            elif piece == 'Q':
                queenmove = queen_moves(color,i,piece_map)
                for move in queenmove:
                    attacking.append(move)
            elif piece == 'K':
                kingmove = king_moves(color,i,piece_map)
                for move in kingmove:
                    attacking.append(move)

    return attacking

def draw_check():
    
    whites_attacking_squares = attacking_squares('W',piece_map)
    black_attacking_squares = attacking_squares('B',piece_map)
    
    if in_check:
        for square in whites_attacking_squares:
            #If there is a king in whites squares, draw at that square
            if piece_map[square][1] == 'K' and piece_map[square][0] == 'B':
                i = square
                row = i // 8
                col = i % 8
                x = col * 100
                y = row * 100
                red_box = pygame.image.load("red_box.png").convert_alpha()
                red_box.set_alpha(50)
                screen.blit(red_box, (x, y))
                break
            
        for square in black_attacking_squares:
            if piece_map[square][1] == 'K' and piece_map[square][0] == 'W':
                i = square
                row = i // 8
                col = i % 8
                x = col * 100
                y = row * 100
                red_box = pygame.image.load("red_box.png").convert_alpha()
                red_box.set_alpha(50)
                screen.blit(red_box, (x, y))
                break
            
            
def waiting_for_data_code(client_socket):
    try:
            # Try to receive data (non-blocking)
                data = client_socket.recv(1024).decode()

                if data:
                    first_index, second_index = data.strip('()').split(',')
                    first_index = int(first_index)
                    second_index = int(second_index)
                    
                    piece_map[second_index] = piece_map[first_index]
                    piece_map[first_index] = "  "
                    print(first_index,",",second_index)

                # Update board with opponent's move
                    your_turn = True
                    
                    
                else:
                    print("No data recieved")

    except socket.timeout:
        print("Timeout")






    


def main():
    global selected_index
    selected_index = None
    global waiting_for_move
    waiting_for_move = True
    global could_move
    could_move = []
    global check_piece
    check_piece = "  "
    global opposite_king
    global opposite_king_index
    global running
    global in_check
    global current_king
    global current_king_index

    current_king = None
    current_king_index = None
    
    screen.fill(WHITE)
    FPS = 20

    whites_turn = True
    opposite_king = None
    opposite_king_index = None
    in_check = None
    player_color = " "

    move_to_index = None
    remember = None
    data_to_send = None

    send_message = False
    your_turn = False


    running = True

    #This is going to connect to the server 
    HOST = '0.0.0.0'
    PORT = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(0.3)
    
    try:
        client_socket.connect((HOST, PORT))
        move = client_socket.recv(1024).decode()
        player_color = move[0]
        
    except Exception as e:
        print("An error connecting occured.")
        client_socket.close()
        pass
        
        
    
    #this is custom set to white before networking is added
    player_color = 'W'
    print("Your color",player_color)



    if player_color == 'W':
        pygame.display.set_caption("Player 1: W")
        your_turn = True
        waiting_for_move = True
    else: 
        pygame.display.set_caption("Player 2: B")
        your_turn = True
        waiting_for_move = True
        



    while running:
        clock.tick(FPS)  # Limit to 30 frames per second

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = round(mouse_x // 100) * 100
        mouse_y = round(mouse_y // 100) * 100

        # Handle events once per frame
        

        if player_color == 'W':
            # if player is white it draws their screen
            draw_white(mouse_x, mouse_y)

            # when its the players turn, when its not their turn, they're waiting for data
            if your_turn:
                # and the player hasnt picked a move yet 
                if waiting_for_move:
                    # Check for mouse clicks in the main event loop
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            mouse_x, mouse_y = event.pos
                            mouse_x = round(mouse_x // 100) * 100
                            mouse_y = round(mouse_y // 100) * 100

                            selected_index = int(xy_to_index(mouse_x/100, mouse_y/100))
                            # player has to only select their piece
                            if piece_map[selected_index][0] == 'W':
                                waiting_for_move = False
                                print("Player selected ", selected_index)
                                could_move = eligible_moves(piece_map[selected_index], selected_index)
                                # ^^^^^^^ will now get compared to the next index, if the new index is in 
                                # there than it can move there 
                                break
                else:
                    # So if the player has selected a piece, needs to get the move_to index 
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            mouse_x, mouse_y = event.pos
                            mouse_x = round(mouse_x // 100) * 100
                            mouse_y = round(mouse_y // 100) * 100

                            move_to_index = int(xy_to_index(mouse_x/100, mouse_y/100))

                            if move_to_index in could_move:
                                piece_map[move_to_index] = piece_map[selected_index]
                                piece_map[selected_index] = "  "
                                waiting_for_move = True
                            else:
                                print("Invalid move")
                                waiting_for_move = True
            else:
                print("Not your turn")                  

        # if player is black it draws their screen
        elif player_color == 'B':
            draw_white(mouse_x, mouse_y)  # change to draw black when done writing logic

            if your_turn:
                if waiting_for_move:
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            print("got here")
                            mouse_x, mouse_y = event.pos
                            mouse_x = round(mouse_x // 100) * 100
                            mouse_y = round(mouse_y // 100) * 100

                            selected_index = int(xy_to_index(mouse_x/100, mouse_y/100))
                            # player has to only select their piece
                            if piece_map[selected_index][0] == 'B':
                                waiting_for_move = False
                                print("Player selected ", selected_index)
                                could_move = eligible_moves(piece_map[selected_index], selected_index)
                                # ^^^^^^^ will now get compared to the next index, if the new index is in 
                                # there than it can move there 
                                break
                                
                else:
                    # So if the player has selected a piece, needs to get the move_to index 
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            mouse_x, mouse_y = event.pos
                            mouse_x = round(mouse_x // 100) * 100
                            mouse_y = round(mouse_y // 100) * 100

                            move_to_index = int(xy_to_index(mouse_x/100, mouse_y/100))

                            if move_to_index in could_move:
                                piece_map[move_to_index] = piece_map[selected_index]
                                piece_map[selected_index] = "  "
                                waiting_for_move = True
                            else:
                                print("Invalid move")
                                waiting_for_move = True
            else:
                print("Not your turn")






                
 #       data_to_send = move_to_index, remember
 #       if send_message:
 #           data_to_send = str(data_to_send)
 #           print("Data to send,",data_to_send)
 #           client_socket.send(data_to_send.encode())
 #           your_turn = False

        
        
        
        pygame.display.flip()
    
    pygame.quit()
        
        
    
    
        
        
        
if __name__ == "__main__":
        
        main()


