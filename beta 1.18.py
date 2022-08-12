from tkinter import *
from header import *
import random
import time
I_AM_DEVELOPER = False
DEBUG = False
mygame = Game()

#------------------------------------------#
# 0.create log.txt for debug               
#------------------------------------------#
with open('log.txt','w') as logfile:
    pass
def logprint(*args, **kwargs):
    with open('log.txt','a') as logfile:
        print(*args, file=logfile, **kwargs)
#------------------------------------------#
# 1.initialize root window                   
#------------------------------------------#
root = Tk()
root.title('downstack practice tool')
root.geometry('1200x680+0+0')

#---------------------------------------------#
# 2.initialize frame, gamebox to display board                 
#---------------------------------------------#

myframe = Frame(root, bg='black', padx=2, pady=2, height = 680, width = 1000)
myframe.place(x=100, y=50)


gameBox = Canvas(myframe, width=298, height=598, bg='#000000', relief = FLAT)
gameBox.pack()

statBox = Canvas(root, width=90, height=200, relief = FLAT)
statBox.place(x=5, y=200)

holdcanva = Canvas(root, width=70, height=70, bg='#000000', relief = FLAT)
holdcanva.place(x=20,y=50)
holdcanva.create_rectangle(3, 3, 70, 70, width=1, fill='black', outline = 'white',)

nextcanva = Canvas(root, width=70, height=320, bg='#000000', relief = FLAT)
nextcanva.place(x=450,y=50)
nextcanva.create_rectangle(3, 3, 70, 320, width=1, fill='black', outline = 'white')

board_rects = []
hold_rects = []
next_rects = []
def init_rectangles():
    if DEBUG:print('initialize squares of tetris board')

    #draw gridline
    for i in range(1,10):
        gameBox.create_line(30*i, 0, 30*i, 602, width=1, fill='white')
    for j in range(1,20):
        gameBox.create_line(0, 30*j, 602, 30*j, width=1, fill='white')
        
    #draw board
    for j in range(20):
        board_rects.append([])
        for i in range(10):
            color = color_table[mygame.board[j][i]]
            rect = gameBox.create_rectangle(30*i, -30*(j-20), 30*(i+1), -30*(j-19), width=1, fill=color, outline = 'white')               
            board_rects[-1].append(rect)
    #draw hold
    for j in range(4):
        hold_rects.append([])
        for i in range(4):
            color = 'black'
            rect = holdcanva.create_rectangle(15*i +5, -15*(j-4) +5, 15*(i+1) +5, -15*(j-3) +5, width=1, fill=color)               
            hold_rects[-1].append(rect)
    #draw next
    for j in range(20):
        next_rects.append([])
        for i in range(4):
            color = 'black'
            rect = nextcanva.create_rectangle(15*i +5, -15*(j-20) +5, 15*(i+1) +5, -15*(j-19) +5, width=1, fill=color)               
            next_rects[-1].append(rect)
init_rectangles()
#--------------------------------------------------------------------------#
# 3 render function to change color of canva in the board
#--------------------------------------------------------------------------#
stat_line_1 = statBox.create_text(45, 20, text="spike", fill="red",font=('Helvetica 15 bold'))
stat_line_2 = statBox.create_text(45, 60, text="combo", fill="red",font=('Helvetica 15'))
stat_line_3 = statBox.create_text(45, 100, text="b2b", fill="red",font=('Helvetica 15'))
stat_line_4 = statBox.create_text(45, 140, text="all clear", fill="red",font=('Helvetica 15'))
stat_line_5 = statBox.create_text(45, 180, text="attack", fill="red",font=('Helvetica 15'))

