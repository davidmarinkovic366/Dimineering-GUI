import pygame

WIDTH:  int = 500
HEIGHT: int = 500

NUM: int = 6

ROWS: int = NUM
COLS: int = NUM
DIM: int = ROWS + 2
CELL_SIZE = WIDTH // DIM
PIECE_LONG = 2 * CELL_SIZE - 2 *(CELL_SIZE // 10)
PIECE_SHORT = CELL_SIZE - 2 *(CELL_SIZE // 10)
PIECE_OFFSET = CELL_SIZE // 10

WHITE: tuple[int, int, int] = (255, 255, 255)
BROWN: tuple[int, int, int] = (198, 134, 66)
OUTLINE: tuple[int, int, int] = (124, 44, 21)
BACKGROUND: tuple[int, int, int] = (210, 212, 220)
PIECE_X_COLOR: tuple[int, int, int] = (237, 237, 55)
PIECE_O_COLOR: tuple[int, int, int] = (124, 51, 184)

