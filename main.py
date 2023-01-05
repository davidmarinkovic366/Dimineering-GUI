import pygame
from Dims import Dims

# from const.constants import WIDTH, HEIGHT
from const.constants import BROWN, WHITE, OUTLINE, BACKGROUND, PIECE_X_COLOR, PIECE_O_COLOR, MENU_BACKGROUND_COLOR, BUTTON_COLOR

dims: Dims = Dims(6)

# num = 8

# rows = num
# cols = num
# dim = rows + 2
# cell_size = WIDTH // dim
# piece_long = 2 * cell_size - 2 *(cell_size // 10)
# piece_short = cell_size - 2 *(cell_size // 10)
# piece_offset = cell_size // 10

pygame.init()

WIN = pygame.display.set_mode((dims.WIDTH, dims.HEIGHT))
pygame.display.set_caption('Domineering!')
font = pygame.font.Font('cascadiacode.ttf', 32)

FPS: int = 60
LETTER_ARRAY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main(dims: Dims) -> None:

    run = True
    clock = pygame.time.Clock()
    player: bool
    move_counter: int = 0

    # x_first, table_size
    res: tuple[bool, int] = init_game(WIN, clock, dims)
    if res == None:
        pygame.quit()

    player = res[0]     # da li X igra prvi?
    dims = res[2]       # overridujemo dimenzije
    # rows = res[1]
    # cols = res[1]
    # dim = rows + 2
    # cell_size = WIDTH // dim
    # piece_long = 2 * cell_size - 2 *(cell_size // 10)
    # piece_short = cell_size - 2 *(cell_size // 10)
    # piece_offset = cell_size // 10

    # refresh(res[1])

    board: list[list[str]] = create_board(res[1])   # kreiramo tabelu u memoriji
    draw_board(WIN, dims)
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                print('You clicked on:', get_cell_pos(pygame.mouse.get_pos(), dims))
                piece_set = False
                if not get_cell_pos(pygame.mouse.get_pos(), dims) == (None, None):
                    piece_set = set_figure(WIN, get_cell_pos(pygame.mouse.get_pos(), dims), player, move_counter, board, dims)
                if piece_set:
                    player = not player
                    move_counter = move_counter + 1

        pygame.display.update()

    pygame.quit()



