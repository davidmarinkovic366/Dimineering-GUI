import pygame

from const.constants import WIDTH, HEIGHT
num: int = 8

rows: int = num
cols: int = num
dim: int = rows + 2
cell_size = WIDTH // dim
piece_long = 2 * cell_size - 2 *(cell_size // 10)
piece_short = cell_size - 2 *(cell_size // 10)
piece_offset = cell_size // 10

from const.constants import BROWN, WHITE, OUTLINE, BACKGROUND, PIECE_X_COLOR, PIECE_O_COLOR, MENU_BACKGROUND_COLOR, BUTTON_COLOR

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
    player: bool
    move_counter: int = 0

    # x_first, table_size
    res: tuple[bool, int] = init_game(WIN, clock)
    if res == None:
        pygame.quit()

    player = res[0]     # da li X igra prvi?
    rows = res[1]
    cols = res[1]
    dim = rows + 2
    cell_size = WIDTH // dim
    piece_long = 2 * cell_size - 2 *(cell_size // 10)
    piece_short = cell_size - 2 *(cell_size // 10)
    piece_offset = cell_size // 10

    # refresh(res[1])

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



###
# Funkcija za odabir ko prvi igra, i kolika je velicina tabele:
# ###
def init_game(win, clock) -> tuple[bool, int] or None:

    win.fill(BACKGROUND)

    first_player: bool = False
    board_size: int = 0
    quit_event: bool = False
    got_player: bool = False
    got_size: bool = False
    

    # Forma za odabir igraca:
    pygame.draw.rect(win, MENU_BACKGROUND_COLOR, (WIDTH // 10, HEIGHT // 8, (WIDTH // 10 * 8), (HEIGHT // 8 * 6)), 0, 5)
    
    text = font.render("First play?", False, OUTLINE, None)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 4)
    win.blit(text, text_rect)

    # Dugme za odabir igraca X:
    x_text = font.render("X", False, OUTLINE, None)
    x_text_rect = x_text.get_rect()
    pygame.draw.rect(win, PIECE_O_COLOR, (WIDTH // 2 - 2 * cell_size, HEIGHT // 2 + cell_size, cell_size, cell_size), 0, 5)
    x_text_rect.center = (WIDTH // 2 - 2 * cell_size + cell_size // 2, HEIGHT // 2 + cell_size + cell_size // 2)
    win.blit(x_text, x_text_rect)

    
    # Dugme za odabir igraca Y:
    y_text = font.render("Y", False, OUTLINE, None)
    y_text_rect = y_text.get_rect()
    pygame.draw.rect(win, PIECE_X_COLOR, (WIDTH // 2 +  cell_size, HEIGHT // 2 + cell_size, cell_size, cell_size), 0, 5)
    y_text_rect.center = (WIDTH // 2 + cell_size + cell_size // 2, HEIGHT // 2 + cell_size + cell_size // 2)
    win.blit(y_text, y_text_rect)

    while not got_player:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_event = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # da li je kliknuto na X?
                if (pos[0] >= WIDTH // 2 - 2 * cell_size and pos[0] <= WIDTH // 2 - cell_size and pos[1] >= HEIGHT // 2 + cell_size and pos[1] <= HEIGHT // 2 + 2 * cell_size):
                    print('X selected!')
                    first_player = True
                    got_player = True

                elif (pos[0] >= WIDTH // 2 + cell_size and pos[0] <= WIDTH // 2 + 2 * cell_size and pos[1] >= HEIGHT // 2 + cell_size and pos[1] <= HEIGHT // 2 + 2 * cell_size):
                    print('Y selected!')
                    first_player = False
                    got_player = True

        pygame.display.update()
    
    # sad trazimo unos velicine tabele:
    win.fill(BACKGROUND)

    # ako smo kliknuli na dugme za zatvaranje prozora, ne proveravamo dalje!
    if quit_event:
        return None
    
    # Forma za unos velicine tabele:
    pygame.draw.rect(win, MENU_BACKGROUND_COLOR, (WIDTH // 10, HEIGHT // 8, (WIDTH // 10 * 8), (HEIGHT // 8 * 6)), 0, 5)
    
    text = font.render("Table size?", False, OUTLINE, None)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 4)
    win.blit(text, text_rect)

    # Rect za ispis unete velicine:
    # Ispis velicine moramo da uradimo unutar while petlje, jer moze da se desi da je dvocifrena, pa moramo da osvezimo prikaz:

    # Unutar ovog kvadrata ispisujemo velicinu:
    pygame.draw.rect(win, PIECE_X_COLOR, (WIDTH // 2 - 2 * cell_size - cell_size // 2, HEIGHT // 2 + cell_size, 2 * cell_size, cell_size), 0, 5)

    # Dugme za potvrdu velicine:
    text = font.render("Play!", False, OUTLINE, None)
    text_rect = text.get_rect()
    pygame.draw.rect(win, PIECE_O_COLOR, (WIDTH // 2 + cell_size // 2, HEIGHT // 2 + cell_size, 2 * cell_size, cell_size), 0, 5)
    text_rect.center = (WIDTH // 2 + cell_size + cell_size // 2, HEIGHT // 2 + cell_size + cell_size // 2)
    win.blit(text, text_rect)

    quit_event = False

    while not got_size:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                got_size = True
                quit_event = True
            
            elif event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_0 and event.key <= pygame.K_9:
                    board_size = board_size * 10 + (event.key - 48)     # pygame ne vraca koje dugme je konkretno kliknuto, vec stanje svih, tako da moramo ovako da proverimo koji je broj, 48 je sifra za 0:
                    
                    pygame.draw.rect(win, PIECE_X_COLOR, (WIDTH // 2 - 2 * cell_size - cell_size // 2, HEIGHT // 2 + cell_size, 2 * cell_size, cell_size), 0, 5)
                    size = font.render(str(board_size), False, OUTLINE, None)
                    size_rect = size.get_rect()
                    size_rect.center = (WIDTH // 2 - 2 * cell_size + cell_size // 2, HEIGHT // 2 + cell_size + cell_size // 2)
                    win.blit(size, size_rect)

                elif event.key == pygame.K_BACKSPACE:
                    board_size = board_size // 10

                    pygame.draw.rect(win, PIECE_X_COLOR, (WIDTH // 2 - 2 * cell_size - cell_size // 2, HEIGHT // 2 + cell_size, 2 * cell_size, cell_size), 0, 5)
                    size = font.render(str(board_size), False, OUTLINE, None)
                    size_rect = size.get_rect()
                    size_rect.center = (WIDTH // 2 - 2 * cell_size + cell_size // 2, HEIGHT // 2 + cell_size + cell_size // 2)
                    win.blit(size, size_rect)

                # ako je pritiskom na enter korisnik potvrdio pocetak igre:
                elif event.key == pygame.K_RETURN:
                    got_size = True
            
            # ako je korisnik misem kliknuo na pocetak igre?
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] >= WIDTH // 2 + cell_size + cell_size // 2 and pos[0] <= WIDTH // 2 + cell_size + cell_size // 2 + 2 * cell_size and pos[1] >= HEIGHT // 2 + cell_size and pos[1] <= HEIGHT // 2 + 2 * cell_size):
                    got_size = True

        # Za slucaj da je velicina i dalje 0?
        if got_size:
            if board_size <= 0:
                got_size = False


        pygame.display.update()

    # ako smo kliknuli na dugme za zatvaranje prozora, zatvaramo prozor i tjt:
    if quit_event:
        return None

    # inace, imamo sve, mozemo da pocnemo sa igrom:
    print(first_player, board_size)
    return (first_player, board_size)




def create_board() -> list[list[str]]:
    table: list = list()
    for rw in range(0, rows):
        table.append(list())
        for cl in range(0, cols):
            table[rw].append(' ')
    return table


def draw_board(win):
    win.fill(BACKGROUND)

    is_brown: bool = True
    for row in range(1, rows + 1):
        if rows % 2 == 0:
            is_brown = not is_brown
        for col in range(1, cols + 1):
            color = BROWN if is_brown else WHITE
            is_brown = not is_brown
            pygame.draw.rect(win, color, (row * cell_size, col * cell_size, cell_size, cell_size))
    
    # Up and down letter array:
    for i in range(1, cols + 1):
        
        text = font.render(LETTER_ARRAY[i-1], True, OUTLINE, None)
        text_rect = text.get_rect()

        text_rect.center = (i * cell_size + cell_size // 2, cell_size // 2)
        WIN.blit(text, text_rect)

        text_rect.center = (i * cell_size + cell_size // 2, (rows + 1) * cell_size + cell_size // 2)
        WIN.blit(text, text_rect)

    # Left and right number array
    num: int = 0
    for i in range(rows, 0, -1):

        text = font.render(str(num), True, OUTLINE, None)
        text_rect = text.get_rect()
        num = num + 1

        text_rect.center = ( cell_size // 2, i * cell_size + cell_size // 2)
        WIN.blit(text, text_rect)

        text_rect.center = ( (cols + 1) * cell_size + cell_size // 2, i * cell_size + cell_size // 2)
        WIN.blit(text, text_rect)


def get_cell_pos(clicked_pos) -> tuple:

    x_temp = clicked_pos[0]
    y_temp = clicked_pos[1]

    x_pos: int = int(x_temp / cell_size)
    y_pos: int = int(y_temp / cell_size)

    if (x_pos < 1 or y_pos < 1) or (x_pos > rows or y_pos > cols):
        return (None, None)

    return (rows - y_pos, x_pos - 1)


def set_figure(win, pos: tuple[int, int], player: bool, counter: int, table: list[list[str]]) -> bool: 
    
    res = check_move(player, table, pos[0], pos[1])
    print(res)
    if not res:
        return False

    # Inace mozemo da postavimo!
    # Igra X:
    if player:

        pygame.draw.rect(win, PIECE_X_COLOR, ((pos[1] + 1) * cell_size + piece_offset, (rows - pos[0] - 1) * cell_size + piece_offset, piece_short, piece_long), 0, 5)
        # print('Drawing on: ', (pos[0] * CELL_SIZE + PIECE_OFFSET, pos[1] * CELL_SIZE + PIECE_OFFSET, PIECE_SHORT, PIECE_LONG))

        text = font.render(str(counter), True, OUTLINE, None)
        text_rect = text.get_rect()
        text_rect.center = ((pos[1] + 1) * cell_size + piece_offset + piece_short // 2, (rows - pos[0] - 1) * cell_size + piece_offset + piece_long // 2)

        win.blit(text, text_rect)

        table[pos[0]][pos[1]] = 'X'
        table[pos[0]  + 1][pos[1]] = 'X'
        return True

    else:

        pygame.draw.rect(win, PIECE_O_COLOR, ((pos[1] + 1) * cell_size + piece_offset, (rows - pos[0]) * cell_size + piece_offset, piece_long, piece_short), 0, 5)
        # print('Drawing on: ', (pos[0] * CELL_SIZE + PIECE_OFFSET, pos[1] * CELL_SIZE + PIECE_OFFSET, PIECE_LONG, PIECE_SHORT))

        text = font.render(str(counter), True, OUTLINE, None)
        text_rect = text.get_rect()
        text_rect.center = ((pos[1] + 1) * cell_size + piece_offset + piece_long // 2, (rows - pos[0]) * cell_size + piece_offset + piece_short // 2)

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