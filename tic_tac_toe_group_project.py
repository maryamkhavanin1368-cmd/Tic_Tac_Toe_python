"""TIC TAC TOE - INTRODUCTION TO COMPUTER SCIENCE, GROUP PROJECT

Final-review draft based on the actual group code shared on 16 November 2026.
Original group attribution in the supplied code:
    Part 2 - Hannaneh Ahmadi (player X/O turns)
    Part 3 - Soheil Amiri (winner detection and highlighting)
Other part owners should confirm their responsibilities before submission.

This version keeps the same basic game logic and adds clear descriptions.
Necessary fixes: correct winner mark for columns/diagonals; check tie only
AFTER all possible winning lines; prevent moves once the game has ended.

How to run: python tic_tac_toe_group_project.py
Needs Python 3 with Tkinter; no extra pip libraries.
"""

# ======================= PART 1: IMPORTS & INITIALIZATION =======================
# Importing packages from Tkinter.
# Tkinter provides the graphical window and buttons; messagebox displays results.
from tkinter import *
from tkinter import messagebox

# This title appears at the top of the game window.
# It replaces the tutorial/example title "GeeksForGeeks-:Tic Tac Toe".
PROJECT_TITLE = "Tic Tac Toe - Computer Group"

# Player1 stores the symbol whose turn it is, and X always starts first.
Player1 = "X"

# stop_game is False while the game is in progress, and becomes True after
# either a winning move or a tie. It prevents any extra move after game over.
stop_game = False

