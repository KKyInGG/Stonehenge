"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
import random
from typing import Any, List, Union
from game import Game
from game_state import GameState


def get_each_substate_score(game: Game, state: GameState) -> int:
    """
    Return a interger that represents the score of the game's state about game
    for the current player.
    """
    if game.is_over(state):
        return get_score_for_current_state(game, state)
    substates = [state.make_move(move)
                 for move in state.get_possible_moves()]
    return max([(-1 * get_each_substate_score(game, substate))
                for substate in substates])


def get_score_for_current_state(game: Game, state: GameState) -> int:
    """
    Return a interger that represents the score of the game's state about game
    for the current player without recursion.
    """
    previous_state = game.current_state
    game.current_state = state
    current_player = state.get_current_player_name()
    last_player = 'p1'
    if current_player == 'p1':
        last_player = 'p2'
    if game.is_winner(current_player):
        game.current_state = previous_state
        return 1
    elif game.is_winner(last_player):
        game.current_state = previous_state
        return -1
    game.current_state = previous_state
    return 0


class TreeState:
    """
    Imcomplete the TreeState Class.
    state - the current game state
    score - the score that each state should have
    children - a list of substates that produce by current game state
    """
    state: GameState
    score: Union[int, None]
    children: List

    def __init__(self, state: GameState) -> None:
        """
        Initialize a class TreeState.
        """
        self.state = state
        self.score = None
        self.children = None


# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Game) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def recursive_strategy(game: Any) -> Any:
    """
    Return a move for game through estimating the best outcome for the current
    player by recursive strategy.
    """
    all_moves = game.current_state.get_possible_moves()
    substates1 = [game.current_state.make_move(m) for m in all_moves]
    score_list = [-1 * get_each_substate_score(game, sub) for sub in substates1]
    random_choose_list = [i for i in
                          range(len(score_list)) if score_list[i] == 1]
    if random_choose_list == []:
        move = random.choice(all_moves)
    else:
        move = all_moves[random.choice(random_choose_list)]
    return game.str_to_move(str(move))


def iterative_strategy(game: Any) -> Any:
    """
    Return a move for game through estimating the best outcome for the current
    player by iterative strategy.
    """
    all_moves = game.current_state.get_possible_moves()
    cur_tree_state = TreeState(game.current_state)
    stack = [cur_tree_state]
    score_list = []
    while stack:
        last_tree_state = stack.pop()
        last_state = last_tree_state.state
        if not last_tree_state.children:
            all_possible_state = [last_state.make_move(move) for move in
                                  last_state.get_possible_moves()]
            if game.is_over(last_state):
                last_tree_state.score = \
                    get_score_for_current_state(game, last_state)
                score_list.append(last_tree_state.score)
            else:
                last_tree_state.children = [TreeState(states) for
                                            states in all_possible_state]
                stack.append(last_tree_state)
                stack.extend(last_tree_state.children)
        else:
            last_tree_state.score = max([-1 * children.score for children in
                                         last_tree_state.children])
    cur_tree_state_children = cur_tree_state.children
    random_win_list = [i for i in range(len(cur_tree_state_children))
                       if cur_tree_state.children[i].score == -1]
    if random_win_list == []:
        move = random.choice(all_moves)
    else:
        move = all_moves[random.choice(random_win_list)]
    return game.str_to_move(str(move))


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
