# ChessProject.py

import pygame
import socket

HOST = '127.0.0.1'
PORT = 5555



import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '1000,50'


pygame.init()
screen = pygame.display.set_mode((800, 800))  
clock = pygame.time.Clock()
pygame.display.set_caption('Pass and Play Chess')
pygame.display.set_icon(pygame.image.load("BK.png"))



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

    if in_check:
        draw_check(opposite_king,opposite_king_index)



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

def draw_check(opposite_king, opposite_king_index):
    for i in range(64):
        if piece_map[i][0] == opposite_king and piece_map[i][1] == 'K':
            row = i // 8
            col = i % 8
            x = col * 100
            y = row * 100
            red_box = pygame.image.load("red_box.png").convert_alpha()
            red_box.set_alpha(50)
            screen.blit(red_box, (x, y))
            break





    


def main():
    global selected_index
    selected_index = None
    global waiting_for_move
    waiting_for_move = False
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
    FPS = 25

    whites_turn = True
    opposite_king = None
    opposite_king_index = None
    in_check = None

    

    running = True


    while running:


        clock.tick(FPS)  # Limit to 30 frames per second
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = round(mouse_x // 100) *100
        mouse_y = round(mouse_y // 100) *100


        #print("Mouse Position: ", mouse_x/100, mouse_y/100)
        if piece_map[int(xy_to_index(mouse_x/100,mouse_y/100))] != "  ":
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 


            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:


                mouse_x, mouse_y = event.pos
                mouse_x = round(mouse_x // 100) *100
                mouse_y = round(mouse_y // 100) *100

                
                selected_index = int(xy_to_index(mouse_x/100,mouse_y/100))
                
            

                if in_check == True and waiting_for_move == False:

                    print("This is running...")
                    
                    #This runs when the next player is in check and needs to click a piece to move 
                    mouse_x, mouse_y = event.pos
                    mouse_x = round(mouse_x // 100) *100
                    mouse_y = round(mouse_y // 100) *100

                    
                    selected = int(xy_to_index(mouse_x/100,mouse_y/100))

                    

                    print("selected-index:",selected)
                    piece = piece_map[selected_index]
                    if piece == "  " or piece[0] == color:
                        print("Cant pick that")
                        break

                    


                    waiting_for_move = True
                    continue
                    #let the player grab a piece 

                elif in_check == True and waiting_for_move == True:
                    mouse_x, mouse_y = event.pos
                    mouse_x = round(mouse_x // 100) *100
                    mouse_y = round(mouse_y // 100) *100


                    new_index1 = int(xy_to_index(mouse_x/100,mouse_y/100))

                    print("You selected",piece,selected,"to move")

                    if piece_map[selected][0] == opposite_king and piece_map[selected][1] == 'K':
                        king_move = king_moves(opposite_king,opposite_king_index,piece_map)
                        if new_index1 not in attacking_square and new_index1 in eligible_moves(piece_map[selected],opposite_king_index):
                            print("Yes the checked king could move there")
                            piece_map[new_index1] = piece_map[selected]
                            piece_map[selected] = "  "
                            #write something right here so if the king takes, recheck the attacking_squares
                            # and if the king is still in attacking then undo because that piece is being
                            # protected by another piece 
                            
                            waiting_for_move = False
                            whites_turn = not whites_turn
                            in_check = False
                            break
                        else:
                            print("Cant move the king there dumbby")
                            break

                        #if the person in check grabs their king// and the new index is out of attacking squares 
                        # and in the eligible squares for the king, then it can move there 
                    
                    
                    print("eligible-moves,",eligible_moves(piece,selected))

                    attacking_square = attacking_squares(color,piece_map)

                   
                    if new_index1 in attacking_square and new_index1 in eligible_moves(piece,selected):

                        #lets add the piece to the newindex and get attackingsqaure, 
                        # if the king isnt in there its an eligible move
                        if selected != "  ":
                            piece_map[new_index1] = piece_map[selected]
                            piece_map[selected] = "  "

                        attacking_square = attacking_squares(color,piece_map)

                        if opposite_king_index not in attacking_square:
                            print("Looks right to me")
                            whites_turn = not whites_turn
                            waiting_for_move = False
                            in_check = False
                            break
                        else:
                            print("No you cant move here")
                            attacking_square = attacking_squares(color,piece_map)
                            if selected != "  " and selected != color:
                                piece_map[selected] = piece_map[new_index1]
                                piece_map[new_index1] = "  "
                            waiting_for_move = False
                            break

                        
                    
                    else: # if the piece being moved is not in attacking squares
                            print("Noo you cant move here2")
                            waiting_for_move = False
                            break

                
                    #now the piece has to move in the attacking squares if not, reselect a piece





        
                
                
                if waiting_for_move == False:
                    #if waiting for move and player does not click empty space
                    

                    if piece_map[selected_index] != "  " and whites_turn and piece_map[selected_index][0] != 'B':
                        move_to_index = selected_index
                        piece_to_move = piece_map[selected_index]
                        waiting_for_move = True
                        color = 'W'

                        opposite_king = 'B'
                        for i in range(64):
                            if piece_map[i] == "BK":
                                opposite_king_index = i
                                break
                        
                        print("Player selected index:", selected_index," Piece:", piece_map[selected_index])
                        could_move = eligible_moves(piece_to_move,selected_index)


                    elif piece_map[selected_index] != "  " and whites_turn==False and piece_map[selected_index][0] != 'W':
                        move_to_index = selected_index
                        piece_to_move = piece_map[selected_index]
                        waiting_for_move = True
                        color = 'B'

                        opposite_king = 'W'
                        for i in range(64):
                            if piece_map[i] == "WK":
                                opposite_king_index = i
                                break
                        

                        print("Player selected index:", selected_index," Piece:", piece_map[selected_index])
                        could_move = eligible_moves(piece_to_move,selected_index)
                else:
                    # if both pieces start with W or B then it cannot capture own piece
                    
                        
                    # if the move_to position is not in the eligible_move array then it wont move 
                    if selected_index not in could_move:
                        print("Not in eligible_move list")
                        print(could_move)
                        waiting_for_move = False
                        break
                    # so if this is the second click we move piece to new location
                    
                    print("Player moved to index:", move_to_index," Piece:", piece_map[move_to_index])
                    
                    
                    temp = piece_map[selected_index]
                    
                    piece_map[selected_index] = piece_map[move_to_index]
                    piece_map[move_to_index] = "  "

                    

                    

                    attacking_square = attacking_squares(color,piece_map)
                    opposite_attacking_square = attacking_squares(opposite_king,piece_map)

                    for i in range(64):
                        if piece_map[i][0] == color and piece_map[i][1] == 'K':
                            current_king_index = i
                            
                            # This finds the current king's index at i, and if that index is in the opposite kings
                            # attacking squares then its pinned and cannot move 
                            if current_king_index in opposite_attacking_square:
                                print("This is illegel, this piece is pinned")
                                piece_map[move_to_index] = piece_map[selected_index]
                                piece_map[selected_index] = temp
                                waiting_for_move = False
                                whites_turn = not whites_turn
                                pass

                    

                    if opposite_king_index in attacking_square:
                        waiting_for_move = False
                        print("Opposite King in check!")

                        in_check = True
                        draw_check(opposite_king,opposite_king_index)
                    
                    
                    

                        
                                
        
                
                
                                






                        


                    
                    waiting_for_move = False
                    selected_index = None
                    
                    
                    whites_turn = not whites_turn
                    
    

        
        #change this when drawing black 
        draw_white(mouse_x,mouse_y)
        
        pygame.display.flip()
    
    pygame.quit()
        
        
    
    
        
        
        
if __name__ == "__main__":
        
        main()


