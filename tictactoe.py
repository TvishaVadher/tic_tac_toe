import tkinter as tk
import winsound

# ---------------- CONFIG ---------------- #
BG_COLOR = "#0f172a"
GRID_COLOR = "#22d3ee"
X_COLOR = "#22d3ee"
O_COLOR = "#f472b6"
WIN_COLOR = "#a855f7"

CELL_SIZE = 140
BOARD_SIZE = 3

# ---------------- SOUND ---------------- #
def play_start():
    for f in [800, 1000, 1200]:
        winsound.Beep(f, 120)

def play_win():
    for f in [1000, 1300, 1600]:
        winsound.Beep(f, 180)

def play_draw():
    winsound.Beep(700, 400)

def play_error():
    for f in [500, 400]:
        winsound.Beep(f, 120)

# ---------------- APP ---------------- #
root = tk.Tk()
root.title("Neon Tic Tac Toe")
root.geometry("420x520")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# ---------------- START SCREEN ---------------- #
start_frame = tk.Frame(root, bg=BG_COLOR)
start_frame.pack(fill="both", expand=True)

tk.Label(
    start_frame,
    text="Neon Tic Tac Toe",
    font=("Segoe UI Black", 22),
    fg=GRID_COLOR,
    bg=BG_COLOR
).pack(pady=20)

p1_entry = tk.Entry(start_frame, font=("Segoe UI", 14), justify="center")
p1_entry.pack(pady=10)
p1_entry.insert(0, "Player 1")

p2_entry = tk.Entry(start_frame, font=("Segoe UI", 14), justify="center")
p2_entry.pack(pady=10)
p2_entry.insert(0, "Player 2")

# ---------------- GAME FRAME ---------------- #
game_frame = tk.Frame(root, bg=BG_COLOR)

canvas = tk.Canvas(
    game_frame,
    width=420,
    height=420,
    bg=BG_COLOR,
    highlightthickness=0
)
canvas.pack(pady=10)

status = tk.Label(
    game_frame,
    text="",
    font=("Segoe UI", 14, "bold"),
    fg="#e5e7eb",
    bg=BG_COLOR
)
status.pack()

# ---------------- GAME STATE ---------------- #
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
game_over = False
player1 = "Player 1"
player2 = "Player 2"

# ---------------- DRAW GRID ---------------- #
def draw_grid():
    canvas.delete("grid")
    for i in range(1, BOARD_SIZE):
        canvas.create_line(
            CELL_SIZE*i, 0,
            CELL_SIZE*i, 420,
            fill=GRID_COLOR, width=3, tags="grid"
        )
        canvas.create_line(
            0, CELL_SIZE*i,
            420, CELL_SIZE*i,
            fill=GRID_COLOR, width=3, tags="grid"
        )

# ---------------- WIN CHECK ---------------- #
def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return ("row", i)
        if board[0][i] == board[1][i] == board[2][i] != "":
            return ("col", i)

    if board[0][0] == board[1][1] == board[2][2] != "":
        return ("diag", 0)
    if board[0][2] == board[1][1] == board[2][0] != "":
        return ("diag", 1)

    return None

# ---------------- WIN LINE ---------------- #
def draw_win_line(info):
    if info[0] == "row":
        y = info[1] * CELL_SIZE + CELL_SIZE//2
        x1, y1, x2, y2 = 20, y, 400, y
    elif info[0] == "col":
        x = info[1] * CELL_SIZE + CELL_SIZE//2
        x1, y1, x2, y2 = x, 20, x, 400
    else:
        if info[1] == 0:
            x1, y1, x2, y2 = 20, 20, 400, 400
        else:
            x1, y1, x2, y2 = 400, 20, 20, 400

    line = canvas.create_line(x1, y1, x1, y1, fill=WIN_COLOR, width=6)
    for i in range(30):
        canvas.coords(
            line,
            x1, y1,
            x1 + (x2-x1)*i/30,
            y1 + (y2-y1)*i/30
        )
        root.update()
        root.after(10)

# ---------------- CLICK HANDLER ---------------- #
def click(event):
    global current_player, game_over

    if game_over:
        return

    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE

    if row > 2 or col > 2:
        return

    if board[row][col] == "":
       

        x = col * CELL_SIZE + CELL_SIZE//2
        y = row * CELL_SIZE + CELL_SIZE//2

        color = X_COLOR if current_player == "X" else O_COLOR
        canvas.create_text(
            x, y,
            text=current_player,
            font=("Segoe UI Black", 64),
            fill=color
        )

        board[row][col] = current_player

        win = check_winner()
        if win:
            play_win()
            winner = player1 if current_player == "X" else player2
            status.config(text=f"{winner} Wins! 🎉")
            draw_win_line(win)
            game_over = True
            return

        if all(board[r][c] != "" for r in range(3) for c in range(3)):
            play_draw()
            status.config(text="It's a Draw 🤝")
            game_over = True
            return

        current_player = "O" if current_player == "X" else "X"
        name = player1 if current_player == "X" else player2
        status.config(text=f"{name}'s Turn ({current_player})")

    else:
        play_error()

canvas.bind("<Button-1>", click)

# ---------------- RESET ---------------- #
def reset():
    global board, current_player, game_over
    canvas.delete("all")
    draw_grid()
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False
    status.config(text=f"{player1}'s Turn (X)")

tk.Button(
    game_frame,
    text="Restart Game",
    font=("Segoe UI", 12, "bold"),
    bg=GRID_COLOR,
    fg=BG_COLOR,
    relief="flat",
    padx=20,
    command=reset
).pack(pady=10)

# ---------------- START GAME ---------------- #
def start_game():
    global player1, player2
    play_start()
    player1 = p1_entry.get() or "Player 1"
    player2 = p2_entry.get() or "Player 2"

    start_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)
    draw_grid()
    status.config(text=f"{player1}'s Turn (X)")

tk.Button(
    start_frame,
    text="START GAME",
    font=("Segoe UI", 14, "bold"),
    bg=GRID_COLOR,
    fg=BG_COLOR,
    padx=30,
    pady=10,
    relief="flat",
    command=start_game
).pack(pady=30)

root.mainloop()
