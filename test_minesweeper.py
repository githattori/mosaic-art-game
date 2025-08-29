import random
from minesweeper import Board


def test_mine_count():
    random.seed(0)
    board = Board(5, 5, 5)
    mines = sum(cell.is_mine for row in board.grid for cell in row)
    assert mines == 5


def test_reveal_not_mine():
    random.seed(1)
    board = Board(3, 3, 1)
    # Find a safe cell
    safe = next((r, c) for r in range(3) for c in range(3) if not board.grid[r][c].is_mine)
    assert board.reveal(*safe) is True
    assert board.grid[safe[0]][safe[1]].is_revealed


def test_reveal_mine():
    random.seed(2)
    board = Board(3, 3, 1)
    mine = next((r, c) for r in range(3) for c in range(3) if board.grid[r][c].is_mine)
    assert board.reveal(*mine) is False