def update_stat():
    if DEBUG:print('updating stat')
    line1 = ''
    line2 = ''
    line3 = ''
    line4 = ''
    line5 = ''
    if mygame.line_sent > 0:
        line1 = f'spike {mygame.line_sent}'
    if mygame.combo > 0:
        line2 = f'combo {mygame.combo}'
    if mygame.b2b > 0:
        line3 = f'b2b {mygame.b2b}'
    if mygame.pc:
        line4 = 'all clear'
    line5 = f'attack {mygame.total_line_sent}'
    statBox.itemconfig(stat_line_1, text = line1)
    statBox.itemconfig(stat_line_2, text = line2)
    statBox.itemconfig(stat_line_3, text = line3)
    statBox.itemconfig(stat_line_4, text = line4)
    statBox.itemconfig(stat_line_5, text = line5)

def update_win_text():
    n = Setting.no_of_unreserved_piece
    if Setting.mode == 'combo':
        winning_requirement1.config(text =f'do {n-1} combo')
        winning_requirement2.config(text ='')
        if mygame.combo == n-1:
            winning_requirement1.config(fg ='green')
    elif Setting.mode == 'combopc':
        winning_requirement1.config(text =f'do {n-1} combo')
        winning_requirement2.config(text ='do a pc')
        if mygame.combo == n-1:
            winning_requirement1.config(fg ='green')
        if mygame.pc:
            winning_requirement2.config(fg ='green')
    elif Setting.mode == 'comboquad':
        winning_requirement1.config(text =f'do {n} combo')
        winning_requirement2.config(text ='do a quad')
        if mygame.combo == n:
            winning_requirement1.config(fg ='green')
        if mygame.line_clear == 4:
            winning_requirement2.config(fg ='green')
    elif Setting.mode == 'combotsd':
        winning_requirement1.config(text =f'do {n} combo')
        winning_requirement2.config(text ='do a tsd')
        if mygame.combo == n:
            winning_requirement1.config(fg ='green')
        if mygame.line_clear == 2 and mygame.b2b >= 0:
            print(mygame.line_clear,mygame.b2b)
            winning_requirement2.config(fg ='green')


def render():
    
    root.focus_set()
    if DEBUG:print('rendering board ', end = '') 
    #render board
    for j in range(20):
        for i in range(10):
            color = color_table[mygame.board[j][i]]
            gameBox.itemconfig(board_rects[j][i], fill = color)
    #render board hold
    if DEBUG:print('rendering hold ', end = '') 
    for j in range(4):
        for i in range(4):
            holdcanva.itemconfig(hold_rects[j][i], fill = 'black')
    if mygame.holdmino != '':
        color = color_table[mygame.holdmino]
        for col, row in mygame.to_shape(mygame.holdmino):
            holdcanva.itemconfig(hold_rects[row-mygame.y][col-mygame.x+1], fill = color)
    
    if DEBUG:print('rendering next piece ', end = '') 
    for j in range(20):
        for i in range(4):
            nextcanva.itemconfig(next_rects[j][i], fill = 'black')
    for piece_idx in range(1, min(len(mygame.bag), 6)):
        color = color_table[mygame.bag[piece_idx]]
        for col, row in mygame.to_shape(mygame.bag[piece_idx]):
            nextcanva.itemconfig(next_rects[row-mygame.y - 4*piece_idx][col-mygame.x+1], fill = color)
    
    def display_shadow(game):
        min_relative_height = 20 
        for col, row in game.to_shape():
            ground_height = 0
            for i in range(row):
                if game.board[i][col] != 'N':
                    ground_height = i+1
            min_relative_height = min(min_relative_height, row - ground_height)
        for col, row in game.to_shape():
            gameBox.itemconfig(board_rects[row-min_relative_height][col], fill = 'grey')
    display_shadow(mygame)

    if DEBUG:print('rendering current piece')

    color = color_table[mygame.tetramino]
    for i, j in mygame.to_shape():
        gameBox.itemconfig(board_rects[j][i], fill = color)
    
    #gameBox.itemconfig(board_rects[mygame.y][mygame.x], fill = 'snow')
    update_stat()
    update_win_text()

