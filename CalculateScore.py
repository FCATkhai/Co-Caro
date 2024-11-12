def evaluateBoard(boardState, player):
    boardState.printBoard()

    size = boardState.size
    win_length = boardState.max_item_win
    player_win_lines = 0
    opponent_win_lines = 0

    # Duyet theo hang
    for row in range(boardState.size):
        for col in range(size - win_length + 1):
            player_count = 0  # so quan O
            opponent_count = 0  # so quan X
            count_empty = 0
            for i in range(boardState.max_item_win):
                if boardState.getPosition(row, col + i) == player:  # neu quan do la cua X
                    player_count += 1  # tang so quan X
                elif boardState.getPosition(row, col + i) == 0:
                    count_empty += 1
                else:  # neu quan do la cua O
                    opponent_count += 1  # tang so quan O

            if count_empty != win_length:
                if player_count == win_length:
                    player_win_lines += 100
                elif player_count + count_empty == win_length:
                    player_win_lines += player_count ** 2
                if opponent_count == win_length:
                    opponent_win_lines += 100
                elif opponent_count + count_empty == win_length:
                    opponent_win_lines += opponent_count ** 2

    # Duyet theo cot
    for col in range(boardState.size):
        for row in range(size - win_length + 1):
            player_count = 0  # so quan O
            opponent_count = 0  # so quan X
            count_empty = 0
            for i in range(boardState.max_item_win):
                if boardState.getPosition(row + i, col) == player:  # neu quan do la cua X
                    player_count += 1  # tang so quan X
                elif boardState.getPosition(row + i, col) == 0:
                    count_empty += 1
                else:  # neu quan do la cua O
                    opponent_count += 1  # tang so quan O

            if count_empty != win_length:
                if player_count == win_length:
                    player_win_lines += 100
                elif player_count + count_empty == win_length:
                    player_win_lines += player_count ** 2
                if opponent_count == win_length:
                    opponent_win_lines += 100
                elif opponent_count + count_empty == win_length:
                    opponent_win_lines += opponent_count ** 2

    # Duyet theo duong cheo thuan \ (cheo xuong)
    for col in range(size - win_length + 1):
        for row in range(size - win_length + 1):
            player_count = 0  # so quan O
            opponent_count = 0  # so quan X
            count_empty = 0
            for i in range(boardState.max_item_win):
                if boardState.getPosition(row + i, col + i) == player:  # neu quan do la cua X
                    player_count += 1  # tang so quan X
                elif boardState.getPosition(row + i, col + i) == 0:
                    count_empty += 1
                else:  # neu quan do la cua O
                    opponent_count += 1  # tang so quan O

            if count_empty != win_length:
                if player_count == win_length:
                    player_win_lines += 100
                elif player_count + count_empty == win_length:
                    player_win_lines += player_count ** 2
                if opponent_count == win_length:
                    opponent_win_lines += 100
                elif opponent_count + count_empty == win_length:
                    opponent_win_lines += opponent_count ** 2

    # Duyet theo duong cheo nghich / (cheo len)
    for row in range(win_length - 1, size):
        for col in range(size - win_length + 1):
            player_count = 0  # so quan O
            opponent_count = 0  # so quan X
            count_empty = 0
            for i in range(boardState.max_item_win):
                if boardState.getPosition(row - i, col + i) == player:  # neu quan do la cua X
                    player_count += 1  # tang so quan X
                elif boardState.getPosition(row - i, col + i) == 0:
                    count_empty += 1
                else:  # neu quan do la cua O
                    opponent_count += 1  # tang so quan O

            if count_empty != win_length:
                if player_count == win_length:
                    player_win_lines += 100
                elif player_count + count_empty == win_length:
                    player_win_lines += player_count ** 2
                if opponent_count == win_length:
                    opponent_win_lines += 100
                elif opponent_count + count_empty == win_length:
                    opponent_win_lines += opponent_count ** 2

    return player_win_lines - opponent_win_lines

