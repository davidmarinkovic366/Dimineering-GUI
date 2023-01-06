import pygame
import copy
from Dims import Dims

# from const.constants import WIDTH, HEIGHT
from const.constants import BROWN, WHITE, OUTLINE, BACKGROUND, PIECE_X_COLOR, PIECE_O_COLOR, MENU_BACKGROUND_COLOR, BUTTON_COLOR

dims: Dims = Dims(6)        # inicijalne dimenzije, za iscrtavanje menija

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

    # x_first, table_size, other_dimensions_for_table
    res: tuple[bool, int, Dims] = init_game(WIN, clock, dims)
    if res == None:
        pygame.quit()

    player = res[0]     # da li X igra prvi?
    dims = res[2]       # overridujemo dimenzije

    board: list[list[str]] = create_board(res[1])   # kreiramo tabelu u memoriji
    draw_board(WIN, dims)

    # Petlja koja traje za vreme trajanja igre:
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
# Funkcija za odabir prvog igraca i dimenzije tabele tabele:
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

    # Ispitivanje korisnickog unosa ko je prvi igrac, X ili Y:
    while not got_player:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_event = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Da li je kliknuto na X?
                if (pos[0] >= dims.WIDTH // 2 - 2 * dims.cell_size and pos[0] <= dims.WIDTH // 2 - dims.cell_size and pos[1] >= dims.HEIGHT // 2 + dims.cell_size and pos[1] <= dims.HEIGHT // 2 + 2 * dims.cell_size):
                    print('X selected!')
                    first_player = True
                    got_player = True

                elif (pos[0] >= dims.WIDTH // 2 + dims.cell_size and pos[0] <= dims.WIDTH // 2 + 2 * dims.cell_size and pos[1] >= dims.HEIGHT // 2 + dims.cell_size and pos[1] <= dims.HEIGHT // 2 + 2 * dims.cell_size):
                    print('Y selected!')
                    first_player = False
                    got_player = True

        pygame.display.update()
    
    
    # Brisanje prvog menija, odnosno, crtamo pozadinu preko svega, ne postoji stvar kao sto je
    # Brisanje nacrtanih elementa u pygame
    win.fill(BACKGROUND)

    # Sad trazimo unos velicine tabele:
    # Ako smo kliknuli na dugme za zatvaranje prozora, ne proveravamo dalje!
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

    # Pomocna promenljiva, za ispitivanje zasto smo izasli iz petlje:
    quit_event = False

    # Ispitivanje korisnickog unosa dimenzije tabele (moze misem i klikom na enter):
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

    # Ako smo kliknuli na dugme za zatvaranje prozora, zatvaramo prozor i tjt:
    if quit_event:
        return None

    # Inace, imamo sve, mozemo da pocnemo sa igrom:
    dim = Dims(board_size)          # Inicijalizujemo dimenzije
    print(first_player, board_size) # Stampa za proveru

    return (first_player, board_size, dim)

# Kreiranje matrice dimenzije dim x dim u memoriji:
def create_board(dim: int) -> list[list[str]]:
    table: list = list()
    for rw in range(0, dim):
        table.append(list())
        for cl in range(0, dim):
            table[rw].append(' ')
    return table

# Crtanje inicijalnog stanja tabele na prozoru:
def draw_board(win, dims: Dims):
    # Pozadina
    win.fill(BACKGROUND)

    # Iscrtavanje kvadratica tabele: 
    is_brown: bool = True
    for row in range(1, dims.rows + 1):
        if dims.rows % 2 == 0:
            is_brown = not is_brown
        for col in range(1, dims.cols + 1):
            color = BROWN if is_brown else WHITE
            is_brown = not is_brown
            pygame.draw.rect(win, color, (row * dims.cell_size, col * dims.cell_size, dims.cell_size, dims.cell_size))
    
    # Gornji i donji tekst na tabeli:
    for i in range(1, dims.cols + 1):
        
        # Inicijalizacija teksta koji se ispisuje:
        text = font.render(LETTER_ARRAY[i-1], True, OUTLINE, None)
        text_rect = text.get_rect()

        # Ispis u gornjem redu:
        text_rect.center = (i * dims.cell_size + dims.cell_size // 2, dims.cell_size // 2)
        WIN.blit(text, text_rect)

        # Ispis u donjem redu:
        text_rect.center = (i * dims.cell_size + dims.cell_size // 2, (dims.rows + 1) * dims.cell_size + dims.cell_size // 2)
        WIN.blit(text, text_rect)

    # Levi i desni tekst na tabeli:
    num: int = 0
    for i in range(dims.rows, 0, -1):

        # Inicijalizacija broja koji se ispisuje:
        text = font.render(str(num), True, OUTLINE, None)
        text_rect = text.get_rect()
        num = num + 1

        # Ispis u levoj koloni:
        text_rect.center = ( dims.cell_size // 2, i * dims.cell_size + dims.cell_size // 2)
        WIN.blit(text, text_rect)

        # Ispis u desnoj koloni:
        text_rect.center = ( (dims.cols + 1) * dims.cell_size + dims.cell_size // 2, i * dims.cell_size + dims.cell_size // 2)
        WIN.blit(text, text_rect)

# Racunanje pozicije polja u memoriji na osnovu dimenzija prozora i pozicije prozora na koju je 
# korisnik kliknuo:
def get_cell_pos(clicked_pos, dims: Dims) -> tuple:

    x_temp = clicked_pos[0]
    y_temp = clicked_pos[1]

    x_pos: int = int(x_temp / dims.cell_size)
    y_pos: int = int(y_temp / dims.cell_size)

    # Ukoliko smo kliknuli van okvira tabele, onda se vraca tuple(None, None) kao ne-validan potez:
    # (Ne validan u pogledu pozicije na koju je kliknuto, postoji funkcija koja ispituje i validnost poteza
    # u pogledu zauzetosti pozicije i dimenzije figure koja se postavlja);
    if (x_pos < 1 or y_pos < 1) or (x_pos > dims.rows or y_pos > dims.cols):
        return (None, None)

    return (dims.rows - y_pos, x_pos - 1)

# Postavljanje figure na tablu / u memoriji i iscrtavanje na klijentskom prozoru;
def set_figure(win, pos: tuple[int, int], player: bool, counter: int, table: list[list[str]], dims: Dims) -> bool: 
    
    # Da li je potez validan u pogledu zauzetosti polja:
    res = check_move(player, table, pos[0], pos[1])
    
    # FIXME: remove;
    # print(res)

    # Vracamo obavestenje da nismo postavili figuru na dato polje:
    if not res:
        return False

    # Inace mozemo da postavimo!
    # Postavljanje u slucaju da figuru postavlja igrac X:
    if player:

        # Iscrtavanje figure igraca X sa pocetkom u datoj poziciji:
        pygame.draw.rect(win, PIECE_X_COLOR, ((pos[1] + 1) * dims.cell_size + dims.piece_offset, (dims.rows - pos[0] - 1) * dims.cell_size + dims.piece_offset, dims.piece_short, dims.piece_long), 0, 5)

        # Ispis rednog broja poteza na vrh figure:
        text = font.render(str(counter), True, OUTLINE, None)
        text_rect = text.get_rect()
        text_rect.center = ((pos[1] + 1) * dims.cell_size + dims.piece_offset + dims.piece_short // 2, (dims.rows - pos[0] - 1) * dims.cell_size + dims.piece_offset + dims.piece_long // 2)

        win.blit(text, text_rect)

        # Postavljanje figure u memoriji:
        table[pos[0]][pos[1]] = 'X'
        table[pos[0] + 1][pos[1]] = 'X'

        # Vracamo odgovor da je figure uspesno postavljena:
        return True

    else:
        # Postavljanje u slucaju da figuru postavlja igrac X:
        
        # Iscrtavanje figure igraca Y sa pocetkom u datoj poziciji:
        pygame.draw.rect(win, PIECE_O_COLOR, ((pos[1] + 1) * dims.cell_size + dims.piece_offset, (dims.rows - pos[0]) * dims.cell_size + dims.piece_offset, dims.piece_long, dims.piece_short), 0, 5)

        # Ispis rednog broja poteza na vrh figure:
        text = font.render(str(counter), True, OUTLINE, None)
        text_rect = text.get_rect()
        text_rect.center = ((pos[1] + 1) * dims.cell_size + dims.piece_offset + dims.piece_long // 2, (dims.rows - pos[0]) * dims.cell_size + dims.piece_offset + dims.piece_short // 2)

        win.blit(text, text_rect)

        # Postavljanje figure u memoriji:
        table[pos[0]][pos[1]] = 'O'
        table[pos[0]][pos[1] + 1] = 'O'

        # Vracamo odgovor da je figure uspesno postavljena:
        return True

    # FIXME: izbrisi, ne moze ovde da dodje svakako;
    # return True


# Proverava da li je moguce postaviti figuru datog igraca na datu poziciju:
def check_move(player: bool, table: list[list[str]], x: int, y: int) -> bool:

    # Provera da li je indeks koji smo uneli uopste moguc za datu matricu:
    if (x < 0 or x >= len(table)) or (y < 0 or y >= len(table)):
        return False

    if player:  
        # Za slucaj da trenutno treba da igra X: 
        # Provera edge-case-ova da li je moguce postavljanje na datoj poziciji za igraca X:
        # Da je x barem 2 polja manji od max visine tabele? Kako bi stala figura koja je visine 2, duzine 1
        if x > len(table) - 2:
            return False

        # Provera da li su pozicije uopste slobodne za igraca O:
        if table[x][y] == ' ' and table[x+1][y] == ' ':
            return True
        else:
            return False

    else:   
        # Za slucaj da trenutno treba da igra O:

        # Provera edge-case-ova da li je moguce postavljanje na datoj poziciji za igraca O:
        # Da je y barem 2 polja manji od max duzine tabele? Kako bi stala figura koja je visine 1, duzine 2
        if y > len(table) - 2:
            return False

        # Provera da li su pozicije uopste slobodne za igraca X:
        if table[x][y] == ' ' and table[x][y+1] == ' ':
            return True
        else:
            return False

# Stanje u grafu predstavljamo preko matrice stanja, e sad, zbog limitacije da matrica ne moze da bude 
# kljuc u dict objektu, moramo nekako drugacije da predstavimo matricu, pa je string jedno od resenja koje
# mozemo da iskoristimo;

# Pretvara matricu u string:
def matrix_to_string(mat: list[list[str]],  rows: int, cols: int) -> str:
    data: str = ''
    for i in range(0, rows):
        for j in range(0, cols):
            data += mat[i][j]

    return data

# Pretvara string u matricu zadatih dimenzija:
def string_to_matrix(str: str, rows: int, cols: int) -> list[list[str]]:
    mat = list()
    for i in range(0, rows):
        mat.append(list())
        for j in range(0, cols):
            mat[i].append(str[i * rows + j])
    
    return mat

# Generisemo sva moguca stanja u koja moze da predje tabela na osnuvo prosledjenog stanja
# i informacije ko sledeci igra;
# [player == True]  -> X 
# [player == False] -> O
def possible_states(table: list[list[str]], dim: int, player: bool) -> list[list[list[str]]] or None:
    # Cuvamo sva moguca stanja u koja moze da predje trenutno stanje:
    states: list = list()

    # Pokusavamo da postavimo figuru na svaku mogucu poziciju:
    for x in range(0, dim):
        for y in range(0, dim):
            if table[x][y] == ' ' and check_move(player, table, x, y):
                
                # Kopiramo tabelu, kako bi mogli da nastavimo sa ispitivanjem: 
                new_table: list[list[str]] = copy.deepcopy(table)
                
                # Postavljamo odgovarajucu figuru na zadatu poziciju:
                if player:
                    new_table[x][y] = 'X'
                    new_table[x+1][y] = 'X'
                else:
                    new_table[x][y] = 'O'
                    new_table[x][y+1] = 'O'

                # Dodajemo stanje u listu mogucih:
                states.append(new_table)
    
    if states:
        return states
    else:
        return None

# Funkcija za procenu stanja;
# Ideja je da je stanje bolje ukoliko protivniku ostavlja manje mogucih poteza, odnosno,
# smanjujemo mu sanse da nama ostavi manje mesta:
# Sto manja vrednost, to bolje stanje za trenutnog igraca!
def evaluate_state(state: list[list[str]], dim: int, next_player: bool) -> int:

    # Brojimo koliko mogucih stanja nakon postavljanja nase figure ima protivnik:
    state_counter: int = 0
    for x in range(0, dim):
        for y in range(0, dim):
            if state[x][y] == ' ' and check_move(next_player, state, x, y):
                state_counter += 1
    
    return state_counter

# Funkcija koja vraca najbolje moguce stanje od liste prosledjenih stanja:
def max_state(states_list: list[list[list[str]]], dim: int, current_player: bool) -> list[list[str]]:

    # Recimo da je prvo stanje najbolje, zbog uporedjivanja:
    max_state: list[list[str]] = states_list[0] # uzimamo prvi kao najbolji
    max_state_val = evaluate_state(max_state, dim, not current_player)

    # Prolazimo kroz sva moguca stanja, i uporedjujemo sa najboljim:
    for st in states_list:
        curr_state_val: int = evaluate_state(st, dim, not current_player)
        # Ukoliko neko stanje ima manju vrednost od trenutnog najboljeg stanja, onda to stanje postaje
        # novo najbolje stanje;
        if curr_state_val < max_state_val:
            max_state = st
            max_state_val = curr_state_val
    
    return max_state

# Funkcija koja vraca najgore moguce stanje od liste prosledjenih stanja:
def min_state(states_list: list[list[list[str]]], dim: int, current_player: bool) -> list[list[str]]:

    # Recimo da je prvo stanje najgore, zbog uporedjivanja:
    min_state: list[list[str]] = states_list[0]
    min_state_val = evaluate_state(min_state, dim, not current_player)

    # Prolazimo kroz sva moguca stanja, i uporedjujemo sa najgorim:
    for st in states_list:
        curr_state_val: int = evaluate_state(st, dim, not current_player)
        # Ukoliko neko stanje ima vecu vrednost od trenutnog najgoreg stanja, onda to stanje postaje
        # novo najgore stanje;
        if curr_state_val > min_state_val:
            min_state = st
            min_state_val = curr_state_val

    return min_state

# Rekurzivna funkcija min-max:
def min_max(state: list[list[str]], dim: int, depth: int, player: bool) -> list[list[str]]:

    # Generisemo sva moguca stanja koja mozemo da odigramo:
    state_list: list[list[list[str]]] = possible_states(state, dim, player)
    # Ukoliko ja igram sledeci, trebam od svih mogucih stanja izaberem ono koje ce najvise da mi doprinese,
    # a ukoliko igra protivnik, najvise mi odgovara da racunam da ce da on odigra ono koje mu najmanje doprinosi:
    fun_state = max_state if player else min_state

    # Ukoliko smo dosli na list, ili smo dosli do max dubine koju proveravamo, vracamo 
    if depth == 0 or state_list == None:
        return state
    
    # Pozivamo min-max za sva moguca stanja koja smo generisali na osnovu prosledjenog:
    return fun_state([min_max(st, dim, depth - 1, not player) for st in state_list])





main(dims)