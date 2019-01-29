"""
An implementation of Stonehenge.
"""
from typing import List
from game import Game
from game_state import GameState


def change_ley_line(cap_list: List[str], index: int) -> str:
    """
    Return a string representation of the current player name who occupied at
    least half of the cells in the cap_list of that index.

    >>> cap_list = ['1B', 'C ']
    >>> '1' == change_ley_line(cap_list, 0)
    True
    """
    count1 = 0
    count2 = 0
    count_blank = 0
    for t in range(len(cap_list)):
        if cap_list[t][index] == '1':
            count1 += 1
        elif cap_list[t][index] == '2':
            count2 += 1
        elif cap_list[t][index] == ' ':
            count_blank += 1
    result = '@'
    if count1 >= (len(cap_list) - count_blank) / 2:
        result = '1'
    elif count2 >= (len(cap_list) - count_blank) / 2:
        result = '2'
    return result


def change_ley_line_horizontal(cap_list: List[str], line_index: int) -> str:
    """
    Return a string representation of the current player name who occupied at
    least half of the cells in the cap_list of the same line_index.

    >>> cap_list = ['1B', 'C']
    >>> '1' == change_ley_line_horizontal(cap_list, 0)
    True
    """
    count1 = 0
    count2 = 0
    line = cap_list[line_index]
    for c in range(len(line)):
        if line[c] == '1':
            count1 += 1
        elif line[c] == '2':
            count2 += 1
    result = '@'
    if count1 >= len(line) / 2:
        result = '1'
    elif count2 >= len(line) / 2:
        result = '2'
    return result


