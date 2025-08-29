import random
from typing import List, Tuple


class Cell:
    """Represents a single cell on the Minesweeper board."""

    def __init__(self) -> None:
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0


class Board:
    """Minesweeper board data structure."""

    def __init__(self, rows: int, cols: int, mines: int) -> None:
        if mines >= rows * cols:
            raise ValueError("Too many mines for the board size")
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid: List[List[Cell]] = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self._place_mines()
        self._compute_neighbors()

    def _neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        coords: List[Tuple[int, int]] = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    coords.append((nr, nc))
        return coords

    def _place_mines(self) -> None:
        spots = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        for r, c in random.sample(spots, self.mines):
            self.grid[r][c].is_mine = True

    def _compute_neighbors(self) -> None:
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].is_mine:
                    continue
                count = sum(1 for nr, nc in self._neighbors(r, c) if self.grid[nr][nc].is_mine)
                self.grid[r][c].neighbor_mines = count

    def reveal(self, r: int, c: int) -> bool:
        """Reveal a cell. Returns False if a mine was revealed."""
        cell = self.grid[r][c]
        if cell.is_revealed or cell.is_flagged:
            return True
        cell.is_revealed = True
        if cell.is_mine:
            return False
        if cell.neighbor_mines == 0:
            for nr, nc in self._neighbors(r, c):
                self.reveal(nr, nc)
        return True

    def toggle_flag(self, r: int, c: int) -> None:
        cell = self.grid[r][c]
        if cell.is_revealed:
            return
        cell.is_flagged = not cell.is_flagged

    def is_victory(self) -> bool:
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def display(self) -> None:
        print("   " + " ".join(str(c) for c in range(self.cols)))
        for r in range(self.rows):
            row_chars = []
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.is_flagged:
                    row_chars.append("F")
                elif not cell.is_revealed:
                    row_chars.append(".")
                elif cell.is_mine:
                    row_chars.append("*")
                elif cell.neighbor_mines > 0:
                    row_chars.append(str(cell.neighbor_mines))
                else:
                    row_chars.append(" ")
            print(f"{r:2} " + " ".join(row_chars))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Play Minesweeper in the terminal")
    parser.add_argument("rows", type=int, nargs="?", default=8)
    parser.add_argument("cols", type=int, nargs="?", default=8)
    parser.add_argument("mines", type=int, nargs="?", default=10)
    args = parser.parse_args()

    board = Board(args.rows, args.cols, args.mines)

    while True:
        board.display()
        if board.is_victory():
            print("Congratulations! You cleared the minefield.")
            break
        cmd = input("Enter command (r row col to reveal, f row col to flag): ")
        parts = cmd.strip().split()
        if len(parts) != 3 or parts[0] not in {"r", "f"}:
            print("Invalid command")
            continue
        try:
            action, r, c = parts[0], int(parts[1]), int(parts[2])
        except ValueError:
            print("Invalid coordinates")
            continue
        if not (0 <= r < board.rows and 0 <= c < board.cols):
            print("Out of bounds")
            continue
        if action == "r":
            if not board.reveal(r, c):
                board.display()
                print("Boom! You hit a mine.")
                break
        else:
            board.toggle_flag(r, c)


if __name__ == "__main__":
    main()
