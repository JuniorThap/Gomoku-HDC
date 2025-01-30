from gobanHD import GobanHD
from src.mcts import MCTS

board = GobanHD(use_HD=False)
mcts = MCTS()

mcts.search(board)