class StonehengeState(GameState):
    """
    The state of a game at a certain point in time.

    === Attributes ===
    side_length - the side length of board
    ley_line - a list contains all ley_line remark
    cap_list - a list contains all cells in the board
    """
    side_length: int
    ley_line: List[str]
    cap_list: List[str]

    def __init__(self, is_p1_turn: bool, side_length: int,
                 ley_line: List[str], cap_list: List[str]) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        >>> ley_line = ['@','@','@','@','@','@']
        >>> Stonehenge = StonehengeState(True, 1, ley_line, ['AB', 'C'])
        >>> Stonehenge.p1_turn == True
        True
        >>> Stonehenge.side_length == 1
        True
        >>> Stonehenge.ley_line == ['@','@','@','@','@','@']
        True
        >>> Stonehenge.cap_list == ['AB', 'C']
        True
        """
        GameState.__init__(self, is_p1_turn)
        self.side_length = side_length
        self.ley_line = ley_line
        self.cap_list = cap_list

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        stone_list = []
        cell = 2
        if self.side_length >= 1:
            stone_list.append((4 + 2 * self.side_length) * ' '
                              + self.ley_line[self.side_length + 1] + '   '
                              + self.ley_line[self.side_length + 2] + '\n')
            stone_list.append((3 + 2 * self.side_length) * ' ' + '/   /\n')
            while cell <= (self.side_length + 1):
                capital = ''
                for i in range(cell):
                    capital += ' - ' + self.cap_list[cell - 2][i]
                if cell == (self.side_length + 1):
                    line = self.ley_line[self.side_length - 1] + capital + '\n'
                    slash = 5 * ' ' + (cell - 1) * '\\ / ' + '\\\n'
                    stone_list.append(line)
                    stone_list.append(slash)
                else:
                    space_num = 2 * (self.side_length - cell + 1)
                    line = space_num * ' ' + self.ley_line[cell - 2] + capital \
                        + '   ' + self.ley_line[cell +
                                                self.side_length + 1] + '\n'
                    slash = (space_num + 3) * ' ' + cell * '/ \\ ' + '/\n'
                    stone_list.append(line)
                    stone_list.append(slash)
                cell += 1
            capital2 = ''
            for i in range(self.side_length):
                capital2 += ' - ' + self.cap_list[-1][i]
            stone_list.append(2 * ' ' + self.ley_line[self.side_length]
                              + capital2 + '   ' +
                              self.ley_line[-1] + '\n')
            stone_list.append(7 * ' ' + self.side_length * '\\   ' + '\n')
            string1 = 8 * ' '
            index4 = 2 * (self.side_length + 1)
            for j in range(self.side_length):
                string1 += self.ley_line[index4 + j] + '   '
            stone_list.append(string1)
        return_string = ''
        for s in stone_list:
            return_string += s
        return return_string

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.

        >>> ley_line = ['@','@','@','@','@','@']
        >>> Stonehenge = StonehengeState(True, 1, ley_line, ['AB', 'C'])
        >>> Stonehenge.get_possible_moves() == ['A','B','C']
        True
        """
        times1 = 0
        times2 = 0
        for char in self.ley_line:
            if char == '1':
                times1 += 1
            if char == '2':
                times2 += 1
        standard = (len(self.ley_line)) / 2
        if times1 >= standard or times2 >= standard:
            return []
        return [cap for line in self.cap_list for cap in line
                if cap.isupper()]

    def make_move(self, move: str) -> "StonehengeState":
        """
        Return the StonehengeState that results from applying move to
        this StonehengeState.

        >>> ley_line = ['@','@','@','@','@','@']
        >>> Stonehenge = StonehengeState(True, 1, ley_line, ['AB', 'C'])
        >>> new_state = Stonehenge.make_move('A')
        >>> new_state.p1_turn
        False
        >>> new_state.ley_line
        ['1', '@', '1', '@', '1', '@']
        >>> new_state.cap_list
        ['1B', 'C']
        """
        n = self.side_length
        ley_line_list = self.ley_line[:]
        cap_list = self.cap_list[:]
        for j in range(len(cap_list)):
            for i in range(len(cap_list[j])):
                if cap_list[j][i] == move:
                    cap_list[j] = cap_list[j][:i] + \
                        self.get_current_player_name()[1] + cap_list[j][i + 1:]
        cap_list2 = cap_list[:]
        cap_list3 = cap_list[:]
        for l in range(n + 1):
            if ley_line_list[l] == "@":
                ley_line_list[l] = change_ley_line_horizontal(cap_list, l)
        for num in range(len(cap_list)):
            if num < n - 1:
                cap_list2[num] = cap_list2[num][:] + \
                                ((n + 1) - len(cap_list2[num])) * ' '
            elif num > n - 1:
                cap_list2[num] = ' ' + cap_list2[num][:]
        for r in range(n + 1, 2 * n + 2):
            index = r - n - 1
            if ley_line_list[r] == "@":
                ley_line_list[r] = change_ley_line(cap_list2, index)
        for num in range(len(cap_list)):
            if num < n - 1:
                cap_list3[num] = ((n + 1) - len(cap_list3[num])) * \
                                ' ' + cap_list3[num][:]
            elif num > n - 1:
                cap_list3[num] = cap_list3[num][:] + ' '
        for r in range(2 * n + 2, len(ley_line_list)):
            index1 = r - (2 * n + 2)
            if ley_line_list[r] == "@":
                ley_line_list[r] = change_ley_line(cap_list3, index1)
        return StonehengeState(not self.p1_turn, n, ley_line_list, cap_list)

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        return "P1's Turn: {} - Board: {}".format(self.p1_turn,
                                                  str(self))

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.

        >>> ley_line = ['@','@','@','@','@','@']
        >>> Stonehenge = StonehengeState(True, 1, ley_line, ['AB', 'C'])
        >>> new_state = Stonehenge.make_move('A')
        >>> new_state.rough_outcome()
        -1
        """
        substates = [self.make_move(move) for move in self.get_possible_moves()]
        if any([is_over_state(substate) for substate in substates]):
            return self.WIN
        sub_substates = []
        for substate in substates:
            sub_substate = [substate.make_move(move)
                            for move in substate.get_possible_moves()]
            each_substate = [is_over_state(sub) for sub in sub_substate]
            sub_substates.append(each_substate)
        count_lose = [1 for sub_list in sub_substates if True in sub_list]
        if len(count_lose) == len(sub_substates):
            return self.LOSE
        return self.DRAW


def is_over_state(substate: StonehengeState) -> bool:
    """
    Return True iff the substate is over.

    >>> ley_line = ['@','@','@','@','@','@']
    >>> Stonehenge = StonehengeState(True, 1, ley_line, ['AB', 'C'])
    >>> new_state = Stonehenge.make_move('A')
    >>> True == is_over_state(new_state)
    True
    """
    times1 = 0
    times2 = 0
    for char in substate.ley_line:
        if char == '1':
            times1 += 1
        if char == '2':
            times2 += 1
    standard = len(substate.ley_line) / 2
    return times1 >= standard or times2 >= standard or \
        substate.get_possible_moves() == []


class StonehengeGame(Game):
    """
    Abstract class for StonehengeGame to be played with two players.

    === Attributes ===
    current_state: current state of the game
    """
    current_state: StonehengeState

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        """
        side_length = int(input("Enter the side length of the board:"))
        upper_alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                       'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                       'U', 'V', 'W', 'X', 'Y', 'Z']
        n = side_length
        ley_line = ['@' for i in range(3 * (n + 1))]
        cell = 2
        cap_list = []
        while cell <= n + 1:
            cap5 = ''
            i = 0
            while i < cell:
                capa = upper_alpha.pop(0)
                cap5 += capa
                i += 1
            cap_list.append(cap5)
            cell += 1
        cap6 = ''
        t = 0
        while t < n:
            capa = upper_alpha.pop(0)
            cap6 += capa
            t += 1
        cap_list.append(cap6)
        self.current_state = StonehengeState(p1_starts, side_length,
                                             ley_line, cap_list)

    def get_instructions(self):
        """
        Return the instructions for this Game.

        :return: The instructions for this Game.
        :rtype: str
        """
        instructions = "Players take turns claiming cells (in the diagram: " \
                       "circles labelled with a capital letter). When a " \
                       "player captures at least half of the cells in a " \
                       "ley-line (in the diagram: hexagons with a line " \
                       "connecting it to cells), then the player " \
                       "captures that ley-line. The first player to capture " \
                       "at least half of the ley-lines is the winner. " \
                       "A ley-line, once claimed, cannot be taken " \
                       "by the other player."
        return instructions

    def is_over(self, state: "StonehengeState") -> bool:
        """
        Return whether or not this game is over.

        :return: True if the game is over, False otherwise.
        :rtype: bool
        """
        return is_over_state(state)

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.

        :param player: The player to check.
        :type player: str
        :return: Whether player has won or not.
        :rtype: bool
        """
        return (self.current_state.get_current_player_name() != player
                and self.is_over(self.current_state))

    def str_to_move(self, string: str) -> str:
        """
        Return the move that string represents. If string is not a move,
        return an invalid move.

        :param string:
        :type string:
        :return:
        :rtype:
        """
        if not string.strip().isupper():
            return '-1'
        return string


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
