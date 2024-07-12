import random
import numpy as np


# ===== Computer_AI Class ===== #
class Computer_AI:
    # init function
    def __init__(self):
        # NOTE:

            #  'neg_diagonal'  |   'diagonal'
            # ===========  |  ===================
            #    *         |             *     
            #     *        |            *      
            #      *       |           *       

        # Get Moves Reference
        self.moves = None

        # Get Game Class Reference
        self.game_class_reference = None

        # Get Computer AI Difficulty
        self.computer_ai_difficulty = None

        # Store The Computer AI's Last Move
        self.computer_last_move = None

    # get_best_move method
    def get_best_move(self):
        """
            The purpose of this function is to return the computer's best move. The move will vary depending on the ai difficulty.
        """
        # Check if AI is easy
        if self.computer_ai_difficulty == 0: computer_best_move = self.easy_ai()

        # Check if AI is 'normal'
        if self.computer_ai_difficulty == 1: computer_best_move = self.normal_ai()

        # Check if AI is 'hard'
        if self.computer_ai_difficulty == 2: computer_best_move = self.hard_ai()

        # Store the best move in the 'computer_last_move'
        self.computer_last_move = computer_best_move

        # Return the computer's move
        return computer_best_move

    # +----------------------------------------+
    # |                                        |
    # |           Create AI Functions          |
    # |                                        |
    # +----------------------------------------+
    # easy_ai method
    def easy_ai(self):
        """
            This function is supposed to return the optimal move for EasyAI.
        """
        # Store the board_positions in 'board' variable
        board = self.game_class_reference.board_positions

        # Store the board_size in 'board_size' variable
        board_size = self.game_class_reference.board_size

        # Store the board_available_cell_positions in 'board_available_cell_positions' variable
        board_available_cell_positions = self.game_class_reference.board_available_cell_positions

        # Store the win_length in 'win_length' variable
        win_length = self.game_class_reference.win_length

        # Store the player's last move in 'player_last_move' variable
        player_last_move = self.game_class_reference.player_last_move

        # Store the moves in 'moves' variable
        moves = self.game_class_reference.total_game_moves

        # Get optimal move
        computer_best_move = self.get_optimal_move(board, board_size, win_length)

        # Check if the board size is 3x3
        if board_size == 3:
            
            # If moves is greater than or equal to four, then make a logical move
            if moves >= 4:
                print("Make a logical move")
                random_move = random.choice(computer_best_move[0])
                return random_move[0]*board_size+random_move[1]
                
            # If moves is lower than four, then make a random move
            else:
                print("Make a random move")
                return random.choice(board_available_cell_positions)
                

        # Check it the board size is greater than 3x3
        else:

            # If the computer makes the first move, then let make a random move
            if moves == 0:
                print("Make a random move")
                return random.choice(board_available_cell_positions)

            # If the player made the first move, then let the computer make a logical move
            elif moves == 1 and player_last_move:
                print("Make a logical move")
                available_moves = []
                for move in [1, 7, 8, 9]:
                    if player_last_move+move < board_size*board_size: available_moves.append(player_last_move+move)
                    if player_last_move-move >= 0: available_moves.append(player_last_move-move)
                return random.choice(available_moves)

            # If 2 or 3 moves have been made, then let the computer make a random move
            elif moves == 2 or moves == 3:
                print("Make a random move")
                return random.choice(board_available_cell_positions)

            else:
                print("Make a logical move")
                random_move = random.choice(computer_best_move[0])
                return random_move[0]*board_size+random_move[1]
                
    # normal_ai method
    def normal_ai(self):
        """
            This function is supposed to return the optimal move for NormalAI.
        """
        # Store the board_positions in 'board' variable
        board = self.game_class_reference.board_positions

        # Store the board_size in 'board_size' variable
        board_size = self.game_class_reference.board_size

        # Store the board_available_cell_positions in 'board_available_cell_positions' variable
        board_available_cell_positions = self.game_class_reference.board_available_cell_positions

        # Store the win_length in 'win_length' variable
        win_length = self.game_class_reference.win_length

        # Store the player's last move in 'player_last_move' variable
        player_last_move = self.game_class_reference.player_last_move

        # Store the moves in 'moves' variable
        moves = self.game_class_reference.total_game_moves

        # Get optimal move
        computer_best_move = self.get_optimal_move(board, board_size, win_length)

        # Check if the board size is 3x3
        if board_size == 3:

            # If the middle cell is available, then take it
            if 4 in board_available_cell_positions:
                print("Take middle cell")
                return 4

            # Make logical moves, after that
            else:
                print("Make a logical move")
                random_move = random.choice(computer_best_move[0])
                return random_move[0]*board_size+random_move[1]                

        # Check it the board size is greater than 3x3
        else:

            # If the computer makes the first move, then let make a random move
            if moves == 0:
                print("Take middle cell")
                middle_cell = int(board_size / 2) + (board_size % 2)
                middle_cell = [middle_cell, middle_cell]
                return middle_cell

            # If the player made the first move, then let the computer make a logical move
            elif moves == 1 and player_last_move:
                print("Make a logical move")
                available_moves = []
                player_cell_move = [int(player_last_move/board_size), player_last_move%board_size]
                # Get the diagonal cells
                if player_cell_move[0]-1>=0 and player_cell_move[1]-1>=0:available_moves.append([player_cell_move[0]-1,player_cell_move[1]-1])
                if player_cell_move[0]+1<board_size and player_cell_move[1]+1<board_size:available_moves.append([player_cell_move[0]+1,player_cell_move[1]+1]) 
                # Get the negative diagonal cells
                if player_cell_move[0]-1>=0 and player_cell_move[1]+1<board_size:available_moves.append([player_cell_move[0]-1,player_cell_move[1]+1])
                if player_cell_move[0]+1<board_size and player_cell_move[1]-1 >= 0:available_moves.append([player_cell_move[0]+1,player_cell_move[1]-1])  
                # Choose a move from the available moves 
                chosen_move = random.choice(available_moves)
                return chosen_move[0]*board_size+chosen_move[1]

            # Let the player make a logical move
            else:
                print("Make a logical move")
                random_move = random.choice(computer_best_move[0])
                return random_move[0]*board_size+random_move[1]                  

    # hard_ai method
    def hard_ai(self):
        """
            This function is supposed to return the optimal move for HardAI.
        """
        # Store the board_positions in 'board' variable
        board = self.game_class_reference.board_positions
        # Store the board_size in 'board_size' variable
        board_size = self.game_class_reference.board_size
        # Store the win_length in 'win_length' variable
        win_length = self.game_class_reference.win_length
        # Store the moves in 'moves' variable
        moves = self.game_class_reference.total_game_moves
        # Create a variable that will hold the best moves for each player
        best_moves = {"C": [], "P": []}
        # Create a variable that will hold the winning moves for each player
        win_moves = {"C": [], "P": []}
        # Create a variable that will record the best score for each player
        best_score = {"C": 0, "P": 0}
        # Get optimal move for hard
        board_cell_score = self.get_hard_optimal_move(board, board_size, win_length)

        # ========== Get The Middle Of The Cell ========== #
        # Check to see if this is the beginning of the game
        if moves <= 1 and ((board_size < 7 and self.game_class_reference.starts_first == "player") or self.game_class_reference.starts_first == "computer"):
            # If the board isn't even (eg. 7, 3, 5), then take this path
            if board_size % 2 != 0:
                # Divide the board by 2 and subtract one from it after adding the remainder. This will get the middle number for the board
                middle_cell_number = (int(board_size / 2) + (board_size % 2))-1
                # Create the middle cell by creating a list with the 'middle_cell_number'
                middle_cell = [middle_cell_number, middle_cell_number]
                # If the middle cell is empty, then take the middle cell
                if board[middle_cell[0]][middle_cell[1]] == " ":return middle_cell[0]*board_size+middle_cell[1]
            # If the board is even, (eg. 6, 4, 8), then take this path
            else:
                # Divide the board by 2. This will get the middle number for the board
                middle_cell_number = int(board_size / 2)
                # Create a variable that will hold all the available middle cells
                middle_cells = []
                # Check to see if any of these cells are empty. If they are, then add to them to the middle cells
                if board[middle_cell_number-1][middle_cell_number-1] == " ": middle_cells.append([middle_cell_number-1, middle_cell_number-1])
                if board[middle_cell_number-1][middle_cell_number] == " ": middle_cells.append([middle_cell_number-1, middle_cell_number])
                if board[middle_cell_number][middle_cell_number] == " ": middle_cells.append([middle_cell_number, middle_cell_number])
                if board[middle_cell_number][middle_cell_number-1] == " ": middle_cells.append([middle_cell_number, middle_cell_number-1])
                # Choose a random middle cell and return it
                random_middle_cell = random.choice(middle_cells)
                return random_middle_cell[0]*board_size+random_middle_cell[1]

        # ========== Get The Highest Score From The 'board_cell_score' Var From Each Player ========== #
        [best_moves, best_score] = self.get_highest_score_from_cell_board(board_size, board_cell_score)


        # ========== Check to see if there are any winning moves ========== #
        # Loop thru every player
        for player in ("C", "P"):
            # Loop thru every move in the best_moves
            for move in best_moves[player]:
                # Create a copy of the board
                new_board = np.copy(board)       
                # Add the symbol to the board
                new_board[move[0]][move[1]] = player  
                # Check to see if the game is over
                game_over = self.game_class_reference.check_win(new_board, player, board_size, win_length) 
                # If the game is over, then move take this spot
                if game_over: win_moves[player].append(move)
        # Check to see if game is over    
        for player in ("C", "P"):
            if len(win_moves[player]) >= 1:
                random_move = random.randrange(0, len(win_moves[player]))
                return win_moves[player][random_move][0]*board_size+win_moves[player][random_move][1]

        # ========== Get The Best Move From All The 'best_moves' Variable ========== #
        final_move = self.get_best_move_from_best_moves(best_moves, best_score, win_length, board_size, board, "C", "P")
        return final_move[0]*board_size+final_move[1]


    # +----------------------------------------+
    # |                                        |
    # |      Create Advanced AI Functions      |
    # |                                        |
    # +----------------------------------------+
    # get_optimal_move method
    def get_optimal_move(self, board, board_size, win_length):
        """
            The purpose of this function is to get the optimal move. The EasyAI and NormalAI use this function.
        """
        # This will hold the best move for the computer
        best_moves = []

        # This will store the best score to determine what is the best move
        best_score = 1000

        # Start looping through all the rows in the board
        for row in range(board_size):

            # Start looping through all the columns in the board
            for col in range(board_size):
                
                # If the board isn't empty, then skip this code
                if not board[row][col] == " ": continue

                # Get the vertical outcome
                vertical_outcome = self.determine_vertical_outcome(row, col, win_length, board_size, board)

                # # Get the horizontal outcome
                horizontal_outcome = self.determine_horizontal_outcome(row, col, win_length, board_size, board)

                # Get the diagonal outcome
                diagonal_outcome = self.determine_diagonal_outcome(row, col, win_length, board_size, board)

                # Get the diagonal inverse outcome
                negative_diagonal_outcome = self.determine_neg_diagonal_outcome(row, col, win_length, board_size, board)

                # Gets all the best possible outcomes
                for outcome in [vertical_outcome, horizontal_outcome, diagonal_outcome, negative_diagonal_outcome]:
                    if outcome: 
                        if outcome[0] < best_score: 
                            best_score = outcome[0]
                            best_moves.clear()
                            best_moves.append(outcome[1])
                        elif outcome[0] ==  best_score:
                            move_exists = True
                            for move in best_moves:
                                if move == outcome[1]: 
                                    move_exists = True
                                    break
                                else: move_exists = False
                            if not move_exists: best_moves.append(outcome[1])
                                
        return [best_moves, best_score]

    # get_optimal_move method
    def get_hard_optimal_move(self, board, board_size, win_length):
        # This will hold the score for each cell
        board_cell_score = {"C": [], "P": []}

        # Loop through each player
        for player in ("C", "P"):

            # Start looping through all the rows in the board
            for row in range(board_size):

                board_cell_score[player].append([])

                # Start looping through all the columns in the board
                for col in range(board_size):

                    # If the cell isn't empty, then skip the following the code
                    if not board[row][col] == " ": 
                        board_cell_score[player][row].append("OCCUPIED")
                        continue

                    # Create a copy of the board
                    new_player_board = np.copy(board)

                    # Get the vertical outcome
                    vertical_cells = self.get_vertical_cells(row, col, win_length, board_size)

                    # Get the horizontal outcome
                    horizontal_cells = self.get_horizontal_cells(row, col, win_length, board_size)

                    # Get the diagonal outcome
                    diagonal_cells = self.get_diagonal_cells(row, col, win_length, board_size)

                    # Get the negative diagonal outcome
                    neg_diagonal_cells = self.get_neg_diagonal_cells(row, col, win_length, board_size)

                    # Store the current cell
                    current_cell = [row, col]

                    # Store the current score
                    current_score = {"v": 0, "h": 0, "d": 0, "d_i": 0}

                    # Create a copy of the board
                    new_player_board[row][col] = player

                    # Get the score for each cell
                    current_score["v"] = self.get_cell_score(current_cell, player, vertical_cells, win_length, new_player_board, "Vertical Cells")
                    current_score["h"] = self.get_cell_score(current_cell, player, horizontal_cells, win_length, new_player_board, "Horizontal Cells")
                    current_score["d"] = self.get_cell_score(current_cell, player, diagonal_cells, win_length, new_player_board, "Diagonal Cells")
                    current_score["d_i"] = self.get_cell_score(current_cell, player, neg_diagonal_cells, win_length, new_player_board, "Negative Diagonal Cells")

                    # Create the 'cell_score_result'
                    cell_score_result = current_score["v"] + current_score["h"] + current_score["d"] + current_score["d_i"]

                    # Add the 'cell_score_result' to the board_cell_score
                    board_cell_score[player][row].append(cell_score_result)

                    # Create a copy of the board
                    new_player_board[row][col] = " "


        return board_cell_score

    # get_cell_score method
    def get_cell_score(self, current_cell, current_player, cell_group, win_length, board, cell_group_name = "Unknown"):
        """
            The purpose of this function is to create and get the score for each cell
        """
        # This will hold the score for the space or empty cells
        space_score = 0

        # This will hold the score for the space or empty cells
        current_score = 0

        # This will record the amount of consecutive symbols
        consecutive_symbols = 0

        # This will record the score for the consecutive symbols
        consecutive_symbol_score = 0

        # This will record the maximum amount of consecutive symbols
        max_consecutive_symbol_score = 0     

        # This will record if the current symbol was found in the row
        tracking_score = 0

        # This will record if the current symbol was found in the row
        cell_number = {"current": [], "final": []}

        # This will record if the current symbol was found in the row
        symbol_found = False

        # This will hold the symbols in each cell on the board
        actual_cell_group = []

        # Get the actual symbols from the board
        for cell in cell_group:
            if not cell: continue
            actual_cell_group.append(board[cell[0]][cell[1]])

        # If the current_symbol is found less than once or once, then return 0
        if actual_cell_group.count(current_player) <= 1: return 0        
        
        # if current_player == "P":
        # print("Cell: {}".format(current_cell))
        # print("Actual Cell Group: {}".format(actual_cell_group))
        # print("Cell Group Name: {}".format(cell_group_name))
        # print("Cell Group: {}".format(cell_group))
        # print(board)
        # print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

        # This variable will keep track off each cell
        i = 0

        # Loop thru all the cells in the actual_cell_group
        for cell in actual_cell_group:

            # If the cell is occupied by the current player, then take this path
            if cell == current_player:

                # print("Occupied by current player")

                # Add a (+1) to the consecutive symbol variable
                consecutive_symbols+=1

                # Multiply the consecutive_symbols by (2) and add it to the 'consecutive_symbol_score' var
                consecutive_symbol_score = consecutive_symbols*2 if consecutive_symbols > 1 else 1

                # Add the space score to the current score
                current_score+=space_score

                # Reset the space score to 0
                space_score = 0

                # Add (1) to the tracking score
                tracking_score+=1

                # Set 'symbol_found' to True
                symbol_found = True

                # If consecutive_symbols is greater than the max_consecutive_symbol_score, then take this path
                if consecutive_symbols > max_consecutive_symbol_score:
                    max_consecutive_symbol_score = consecutive_symbols
                    cell_number["current"].append(i)

                # If consecutive_symbols score is equal to the win_length
                if consecutive_symbols == win_length:
                    # print("Game over!\nMultiply 'win_length' by '100'")
                    return win_length*100

            # If the cell isn't occupied, then take this path
            elif cell == " ":

                # print("Found an empty cell")

                # Add (1) to the tracking score
                tracking_score+=1

                # If there are 'consecutive_symbols', then take this path
                if consecutive_symbols > 0:

                    # Reset 'consecutive_symbols' to 0
                    consecutive_symbols = 0

                    # Add 'consecutive_symbol_score' to the current score
                    current_score+=consecutive_symbol_score

                    if len(cell_number["current"]) > len(cell_number["final"]): 
                        cell_number["final"] = cell_number["current"]

                    cell_number["current"] = []

                    # print("Reset cosecutive symbol variables")

                # If symbol_found is True, then add (-.1) to 'space_score'
                if symbol_found: space_score-=.1

            # If cell is occupied by the opponent, then take this path
            elif cell == ("P" if current_player == "C" else "C"):

                # Set 'consecutive_symbol_score' to 0
                consecutive_symbol_score = 0

                # Set 'consecutive_symbols' to 0
                consecutive_symbols = 0

                # Set 'current_score' to 0
                current_score = 0

                # Set 'space_score' to 0
                space_score = 0

                # Set 'tracking_score' to 0
                tracking_score = 0

                # Set 'symbol_found' to False
                symbol_found = False

                if len(cell_number["current"]) > len(cell_number["final"]): 
                    cell_number["final"] = cell_number["current"]

                cell_number["current"] = []

                # print("Reset because of opponent")

            i+=1

            # print(" ")

        # print("Finished Looping")

        # If consecutive_symbols is 1, then set 'consecutive_symbol_score' to 1, else multiply the 'consecutive_symbols' by 2
        consecutive_symbol_score = 1 if consecutive_symbols == 1 else consecutive_symbols*2
        
        # If the following requirements are met, then take this path
        #   * If 'consecutive_symbol_score' is greater than 0
        #   * If 'tracking_score' is greater than or equal to the 'win_length'
        #   * If 'symbol_found' is True
        if consecutive_symbol_score > 0 and tracking_score >= win_length and symbol_found == True:

            # Add 'consecutive_symbol_score' and 'space_score' to the 'current_score'
            current_score+=consecutive_symbol_score+space_score

            # print("Add extras to the current score!")

        # If 'tracking_score' is less than win_length, then reset the 'current_score' var to 0
        if tracking_score < win_length: 
            
            current_score = 0

            # print("Reset the current score to 0 for some reason?!")

        # If there are the same number of symbols or 1 less than the win_length, then take this path
        # if current_player == "P":
        #     print("Something", cell_number["final"])
        if len(cell_number["final"]) == win_length or len(cell_number["final"]) == win_length-1:

            # If there is a space before and after the consecutive symbols, then add 50, because that means this is a fork.
            # Example:
            #   ' ', 'X', 'X', 'X', ' '
            # This is a good visual example. If there are the same consecutive symbols in a row or 1 less the 'win_length' and there is space after and before, the consecutive symbols, then add 50, because it's a fork
            # print(actual_cell_group[cell_number["final"][0]-1] == " ")
            # print(actual_cell_group[cell_number["final"][0]-1])
            if actual_cell_group[cell_number["final"][0]-1] == " " and cell_number["final"][0]-1 >= 0 and actual_cell_group[cell_number["final"][-1]+1] == " ":
                # if current_player == "P":
                #     print(current_player) 
                #     print(cell_group_name)
                    # print(actual_cell_group[cell_number["final"][0]-1])
                    # print(actual_cell_group[cell_number["final"][-1]+1])

                current_score+=50
        # if current_player == "P":
        #     print(current_score)
        return current_score 


































































































































    # # create_cell_score method
    # def create_cell_score(self, win_length, cell_group, current_cell, current_player, board):

    #     # This will hold the score for the space or empty cells
    #     space_score = 0

    #     # This will hold the score for the space or empty cells
    #     current_score = 0

    #     # This will record the amount of consecutive symbols
    #     consecutive_symbols = 0

    #     # This will record the score for the consecutive symbols
    #     consecutive_symbol_score = 0

    #     # This will record if the current symbol was found in the row
    #     tracking_score = 0

    #     # This will record if the current symbol was found in the row
    #     symbol_found = False

    #     # This will hold the symbols in each cell on the board
    #     actual_cell_group = []

    #     # Get the actual symbols from the board
    #     for cell in cell_group:
    #         if not cell: continue
    #         actual_cell_group.append(board[cell[0]][cell[1]])

    #     # If the current_symbol is found less than once or once, then return 0
    #     if actual_cell_group.count(current_player) <= 1: return 0

    #     # Loop thru all the cells in the actual_cell_group
    #     for cell in actual_cell_group:

    #         # If the cell is occupied by the current player, then take this path
    #         if cell == current_player:

    #             # Add a (+1) to the consecutive symbol variable
    #             consecutive_symbols+=1

    #             # Multiply the consecutive_symbols by (2) and add it to the 'consecutive_symbol_score' var
    #             consecutive_symbol_score = consecutive_symbols*2 if consecutive_symbols > 1 else 1

    #             # Add the space score to the current score
    #             current_score+=space_score

    #             # Reset the space score to 0
    #             space_score = 0

    #             # Add (1) to the tracking score
    #             tracking_score+=1

    #             # Set 'symbol_found' to True
    #             symbol_found = True

    #         # If the cell isn't occupied, then take this path
    #         elif cell == " ":

    #             # Add (1) to the tracking score
    #             tracking_score+=1

    #             # If there are 'consecutive_symbols', then take this path
    #             if consecutive_symbols > 0:

    #                 # Reset 'consecutive_symbols' to 0
    #                 consecutive_symbols = 0

    #                 # Add 'consecutive_symbol_score' to the current score
    #                 current_score+=consecutive_symbol_score

    #                 print("Reset cosecutive")

    #             if symbol_found:

    #                 space_score-=.1

    #             print("Space:", space_score)

    #             print("Current score", current_score)

    #         elif cell == ("P" if current_player == "C" else "C"):

    #             consecutive_symbol_score = 0

    #             consecutive_symbols = 0

    #             current_score = 0

    #             space_score = 0

    #             tracking_score = 0

    #             symbol_found = False

    #             print("Reset because of opponent")

    #     consecutive_symbol_score = 1 if consecutive_symbols == 1 else consecutive_symbols*2

    #     if consecutive_symbol_score > 0 and tracking_score >= win_length and symbol_found == True:

    #         current_score+=consecutive_symbol_score+space_score
    #         print("Add finally")

    #     if tracking_score <= win_length-1:

    #         current_score = 0


    #     print(current_cell)
    #     print(current_score)
    #     print(tracking_score)
    #     print("===================")
    #     return current_score

































    # # create_cell_score method
    # def create_cell_score(self, win_length, cell_group, current_cell, current_player, board):

    #     # This will hold the score for the space or empty cells
    #     space_score = 0

    #     # This will hold the score for the space or empty cells
    #     current_score = 0

    #     # This will record the amount of consecutive symbols
    #     consecutive_symbols = 0

    #     # This will record the score for the consecutive symbols
    #     consecutive_symbol_score = 0

    #     # This will record if the current symbol was found in the row
    #     tracking_score = 0

    #     # This will record if the current symbol was found in the row
    #     symbol_found = False

    #     # This will hold the symbols in each cell on the board
    #     actual_cell_group = []

    #     # Get the actual symbols from the board
    #     for cell in cell_group:
    #         if not cell: continue
    #         actual_cell_group.append(board[cell[0]][cell[1]])

    #     # If the current_symbol is found less than once or once, then return 0
    #     if actual_cell_group.count(current_player) <= 1: return 0

    #     # Loop thru all the cells in the actual_cell_group
    #     for cell in actual_cell_group:

    #         # If the cell is occupied by the current player, then take this path
    #         if cell == current_player:

    #             # Add a (+1) to the consecutive symbol variable
    #             consecutive_symbols+=1

    #             # Multiply the consecutive_symbols by (2) and add it to the 'consecutive_symbol_score' var
    #             consecutive_symbol_score = consecutive_symbols*2 if consecutive_symbols > 1 else 1

    #             # Add the space score to the current score
    #             current_score+=space_score

    #             # Reset the space score to 0
    #             space_score = 0

    #             # Add (1) to the tracking score
    #             tracking_score+=1

    #             # Set 'symbol_found' to True
    #             symbol_found = True

    #         # If the cell isn't occupied, then take this path
    #         elif cell == " ":

    #             # Add (1) to the tracking score
    #             tracking_score+=1

    #             # If there are 'consecutive_symbols', then take this path
    #             if consecutive_symbols > 0:

    #                 # Reset 'consecutive_symbols' to 0
    #                 consecutive_symbols = 0

    #                 # Add 'consecutive_symbol_score' to the current score
    #                 current_score+=consecutive_symbol_score

    #                 print("Reset cosecutive")

    #             if symbol_found:

    #                 space_score-=.1

    #             print("Space:", space_score)

    #             print("Current score", current_score)

    #         elif cell == ("P" if current_player == "C" else "C"):

    #             consecutive_symbol_score = 0

    #             consecutive_symbols = 0

    #             current_score = 0

    #             space_score = 0

    #             tracking_score = 0

    #             symbol_found = False

    #             print("Reset because of opponent")

    #     consecutive_symbol_score = 1 if consecutive_symbols == 1 else consecutive_symbols*2

    #     if consecutive_symbol_score > 0 and tracking_score >= win_length and symbol_found == True:

    #         current_score+=consecutive_symbol_score+space_score

    #     if tracking_score <= win_length-1:

    #         current_score = 0


    #     print(current_cell)
    #     print(current_score)
    #     print(tracking_score)
    #     print("===================")
    #     return current_score





        # print(actual_cell_group.count(current_player))

        # # Loop thru all the cells
        # for cell in actual_cell_group:

        #     previous_cell = cell

        #     if cell == current_player:

        #         consecutive_symbols+=1

        #         if 

        #         symbol_found = True

        #     if cell == " ":

        #         if consecutive_symbols

        #         current_score-=.1





        # current_score = 0

        # final_score = 0

        # consecutive_symbols = 0

        # symbol_found = False

        # previous_cell = None

        # actual_cell_group = []




        # for cell in cell_group:

        #     if not cell: continue

        #     if cell == current_cell: continue

        #     previous_cell = board[cell[0]][cell[1]]

        #     if board[cell[0]][cell[1]] == " ":

        #         if consecutive_symbols >= 1:

        #             current_score-=.1

        #         # consecutive_symbols = 0

        #     elif board[cell[0]][cell[1]] == current_player:

        #         consecutive_symbols+=1

        #         symbol_found = True

        #         # print("Found it")
                

        #     elif board[cell[0]][cell[1]] == ("P" if current_player == "C" else "C"):

        #         consecutive_symbols = 0

        # if not symbol_found:

        #     return 0

            

        # final_score = (consecutive_symbols*2) + current_score

        # if consecutive_symbols == 0 and symbol_found:

        #     final_score+=1

        # return final_score



        print("Done")

    # get_highest_score_from_cell_board method
    def get_highest_score_from_cell_board(self, board_size, board_cell_score):
        """
            The purpose of this function is to get the best move from the cell board
        """
        # Create a variable that will hold the best moves for each player
        best_moves = {"C": [], "P": []}
        # Create a variable that will record the best score for each player
        best_score = {"C": 0, "P": 0}
        # Loop thru each player
        for player in ("C", "P"):
            # Loop thru all the rows in the board
            for row in range(0, board_size):
                # Loop thru all the columns in each row
                for col in range(0, board_size):
                    # If cell is occupied, then skip the following code
                    if board_cell_score[player][row][col] == "OCCUPIED": continue
                    # If cell value is greater than the best_score, then let the best_score have the value of the cell
                    if board_cell_score[player][row][col] > best_score[player]:
                        # Clear all the moves from the best_moves[player]
                        best_moves[player].clear()
                        # Set the best_moves of the player to the row and column
                        best_moves[player].append([row, col])
                        # Set the best_score to board_cell_score[player][row][col]
                        best_score[player] = board_cell_score[player][row][col] 
                    # If cell value is the same as the best_score, then add the cell to the best_moves
                    elif board_cell_score[player][row][col] == best_score[player]:
                        # Set the best_moves of the player to the row and column
                        best_moves[player].append([row, col])
        return [best_moves, best_score]   

    # get_best_move_from_best_moves method   
    def get_best_move_from_best_moves(self, best_moves, best_score, win_length, board_size, board, current_player, opponent_player):
        # If one player has a higher score, then take this path
        if best_score[current_player] != best_score[opponent_player]:
            # If 'Player' has higher score than the computer and the computer has a score lower than 50, then set it to 'P', else set it to 'C'
            player = opponent_player if best_score[opponent_player] > best_score[current_player] and best_score[current_player] < 50 else current_player  
            # Create a variable that will hold the best move
            best_player_move = {"score": 0, "cell": None}  
            # Loop through all the moves in 'best_moves[player]', which can be either the computers or the players
            for move in best_moves[player]:
                # Create a copy of the board
                new_board_copy = np.copy(board)   
                # Get optimal move for hard
                new_board_cell_score = self.get_hard_optimal_move(new_board_copy, board_size, win_length)
                # This will record all the test moves to see which one is the most promising move
                test_moves = []
                # Set the test moves from greatest to smallest
                for row in range(board_size):
                    for col in range(board_size):
                        if new_board_cell_score[player][row][col] == "OCCUPIED": continue
                        test_moves.append({"score": new_board_cell_score[player][row][col], "cell": [row, col]})
                test_moves.sort(key = self.get_score, reverse = True)
                # If test_move has a higher score than the best_player_move, then set the best_player_move to the test_move
                if test_moves[0]["score"] > best_player_move["score"]:
                    best_player_move = {"score": test_moves[0]["score"], "cell": move}
            # Return the best move
            return best_player_move["cell"]
            # best_player_move["cell"][0]*board_size+best_player_move["cell"][1]    
        # If the scores are the same, then take this path
        else:
            random_move = random.choice(best_moves[current_player])
            return random_move
  

    # +----------------------------------------+
    # |                                        |
    # |    Create Determine Move Functions     |
    # |                                        |
    # +----------------------------------------+
    # determine_vertical_outcome method
    def determine_vertical_outcome(self, row, col, win_length, board_size, board):
        # ========== Create Variables That Will Store Data ========== #
        # Create best_score
        best_scores = {"P": 1000, "C": 1000}

        # Create best_score
        best_move = {"P": None, "C": None}

        # Create a variable that will hold the vertical cells
        vertical_cells = self.get_vertical_cells(row, col, win_length, board_size)
        # ========== Loop Through All The Cells ========== #
        # Loop through all the players ("player", "computer")
        for player in ["P", "C"]:

            # Create a new board for each player
            new_board = np.copy(board)

            # Create a current score for each player
            current_score = 0

            # Loop through all the vertical cells
            for cell in vertical_cells:

                # If cell doesn't actually exist, then skip the following code
                if cell == None: continue

                # Check if cell is empty
                if new_board[cell[0]][cell[1]] == " ": 

                    # Add player to new board
                    new_board[cell[0]][cell[1]] = player

                    # Add two to current score, which means the computer moved, then the player moved after
                    current_score+=1 if player == "C" and current_score == 0 else 2

                    # Check if game is over
                    game_over = self.game_class_reference.check_win(new_board, player, board_size, win_length)

                    # If game is over then store the amount of moves it took and the move
                    if game_over:
                        best_scores[player] = current_score
                        best_move[player] = cell
                        break

        # ========== Return The Optimal Move ========== #
        # If the player has a lower score (which means a better of chance of winning), then return the player move as the optimal move
        if best_scores["P"] < best_scores["C"]: return [best_scores["P"], best_move["P"]]

        # If the computer has a lower score (which means a better of chance of winning), then return the computer move as the optimal move
        else: return [best_scores["C"], best_move["C"]]

    # determine_horizontal_outcome method
    def determine_horizontal_outcome(self, row, col, win_length, board_size, board):
        # ========== Create Variables That Will Store Data ========== #
        # Create best_score
        best_scores = {"P": 1000, "C": 1000}

        # Create best_score
        best_move = {"P": None, "C": None}

        # Create a variable that will hold the horizontal cells
        horizontal_cells = self.get_horizontal_cells(row, col, win_length, board_size)

        # ========== Loop Through All The Cells ========== #
        # Loop through all the players ("player", "computer")
        for player in ["P", "C"]:

            # Create a new board for each player
            new_board = np.copy(board)

            # Create a current score for each player
            current_score = 0

            # Loop through all the vertical cells
            for cell in horizontal_cells:

                # If cell doesn't actually exist, then skip the following code
                if cell == None: continue

                # Check if cell is empty
                if new_board[cell[0]][cell[1]] == " ": 

                    # Add player to new board
                    new_board[cell[0]][cell[1]] = player

                    # Add two to current score, which means the computer moved, then the player moved after
                    current_score+=1 if player == "C" and current_score == 0 else 2

                    # Check if game is over
                    game_over = self.game_class_reference.check_win(new_board, player, board_size, win_length)

                    # If game is over then store the amount of moves it took and the move
                    if game_over:
                        best_scores[player] = current_score
                        best_move[player] = cell
                        break

        # ========== Return The Optimal Move ========== #
        # If the player has a lower score (which means a better of chance of winning), then return the player move as the optimal move
        if best_scores["P"] < best_scores["C"]: return [best_scores["P"], best_move["P"]]

        # If the computer has a lower score (which means a better of chance of winning), then return the computer move as the optimal move
        elif best_scores["C"] < best_scores["P"]: return [best_scores["C"], best_move["C"]]

    # determine_diagonal_outcome method
    def determine_diagonal_outcome(self, row, col, win_length, board_size, board):
        # ========== Create Variables That Will Store Data ========== #
        # Create best_score
        best_scores = {"P": 1000, "C": 1000}

        # Create best_score
        best_move = {"P": None, "C": None}

        # Create a variable that will hold the diagonal cells
        diagonal_cells = self.get_diagonal_cells(row, col, win_length, board_size)

        # ========== Loop Through All The Cells ========== #
        # Loop through all the players ("player", "computer")
        for player in ["P", "C"]:

            # Create a new board for each player
            new_board = np.copy(board)

            # Create a current score for each player
            current_score = 0

            # Loop through all the vertical cells
            for cell in diagonal_cells:

                # If cell doesn't actually exist, then skip the following code
                if cell == None: continue

                # Check if cell is empty
                if new_board[cell[0]][cell[1]] == " ": 

                    # Add player to new board
                    new_board[cell[0]][cell[1]] = player

                    # Add two to current score, which means the computer moved, then the player moved after
                    current_score+=1 if player == "C" and current_score == 0 else 2

                    # Check if game is over
                    game_over = self.game_class_reference.check_win(new_board, player, board_size, win_length)

                    # If game is over then store the amount of moves it took and the move
                    if game_over:
                        best_scores[player] = current_score
                        best_move[player] = cell
                        break

        # ========== Return The Optimal Move ========== #
        # If the player has a lower score (which means a better of chance of winning), then return the player move as the optimal move
        if best_scores["P"] < best_scores["C"]: return [best_scores["P"], best_move["P"]]

        # If the computer has a lower score (which means a better of chance of winning), then return the computer move as the optimal move
        else: return [best_scores["C"], best_move["C"]]

    # determine_neg_diagonal_outcome method
    def determine_neg_diagonal_outcome(self, row, col, win_length, board_size, board):
        # ========== Create Variables That Will Store Data ========== #
        # Create best_score
        best_scores = {"P": 1000, "C": 1000}

        # Create best_score
        best_move = {"P": None, "C": None}

        # Create a variable that will hold the diagonal cells
        neg_diagonal_cells = self.get_neg_diagonal_cells(row, col, win_length, board_size)

        # ========== Loop Through All The Cells ========== #
        # Loop through all the players ("player", "computer")
        for player in ["P", "C"]:

            # Create a new board for each player
            new_board = np.copy(board)

            # Create a current score for each player
            current_score = 0

            # Loop through all the vertical cells
            for cell in neg_diagonal_cells:

                # If cell doesn't actually exist, then skip the following code
                if cell == None: continue

                # Check if cell is empty
                if new_board[cell[0]][cell[1]] == " ": 

                    # Add player to new board
                    new_board[cell[0]][cell[1]] = player

                    # Add two to current score, which means the computer moved, then the player moved after
                    current_score+=1 if player == "C" and current_score == 0 else 2

                    # Check if game is over
                    game_over = self.game_class_reference.check_win(new_board, player, board_size, win_length)

                    # If game is over then store the amount of moves it took and the move
                    if game_over:
                        best_scores[player] = current_score
                        best_move[player] = cell
                        break

        # ========== Return The Optimal Move ========== #
        # If the player has a lower score (which means a better of chance of winning), then return the player move as the optimal move
        if best_scores["P"] < best_scores["C"]: return [best_scores["P"], best_move["P"]]

        # If the computer has a lower score (which means a better of chance of winning), then return the computer move as the optimal move
        else: return [best_scores["C"], best_move["C"]]


    # +----------------------------------------+
    # |                                        |
    # |         Create Helper Functions        |
    # |                                        |
    # +----------------------------------------+
    # get_score method
    def get_score(self, element):
        """
        (Helper Function)\n
           The purpose of this function is to get the score from the moves. This is only used in the 'get_best_move_from_best_moves' function
        """
        return element['score']

    # get_vertical_cells method
    def get_vertical_cells(self, row, col, win_length, board_size):
        """
        (Helper Function)\n
            This will get all the previous and next cells vertically. This will get the win_length amount of cells. For example, if the win_length is three, then it will get three cells before the current cell and three cells after the current cell
        """
        # Create a variable that will hold the vertical cells
        vertical_cells = []

        # Get all the vertically previous cells after the current cell
        for vertical_cell_row in reversed(range(1, win_length)):

            # Store the previous cells in vertical cells container
            vertical_cells.append(None if row-vertical_cell_row < 0 else [row-vertical_cell_row, col])

        # Get the current cell
        vertical_cells.append([row, col])

        # Get all the vertically next cells after the current cell
        for vertical_cell_row in range(1, win_length):

            # Store the next cells in vertical cells container
            vertical_cells.append(None if row+vertical_cell_row > board_size-1 else [row+vertical_cell_row, col])

        return vertical_cells

    # get_horizontal_cells method
    def get_horizontal_cells(self, row, col, win_length, board_size):
        """
        (Helper Function)\n
            This will get all the previous and next cells horizontally. This will get the win_length amount of cells. For example, if the win_length is three, then it will get three cells before the current cell and three cells after the current cell
        """
        # Create a variable that will hold the horizontal cells
        horizontal_cells = []

        # Get all the horizontally previous cells after the current cell
        for horizontal_cell_row in reversed(range(1, win_length)):

            # Store the previous cells in horizontal cells container
            horizontal_cells.append(None if col-horizontal_cell_row < 0 else [row, col-horizontal_cell_row])

        # Get the current cell
        horizontal_cells.append([row, col])

        # Get all the 4 horizontally next cells after the current cell
        for horizontal_cell_row in range(1, win_length):

            # Store the next cells in horizontal cells container
            horizontal_cells.append(None if col+horizontal_cell_row > board_size-1 else [row, col+horizontal_cell_row])

        return horizontal_cells

    # get_diagonal_cells method
    def get_diagonal_cells(self, row, col, win_length, board_size):
        """
        (Helper Function)\n
            This will get all the previous and next cells diagonally. This will get the win_length amount of cells. For example, if the win_length is three, then it will get three cells before the current cell and three cells after the current cell
        """
        # Create a variable that will hold the diagonal cells
        diagonal_cells = []

        # Get all the diagonally previous cells after the current cell
        for diagonal_cell_row in reversed(range(1, win_length)):

            # Store the previous cells in diagonal cells container
            diagonal_cells.append([row-diagonal_cell_row, col-diagonal_cell_row] if row-diagonal_cell_row >= 0 and col-diagonal_cell_row >= 0 else None)

        # Get the current cell
        diagonal_cells.append([row, col])

        # Get all the diagonally next cells after the current cell
        for diagonal_cell_row in range(1, win_length):

            # Store the next cells in diagonal cells container
            diagonal_cells.append([row+diagonal_cell_row, col+diagonal_cell_row] if row+diagonal_cell_row <= board_size-1 and col+diagonal_cell_row <= board_size-1 else None)

        return diagonal_cells

    # get_neg_diagonal_cells method
    def get_neg_diagonal_cells(self, row, col, win_length, board_size):
        """
        (Helper Function)\n
            This will get all the previous and next cells negative diagonally. This will get the win_length amount of cells. For example, if the win_length is three, then it will get three cells before the current cell and three cells after the current cell
        """
        # Create a variable that will hold the diagonal cells
        neg_diagonal_cells = []

        # Get all the diagonally previous cells after the current cell
        for neg_diagonal_cell_row in reversed(range(1, win_length)):

            # Store the previous cells in diagonal cells container
            neg_diagonal_cells.append([row-neg_diagonal_cell_row, col+neg_diagonal_cell_row] if row-neg_diagonal_cell_row >= 0 and col+neg_diagonal_cell_row <= board_size-1 else None)

        # Get the current cell
        neg_diagonal_cells.append([row, col])

        # Get all the diagonally next cells after the current cell
        for neg_diagonal_cell_row in range(1, win_length):

            # Store the next cells in diagonal cells container
            neg_diagonal_cells.append([row+neg_diagonal_cell_row, col-neg_diagonal_cell_row] if row+neg_diagonal_cell_row <= board_size-1 and col-neg_diagonal_cell_row >= 0 else None)

        return neg_diagonal_cells