#--------------------------------------------------------------------------#
# 4. bind piece movement with keyboard
#--------------------------------------------------------------------------#

class Setting:
    delay = 0
    das = 133/1000
    arr = 0/1000
    left_on_press = False
    right_on_press = False
    mode = 'combo'
    no_of_unreserved_piece = 5


def press_left(first_call=False):
    if first_call and Setting.left_on_press:
        return
    if first_call:
        Setting.timer1 = time.perf_counter()
        Setting.delay = Setting.das
        mygame.move_left()
        render()
        Setting.right_on_press = False
        Setting.left_on_press = True
    elif not Setting.left_on_press:
        return
    current_time = time.perf_counter()

    if current_time - Setting.timer1 > Setting.delay:
        if Setting.arr == 0:
            mygame.move_leftmost()
        else:
            mygame.move_left()
        render()
        Setting.delay = Setting.arr
        Setting.timer1 = current_time
        


    root.after(1, press_left)

def release_left():
    Setting.left_on_press = False


def press_right(first_call=False):
    if first_call and Setting.right_on_press:
        return
    if first_call:
        Setting.timer2 = time.perf_counter()
        Setting.delay = Setting.das
        mygame.move_right()
        render()
        Setting.left_on_press = False
        Setting.right_on_press = True
    elif not Setting.right_on_press:
        return
    current_time = time.perf_counter()
    if current_time - Setting.timer2 > Setting.delay:
        if Setting.arr == 0:
            mygame.move_rightmost()
        else:
            mygame.move_right()
        render()
        Setting.delay = Setting.arr
        Setting.timer2 = current_time

    root.after(1, press_right)

def release_right():
    Setting.right_on_press = False

def restart():
    logprint('restart')
    mygame.__init__()
    render()

root.bind('<KeyPress-Left>', lambda event: (press_left(first_call=True)))
root.bind('<KeyRelease-Left>', lambda event: (release_left()))
root.bind('<KeyPress-Right>', lambda event: (press_right(first_call=True)))
root.bind('<KeyRelease-Right>', lambda event: (release_right()))

root.bind('<Down>', lambda event: (mygame.softdrop(), render()))
root.bind('<Up>', lambda event: (mygame.rotate_clockwise(), render()))
root.bind('<space>', lambda event: (mygame.harddrop(), render()))

root.bind('<z>', lambda event: (mygame.rotate_anticlockwise(), render()))
root.bind('<Shift-Z>', lambda event: (mygame.rotate_anticlockwise(), render()))
root.bind('<x>', lambda event: (mygame.rotate_clockwise(), render()))
root.bind('<Shift-X>', lambda event: (mygame.rotate_clockwise(), render()))
root.bind('<a>', lambda event: (mygame.rotate_180(), render()))
root.bind('<Shift-A>', lambda event: (mygame.rotate_180(), render()))
root.bind('<r>', lambda event: (retry()))
root.bind('<Shift_L>', lambda event: (mygame.hold(), render()))
root.bind('<c>', lambda event: (mygame.hold(), render()))

#--------------------------------------------------------------------------#
# 5. create buttons for downstack practice map generation
#--------------------------------------------------------------------------#
class record:
    added_line = []
    board = []
    piece_added = []
    finished_map = [['N' for i in range(10)] for j in range(20)]
    shuffled_queue = ['I','O','J','L','S','Z','T']

def load_board(game):
    logprint('loading board\n')
    with open('board.txt','r') as file:
        data = file.read().splitlines()
    for row_idx, row in enumerate(data):
        for col_idx, cell in enumerate(row):
            game.board[19-row_idx][col_idx] = cell

def add_line(game, row_idx):
    for i in range(10):
        for j in range(19,row_idx,-1):
            game.board[j][i] = game.board[j-1][i]
        
        game.board[row_idx][i] = 'G'
    record.added_line.append(row_idx)
    