###
# Funkcija za odabir ko prvi igra, i kolika je velicina tabele:
# ###
def init_game(win, clock, dims: Dims) -> tuple[bool, int, Dims] or None:

    win.fill(BACKGROUND)

    first_player: bool = False
    board_size: int = 0
    quit_event: bool = False
    got_player: bool = False
    got_size: bool = False
    

    # Forma za odabir igraca:
    pygame.draw.rect(win, MENU_BACKGROUND_COLOR, (dims.WIDTH // 10, dims.HEIGHT // 8, (dims.WIDTH // 10 * 8), (dims.HEIGHT // 8 * 6)), 0, 5)
    
    text = font.render("First play?", False, OUTLINE, None)
    text_rect = text.get_rect()
    text_rect.center = (dims.WIDTH // 2, dims.HEIGHT // 4)
    win.blit(text, text_rect)

    # Dugme za odabir igraca X:
    x_text = font.render("X", False, OUTLINE, None)
    x_text_rect = x_text.get_rect()
    pygame.draw.rect(win, PIECE_O_COLOR, (dims.WIDTH // 2 - 2 * dims.cell_size, dims.HEIGHT // 2 + dims.cell_size, dims.cell_size, dims.cell_size), 0, 5)
    x_text_rect.center = (dims.WIDTH // 2 - 2 * dims.cell_size + dims.cell_size // 2, dims.HEIGHT // 2 + dims.cell_size + dims.cell_size // 2)
    win.blit(x_text, x_text_rect)

    
    # Dugme za odabir igraca Y:
    y_text = font.render("Y", False, OUTLINE, None)
    y_text_rect = y_text.get_rect()
    pygame.draw.rect(win, PIECE_X_COLOR, (dims.WIDTH // 2 +  dims.cell_size, dims.HEIGHT // 2 + dims.cell_size, dims.cell_size, dims.cell_size), 0, 5)
    y_text_rect.center = (dims.WIDTH // 2 + dims.cell_size + dims.cell_size // 2, dims.HEIGHT // 2 + dims.cell_size + dims.cell_size // 2)
    win.blit(y_text, y_text_rect)

    while not got_player:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_event = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # da li je kliknuto na X?
                if (pos[0] >= dims.WIDTH // 2 - 2 * dims.cell_size and pos[0] <= dims.WIDTH // 2 - dims.cell_size and pos[1] >= dims.HEIGHT // 2 + dims.cell_size and pos[1] <= dims.HEIGHT // 2 + 2 * dims.cell_size):
                    print('X selected!')
                    first_player = True
                    got_player = True

                elif (pos[0] >= dims.WIDTH // 2 + dims.cell_size and pos[0] <= dims.WIDTH // 2 + 2 * dims.cell_size and pos[1] >= dims.HEIGHT // 2 + dims.cell_size and pos[1] <= dims.HEIGHT // 2 + 2 * dims.cell_size):
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
    pygame.draw.rect(win, MENU_BACKGROUND_COLOR, (dims.WIDTH // 10, dims.HEIGHT // 8, (dims.WIDTH // 10 * 8), (dims.HEIGHT // 8 * 6)), 0, 5)
    
    text = font.render("Table size?", False, OUTLINE, None)
    text_rect = text.get_rect()
    text_rect.center = (dims.WIDTH // 2, dims.HEIGHT // 4)
    win.blit(text, text_rect)

    # Rect za ispis unete velicine:
    # Ispis velicine moramo da uradimo unutar while petlje, jer moze da se desi da je dvocifrena, pa moramo da osvezimo prikaz:

    # Unutar ovog kvadrata ispisujemo velicinu:
    pygame.draw.rect(win, PIECE_X_COLOR, (dims.WIDTH // 2 - 2 * dims.cell_size - dims.cell_size // 2, dims.HEIGHT // 2 + dims.cell_size, 2 * dims.cell_size, dims.cell_size), 0, 5)

    # Dugme za potvrdu velicine:
    text = font.render("Play!", False, OUTLINE, None)
    text_rect = text.get_rect()
    pygame.draw.rect(win, PIECE_O_COLOR, (dims.WIDTH // 2 + dims.cell_size // 2, dims.HEIGHT // 2 + dims.cell_size, 2 * dims.cell_size, dims.cell_size), 0, 5)
    text_rect.center = (dims.WIDTH // 2 + dims.cell_size + dims.cell_size // 2, dims.HEIGHT // 2 + dims.cell_size + dims.cell_size // 2)
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
                    
                    pygame.draw.rect(win, PIECE_X_COLOR, (dims.WIDTH // 2 - 2 * dims.cell_size - dims.cell_size // 2, dims.HEIGHT // 2 + dims.cell_size, 2 * dims.cell_size, dims.cell_size), 0, 5)
                    size = font.render(str(board_size), False, OUTLINE, None)
                    size_rect = size.get_rect()
                    size_rect.center = (dims.WIDTH // 2 - 2 * dims.cell_size + dims.cell_size // 2, dims.HEIGHT // 2 + dims.cell_size + dims.cell_size // 2)
                    win.blit(size, size_rect)

                elif event.key == pygame.K_BACKSPACE:
                    board_size = board_size // 10

                    pygame.draw.rect(win, PIECE_X_COLOR, (dims.WIDTH // 2 - 2 * dims.cell_size - dims.cell_size // 2, dims.HEIGHT // 2 + dims.cell_size, 2 * dims.cell_size, dims.cell_size), 0, 5)
                    size = font.render(str(board_size), False, OUTLINE, None)
                    size_rect = size.get_rect()
                    size_rect.center = (dims.WIDTH // 2 - 2 * dims.cell_size + dims.cell_size // 2, dims.HEIGHT // 2 + dims.cell_size + dims.cell_size // 2)
                    win.blit(size, size_rect)

                # ako je pritiskom na enter korisnik potvrdio pocetak igre:
                elif event.key == pygame.K_RETURN:
                    got_size = True
            
            # ako je korisnik misem kliknuo na pocetak igre?
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] >= dims.WIDTH // 2 + dims.cell_size + dims.cell_size // 2 and pos[0] <= dims.WIDTH // 2 + dims.cell_size + dims.cell_size // 2 + 2 * dims.cell_size and pos[1] >= dims.HEIGHT // 2 + dims.cell_size and pos[1] <= dims.HEIGHT // 2 + 2 * dims.cell_size):
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
    dim = Dims(board_size)          # inicijalizujemo dimenzije
    print(first_player, board_size) # stampa za proveru

    return (first_player, board_size, dim)




def create_board(dim: int) -> list[list[str]]:
    table: list = list()
    for rw in range(0, dim):
        table.append(list())
        for cl in range(0, dim):
            table[rw].append(' ')
    return table


def draw_board(win, dims: Dims):
    win.fill(BACKGROUND)

    is_brown: bool = True
    for row in range(1, dims.rows + 1):
        if dims.rows % 2 == 0:
            is_brown = not is_brown
        for col in range(1, dims.cols + 1):
            color = BROWN if is_brown else WHITE
            is_brown = not is_brown
            pygame.draw.rect(win, color, (row * dims.cell_size, col * dims.cell_size, dims.cell_size, dims.cell_size))
    
    # Up and down letter array:
    for i in range(1, dims.cols + 1):
        
        text = font.render(LETTER_ARRAY[i-1], True, OUTLINE, None)
        text_rect = text.get_rect()

        text_rect.center = (i * dims.cell_size + dims.cell_size // 2, dims.cell_size // 2)
        WIN.blit(text, text_rect)

        text_rect.center = (i * dims.cell_size + dims.cell_size // 2, (dims.rows + 1) * dims.cell_size + dims.cell_size // 2)
        WIN.blit(text, text_rect)

    # Left and right number array
    num: int = 0
    for i in range(dims.rows, 0, -1):

        text = font.render(str(num), True, OUTLINE, None)
        text_rect = text.get_rect()
        num = num + 1

        text_rect.center = ( dims.cell_size // 2, i * dims.cell_size + dims.cell_size // 2)
        WIN.blit(text, text_rect)

        text_rect.center = ( (dims.cols + 1) * dims.cell_size + dims.cell_size // 2, i * dims.cell_size + dims.cell_size // 2)
        WIN.blit(text, text_rect)


def get_cell_pos(clicked_pos, dims: Dims) -> tuple:

    x_temp = clicked_pos[0]
    y_temp = clicked_pos[1]

    x_pos: int = int(x_temp / dims.cell_size)
    y_pos: int = int(y_temp / dims.cell_size)

    if (x_pos < 1 or y_pos < 1) or (x_pos > dims.rows or y_pos > dims.cols):
        return (None, None)

    return (dims.rows - y_pos, x_pos - 1)


def set_figure(win, pos: tuple[int, int], player: bool, counter: int, table: list[list[str]], dims: Dims) -> bool: 
    
    res = check_move(player, table, pos[0], pos[1])
    print(res)
    if not res:
        return False

    # Inace mozemo da postavimo!
    # Igra X:
    if player:

        pygame.draw.rect(win, PIECE_X_COLOR, ((pos[1] + 1) * dims.cell_size + dims.piece_offset, (dims.rows - pos[0] - 1) * dims.cell_size + dims.piece_offset, dims.piece_short, dims.piece_long), 0, 5)
        # print('Drawing on: ', (pos[0] * CELL_SIZE + PIECE_OFFSET, pos[1] * CELL_SIZE + PIECE_OFFSET, PIECE_SHORT, PIECE_LONG))

        text = font.render(str(counter), True, OUTLINE, None)
        text_rect = text.get_rect()
        text_rect.center = ((pos[1] + 1) * dims.cell_size + dims.piece_offset + dims.piece_short // 2, (dims.rows - pos[0] - 1) * dims.cell_size + dims.piece_offset + dims.piece_long // 2)

        win.blit(text, text_rect)

        table[pos[0]][pos[1]] = 'X'
        table[pos[0] + 1][pos[1]] = 'X'
        return True

    else:

        pygame.draw.rect(win, PIECE_O_COLOR, ((pos[1] + 1) * dims.cell_size + dims.piece_offset, (dims.rows - pos[0]) * dims.cell_size + dims.piece_offset, dims.piece_long, dims.piece_short), 0, 5)
        # print('Drawing on: ', (pos[0] * CELL_SIZE + PIECE_OFFSET, pos[1] * CELL_SIZE + PIECE_OFFSET, PIECE_LONG, PIECE_SHORT))

        text = font.render(str(counter), True, OUTLINE, None)
        text_rect = text.get_rect()
        text_rect.center = ((pos[1] + 1) * dims.cell_size + dims.piece_offset + dims.piece_long // 2, (dims.rows - pos[0]) * dims.cell_size + dims.piece_offset + dims.piece_short // 2)

        win.blit(text, text_rect)

        table[pos[0]][pos[1]] = 'O'
        table[pos[0]][pos[1] + 1] = 'O'

        return True

    # FIXME: izbrisi, ne moze ovde da dodje svakako;
    # return True


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

main(dims)