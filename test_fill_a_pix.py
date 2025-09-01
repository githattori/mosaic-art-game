from fill_a_pix import FillAPix, sample_solution


def test_clues():
    board = FillAPix(sample_solution())
    assert board.clues[2][2] == 9
    assert board.clues[0][0] == 3


def test_is_solved():
    board = FillAPix(sample_solution())
    # Initially puzzle is not solved
    assert not board.is_solved()
    # Fill according to solution
    for r in range(board.rows):
        for c in range(board.cols):
            if board.solution[r][c] == 1:
                board.mark_filled(r, c)
    assert board.is_solved()
    # Introduce an incorrect fill
    board.mark_filled(0, 0)
    assert not board.is_solved()