def del_line(game, row_idx):
    for i in range(10):
        for j in range(row_idx,19):
            game.board[j][i] = game.board[j+1][i]
        
        game.board[19][i] = 'N'
def convert_garbage(game):
    for i in range(10):
        for j in range(0,19):
            if game.board[j][i] not in 'GN':
                game.board[j][i] = 'G'
def add_random_line(game):
    max_height = game.get_max_height()
    row_index = random.randint(0,max_height+1)
    record.added_line.clear()
    rng = random.random()
    logprint('\nrng = ', rng)
    if rng<0.1:
        add_line(game, row_index)
        add_line(game, row_index+1)
        add_line(game, row_index+2)
        logprint('add line ', row_index, row_index+1, row_index+2)
    elif rng<0.15 and row_index < max_height+1:
        add_line(game, row_index)
        add_line(game, row_index+2)
        logprint('add line ', row_index, row_index+2)
    elif rng<0.5:
        
        add_line(game, row_index)
        add_line(game, row_index+1)
        logprint('add line ', row_index, row_index+1)
    else:
        add_line(game, row_index)
        logprint('add line ', row_index)

def add_random_line_less_skim(game):
    non_garbages = [0 for _ in range(20)]
    for row_idx in range(20):
        for col_idx in range(10):
            if game.board[row_idx][col_idx] != 'G':
                non_garbages[row_idx] += 1
    
    garbage_height = 0
    for num in non_garbages:
        if num == 1:
            garbage_height+=1
        else:
            break
    row_index = garbage_height
    record.added_line.clear()
    rng = random.random()
    logprint('\nrng = ', rng)
    if rng<0.1:
        add_line(game, row_index)
        add_line(game, row_index+1)
        add_line(game, row_index+2)
        logprint('add line ', row_index, row_index+1, row_index+2)
    elif rng<0.5:
        
        add_line(game, row_index)
        add_line(game, row_index+1)
        logprint('add line ', row_index, row_index+1)
    else:
        add_line(game, row_index)
        logprint('add line ', row_index)


def try_drop(game):
    shape = game.to_shape()
    lowest_height = min(r for c,r in shape)
    for fall in range(1, lowest_height+1):
        
        all_g = True
        
        for col, row in shape:
            if game.board[row-fall][col] != 'G':
                all_g = False
        if all_g:
            for col, row in shape:
                game.board[row-fall][col] = 'N'
            game.y -= fall
            return True
            
    return False

def is_spinable(game, depth = 1):
    if depth > 2:
        return False
    piece_info = (game.x, game.y, game.orientation)

    if depth == 2:
        if game.move_left():
            if game.is_exposed() and not is_floatable(game):
                #add conditino
                game.x += 1
                return True
        if game.move_right():
            if game.is_exposed() and not is_floatable(game):
                #add conditino
                game.x -= 1
                return True
    if game.rotate_clockwise():
        if (game.is_exposed() and not is_floatable(game)) or is_spinable(game, depth+1):
            #add conditino
            game.rotate_anticlockwise()
            if piece_info == (game.x, game.y, game.orientation):

                return True

    (game.x, game.y, game.orientation) = piece_info
    if game.rotate_anticlockwise():
        #add conditino
        if (game.is_exposed() and not is_floatable(game)) or is_spinable(game, depth+1):
            game.rotate_clockwise()
            if piece_info == (game.x, game.y, game.orientation):
                return True


    (game.x, game.y, game.orientation) = piece_info
    if game.rotate_180():
        if game.is_exposed() and not is_floatable(game):
            #add conditino
            game.rotate_180()
            return True

    return False
def show_expose(game):
    print('is exposed', game.is_exposed())
    print('is spinable', is_spinable(game))

