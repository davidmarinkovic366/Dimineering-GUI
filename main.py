import pygame
from const.constants import WIDTH, HEIGHT, ROWS, COLS, CELL_SIZE, PIECE_OFFSET, PIECE_SHORT, PIECE_LONG
from const.constants import BROWN, WHITE, OUTLINE, BACKGROUND, PIECE_X_COLOR, PIECE_O_COLOR

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Domineering!')
font = pygame.font.Font('cascadiacode.ttf', 32)

FPS: int = 60
LETTER_ARRAY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():

    run = True
    clock = pygame.time.Clock()
    board: list[list[str]] = create_board()
    player: bool = True   # True = X, False = O
    move_counter: int = 0

    draw_board(WIN)
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                print('You clicked on:', get_cell_pos(pygame.mouse.get_pos()))
                piece_set = False
                if not get_cell_pos(pygame.mouse.get_pos()) == (None, None):
                    piece_set = set_figure(WIN, get_cell_pos(pygame.mouse.get_pos()), player, move_counter, board)
                if piece_set:
                    player = not player
                    move_counter = move_counter + 1

        pygame.display.update()

    pygame.quit()

def create_board() -> list[list[str]]:
    table: list = list()
    for rw in range(0, ROWS):
        table.append(list())
        for cl in range(0, COLS):
            table[rw].append(' ')
    return table

def draw_board(win):

    win.fill(BACKGROUND)

    is_brown: bool = True
    for row in range(1, ROWS + 1):
        if ROWS % 2 == 0:
            is_brown = not is_brown
        for col in range(1, COLS + 1):
            color = BROWN if is_brown else WHITE
            is_brown = not is_brown
            pygame.draw.rect(win, color, (row * CELL_SIZE, col * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Up and down letter array:
    for i in range(1, COLS + 1):
        
        text = font.render(LETTER_ARRAY[i-1], True, OUTLINE, None)
        text_rect = text.get_rect()

        text_rect.center = (i * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 2)
        WIN.blit(text, text_rect)

        text_rect.center = (i * CELL_SIZE + CELL_SIZE // 2, (ROWS + 1) * CELL_SIZE + CELL_SIZE // 2)
        WIN.blit(text, text_rect)

    # Left and right number array
    num: int = 0
    for i in range(ROWS, 0, -1):

        text = font.render(str(num), True, OUTLINE, None)
        text_rect = text.get_rect()
        num = num + 1

        text_rect.center = ( CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2)
        WIN.blit(text, text_rect)

        text_rect.center = ( (COLS + 1) * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2)
        WIN.blit(text, text_rect)


def get_cell_pos(clicked_pos) -> tuple:

    x_temp = clicked_pos[0]
    y_temp = clicked_pos[1]

    x_pos: int = int(x_temp / CELL_SIZE)
    y_pos: int = int(y_temp / CELL_SIZE)

    if (x_pos < 1 or y_pos < 1) or (x_pos > ROWS or y_pos > COLS):
        return (None, None)

    return (ROWS - y_pos, x_pos - 1)


def set_figure(win, pos: tuple[int, int], player: bool, counter: int, table: list[list[str]]) -> bool: 
    
    res = check_move(player, table, pos[0], pos[1])
    print(res)
    if not res:
        return False

    # Inace mozemo da postavimo!
    # Igra X:
    if player:

        pygame.draw.rect(win, PIECE_X_COLOR, ((pos[1] + 1) * CELL_SIZE + PIECE_OFFSET, (ROWS - pos[0] - 1) * CELL_SIZE + PIECE_OFFSET, PIECE_SHORT, PIECE_LONG), 0, 5)
        # print('Drawing on: ', (pos[0] * CELL_SIZE + PIECE_OFFSET, pos[1] * CELL_SIZE + PIECE_OFFSET, PIECE_SHORT, PIECE_LONG))

        text = font.render(str(counter), True, OUTLINE, None)
        text_rect = text.get_rect()
        text_rect.center = ((pos[1] + 1) * CELL_SIZE + PIECE_OFFSET + PIECE_SHORT // 2, (ROWS - pos[0] - 1) * CELL_SIZE + PIECE_OFFSET + PIECE_LONG // 2)

        win.blit(text, text_rect)

        table[pos[0]][pos[1]] = 'X'
        table[pos[0]  + 1][pos[1]] = 'X'
        return True

    else:

        pygame.draw.rect(win, PIECE_O_COLOR, ((pos[1] + 1) * CELL_SIZE + PIECE_OFFSET, (ROWS - pos[0]) * CELL_SIZE + PIECE_OFFSET, PIECE_LONG, PIECE_SHORT), 0, 5)
        # print('Drawing on: ', (pos[0] * CELL_SIZE + PIECE_OFFSET, pos[1] * CELL_SIZE + PIECE_OFFSET, PIECE_LONG, PIECE_SHORT))

        text = font.render(str(counter), True, OUTLINE, None)
        text_rect = text.get_rect()
        text_rect.center = ((pos[1] + 1) * CELL_SIZE + PIECE_OFFSET + PIECE_LONG // 2, (ROWS - pos[0]) * CELL_SIZE + PIECE_OFFSET + PIECE_SHORT // 2)

        win.blit(text, text_rect)

        table[pos[0]][pos[1]] = 'O'
        table[pos[0]][pos[1] + 1] = 'O'

        return True



    return True


# Proverava da li je moguce postaviti figuru datog igraca na datu poziciju:
def check_move(player: bool, table: list[list[str]], x: int, y: int) -> bool:

    # TODO: Provera da li je indeks koji smo uneli uopste moguc za datu matricu:
    if (x < 0 or x >= len(table)) or (y < 0 or y >= len(table)):
        # print("Invalid index for position! Please try again!")
        return False

    if player:  
        # Za slucaj da trenutno treba da igra X: 
        # TODO: Provera edge-case-ova da li je moguce postavljanje na datoj poziciji za igraca X:
        # Da je x barem 2 polja manji od max visine tabele? Kako bi stala figura koja je visine 2, duzine 1
        if x > len(table) - 2:
            # print("Invalid index for position! Please try again!")
            return False

        # TODO: Provera da li su pozicije uopste slobodne za igraca O:
        if table[x][y] == ' ' and table[x+1][y] == ' ':
            return True
        else:
            # print("Invalid move, position is already occupied!")
            return False

    else:   
        # Za slucaj da trenutno treba da igra O:

        # TODO: Provera edge-case-ova da li je moguce postavljanje na datoj poziciji za igraca O:
        # Da je y barem 2 polja manji od max duzine tabele? Kako bi stala figura koja je visine 1, duzine 2
        if y > len(table) - 2:
            # print("Invalid index for position! Please try again!")
            return False

        # TODO: Provera da li su pozicije uopste slobodne za igraca X:
        if table[x][y] == ' ' and table[x][y+1] == ' ':
            return True
        else:
            # print("Invalid move, position is already occupied!")
            return False

main()