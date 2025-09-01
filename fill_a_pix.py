from __future__ import annotations

from typing import List, Optional


class FillAPix:
    """Simple Fill-a-Pix puzzle board."""

    def __init__(self, solution: List[List[int]]) -> None:
        self.solution = solution
        self.rows = len(solution)
        self.cols = len(solution[0]) if self.rows else 0
        self.player: List[List[Optional[bool]]] = [
            [None for _ in range(self.cols)] for _ in range(self.rows)
        ]
        self.clues = self._compute_clues()

    def _compute_clues(self) -> List[List[int]]:
        clues = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.solution[nr][nc]:
                                count += 1
                clues[r][c] = count
        return clues

    def mark_filled(self, r: int, c: int) -> None:
        self.player[r][c] = True

    def mark_empty(self, r: int, c: int) -> None:
        self.player[r][c] = False

    def is_solved(self) -> bool:
        for r in range(self.rows):
            for c in range(self.cols):
                if self.player[r][c] is True and self.solution[r][c] != 1:
                    return False
                if self.player[r][c] is not True and self.solution[r][c] == 1:
                    return False
        return True

    def display(self) -> None:
        print("   " + " ".join(str(c) for c in range(self.cols)))
        for r in range(self.rows):
            row_chars = []
            for c in range(self.cols):
                mark = self.player[r][c]
                if mark is True:
                    row_chars.append("#")
                elif mark is False:
                    row_chars.append("X")
                else:
                    row_chars.append(str(self.clues[r][c]))
            print(f"{r:2} " + " ".join(row_chars))


def sample_solution() -> List[List[int]]:
    """Return a small 5x5 sample picture used as a puzzle."""
    return [
        [0, 1, 0, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 0, 1, 0],
    ]


def main() -> None:
    board = FillAPix(sample_solution())
    while True:
        board.display()
        if board.is_solved():
            print("Puzzle solved!")
            break
        cmd = input("Enter command (f row col to fill, x row col to mark empty): ")
        parts = cmd.strip().split()
        if len(parts) != 3 or parts[0] not in {"f", "x"}:
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
        if action == "f":
            board.mark_filled(r, c)
        else:
            board.mark_empty(r, c)


if __name__ == "__main__":
    main()
