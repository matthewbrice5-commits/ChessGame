import socket 
import threading
import time
import sys
import select
from typing import List


HOST = '0.0.0.0'

PORT = 5555

players: List[socket.socket] = []

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))

#change to 2 when getting second player on 
server.listen(2)

print("Server start on port,",PORT," Waiting for two players...")

#also change this to two to send both player's their color
for i in range(2):
    player, address = server.accept()
    players.append(player)
    print(f"Player {i+1} connected from {address}")
    if i == 0:
        player.send("W, Hello Player 1!".encode())
    else: 
        player.send("B, Hello Player 2!".encode())


#Now the server assigns who the players are 


#after the player makes a move, it needs to collect the data, ex selected_index, move_to_index 
#and forward that to the server, who then needs to send to the other player 

# the other player(B) then has to wait for the message to come through, swap the selected and move to index
#make their move, and then send that to server, who then sends it again to white and back and forth so one...


for player in players:
    player.setblocking(False)

def wait_for_enter():
    global running
    input("Press ENTER to stop server...\n")
    running = False
    print("\nShutting down server...")

# Start the input thread
input_thread = threading.Thread(target=wait_for_enter, daemon=True)
input_thread.start()

while True:

    for i in range(2):
        player_socket = players[i]
        try:
            data = player_socket.recv(1024).decode()
            if data:  # Only print if there's actual data
                if i == 0:
                    print("from Player 1: " + str(data))
                    #Below this should send to player 2
                    if len(players) > 1:
                        try:
                            players[1].send(data.encode())
                            print(f"Forwarded move to Player 2")
                        except Exception as e:
                            print(f"Error sending to Player 2: {e}")


                else:
                    print("from Player 2: " + str(data))
                    if len(players) > 0:
                        try:
                            players[0].send(data.encode())
                            print(f"Forwarded move to Player 1")
                        except Exception as e:
                            print(f"Error sending to Player 1: {e}")

        except BlockingIOError:
            # No data available from this socket right now - this is expected
            continue
        except Exception as e:
            print(f"Error receiving data: {e}")
            # Remove dead connection
            if player_socket in players:
                players.remove(player_socket)
            break
    
    time.sleep(0.1)  # Small delay to prevent CPU spinning
    






print("Closing all connections...")

# Close all player sockets
for player_socket in players:
    try:
        player_socket.close()
        print(f"Closed connection to player")
    except:
        pass

# Close the server socket
server.close()
print("Server socket closed")





input("Press Enter to close program")
