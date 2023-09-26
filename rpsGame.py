# Name: Sabrina Estrada
# Description: Rock, paper, scissors game part of the chat/game project

# Citation for the ASCII art:
# Date: 06/11/2023
# Title: Rock, Paper, Scissors ASCII Art by wynand1004
# Available at: https://gist.github.com/wynand1004/b5c521ea8392e9c6bfe101b025c39abe

# wanted to make the user input to be on the left side and their partner to be on the right in the terminal
# so I flipped the ASCII art from the github which is why there are two ASCII dictionaries

left = {'rock':
"""
    _______
---'   ____) 
      (_____)
      (_____)
      (____) 
---.__(___) 
""", 'paper':
"""
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)   
""", 'scissors':
"""
    _______
---'    ____)____
           ______)
        __________)
      (____)      
---.__(___)
"""}

right = {'rock':
"""
  _______
 (____     '---
(_____)
(_____)
 (____)
  (___)__.---
""", 'paper':
"""
      _______ 
 ____(____    '---
(______
(_______
 (_______
   (__________.---
""", 'scissors':
"""
       _______
  ____(____   '---
 (______
(__________
     (____)
      (___)__.---
"""}

result = ''

# this is the game logic, if the inputs are the same then its a draw
def game(server_choice, client_choice):
    if server_choice == client_choice:
        result = "Draw"
    # handles who wins based on their inputs, rock paper scissors logic. These are all the options if the server would win the round
    elif (server_choice == 'paper' and client_choice == 'rock') or (server_choice == 'scissors' and client_choice == 'paper') or (server_choice == 'rock' and client_choice == 'scissors'):
        result = "Server wins!"
    else:
        result = "Client wins!"
    # returns the result, client/server wins or draw
    return result

# Citation for displaying the ASCII art:
# Date: 06/11/2023
# Title: How do I place two or more ASCII images side by side?
# Available at: https://stackoverflow.com/questions/69795265/how-do-i-place-two-or-more-ascii-images-side-by-side

# this is the logic to display the ASCII art, there are two to display on the server end and
# the other to handle the display on the client's end
def print_client_art(client_choice, server_choice):
    # this will display the client on the left side and the server on the right
    server_art = right[server_choice]
    client_art = left[client_choice]

    # needs to split the ASCII art into lines, needed to print the art side by side
    server_art_lines = server_art.splitlines()
    client_art_lines = client_art.splitlines()

    # since the ASCII art can be of different lengths, we need to calculate the padding
    # so find the longest line in the client's ASCII art and this will be used to calculate the padding
    max_length = max(len(line) for line in client_art_lines)

    # a and b are the individual lines of the ASCII that will be printed one by one
    # the padding is calculated byt using the max length of the client ASCII art lines and the current line b.
    # The + 2 is to print extra space between the two ASCII images
    for a, b in zip(server_art_lines, client_art_lines):
        print((b + (" " * (max_length - len(b) + 2)) + a))
    # prints the lines one by one

# same logic as the other one but flipped so that the server is being printed on the left side
def print_server_art(server_choice, client_choice):
    # this will display the server on the left side and the client on the right
    server_art = left[server_choice]
    client_art = right[client_choice]

    # needs to split the ASCII art into lines, needed to print the art side by side
    server_art_lines = server_art.splitlines()
    client_art_lines = client_art.splitlines()

    max_length = max(len(line) for line in server_art_lines)

    for a, b in zip(server_art_lines, client_art_lines):
        print((a + (" " * (max_length - len(a) + 2)) + b))


