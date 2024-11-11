def evaluateBoard_temp(boardState):
    score = 0
    o_player = 2
    x_player = 1
    boardState.printBoard()

    size = boardState.size
    win_length = boardState.max_item_win
    win_lines_X = 0
    win_lines_O = 0

    if check_win(boardState, x_player):
        score -= 100
    if check_win(boardState, o_player):
        score += 100

    # Duyet theo hang
    for row in range(boardState.size):
        for col in range(size - win_length + 1):
            countO = 0  # so quan O
            countX = 0  # so quan X
            count_empty = 0
            for i in range(boardState.max_item_win):
                if boardState.getPosition(row, col + i) == x_player:  # neu quan do la cua X
                    countX += 1  # tang so quan X
                if boardState.getPosition(row, col + i) == o_player:  # neu quan do la cua O
                    countO += 1  # tang so quan O
                if boardState.getPosition(row, col + i) == 0:
                    count_empty += 1
            if count_empty != win_length:
                if countX + count_empty == win_length:
                    win_lines_X += 1
                if countO + count_empty == win_length:
                    win_lines_O += 1

    # Duyet theo cot
    for col in range(boardState.size):
        for row in range(size - win_length + 1):
            countO = 0  # so quan O
            countX = 0  # so quan X
            count_empty = 0
            for i in range(boardState.max_item_win):
                if boardState.getPosition(row + i, col) == x_player:  # neu quan do la cua X
                    countX += 1  # tang so quan X
                if boardState.getPosition(row + i, col) == o_player:  # neu quan do la cua O
                    countO += 1  # tang so quan O
                if boardState.getPosition(row + i, col) == 0:
                    count_empty += 1
            if count_empty != win_length:
                if countX + count_empty == win_length:
                    win_lines_X += 1
                if countO + count_empty == win_length:
                    win_lines_O += 1

    # Duyet theo duong cheo thuan \ (cheo xuong)
    for col in range(size - win_length + 1):
        for row in range(size - win_length + 1):
            countO = 0  # so quan O
            countX = 0  # so quan X
            count_empty = 0
            for i in range(boardState.max_item_win):
                if boardState.getPosition(row + i, col + i) == x_player:  # neu quan do la cua X
                    countX += 1  # tang so quan X
                if boardState.getPosition(row + i, col + i) == o_player:  # neu quan do la cua O
                    countO += 1  # tang so quan O
                if boardState.getPosition(row + i, col + i) == 0:
                    count_empty += 1

            if count_empty != win_length:
                if countX + count_empty == win_length:
                    win_lines_X += 1
                if countO + count_empty == win_length:
                    win_lines_O += 1

    # Duyet theo duong cheo nghich / (cheo len)
    for row in range(win_length - 1, size):
        for col in range(size - win_length + 1):
            countO = 0  # so quan O
            countX = 0  # so quan X
            count_empty = 0
            for i in range(boardState.max_item_win):
                if boardState.getPosition(row - i, col + i) == x_player:  # neu quan do la cua X
                    countX += 1  # tang so quan X
                if boardState.getPosition(row - i, col + i) == o_player:  # neu quan do la cua O
                    countO += 1  # tang so quan O
                if boardState.getPosition(row - i, col + i) == 0:
                    count_empty += 1

            if count_empty != win_length:
                if countX + count_empty == win_length:
                    win_lines_X += 1
                if countO + count_empty == win_length:
                    win_lines_O += 1
    score += win_lines_O
    score -= win_lines_X
    return score


def check_win(boardState, player):
    for row in range(boardState.size):
        for col in range(boardState.size):
            if boardState.squares[row][col] == player:
                if boardState.final_state(row, col) == player:
                    return True
    return False


def evaluateBoard(boardState, player):
    score = 0
    o_player = 2
    x_player = 1
    boardState.printBoard()

    size = boardState.size
    win_length = boardState.max_item_win
    win_lines_X = 0
    win_lines_O = 0

    # Duyet theo hang
    for row in range(boardState.size):
        for col in range(size - win_length + 1):
            countO = 0  # so quan O
            countX = 0  # so quan X
            count_empty = 0
            for i in range(boardState.max_item_win):
                if boardState.getPosition(row, col + i) == x_player:  # neu quan do la cua X
                    countX += 1  # tang so quan X
                if boardState.getPosition(row, col + i) == o_player:  # neu quan do la cua O
                    countO += 1  # tang so quan O
                if boardState.getPosition(row, col + i) == 0:
                    count_empty += 1
            if count_empty != win_length:
                if countX == win_length:
                    win_lines_X += 100
                elif countX + count_empty == win_length:
                    win_lines_X += 1
                if countO == win_length:
                    win_lines_O += 100
                elif countO + count_empty == win_length:
                    win_lines_O += 1

    # Duyet theo cot
    for col in range(boardState.size):
        for row in range(size - win_length + 1):
            countO = 0  # so quan O
            countX = 0  # so quan X
            count_empty = 0
            for i in range(boardState.max_item_win):
                if boardState.getPosition(row + i, col) == x_player:  # neu quan do la cua X
                    countX += 1  # tang so quan X
                if boardState.getPosition(row + i, col) == o_player:  # neu quan do la cua O
                    countO += 1  # tang so quan O
                if boardState.getPosition(row + i, col) == 0:
                    count_empty += 1
            if count_empty != win_length:
                if countX == win_length:
                    win_lines_X += 100
                elif countX + count_empty == win_length:
                    win_lines_X += 1
                if countO == win_length:
                    win_lines_O += 100
                elif countO + count_empty == win_length:
                    win_lines_O += 1

    # Duyet theo duong cheo thuan \ (cheo xuong)
    for col in range(size - win_length + 1):
        for row in range(size - win_length + 1):
            countO = 0  # so quan O
            countX = 0  # so quan X
            count_empty = 0
            for i in range(boardState.max_item_win):
                if boardState.getPosition(row + i, col + i) == x_player:  # neu quan do la cua X
                    countX += 1  # tang so quan X
                if boardState.getPosition(row + i, col + i) == o_player:  # neu quan do la cua O
                    countO += 1  # tang so quan O
                if boardState.getPosition(row + i, col + i) == 0:
                    count_empty += 1

            if count_empty != win_length:
                if countX == win_length:
                    win_lines_X += 100
                elif countX + count_empty == win_length:
                    win_lines_X += 1
                if countO == win_length:
                    win_lines_O += 100
                elif countO + count_empty == win_length:
                    win_lines_O += 1

    # Duyet theo duong cheo nghich / (cheo len)
    for row in range(win_length - 1, size):
        for col in range(size - win_length + 1):
            countO = 0  # so quan O
            countX = 0  # so quan X
            count_empty = 0
            for i in range(boardState.max_item_win):
                if boardState.getPosition(row - i, col + i) == x_player:  # neu quan do la cua X
                    countX += 1  # tang so quan X
                if boardState.getPosition(row - i, col + i) == o_player:  # neu quan do la cua O
                    countO += 1  # tang so quan O
                if boardState.getPosition(row - i, col + i) == 0:
                    count_empty += 1

            if count_empty != win_length:
                if countX == win_length:
                    win_lines_X += 100
                elif countX + count_empty == win_length:
                    win_lines_X += 1
                if countO == win_length:
                    win_lines_O += 100
                elif countO + count_empty == win_length:
                    win_lines_O += 1
    if player == 2:
        return 1.2 * win_lines_O - win_lines_X
    else:
        return win_lines_O - 1.2 * win_lines_X
