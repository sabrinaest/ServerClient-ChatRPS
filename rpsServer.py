# Name: Sabrina Estrada
# Description: Create a chat between the client and server, either can initiate an ASCII game of rock, paper, scissors

from socket import *
from rpsGame import game, print_server_art  # imports the rock, paper, scissors game

# Citation for the following code:
# Date: 06/11/2023
# Adapted from: Kurose, James F, and Keith W Ross.
# Computer Networking : A Top-down Approach. Hoboken, Pearson, 2021, pp. 161–165.

# TCPServer.py
serverPort = 1030
serverName = '127.0.0.1'

# Create the client's socket (Kurose & Ross, 2021, p. 162)
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)


game_start = False      # boolean to help enter game mode
first_message = True    # boolean to make sure that it only prints the prompt to the server once (after first message from client)
gaming_results = {}     # to store the server and client choices for the game
# keeps track of the score board (best out of 3 wins)
server_wins = 0
client_wins = 0
# valid inputs for game, data validation
valid_inputs = ['rock', 'scissors', 'paper']
# prints the connection info
print('Server listening on: localhost on port:' + str(serverPort))
print("Connected by (" + str(serverName) + ',' + str(serverPort))
print("Waiting for message. . . . . ")
connectionSocket, addr = serverSocket.accept()

while True:
    # gets the reply from the client
    clientReply = connectionSocket.recv(1024).decode()

    # when the game hasn't started yet, process the clients responses
    if not game_start:

        # if the client wants to play the game, then get the server's input and store it in the dict
        # but send a message to the client saying the server wants to play too, so it can get the
        # client input for the game and send it to the server
        if clientReply == 'play rock, paper, scissors':
            print('Client wants to play rock, paper, scissors! Best of three!')
            serverInput = input("Enter your choice (rock, paper, scissors): ")
            serverInput = serverInput.lower()
            while serverInput not in valid_inputs:
                print("Oops! That's not a valid input, try again!")
                serverInput = input("Enter your choice (rock, paper, scissors): ")
                serverInput = serverInput.lower()
            gaming_results['server'] = serverInput
            game_start = True
            connectionSocket.send("Okay, let's play rock, paper, scissors! Best out of 3 :)".encode())

        # handles other chat-like messages from the client, very similar to the client code
        else:
            print(clientReply)

            if clientReply == '/q':
                print('Client has requested shutdown. Shutting down')
                connectionSocket.close()
                break

            if first_message:   # prints the prompt to the server after the client sends the first message
                print("Type /q to quit")
                print("Enter message to send. Please wait for input prompt before entering a message. . .")
                print("Note: Type 'play rock, paper, scissors' to start a game of rock, paper, scissors")
                first_message = False

            # displays the input and sends it to the client
            if clientReply != 'play rock, paper, scissors' and not first_message:
                serverInput = input("Enter Input > ")
                if serverInput == '/q':
                    print('Shutting down')
                    connectionSocket.send(serverInput.encode())
                    connectionSocket.close()
                    break

                # handles if the server wants to play the game
                if serverInput == 'play rock, paper, scissors':
                    server_choice = input("Enter your choice (rock, paper, scissors): ")
                    server_choice = server_choice.lower()
                    while server_choice not in valid_inputs:
                        print("Oops! That's not a valid input, try again!")
                        server_choice = input("Enter your choice (rock, paper, scissors): ")
                        server_choice = server_choice.lower()
                    gaming_results['server'] = server_choice    # store the server's choice in the dict
                    game_start = True
                    connectionSocket.send(serverInput.encode()) # send the play game string back to client
                else:
                    connectionSocket.send(serverInput.encode()) # sends the message with the user input from server like normal for all other messages

    # if the game has started, this is where the game logic happens
    else:
        # send to the client what has been stored in the gaming dict for the server's input
        # this is basically the same gaming logic as the client code
        connectionSocket.send(gaming_results['server'].encode())
        if clientReply in ['rock', 'paper', 'scissors']:
            gaming_results['client'] = clientReply
            server_choice = gaming_results['server']
            game_results = game(server_choice, clientReply)
            art = print_server_art(server_choice, clientReply)
            print('\n' + game_results)
            gaming_results = {}
            if game_results == 'Server wins!':
                server_wins += 1
            if game_results == 'Client wins!':
                client_wins += 1
            if server_wins < 3 and client_wins < 3:
                promptUser = "Next round!"
                print("Next round!")
                serverInput = input("Enter your choice (rock, paper, scissors): ")
                serverInput = serverInput.lower()
                while serverInput not in valid_inputs:
                    print("Oops! That's not a valid input, try again!")
                    serverInput = input("Enter your choice (rock, paper, scissors): ")
                    serverInput = serverInput.lower()
                gaming_results['server'] = serverInput
                # this will send "Next Round" to the client
                # this helps so that the server/client both can get the inputs they need for the game
                # the server will get the client input in the next iteration since it waits for the client's message
                connectionSocket.send(promptUser.encode())
            else:
                if server_wins > client_wins:
                    winner = "Server"
                else:
                    winner = "Client"
                game_over = "Game Over!" + winner + ' wins!'
                server_wins = 0
                client_wins = 0
                print("Game Over! " + winner + " wins!")
                game_start = False