def get_unstability(game):
    grounded_position=set()
    ungrounded_position=set()
    for col_idx in range(10):
        is_grounded = True
        for row_idx in range(20):
            if game.board[row_idx][col_idx] == 'G':
                if is_grounded:
                    grounded_position.add((row_idx,col_idx))
                else:
                    ungrounded_position.add((row_idx,col_idx))
            else:
                is_grounded = False
    
    #test if ungrounded are next to grounded
    unstability = 0
    for row_idx, col_idx in ungrounded_position:
        right_grounded = col_idx < 9 and (row_idx, col_idx+1) in grounded_position
        left_grounded = col_idx > 0 and (row_idx, col_idx-1) in grounded_position
        if not (right_grounded or left_grounded):
            unstability += 1    
    return unstability

def is_cheese_hole(game):
    height = []
    for col_idx in range(10):
        h=0
        for row_idx in range(20):
            if game.board[row_idx][col_idx] == 'G':
                h=row_idx
        height.append(h)
    holes = [0 for _ in range(20)]
    non_garbages = [0 for _ in range(20)]
    for row_idx in range(20):
        for col_idx in range(10):
            if game.board[row_idx][col_idx] != 'G':
                non_garbages[row_idx] += 1
            if game.board[row_idx][col_idx] != 'G' and row_idx < height[col_idx]:
                holes[row_idx] += 1

    
    no_of_non_cheese_holes = 0
    is_cheese_level = True
    for non_garbage, hole in zip(non_garbages,holes):
        if non_garbage != 1:
            is_cheese_level = False
        if not is_cheese_level:
            no_of_non_cheese_holes += hole
    return no_of_non_cheese_holes <= 1
    
def is_floatable(game):
    for col, row in game.to_shape():
        if row == 0 or game.board[row-1][col] == 'G':
            return False
    return True

def try_a_piece(game):
    # find position piece that include (x,y)
    # find neighbour piece
    previous_board = [[cell for cell in row] for row in game.board]
    if try_drop(game):
        floatable = is_floatable(game)
        reachable = game.is_exposed() or is_spinable(game)
        clearable = set(record.added_line).issubset({row for col, row in game.to_shape()})#any(row in record.added_line for col, row in game.to_shape())
        unstability = get_unstability(game)

        
        if reachable and clearable and not floatable and unstability == 0 and is_cheese_hole(game):
            if DEBUG: print('can place here')
            game.board = [[cell for cell in row] for row in previous_board]
            return True
        else:
            if DEBUG: print('cannot place here')
            game.board = [[cell for cell in row] for row in previous_board]
            #logprint(f'\timpossible {game.tetramino} piece placement when x,y,ori =',  game.x, game.y, game.orientation)

    return False



def try_all_pieces(game):
    random.shuffle(possible_piece_info_table)
    for piece, ori_idx, col_idx in possible_piece_info_table:
        game.tetramino = piece
        game.x = col_idx
        game.y = 18
        game.orientation = ori_idx
        
        if try_a_piece(game):
            record.piece_added.append(piece)
            logprint(f'--- generated {piece} piece in the map', 'x,y,ori = ', game.x, game.y, game.orientation)
            logprint('\n'.join(str(row) for row in reversed(game.board)))
            return True
    
    logprint('*** fail to generate piece in the map')
    logprint('\n'.join(str(row) for row in reversed(game.board)))
    return False

def try_a_move(game):
    if skim_or_not.get() == 1:
        add_random_line(game)
    else:
        add_random_line_less_skim(game)
    if try_all_pieces(game):
        
        game.lock()
        record.board.append([[cell for cell in row] for row in game.board])
        return True
    else:

        return False

def print_answer(game):
    with open('ans.txt','w') as file:
        for board in record.board:
            for r in range(20):

                file.write(''.join(board[19-r]) + '\n')
            file.write('----------\n')
    return True
def get_shuffled_holdable_queue(queue):
    result = []
    size = len(queue)
    if 2<= size <=7:
        for pointer in random.choice(reverse_hold_table[size]):
            result.append(queue[pointer])
    return result
