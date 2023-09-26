# Name: Sabrina Estrada
# Description: Create a chat between the client and server, either can initiate an ASCII game of rock, paper, scissors

from socket import *
from rpsGame import game, print_client_art  # imports the rock, paper, scissors game

# Citation for the following code:
# Date: 06/11/2023
# Adapted from: Kurose, James F, and Keith W Ross.
# Computer Networking : A Top-down Approach. Hoboken, Pearson, 2021, pp. 161–165.

# TCPClient.py

serverName = '127.0.0.1'
serverPort = 1030
game_start = False      # boolean to help enter game mode
gaming_results = {}     # to store the server and client choices for the game
# keeps track of the score board (best out of 3 wins)
server_wins = 0
client_wins = 0
# valid inputs for game, data validation
valid_inputs = ['rock', 'scissors', 'paper']
# prompts the client
print('Server listening on: localhost on port:' + str(serverPort))
print("Type /q to quit")
print("Enter message to send. Please wait for input prompt before entering message. . .")
print("Note: Type 'play rock, paper, scissors' to start a game of rock, paper, scissors")

# Create the client's socket (Kurose & Ross, 2021, p. 162)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    if game_start:      # if the game has started, enter this conditional to go through the game logic
        if 'client' not in gaming_results:          # checks to see if we have a stored response from the client
            userInput = input("Enter your choice (rock, paper, scissors): ")
            userInput = userInput.lower()           # helps with data validation, so user can enter valid input with a capital letter
            while userInput not in valid_inputs:    # data validation loop, allows user to try again
                print("Oops! That's not a valid input, try again!")
                userInput = input("Enter your choice (rock, paper, scissors): ")
                userInput = userInput.lower()
            gaming_results['client'] = userInput    # store the client response for the game, to use later
            clientSocket.send(userInput.encode())   # send the response to the server

            # get the server reply and check if within the valid inputs, if it is store it in the results
            serverReply = clientSocket.recv(2048).decode()

            if serverReply in ['rock', 'paper', 'scissors']:
                gaming_results['server'] = serverReply

            # if we have both server and client choices then we can call the game and enter the inputs, print out the results
            if 'server' in gaming_results and 'client' in gaming_results:
                server_choice = gaming_results['server']
                client_choice = gaming_results['client']

                # gets the results on who won and prints the ascii w/ client to the left and server to the right
                results = game(server_choice, client_choice)
                art = print_client_art(client_choice, server_choice)
                print('\n' + results)

                # start from scratch for a new game
                gaming_results = {}

                # increment the score board depending on who wins
                if results == 'Server wins!':
                    server_wins += 1
                elif results == 'Client wins!':
                    client_wins += 1

                # continue the game if no one has won 3 rounds
                if server_wins < 3 and client_wins < 3:
                    print("Next round!")
                    userInput = input("Enter your choice (rock, paper, scissors): ")
                    userInput = userInput.lower()
                    while userInput not in valid_inputs:
                        print("Oops! That's not a valid input, try again!")
                        userInput = input("Enter your choice (rock, paper, scissors): ")
                        userInput = userInput.lower()
                    gaming_results['client'] = userInput
                    clientSocket.send(userInput.encode())   # send the client's new input for the next round to the server

                # else someone has won 3 rounds print the results of who won
                else:
                    if server_wins > client_wins:
                        winner = "Server"
                    else:
                        winner = "Client"

                    # reset the score board since game is over
                    server_wins = 0
                    client_wins = 0
                    print("Game Over! " + winner + " wins!")

                    # reset the boolean to False, since game is over
                    game_start = False
            else:
                print(serverReply)

        # this else statement helps when the game enters the next round
        # After the first round it gets the new client input for the next game and sends it to the server
        # the server will store that input then send "Next round" to the client first
        # then this else statement will continue to get triggered until the client receives a valid input for the game
        else:
            # the logic is very similar to the previous conditional
            serverReply = clientSocket.recv(2048).decode()
            if serverReply in ['rock', 'paper', 'scissors']:
                gaming_results['server'] = serverReply

            if 'server' in gaming_results and 'client' in gaming_results:
                server_choice = gaming_results['server']
                client_choice = gaming_results['client']
                results = game(server_choice, client_choice)
                art = print_client_art(client_choice, server_choice)
                print('\n' + results)
                gaming_results = {}
                if results == 'Server wins!':
                    server_wins += 1
                elif results == 'Client wins!':
                    client_wins += 1
                if server_wins < 3 and client_wins < 3:
                    print("Next round!")
                    userInput = input("Enter your choice (rock, paper, scissors): ")
                    userInput = userInput.lower()
                    while userInput not in valid_inputs:
                        print("Oops! That's not a valid input, try again!")
                        userInput = input("Enter your choice (rock, paper, scissors): ")
                        userInput = userInput.lower()
                    gaming_results['client'] = userInput
                    clientSocket.send(userInput.encode())
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

    else:       # else: the game has not started, go through regular chat session w/ server
        userInput = input("Enter Input > ")
        if userInput == '/q':                       # conditional if client wants to exit
            clientSocket.send(userInput.encode())   # let the server know client wants to exit out
            print('Shutting Down!')
            clientSocket.close()
            break                                   # exit out
        if userInput == 'play rock, paper, scissors':       # if the client wants to play rock, paper, scissors
            print("Oo a game! Let's see if Server says")    # it has to let the server know first so it enters game mode
            game_start = True                               # boolean to enter game mode

        if userInput != '/q':                                   # send the socket and receive the reply from the server
            clientSocket.send(userInput.encode())

            serverReply = clientSocket.recv(2048).decode()
            if serverReply == 'play rock, paper, scissors':     # conditional to handle if the server wants to play the game
                print('Server wants to play rock, paper, scissors! Best of three!')
                game_start = True
            if serverReply == '/q':                             # conditional if the server wants to quit
                print("Server has requested shutdown. Shutting down")
                clientSocket.close()                            # close down and break loop on client side
                break
            else:
                print(serverReply)                              # else print server reply as usual




