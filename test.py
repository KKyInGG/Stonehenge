from typing import List
import string


def drawing(side_length: int) -> List[str]:
    """
    Initialize this Game, using p1_starts to find who the first player is.
    """
    print("enter function")
    stone_list = []
    upper_alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                   'Y', 'Z']
    n = side_length
    cell = 2
    capital = ''
    if side_length >= 1:
        stone_list.append((4 + 2 * n) * ' ' + '@   @\n')
        stone_list.append((3 + 2 * n) * ' ' + '/   /\n')
        print("enter before while")
        while cell <= (n + 1):
            print("enter while")
            for i in range(cell):
                cap = ' - ' + upper_alpha.pop(0)
                capital += cap
            if cell == (n + 1):
                line = '@' + capital + '\n'
                slash = 5 * ' ' + (cell - 1) * '\\ / ' + '\\\n'
                stone_list.append(line)
                stone_list.append(slash)
            else:
                space_num = 2 * (n - cell + 1)
                line = space_num * ' ' + '@' + capital + '   @\n'
                slash = (space_num + 3) * ' ' + cell * '/ \\ ' + '/\n'
                stone_list.append(line)
                stone_list.append(slash)
        cell += 1
        capital2 = ''
        for i in range(n):
            cap2 = ' - ' + upper_alpha.pop(0)
            capital2 += cap2
        stone_list.append(2 * ' ' + capital2 + '   @\n')
        stone_list.append(7 * ' ' + n * '\\   ' + '\n')
        stone_list.append(8 * ' ' + n * '@   ')
    return stone_list