def play(game, retry = True):
    restart()
    if retry:
        logprint('retry')
    winning_requirement1.config(fg ='black')
    winning_requirement2.config(fg ='black')

    
    if not retry:
        queue = list(reversed(record.piece_added))
        if Setting.mode == 'comboquad':
            queue.append('I')
        elif Setting.mode == 'combotsd':
            queue.append('T')
        record.shuffled_queue = get_shuffled_holdable_queue(queue)
    
    game.bag = ''.join(record.shuffled_queue) + 'G'*14
    game.update()
    game.holdmino = ''
    if len(record.board)>0:
        game.board = [['G' if cell == 'G' else 'N' for cell in row] for row in record.board[-1]]

def toggle_mode(game):
    game.drawmode = not game.drawmode

if I_AM_DEVELOPER:
    root.bind('<Key-0>', lambda event: (load_board(mygame), render()))
    root.bind('<Key-1>', lambda event: (add_line(mygame, int(input('enter row_idx to add'))), render()))
    root.bind('<Key-2>', lambda event: (toggle_mode(mygame)))
    root.bind('<Key-3>', lambda event: (convert_garbage(mygame), render()))
    root.bind('<Key-4>', lambda event: (add_random_line(mygame), render()))
    root.bind('<Key-6>', lambda event: (try_drop(mygame), render()))
    root.bind('<Key-7>', lambda event: (show_expose(mygame)))
    root.bind('<Key-8>', lambda event: (try_a_piece(mygame), render()))
    root.bind('<Key-9>', lambda event: (try_all_pieces(mygame), render()))

    root.bind('<Key-5>', lambda event: (try_a_move(mygame), render()))
    root.bind('<p>', lambda event: (print_answer(mygame), render()))
    root.bind('<s>', lambda event: (get_unstability(mygame), render()))
    root.bind('<h>', lambda event: (is_cheese_hole(mygame), render()))
    root.bind('<g>', lambda event: (generate_final_map(), render()))
    root.bind('<Return>', lambda event: (play(mygame), render()))

#generate map

def generate_a_ds_map(move):

    for trial in range(5):
        logprint('move=',move,'trial=',trial)
        if move == 1:
            success_generate = try_a_move(mygame) and all(record.piece_added.count(piece) <=2 for piece in 'OTJLZS') and record.piece_added.count('I') <= 1
        else:
            success_generate = try_a_move(mygame) and all(record.piece_added.count(piece) <=2 for piece in 'OTJLZS') and record.piece_added.count('I') <= 1 and generate_a_ds_map(move - 1)
        if success_generate:
            return True
        else:
            logprint('regenerate map')
            record.board = record.board[:Setting.no_of_unreserved_piece-move]
            record.piece_added = record.piece_added[:Setting.no_of_unreserved_piece-move]
            if len(record.board) > 0:
                mygame.board = [[cell for cell in row] for row in record.board[-1]]
            else:
                mygame.board = [[cell for cell in row] for row in record.finished_map]
    logprint('reach try limit, move back')
    return False


def generate_final_map():
    
    restart()

    if Setting.mode == 'combopc':
        return True
    elif Setting.mode == 'combo':
        height = [random.randint(0,2) for _ in range(10)]
        gap_col = random.randint(0,9)
        height[gap_col] = 0
        for j in range(20):
            for i in range(10):
                if j < height[i]:
                    mygame.board[j][i] = 'G'

    elif Setting.mode == 'comboquad':
        height = [random.randint(4,6) for _ in range(10)]
        gap_col = random.randint(0,9)
        height[gap_col] = 0
        for j in range(20):
            for i in range(10):
                if j < height[i]:
                    mygame.board[j][i] = 'G'
    elif Setting.mode == 'combotsd':
        height = [random.randint(2,4) for _ in range(10)]
        tsd_col = random.randint(1,8)
        height[tsd_col] = 0
        height[tsd_col + 1] = 1
        height[tsd_col - 1] = 1
        for j in range(20):
            for i in range(10):
                if j < height[i]:
                    mygame.board[j][i] = 'G'
        if tsd_col == 1:
            is_left = False
        elif tsd_col == 8:
            is_left = True
        else:
            is_left = random.randint(0,1)
        
        if is_left:
            mygame.board[2][tsd_col-1] = 'G'
            mygame.board[0][tsd_col-2] = 'G'
            mygame.board[1][tsd_col-2] = 'G'
            mygame.board[2][tsd_col-2] = 'G'
        else:
            mygame.board[2][tsd_col+1] = 'G'
            mygame.board[0][tsd_col+2] = 'G'
            mygame.board[1][tsd_col+2] = 'G'
            mygame.board[2][tsd_col+2] = 'G'            
