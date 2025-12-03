import tkinter as tk
import random
import winsound  # للصوت


# ------------------ GAME VARIABLES ------------------
human = "x"
computer = "o"
board = [""] * 9

buttons = []
winning_combos = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
]

humanScore = 0
computerScore = 0
drawScore = 0


# ------------------ SOUND FUNCTIONS ------------------
def play_sound(filename):
    """Play a sound file asynchronously."""
    try:
        winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except:
        pass


# ------------------ ANIMATION ------------------
def animate_button(btn, color):
    original = btn.cget("bg")
    btn.config(bg=color)
    btn.after(150, lambda: btn.config(bg=original))


# ------------------ SCOREBOARD ------------------
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
    for btn in buttons:
        btn.config(text="", state="normal", bg="white")
    resultlabel.config(text="--", fg="yellow")


# ------------------ GAME LOGIC ------------------
def check_winner(player):
    for a, b, c in winning_combos:
        if board[a] == board[b] == board[c] == player:
            return True
    return False


def disable_all_buttons():
    for b in buttons:
        b.config(state="disabled")


def find_best_spot(player):
    """Find winning or blocking move."""
    for a, b, c in winning_combos:
        if board[a] == board[b] == player and board[c] == "":
            return c
        if board[a] == board[c] == player and board[b] == "":
            return b
        if board[b] == board[c] == player and board[a] == "":
            return a
    return None


def computer_move():
    # محاولة الفوز
    spot = find_best_spot("o")
    if spot is not None:
        buttons[spot].config(text="o", fg="red", state="disabled")
        animate_button(buttons[spot], "#ffcccc")
        play_sound("click.wav")
        board[spot] = "o"
        return

    # منع اللاعب
    spot = find_best_spot("x")
    if spot is not None:
        buttons[spot].config(text="o", fg="red", state="disabled")
        animate_button(buttons[spot], "#ffcccc")
        play_sound("click.wav")
        board[spot] = "o"
        return

    # خذ المركز
    if board[4] == "":
        buttons[4].config(text="o", fg="red", state="disabled")
        animate_button(buttons[4], "#ffcccc")
        play_sound("click.wav")
        board[4] = "o"
        return

    # خذ كورنر
    for corner in [0, 2, 6, 8]:
        if board[corner] == "":
            buttons[corner].config(text="o", fg="red", state="disabled")
            animate_button(buttons[corner], "#ffcccc")
            play_sound("click.wav")
            board[corner] = "o"
            return

    # خذ ضلع
    for edge in [1, 3, 5, 7]:
        if board[edge] == "":
            buttons[edge].config(text="o", fg="red", state="disabled")
            animate_button(buttons[edge], "#ffcccc")
            play_sound("click.wav")
            board[edge] = "o"
            return


def player_move(b):
    global humanScore, computerScore, drawScore

    index = buttons.index(b)
    play_sound("click.wav")
    animate_button(b, "#cce5ff")

    b.config(text="x", fg="blue", state="disabled")
    board[index] = human

    # فوز اللاعب
    if check_winner(human):
        humanScore += 1
        humanscorelabel.config(text=f"Human = {humanScore}")
        resultlabel.config(text="You Win!", fg="green")
        play_sound("win.wav")
        disable_all_buttons()
        return

    # تعادل
    if "" not in board:
        drawScore += 1
        drawscorelabel.config(text=f"Draw = {drawScore}")
        resultlabel.config(text="Draw!", fg="yellow")
        play_sound("draw.wav")
        disable_all_buttons()
        return

    # الكمبيوتر يلعب
    computer_move()

    # فوز الكمبيوتر
    if check_winner(computer):
        computerScore += 1
        computerscorelabel.config(text=f"Computer = {computerScore}")
        resultlabel.config(text="Computer Wins!", fg="red")
        play_sound("lose.wav")
        disable_all_buttons()
        return

    # تعادل بعد الكمبيوتر
    if "" not in board:
        drawScore += 1
        drawscorelabel.config(text=f"Draw = {drawScore}")
        resultlabel.config(text="Draw!", fg="yellow")
        play_sound("draw.wav")
        disable_all_buttons()
        return


# ------------------ GUI ------------------
window = tk.Tk()
window.title("Tic Tac Toe AI")
window.geometry("400x500")
window.configure(bg="black")

# Title
titlelabel = tk.Label(window, text="Tic Tac Toe", font=("fixedsys", 22, "bold"),
                      fg="red", bg="black")
titlelabel.pack(pady=10)

# Score Frame
scoreframe = tk.Frame(window, bg="black")
scoreframe.pack(pady=10)

humanscorelabel = tk.Label(scoreframe, text="Human = 0", font=("fixedsys", 14),
                           fg="white", bg="black")
humanscorelabel.grid(row=0, column=0, padx=10)

computerscorelabel = tk.Label(scoreframe, text="Computer = 0", font=("fixedsys", 14),
                              fg="white", bg="black")
computerscorelabel.grid(row=0, column=1, padx=10)

drawscorelabel = tk.Label(scoreframe, text="Draw = 0", font=("fixedsys", 14),
                           fg="white", bg="black")
drawscorelabel.grid(row=0, column=2, padx=10)

# Buttons Grid
buttonsframe = tk.Frame(window, bg="black")
buttonsframe.pack()

for r in range(3):
    for c in range(3):
        btn = tk.Button(buttonsframe, text="", bg="white",
                        font=("Arial", 32), width=4, height=1)
        btn.config(command=lambda b=btn: player_move(b))
        btn.grid(row=r, column=c, padx=5, pady=5)
        buttons.append(btn)

# Control Buttons Frame
controlframe = tk.Frame(window, bg="black")
controlframe.pack(pady=20)

restartbutton = tk.Button(controlframe, text="Restart Game",
                          font=("fixedsys", 12), width=15, command=restart_game)
restartbutton.grid(row=0, column=0, padx=10)

resetscorebutton = tk.Button(controlframe, text="Reset Scoreboard",
                             font=("fixedsys", 12), width=15, command=reset_scoreboard)
resetscorebutton.grid(row=0, column=1, padx=10)

# Result Label
resultlabel = tk.Label(window, text="--", font=("fixedsys", 16),
                       fg="yellow", bg="black")
resultlabel.pack(pady=10)

window.mainloop()
