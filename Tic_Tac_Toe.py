import tkinter as tk
import random

# Game variables

human = "x"
computer = "o"
board = [""] * 9

buttons = []  # buttons list to make 3x3 grid of buttons

winning_combos = [
    (0, 1, 2),  # الصف الأول
    (3, 4, 5),  # الصف الثاني
    (6, 7, 8),  # الصف الثالث
    (0, 3, 6),  # العمود الأول
    (1, 4, 7),  # العمود الثاني
    (2, 5, 8),  # العمود الثالث
    (0, 4, 8),  # القطر
    (2, 4, 6)   # القطر الثاني
]

humanScore = 0
computerScore = 0
drawScore = 0

def reset_scoreboard():
    global humanScore, computerScore, drawScore
    humanScore = 0
    computerScore = 0
    drawScore = 0
    humanscorelabel.config(text="Human = 0")
    computerscorelabel.config(text="Computer = 0")
    drawscorelabel.config(text="Draw = 0")
    resultlabel.config(text="--", fg="yellow")


def restart_game():
    global board
    board = [""] * 9
    for button in buttons:
        button.config(text="", state="normal")
    resultlabel.config(text="--", fg="yellow")
    
def check_winner(player):
    for a, b, c in winning_combos:
        if board[a] == board[b] == board[c] == player:
            return True
    return False

def disable_all_buttons():
    for b in buttons:
        b.config(state="disabled")

def find_best_spot(player):
    for a, b, c in winning_combos:
        if board[a] == board[b] == player and board[c] == "":
            return c
        if board[a] == board[c] == player and board[b] == "":
            return b
        if board[b] == board[c] == player and board[a] == "":
            return a
    return None

def computer_move():
    spot = find_best_spot("o")
    if spot is not None:
        buttons[spot].config(text="o", state="disabled")
        board[spot] = "o"
        return
    spot = find_best_spot("x")
    if spot is not None:
        buttons[spot].config(text="o", state="disabled")
        board[spot] = "o"
        return
    if board[4] == "":
        spot = 4
        buttons[spot].config(text="o", state="disabled")
        board[spot] = "o"
        return
    for corner in [0, 2, 6, 8]:
        if board[corner] == "":
            spot = corner
            buttons[spot].config(text="o", state="disabled")
            board[spot] = "o"
            return
    for edge in [1, 3, 5, 7]:
        if board[edge] == "":
            spot = edge
            buttons[spot].config(text="o", state="disabled")
            board[spot] = "o"
            return 
    return

def player_move(b):
    global humanScore, computerScore, drawScore
    index = buttons.index(b)
    playermove = b.config(text=human, state="disabled")
    board[index] = human

    if check_winner(human):
        humanScore += 1
        humanscorelabel.config(text=f"Human = {humanScore}")
        resultlabel.config(text="You Win!", fg="green")
        disable_all_buttons()
        return
    elif "" not in board:
        drawScore += 1
        drawscorelabel.config(text=f"Draw = {drawScore}")
        resultlabel.config(text="It's a Draw!", fg="yellow")
        disable_all_buttons()
        return
    else:
        computer_move()

        if check_winner(computer):
            computerScore += 1
            computerscorelabel.config(text=f"Computer = {computerScore}")
            resultlabel.config(text="Computer Wins!", fg="red")
            disable_all_buttons()
            return
            
        elif "" not in board:
            drawScore += 1
            drawscorelabel.config(text=f"Draw = {drawScore}")
            resultlabel.config(text="It's a Draw!", fg="yellow")
            disable_all_buttons()
            return

# Main Window 

window = tk.Tk()
window.title("Tic Tac Toe Almdrasa")
window.geometry("400x500")
window.configure(bg="black")

# Title Label

titlelabel = tk.Label(window, text="Tic Tac Toe", font=("fixedsys", 20, "bold"), fg="red", bg="black")
titlelabel.pack(pady=10)

# score Frame & Labels

scoreframe = tk.Frame(window, bg="black")
scoreframe.pack(pady=10)

humanscorelabel = tk.Label(scoreframe, text="Human = 0", font=("fixedsys", 14), fg="white", bg="black")
humanscorelabel.grid(row=0, column=0, padx=10)

computerscorelabel = tk.Label(scoreframe, text="Computer = 0", font=("fixedsys", 14), fg="white", bg="black")
computerscorelabel.grid(row=0, column=1, padx=10)

drawscorelabel = tk.Label(scoreframe, text="Draw = 0", font=("fixedsys", 14), fg="white", bg="black")
drawscorelabel.grid(row=0, column=2, padx=10)

# Buttons Frame (Game Board)

buttonsframe = tk.Frame(window, bg="black")
buttonsframe.pack()

for r in range(3):
    for c in range(3):
        button = tk.Button(buttonsframe, text="", font=("Arial", 32), width=4, height=1,)
        button.config(command=lambda b=button: player_move(b))
        button.grid(row=r, column=c, padx=5, pady=5)
        buttons.append(button)
       

# Control Buttons Frame

controlframe = tk.Frame(window, bg="black")
controlframe.pack(pady=20)

restartbutton = tk.Button(controlframe, text="Restart Game", font=("fixedsys", 12), width=15, 
                          command=restart_game)
restartbutton.grid(row=0, column=0, padx=10)

resetscorebutton = tk.Button(controlframe, text="Reset Scoreboard", font=("fixedsys", 12), width=15,
                             command=reset_scoreboard)
resetscorebutton.grid(row=0, column=1, padx=10)

# result label 
resultlabel = tk.Label(window, text="--", font=("fixedsys", 16), fg="yellow", bg="black"
                       )
resultlabel.pack(pady=10) 

window.mainloop()