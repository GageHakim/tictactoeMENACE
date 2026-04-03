import json
import random
from itertools import combinations


# 1. Load and Reconstruct the Model (Note that this playing is created completely by gemini, and is only used to have a person play against it to test its abilities. Not a part of the core project but good if you want to try to beat it.
def load_model(filename="data_list.json"):
    try:
        with open(filename, "r") as f:
            raw_data = json.load(f)
        # Convert the list of [key, value] pairs back into a dictionary with tuple keys
        # The values remain lists of lists (the next valid board states)
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

    board = [0] * 9
    print("Welcome to Tic-Tac-Toe vs. AI")
    print("Positions are mapped 1-9, left-to-right, top-to-bottom.")

    # Human is 1 ('X'), AI is -1 ('O')
    turn = 0

    while True:
        print_board(board)
        player = 1 if turn % 2 == 0 else -1

        # Check for terminal states before the turn begins
        if check_win(board, 1):
            print("Human (X) wins!")
            break
        if check_win(board, -1):
            print("AI (O) wins!")
            break
        if turn == 9:
            print("It's a tie!")
            break

        if player == 1:
            # Human Turn
            move_idx = get_human_move(board)
            board[move_idx] = 1
        else:
            # AI Turn
            print("AI is making a move...")
            b_tup = tuple(board)

            # AI Logic: Look up the current board state in the trained data
            valid_next_states = steps.get(b_tup, [])

            if valid_next_states:
                # Pick a random move from the remaining valid options
                board = random.choice(valid_next_states)
            else:
                # Fallback: If the training data has pruned all moves (believing it's a forced loss),
                # or the state wasn't explored, pick a random valid empty square.
                empty_spots = [i for i, x in enumerate(board) if x == 0]
                if empty_spots:
                    fallback_move = random.choice(empty_spots)
                    board[fallback_move] = -1
                else:
                    break  # Should not be reached due to turn counter, but safe to include

        turn += 1


if __name__ == "__main__":
    play_game()