def play_a_map(mode, seed = None):
    if seed == None:
        seed = random.randrange(9223372036854775807)
    random.seed(seed)
    logprint('\ngenerating a map with seed = ',seed)
    restart()
    if get_no_of_piece() is False:
        no_of_piece_str.set('5')
    Setting.no_of_unreserved_piece = get_no_of_piece() - (mode in ['comboquad','combotsd'])
    Setting.mode = mode
    logprint('mode=', mode, '; no of unreserved piece=', Setting.no_of_unreserved_piece)
    generate_final_map()
    record.finished_map = [[cell for cell in row] for row in mygame.board]
    mygame.drawmode = True
    record.piece_added = []
    record.board = []
    for i in range(10):
        if generate_a_ds_map(Setting.no_of_unreserved_piece) is True:
            break
        else:
            logprint('refresh and generate for times', i)

    print_answer(mygame)
    play(mygame, retry = False)
    
    mygame.drawmode = False
    render()

def play_a_combo_map(seed = None):
    play_a_map(mode = 'combo', seed = seed)

def play_a_combopc_map(seed = None):
    play_a_map(mode = 'combopc', seed = seed)

def play_a_comboquad_map(seed = None):
    play_a_map(mode = 'comboquad', seed = seed)

def play_a_combotsd_map(seed = None):
    play_a_map(mode = 'combotsd', seed = seed)
#------------------------------------------#
# 6.buttons for map control     
#------------------------------------------#
ds_button = Button(root, text="combo->pc practice", width=20, height=1, font=('Arial', 20), command = play_a_combopc_map)
ds_button.place(x=600, y=50)

ds_button = Button(root, text="combo practice", width=20, height=1, font=('Arial', 20), command = play_a_combo_map)
ds_button.place(x=600, y=125)
ds_button = Button(root, text="combo->quad practice", width=20, height=1, font=('Arial', 20), command = play_a_comboquad_map)
ds_button.place(x=600, y=200)
ds_button = Button(root, text="combo->tsd practice", width=20, height=1, font=('Arial', 20), command = play_a_combotsd_map)
ds_button.place(x=600, y=275)
def retry():
    play(mygame)
    render()
retry_button = Button(root, text="retry", width=10, height=1, font=('Arial', 20), command = retry)
retry_button.place(x=600, y=350)
def show_ans():
    mygame.board = [[cell for cell in row] for row in record.board[-1]]
    render()
    root.after(1000, retry)
ans_button = Button(root, text="show answer", width=10, height=1, font=('Arial', 20), command = show_ans)
ans_button.place(x=600, y=425)

#------------------------------------------#
# 7.display winning requirements        
#------------------------------------------#
winning_requirement_header = LabelFrame(root, text = "winning requirement:", height = 100, width = 400, font=('Arial', 20) )
winning_requirement_header.place(x=500,y=500)
winning_requirement1 = Label(winning_requirement_header, text = "do 5 combo", font=('Arial', 15), fg='black')  
winning_requirement1.pack()
winning_requirement2 = Label(winning_requirement_header, text = "do a quad", font=('Arial', 15), fg='black')  
winning_requirement2.pack()

