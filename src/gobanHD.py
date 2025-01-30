import torch, torchhd

class GobanHD:
    def __init__(self, H=13, W=13, D=10000, use_HD=True):
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.W = W
        self.H = H

        # Create positions
        positions = []
        for i in range(W):
            for j in range(H):
                positions.append((i, j))
        self.positions = positions

        self.empty_board = torch.zeros((H, W), dtype=int, device=self.device)
        self.last_action = None
        self.last_turn = -1
        self.n_turn = 0
        self.winner = 0
        

        # Create HD position
        self.use_HD = use_HD
        if use_HD:
            self.D = D
            X = torchhd.level(W, D)
            Y = torchhd.level(H, D)
            encoded_pos = []
            for i, x in enumerate(X):
                for j, y in enumerate(Y):
                    binding = x.bind(torchhd.permute(y))
                    encoded_pos.append(binding)
            self.encoded_pos = torch.stack(encoded_pos).T.to(self.device)


    def start_board(self, initial_state=None):
        self.board = self.empty_board.clone()
        self.t_positions = self.positions.copy()
        self.last_action = None
        self.last_turn = -1
        self.n_turn = 0
        self.winner = 0
        
        # HD board
        if self.use_HD:
            # Use initial state from model.initial_state
            self.HDboard = initial_state.clone()
            self.t_encoded_pos = self.encoded_pos.clone()

    def check_gomoku(self):
        '''
        -1 -> black win
         0 -> draw
         1 -> white win
         2 -> on going
        '''
        def check_five_in_a_row(arr):
            for i in range(arr.size(0) - 4):
                segment = arr[i:i + 5]
                if torch.all(segment == 1):
                    return 1
                elif torch.all(segment == -1):
                    return -1
            return 2

        if self.n_turn < 9:
            return 2
        
        # Get row col from last action
        row, col = self.last_action

        # Check the affected row
        result = check_five_in_a_row(self.board[row, :])
        if result != 2:
            self.winner = self.last_turn
            return result

        # Check the affected column
        result = check_five_in_a_row(self.board[:, col])
        if result != 2:
            self.winner = self.last_turn
            return result

        # Check diagonals
        # Main diagonal (\ direction) - only check the diagonal that contains (row, col)
        diag = self.board.diagonal(col - row)
        if diag.size(0) >= 5:
            result = check_five_in_a_row(diag)
            if result != 2:
                self.winner = self.last_turn
                return result

        # Anti-diagonal (/ direction) - only check the anti-diagonal that contains (row, col)
        anti_diag = self.board.flip(1).diagonal(col - row)
        if anti_diag.size(0) >= 5:
            result = check_five_in_a_row(anti_diag)
            if result != 2:
                self.winner = self.last_turn
                return result

        # Check for draw (if no empty spots left)
        if len(self.t_positions) == 0:
            self.winner = 0
            return 0
        
        return 2  # 2 signifies the game is still ongoing

    def get_position(self, index):
        return self.t_positions[index]
    
    def get_encoded_position(self, index):
        return self.t_encoded_pos[index]
    
    def get_position_index(self, position):
        return self.t_positions.index(position)
    
    def get_encoded_position_index(self, encoded_pos):
        return self.t_encoded_pos.index(encoded_pos)

    def update_board(self, index, turn=None, S=None):
        self.last_turn = self.last_turn * -1 if turn is None else turn
        self.board[self.t_positions[index]] = self.last_turn
        row, col = self.t_positions.pop(index)
        
        if self.use_HD:
            self.HDboard = torchhd.normalize(self.HDboard.bundle(S))
            self.t_encoded_pos = torch.cat((self.t_encoded_pos[:, :index], self.t_encoded_pos[:, index+1:]), dim=1)

        # Update action
        self.last_action = (row, col)
        self.n_turn = len(self.positions) - len(self.t_positions)
        
        return self
    
    def clone(self):
        new_board = GobanHD(use_HD=self.use_HD)

        new_board.device = self.device
        new_board.W = self.W
        new_board.H = self.H

        new_board.positions = self.positions.copy()
        new_board.last_action = self.last_action
        new_board.last_turn = self.last_turn
        new_board.n_turn = self.n_turn
        new_board.board = self.board.clone()
        new_board.t_positions = self.t_positions.copy()
        new_board.winner = self.winner

        if self.use_HD:
            new_board.D = self.D
            new_board.encoded_pos = self.encoded_pos.clone()
            new_board.empty_board = self.empty_board.clone()
            new_board.HDboard = self.HDboard.clone()
            new_board.t_encoded_pos = self.t_encoded_pos.clone()

        return new_board
    
    def generate_states(self):
        states = []
        for index in range(len(self.t_positions)):
            states.append(self.clone().update_board(index))
        return states
    