# states is our 3 x 3 game-state matrix. Zero means the square is empty.
# Once a square is played, the matching value becomes "X" or "O".
states = [[0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]

# b is another 3 x 3 matrix, holding the Tkinter Button object in each cell.
# The actual buttons are created later in make_window().
b = [[None, None, None],
     [None, None, None],
     [None, None, None]]

# These values are used to give the board a consistent appearance.
DEFAULT_BG = "#edf2f7"
DEFAULT_ACTIVE_BG = "#dbeafe"
WINNER_BG = "lightgreen"


# ############ START OF HANNANEH'S CODE - PART 2 ############
def clicked(r, c):
    """Run this function when someone clicks a square on the board.

    r = row number (0, 1 or 2), and c = column number (0, 1 or 2).
    """
    # Read and update the Player1 variable created outside the function.
    global Player1

    # Ignore the click if the game has already ended, or the chosen box is used.
    # In the shared draft, this was checked for each player separately.
    if stop_game or states[r][c] != 0:
        return

    # Display the current player's symbol inside the button.
    # configure() changes the visible text on an existing Tkinter button.
    # The state matrix stores the same symbol, allowing us to check the rules.
    if Player1 == "X":
        b[r][c].configure(text="X", fg="#1d4ed8")
        states[r][c] = "X"
    else:
        b[r][c].configure(text="O", fg="#ea580c")
        states[r][c] = "O"

    # After EACH valid move, test whether someone has won or the board is full.
    check_if_win()

    # Switch turns only when the game has NOT ended.
    # This means the winner stays visible as the last player who moved.
    if not stop_game:
        Player1 = "O" if Player1 == "X" else "X"
        status_label.configure(text=f"Player {Player1}'s turn", fg="#334155")
# ############ END OF HANNANEH'S CODE - PART 2 ############


# ############ START OF SOHEIL'S CODE - PART 3 ############
def show_winner(cells, mark):
    """Highlight the three winning boxes and display a winner message.

    cells contains three (row, column) pairs for the winning line.
    mark contains the winner's symbol: "X" or "O".
    """
    global stop_game
    stop_game = True  # Lock the game after a winning move.

    # Change the background color of the three winning buttons.
    # bg: normal button background; activebackground: color when it is pressed.
    for r, c in cells:
        b[r][c].configure(bg=WINNER_BG, activebackground=WINNER_BG)

    # Show the winner both in the window and in a Tkinter message box.
    status_label.configure(text=f"Player {mark} wins!", fg="#166534")
    messagebox.showinfo("Winner", f"{mark} is the winner.")


def check_if_win():
    """Check all rows, columns and diagonals, then check for a tie.

    Important corrections to the group draft:
    1. A column/diagonal winner must be read from a cell IN that winning line.
    2. A tie check belongs AFTER all winning-line checks, not inside the loop.
    3. A tie occurs only when EVERY one of the nine cells is not zero.
    """
    global stop_game

    # Loop i = 0, 1, 2 to inspect all three horizontal and vertical lines.
    for i in range(3):
        # Checking the boxes horizontally (left to right, row i).
        if states[i][0] != 0 and states[i][0] == states[i][1] == states[i][2]:
            show_winner([(i, 0), (i, 1), (i, 2)], states[i][0])
            return  # Stop checking after finding a winner.

        # Checking the boxes vertically (top to bottom, column i).
        # For column i, the winner symbol is states[0][i].
        if states[0][i] != 0 and states[0][i] == states[1][i] == states[2][i]:
            show_winner([(0, i), (1, i), (2, i)], states[0][i])
            return

    # Checking the diagonal from top left to bottom right.
    if states[0][0] != 0 and states[0][0] == states[1][1] == states[2][2]:
        show_winner([(0, 0), (1, 1), (2, 2)], states[0][0])
        return

    # Checking the diagonal from top right to bottom left.
    if states[0][2] != 0 and states[0][2] == states[1][1] == states[2][0]:
        show_winner([(0, 2), (1, 1), (2, 0)], states[0][2])
        return

    # If all nine boxes are occupied and there was NO winning line, it is a tie.
    # all(...) is a reliable way to check that every value is different from 0.
    if all(states[r][c] != 0 for r in range(3) for c in range(3)):
        stop_game = True
        status_label.configure(text="The game is tied!", fg="#92400e")
        messagebox.showinfo("Game Over", "The score is tied.")
# ############ END OF SOHEIL'S CODE - PART 3 ############


# ======================== PART 4: RESET & GAME WINDOW =========================
def new_game():
    """Reset all nine squares and start a new round with Player X."""
    global Player1, stop_game

    # Reset game variables to their starting values.
    Player1 = "X"
    stop_game = False

    # Clear both the stored state and the displayed button in each square.
    for r in range(3):
        for c in range(3):
            states[r][c] = 0
            b[r][c].configure(text="", fg="#0f172a", bg=DEFAULT_BG,
                              activebackground=DEFAULT_ACTIVE_BG)

    status_label.configure(text="Player X's turn", fg="#334155")


def make_window():
    """Create the Tkinter window and all of the GUI buttons."""
    global status_label

    # Tk() creates the application's main graphical window.
    root = Tk()
    root.title(PROJECT_TITLE)
    root.geometry("520x590")
    root.resizable(False, False)  # Keep the 3 x 3 board in a fixed position.
    root.configure(bg="white")

    # Add a heading so the audience can identify the group project.
    Label(root, text="TIC TAC TOE", font=("Arial", 25, "bold"),
          bg="white", fg="#0f172a").pack(pady=(18, 4))
    Label(root, text="Introduction to Computer Science - Group Project",
          font=("Arial", 10), bg="white", fg="#64748b").pack()

    # Show whose turn it is or show the final game result.
    status_label = Label(root, text="Player X's turn", font=("Arial", 15, "bold"),
                         bg="white", fg="#334155")
    status_label.pack(pady=(18, 12))

    # Create a container for the nine buttons.
    board = Frame(root, bg="white")
    board.pack()

    # Nested for loops: i is a row and j is a column.
    # A lambda supplies the correct (row, column) to clicked() for each button.
    for i in range(3):
        for j in range(3):
            b[i][j] = Button(board, height=2, width=5,
                             font=("Arial", 27, "bold"),
                             bg=DEFAULT_BG, activebackground=DEFAULT_ACTIVE_BG,
                             relief="flat",
                             command=lambda r=i, c=j: clicked(r, c))
            b[i][j].grid(row=i, column=j, padx=4, pady=4)

    # Optional improvement: give players an easy way to play another round.
    Button(root, text="New Game", command=new_game,
           font=("Arial", 12, "bold"), bg="#0f766e", fg="white",
           relief="flat", padx=18, pady=8).pack(pady=(17, 0))
    Label(root, text="Two players  |  X starts first",
          font=("Arial", 10), bg="white", fg="#64748b").pack(pady=9)
    return root


# Only open the window when this file is run directly.
# This also lets tests import the functions without opening a game window.
if __name__ == "__main__":
    application = make_window()
    application.mainloop()  # Listen for clicks until the user closes the window.
