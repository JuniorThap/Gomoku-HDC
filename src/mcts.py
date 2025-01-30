from math import log, sqrt
import random
from abc import ABC, abstractmethod

class MCTS:
    class Node:
        def __init__(self, parent, board):
            self.board = board
            self.parent = parent
            self.visits = 0
            self.score = 0
            self.children = {}
            self.is_terminal = board.check_gomoku() != 2 # 2 is on-going state 
            self.is_fully_expanded = self.is_terminal
    

    # Search for the best move in the current state
    def search(self, board, n_simulation):
        self.root = self.Node(parent=None, board=board)
        self.my_turn = -board.last_turn # last turn is opponent turn (-1 for black, 1 for white)

        for _ in range(n_simulation):
            node = self.select(self.root)
            score = self.rollout(node.board, self.my_turn)
            self.backpropagation(node, score)

        return self.get_best_move(self.root, 0).board.last_action

    
    # Select most promising node
    def select(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)
            else:
                return self.expand(node)
            
        return node

    # Expand a new node
    def expand(self, node):
        states = node.board.generate_states()

        for state in states:
            action_name = str(state.last_action)
            if action_name not in node.children.keys():
                new_node = self.Node(node, state)

                node.children[action_name] = new_node
                node.is_fully_expanded = len(states) == len(node.children)

                return new_node

    # Simulate the game until the end (for this example, Randomly pick the action)
    def rollout(self, board, my_turn):
        while board.check_gomoku() == 2:
            try:
                board = random.choice(board.generate_states())
            except:
                # return a draw score
                return 0
        
        '''
            Win State Table
                +-----------------------------------------+
                | winner\my_turn | 1 (white) | -1 (black) |
                +----------------+-----------+------------+
                |   1 (white)    | 1*1 = 1   | 1*-1 = -1  |
                +----------------+-----------+------------+
                |  -1 (black)    | -1*1 = -1 | -1*-1 = 1  |
                +----------------+-----------+------------+
            -> 1 is for white, -1 is for black
            -> also 1 is for win score, -1 is for lose score
            -> for example, my turn is black (-1), the winner is white (1) so I get the lose score (-1*1 = -1)
        '''
        return my_turn * board.winner
        
    def backpropagation(self, node, score):
        while node is not None:
            node.visits += 1
            node.score += score
            node = node.parent

    def get_best_move(self, node, exploration_constant):
        best_score = float('-inf')
        best_moves = []

        for child_node in node.children.values():
            score = self.UCB1(child_node, exploration_constant)

            if score > best_score:
                best_score = score
                best_moves = [child_node]
            elif score == best_score:
                best_moves.append(child_node)
        
        return random.choice(best_moves)


    def UCB1(self, node, exploration_constant):
        return (node.score / node.visits) + (exploration_constant * sqrt(log(node.parent.visits) / node.visits))
