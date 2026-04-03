import random
import json
from itertools import combinations
import matplotlib.pyplot as plt

# Global state dictionary
steps = {}
valueMap = [8, 3, 4, 1, 5, 9, 6, 7, 2] # We emply a value map or a magic square here based off of the idea of the game of 15. Instead of manually detecting if there are adjacent games that line up we just use the logic of the game of 15


def check_win(board, player):
    slots = [valueMap[i] for i in range(9) if board[i] == player] # we map the value map onto the played moves, so we can conduct the game of 15
    if len(slots) < 3: # the win condition is only checked when we have more than three moves of the player already in play
        return False
    return any(sum(c) == 15 for c in combinations(slots, 3))


def genStep(board, turn=0): # we first generate all possible iterations of our tic tac toe game using a recurisve function
    b_tup = tuple(board) # we use a tuple here because dict keys cannot be lists. We use a dictionary to store our game states so that every board is both a key and a value, so when we are given a board in game, we can go to steps to figure out the possible subsequent moves.
    if b_tup in steps: return
    steps[b_tup] = []
    if check_win(board, 1) or check_win(board, -1) or turn == 9: return # we check every pass through of the recursive function if that game is over, if it is we return back to the prior recursive function

    player = 1 if turn % 2 == 0 else -1 #in our code player 1 is denoted as 1, and player 2 is denoted by -1 in our code
    for i in range(9): #here we use a loop to recursively generate a move for each turn until the game is over. The game per pass through gets added a move, this ensures that all game states are obtained
        if board[i] == 0:
            newBoard = list(board)
            newBoard[i] = player
            steps[b_tup].append(newBoard) #
            genStep(newBoard, turn + 1)


def playStep(board, turn=0):
    b_tup = tuple(board)
    if not steps[b_tup]: return 'loss' #if there are no future moves, that means that when generating, the prior move was the final move. ANd if the prior move was the final move, that of course means that the prior move was the final move, and hence loss.

    next_board = random.choice(steps[b_tup]) # we randomly select the next move, and if we run the program enougn times then we should be able to reach an optimal play level.
    player = 1 if turn % 2 == 0 else -1 # as above

    if check_win(next_board, player): return 'win' # if the next move results in a win, then we return a win
    if turn == 8: return 'tie' # turn 8 here is actually the 9th turn in the program, so if there is not loss or win, then it is a tie

    outcome = playStep(next_board, turn + 1) # If there is no win or loss, we play the next move by passing the new board back in.
    #Here we are now done with the run of the game and go on to pruning incorrect consequences. We keep moves that win and tie, and remove moves that lose.
    if outcome == 'win':
        if next_board in steps[b_tup]: steps[b_tup].remove(next_board) # if we got returned a win, that means the subsequent trun resulted in a win. Remember this is recursive. As such, we want to eliminate the move that allowed the other player to win. This is our pruning.
        if not steps[b_tup]: return 'loss'
        return 'neutral'

    if outcome == 'loss': return 'win' # we alternate here, which hopefully makes sense. If player 1 won, then the prior player which was player 2, that now gets returned the function, has lost
    return outcome


def evaluate_agent(current_steps, num_games=100):
    """Evaluates the AI (-1) against a purely random player (1)."""
    wins, losses, ties = 0, 0, 0
    for _ in range(num_games):
        board = [0] * 9
        turn = 0
        while True:
            player = 1 if turn % 2 == 0 else -1
            if check_win(board, 1):
                losses += 1
                break
            if check_win(board, -1):
                wins += 1
                break
            if turn == 9:
                ties += 1
                break

            if player == 1:
                # Random opponent move
                empty = [i for i, x in enumerate(board) if x == 0]
                board[random.choice(empty)] = 1
            else:
                # AI move based on current pruned tree
                b_tup = tuple(board)
                valid_states = current_steps.get(b_tup, [])
                if valid_states:
                    # FIX: Cast to list to create a copy, preventing dictionary mutation
                    board = list(random.choice(valid_states))
                else:
                    empty = [i for i, x in enumerate(board) if x == 0]
                    board[random.choice(empty)] = -1
            turn += 1
    return wins, losses, ties


# --- Training and Graphing Logic ---
genStep([0] * 9)

epochs = []
win_rates = []
loss_rates = []
tie_rates = []

total_iterations = 5000000
eval_interval = 100000  # Evaluate every 1000 games

for i in range(total_iterations):
    playStep([0] * 9, 0)

    # Run evaluation
    if i % eval_interval == 0:
        w, l, t = evaluate_agent(steps, num_games=100)
        epochs.append(i)
        win_rates.append(w)
        loss_rates.append(l)
        tie_rates.append(t)

# Export data
restructured_data = [[list(k), v] for k, v in steps.items()]
with open("data_list.json", "w") as f:
    json.dump(restructured_data, f)

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(epochs, win_rates, label='AI Wins', color='blue')
plt.plot(epochs, loss_rates, label='AI Losses', color='red')
plt.plot(epochs, tie_rates, label='Ties', color='green')

plt.title('AI Performance During Training (vs. Random Opponent)')
plt.xlabel('Training Iterations')
plt.ylabel('Outcomes (per 100 games)')
plt.legend()
plt.grid(True)
plt.savefig('training_graph.png')
plt.show()