#------------------------------------------#
# 8.create spinbox for no of piece, mode
#------------------------------------------#>lk
setting_frame = LabelFrame(root, text = "setting:", height = 100, width = 400, font=('Arial', 20) )
setting_frame.place(x=800,y=500)
no_of_piece_label = Label(setting_frame, text = 'enter number of piece (2 to 7)', font=('Arial', 15), fg='black')
no_of_piece_label.pack(anchor = 'w')



no_of_piece_str = StringVar()
no_of_piece_str.set('5')
no_of_piece_box = Spinbox(setting_frame, from_ = 2, to = 7, textvariable = no_of_piece_str, state = 'disable')
no_of_piece_box.pack(anchor = 'w', padx=20)

skim_label = Label(setting_frame, text = 'do you want more skims in solutions', font=('Arial', 15), fg='black')
skim_label.pack(anchor = 'w')
skim_or_not = IntVar()
skim_box = Checkbutton(setting_frame,text = 'more', variable = skim_or_not, onvalue=1, offvalue=0)
skim_box.pack(anchor = 'w',padx=20)

setting_frame.bind('<Enter>',lambda event: no_of_piece_box.config(state = 'normal'))
setting_frame.bind('<Leave>',lambda event: no_of_piece_box.config(state = 'disable'))
def get_no_of_piece():
    text = no_of_piece_box.get()
    if text in ['2','3','4','5','6','7']:
        return int(text)
    else:
        return False 
#------------------------------------------#
# 9.how to play
#------------------------------------------#
how_to_play_frame = LabelFrame(root, text = "how to play ", height = 200, width = 200, font=('Arial', 20) )
how_to_play_frame.place(x=950,y=50)
how_to_play_text = '''move left: ←
move right: →
rotate clockwise: x / ↑
rotate anticlockwise: z
rotate 180 degree: a
hold: left shift / c
softdrop: ↓
harddrop: space
retry: r
'''
how_to_play_label = Label(how_to_play_frame, text = how_to_play_text,  font=('Arial', 15), fg='black',anchor = 'w')
how_to_play_label.pack(anchor = 'w')

#------------------------------------------#
# 10.handling
#------------------------------------------#
handling_frame = LabelFrame(root, text = "handling:", height = 150, width = 300, font=('Arial', 20) )
handling_frame.place(x=800,y=350)

arr_frame = Canvas(handling_frame, height = 50, width = 300)
arr_frame.pack()
das_frame = Canvas(handling_frame, height = 50, width = 300)
das_frame.pack()

arr_label = Label(arr_frame, text = 'ARR (0 to 100)',  font=('Arial', 10), fg='black')
arr_label.pack(anchor = 'w', side = 'left', ipadx=10)
arr = StringVar()
arr.set('0')
arr_box = Spinbox(arr_frame, from_ = 0, to = 100, textvariable = arr, state = 'disable')
arr_box.pack()

das_label = Label(das_frame, text = 'DAS (1 to 200)',  font=('Arial', 10), fg='black')
das_label.pack(anchor = 'w', side = 'left', ipadx=10)
das = StringVar()
das.set('133')
das_box = Spinbox(das_frame, from_ = 1, to = 200, textvariable = das, state = 'disable')
das_box.pack()

def save_handling():
    if not arr.get().isnumeric():
        arr.set('0')
    elif not (0<= int(arr.get()) <= 100):
        arr.set('0')
    Setting.arr = int(arr.get())/1000

    if not das.get().isnumeric():
        das.set('0')
    elif not (1<= int(das.get()) <= 200):
        das.set('133')
    Setting.arr = int(arr.get())/1000

handling_frame.bind('<Enter>', lambda event: (arr_box.config(state = 'normal'), das_box.config(state = 'normal')))
handling_frame.bind('<Leave>',lambda event: (save_handling(), arr_box.config(state = 'disable'), das_box.config(state = 'disable')))




render()
root.mainloop()


