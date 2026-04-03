import json
import random
from itertools import combinations

def load_model(filename="data_list.json"):
    try:
        with open(filename, "r") as f:
            raw_data = json.load(f)
        return {tuple(k): v for k, v in raw_data}
    except FileNotFoundError:
        print(f"Error: {filename} not found. Run the training script first.")
        return None

valueMap = [8, 3, 4, 1, 5, 9, 6, 7, 2]

def check_win(board, player):
    """Evaluates the board using the magic square method."""
    slots = [valueMap[i] for i in range(9) if board[i] == player]
    if len(slots) < 3:
        return False
    return any(sum(c) == 15 for c in combinations(slots, 3))

def print_board(board):
    """Renders the board state visually."""
    symbols = {1: 'X', -1: 'O', 0: ' '}
    b = [symbols[x] for x in board]
    print(
        f"\n {b[0]} | {b[1]} | {b[2]} \n---+---+---\n {b[3]} | {b[4]} | {b[5]} \n---+---+---\n {b[6]} | {b[7]} | {b[8]} \n")

def get_human_move(board):
    """Prompts the human for a valid move."""
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            if move < 0 or move > 8:
                print("Invalid input. Choose a number between 1 and 9.")
            elif board[move] != 0:
                print("That space is already taken.")
            else:
                return move
        except ValueError:
            print("Invalid input. Please enter a number.")

def play_game():
    steps = load_model()
    if not steps:
        return

    print("Tic-Tac-Toe vs. AI")
    print("Positions are mapped 1-9, left-to-right, top-to-bottom.")

    # Determine turn order
    while True:
        order = input("Do you want to go first (1) or second (2)? ")
        if order in ['1', '2']:
            break
            print("Invalid choice. Enter 1 or 2.")

    # Assign values based on turn order
    if order == '1':
        human_val = 1
        ai_val = -1
        print("You are playing as 'X' and will go first.")
    else:
        human_val = -1
        ai_val = 1
        print("You are playing as 'O' and will go second. AI plays 'X'.")

    board = [0] * 9
    turn = 0

    while turn < 9:
        print_board(board)
        # current_player is 1 on even turns (0, 2, 4), -1 on odd turns (1, 3, 5)
        current_player = 1 if turn % 2 == 0 else -1

        if current_player == human_val:
            # Human Turn
            move_idx = get_human_move(board)
            board[move_idx] = human_val
        else:
            # AI Turn
            print("AI is making a move...")
            b_tup = tuple(board)
            valid_next_states = steps.get(b_tup, [])

            if valid_next_states:
                board = random.choice(valid_next_states)
            else:
                empty_spots = [i for i, x in enumerate(board) if x == 0]
                if empty_spots:
                    fallback_move = random.choice(empty_spots)
                    board[fallback_move] = ai_val

        # Check for terminal states immediately after a move is made
        if check_win(board, human_val):
            print_board(board)
            print("Human wins!")
            return
        if check_win(board, ai_val):
            print_board(board)
            print("AI wins!")
            return

        turn += 1

    print_board(board)
    print("It's a tie!")

if __name__ == "__main__":
    play_game()