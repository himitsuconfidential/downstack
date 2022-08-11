import random
import time

color_table = {'Z': 'red',
               'L': 'orange',
               'O': 'yellow',
               'S': 'lime',
               'I': 'cyan',
               'J': 'blue',
               'T': 'magenta',
               'G': 'silver',
               'N': 'black',
               }

#shape code:48~63
#0123
#4567
#89:;
#<=>?
shape_table = {'Z': ['0156', '1458', '459:', '2569'],
               'L': ['2456', '0159', '4568', '159:'],
               'O': ['0145', '0145', '0145', '0145'],
               'S': ['1245', '0459', '5689', '156:'],
               'I': ['4567', '159=', '89:;', '26:>'],
               'J': ['0456', '1589', '456:', '1259'],
               'T': ['1456', '1459', '4569', '1569'],
               'G': ['5'],
               }
possible_x_table={
    'O': [(1,9),(1,9),(1,9),(1,9)],
    'I': [(1,7),(0,9),(1,7),(1,8)],
    'Z': [(1,8),(1,9),(1,8),(0,8)],
    'S': [(1,8),(1,9),(1,8),(0,8)],
    'T': [(1,8),(1,9),(1,8),(0,8)],
    'J': [(1,8),(1,9),(1,8),(0,8)],
    'L': [(1,8),(1,9),(1,8),(0,8)],
    }
possible_piece_info_table = [(p,idx,c) for p in possible_x_table for idx,cr in enumerate(possible_x_table[p]) for c in range(cr[0], cr[1]+1)]
pure_line_clear_table = [0, 0, 1, 2, 4]
tspin_line_clear_table = [0, 2, 4, 6]
tspin_mini_line_clear_table = [0, 0, 0, 0, 0]
line_clear_table = {True: tspin_line_clear_table, False: pure_line_clear_table, 'tspinmini': tspin_mini_line_clear_table}
combo_table = [0,0,1,1,1,2,2,3,3,4,4,4]
jltsz_clockwise_kick_table = [[(-1,0), (-1,1), (0,-2), (-1,-2)],
                              [(1,0), (1,-1), (0,2), (1,2)],
                              [(1,0), (1,1), (0,-2), (1,-2)],
                              [(-1,0), (-1,-1), (0,2), (-1,2)]]
jltsz_anticlockwise_kick_table = [[(1,0), (1,1), (0,-2), (1,-2)],
                              [(-1,0), (-1,-1), (0,2), (-1,2)],
                              [(-1,0), (-1,1), (0,-2), (-1,-2)],
                              [(1,0), (1,-1), (0,2), (1,2)]]
#jltsz_180_kick_table = [[(1,0), (1,1), (0,-2), (1,-2)],
#                              [(-1,0), (-1,-1), (0,2), (-1,2)],
#                              [(-1,0), (-1,1), (0,-2), (-1,-2)],
#                              [(1,0), (1,-1), (0,2), (1,2)]]#????
i_clockwise_kick_table = [[(-2,0), (1,0), (-2,-1), (1,2)],
                          [(-1,0), (2,0), (-1,2), (2,-1)],
                          [(2,0), (-1,0), (2,1), (-1,-2)],
                          [(1,0), (-2,0), (1,-2), (-2,1)]]
i_anticlockwise_kick_table = [[(-1,0), (2,0), (-1,2), (2,-1)],
                              [(-2,0), (1,0), (-2,-1), (1,2)],
                              [(1,0), (-2,0), (1,-2), (-2,1)],
                              [(2,0), (-1,0), (2,1), (-1,-2)]]
tspin_test2_table = [[(-1,1), (1,1)],
                    [(-1,1), (-1, -1)],
                    [(-1,-1), (1, -1)],
                    [(1,1), (1, -1)]]
tspin_test3_table = [(-1,-1), (-1, 1), (1,1), (1, -1)]

reverse_hold7_table = [
[0, 1, 2, 3, 4, 5, 6],
[0, 1, 2, 3, 4, 6, 5],
[0, 1, 2, 3, 5, 4, 6],
[0, 1, 2, 3, 6, 4, 5],
[0, 1, 2, 4, 3, 5, 6],
[0, 1, 2, 4, 3, 6, 5],
[0, 1, 2, 5, 3, 4, 6],
[0, 1, 2, 6, 3, 4, 5],
[0, 1, 3, 2, 4, 5, 6],
[0, 1, 3, 2, 4, 6, 5],
[0, 1, 3, 2, 5, 4, 6],
[0, 1, 3, 2, 6, 4, 5],
[0, 1, 4, 2, 3, 5, 6],
[0, 1, 4, 2, 3, 6, 5],
[0, 1, 5, 2, 3, 4, 6],
[0, 1, 6, 2, 3, 4, 5],
[0, 2, 1, 3, 4, 5, 6],
[0, 2, 1, 3, 4, 6, 5],
[0, 2, 1, 3, 5, 4, 6],
[0, 2, 1, 3, 6, 4, 5],
[0, 2, 1, 4, 3, 5, 6],
[0, 2, 1, 4, 3, 6, 5],
[0, 2, 1, 5, 3, 4, 6],
[0, 2, 1, 6, 3, 4, 5],
[0, 3, 1, 2, 4, 5, 6],
[0, 3, 1, 2, 4, 6, 5],
[0, 3, 1, 2, 5, 4, 6],
[0, 3, 1, 2, 6, 4, 5],
[0, 4, 1, 2, 3, 5, 6],
[0, 4, 1, 2, 3, 6, 5],
[0, 5, 1, 2, 3, 4, 6],
[0, 6, 1, 2, 3, 4, 5],
[1, 0, 2, 3, 4, 5, 6],
[1, 0, 2, 3, 4, 6, 5],
[1, 0, 2, 3, 5, 4, 6],
[1, 0, 2, 3, 6, 4, 5],
[1, 0, 2, 4, 3, 5, 6],
[1, 0, 2, 4, 3, 6, 5],
[1, 0, 2, 5, 3, 4, 6],
[1, 0, 2, 6, 3, 4, 5],
[1, 0, 3, 2, 4, 5, 6],
[1, 0, 3, 2, 4, 6, 5],
[1, 0, 3, 2, 5, 4, 6],
[1, 0, 3, 2, 6, 4, 5],
[1, 0, 4, 2, 3, 5, 6],
[1, 0, 4, 2, 3, 6, 5],
[1, 0, 5, 2, 3, 4, 6],
[1, 0, 6, 2, 3, 4, 5],
[2, 0, 1, 3, 4, 5, 6],
[2, 0, 1, 3, 4, 6, 5],
[2, 0, 1, 3, 5, 4, 6],
[2, 0, 1, 3, 6, 4, 5],
[2, 0, 1, 4, 3, 5, 6],
[2, 0, 1, 4, 3, 6, 5],
[2, 0, 1, 5, 3, 4, 6],
[2, 0, 1, 6, 3, 4, 5],
[3, 0, 1, 2, 4, 5, 6],
[3, 0, 1, 2, 4, 6, 5],
[3, 0, 1, 2, 5, 4, 6],
[3, 0, 1, 2, 6, 4, 5],
[4, 0, 1, 2, 3, 5, 6],
[4, 0, 1, 2, 3, 6, 5],
[5, 0, 1, 2, 3, 4, 6],
[6, 0, 1, 2, 3, 4, 5],
]

reverse_hold6_table=[
[0, 1, 2, 3, 4, 5],
[0, 1, 2, 3, 5, 4],
[0, 1, 2, 4, 3, 5],
[0, 1, 2, 5, 3, 4],
[0, 1, 3, 2, 4, 5],
[0, 1, 3, 2, 5, 4],
[0, 1, 4, 2, 3, 5],
[0, 1, 5, 2, 3, 4],
[0, 2, 1, 3, 4, 5],
[0, 2, 1, 3, 5, 4],
[0, 2, 1, 4, 3, 5],
[0, 2, 1, 5, 3, 4],
[0, 3, 1, 2, 4, 5],
[0, 3, 1, 2, 5, 4],
[0, 4, 1, 2, 3, 5],
[0, 5, 1, 2, 3, 4],
[1, 0, 2, 3, 4, 5],
[1, 0, 2, 3, 5, 4],
[1, 0, 2, 4, 3, 5],
[1, 0, 2, 5, 3, 4],
[1, 0, 3, 2, 4, 5],
[1, 0, 3, 2, 5, 4],
[1, 0, 4, 2, 3, 5],
[1, 0, 5, 2, 3, 4],
[2, 0, 1, 3, 4, 5],
[2, 0, 1, 3, 5, 4],
[2, 0, 1, 4, 3, 5],
[2, 0, 1, 5, 3, 4],
[3, 0, 1, 2, 4, 5],
[3, 0, 1, 2, 5, 4],
[4, 0, 1, 2, 3, 5],
[5, 0, 1, 2, 3, 4],]

reverse_hold5_table = [
[0, 1, 2, 3, 4],
[0, 1, 2, 4, 3],
[0, 1, 3, 2, 4],
[0, 1, 4, 2, 3],
[0, 2, 1, 3, 4],
[0, 2, 1, 4, 3],
[0, 3, 1, 2, 4],
[0, 4, 1, 2, 3],
[1, 0, 2, 3, 4],
[1, 0, 2, 4, 3],
[1, 0, 3, 2, 4],
[1, 0, 4, 2, 3],
[2, 0, 1, 3, 4],
[2, 0, 1, 4, 3],
[3, 0, 1, 2, 4],
[4, 0, 1, 2, 3],]

reverse_hold4_table = [
[0, 1, 2, 3],
[0, 1, 3, 2],
[0, 2, 1, 3],
[0, 3, 1, 2],
[1, 0, 2, 3],
[1, 0, 3, 2],
[2, 0, 1, 3],
[3, 0, 1, 2],]


reverse_hold3_table = [
[0, 1, 2],
[0, 2, 1],
[1, 0, 2],
[2, 0, 1],]

reverse_hold2_table = [
[0, 1],
[1, 0],]

reverse_hold_table = {
2: reverse_hold2_table,
3: reverse_hold3_table,
4: reverse_hold4_table,
5: reverse_hold5_table,
6: reverse_hold6_table,
7: reverse_hold7_table,
}
class Status_copy():
    def __init__(self, game):
        self.combo = game.combo
        self.b2b = game.b2b
        self.line_clear = game.line_clear
        self.total_line_clear = game.total_line_clear
        self.line_sent = game.line_sent
        self.total_line_sent = game.total_line_sent
        self.total_piece = game.total_piece
        self.start_time = game.start_time


class Game():
    def __init__(self, seed=None):
        self.previous_keys = []
        self.mode = 'play'
        self.seed = random.random() if seed == None else seed
        random.seed(self.seed)


        self.std_bag = list('IJLSZOT')
        self.holdmino = ''
        random.shuffle(self.std_bag)
        self.bag = ''.join(self.std_bag)
        self.frame_num = 0
        
        self.tetramino = self.bag[0]
        self.x = 4
        self.y = 18
        self.orientation = 0
        self.lastmove = ''
        self.board = [['N' for i in range(10)] for j in range(20)]


        self.total_piece = 0
        self.drawmode = False

        self.combo = -1
        self.b2b = -1
        self.pc = False
        self.line_clear = 0
        self.total_line_clear = 0
        self.line_sent = 0
        self.total_line_sent = 0
    def to_shape(self, tetramino = None):
        if tetramino == None:
            tetramino = self.tetramino
            orientation = self.orientation
        else:
            orientation = 0
        
        shape_code = shape_table[tetramino][orientation]
        res = []
        for c in shape_code:
            coor_id = ord(c) - ord('5') 
            x = (coor_id+5) % 4 - 1 + self.x 
            y = -((coor_id+5) // 4 - 1) + self.y
            res.append((x, y))
        return res
    def is_collide(self) -> bool:
        for col, row in self.to_shape():
            if self.drawmode:
                if col <0 or col >9 or row<0 or row>19 or self.board[row][col] == 'G':
                    return True
            elif col <0 or col >9 or row<0 or row>19 or self.board[row][col] != 'N':
                return True
        return False
    def move_left(self):
        
        previous_x = self.x
        self.x -= 1
        if not self.is_collide(): 
            self.lastmove = 'LEFT'
            return True
            
        self.x = previous_x
        return False
    def move_right(self):
        previous_x = self.x
        self.x += 1
        if not self.is_collide():
            self.lastmove = 'RIGHT'
            return True
        self.x = previous_x

        return False
    def move_leftmost(self):
        for _ in range(10):
            if not self.move_left():
                return
    def move_rightmost(self):
        for _ in range(10):
            if not self.move_right():
                return
    def rotate_anticlockwise(self):
        previous_orientation = self.orientation
        previous_x = self.x
        previous_y = self.y
        self.orientation = (self.orientation+1)%4
        if not self.is_collide():
            self.lastmove = 'z'
            return True
        kick_table = jltsz_anticlockwise_kick_table if self.tetramino in 'JLTSZ' else i_anticlockwise_kick_table
        for idx, kick in enumerate(kick_table[previous_orientation]):
            x, y = kick
            self.x += x
            self.y += y
            if not self.is_collide():
                self.lastmove = 'zkick' + str(idx+1)
                return True
            self.x = previous_x
            self.y = previous_y
        self.orientation = previous_orientation

        return False
            
    def rotate_clockwise(self):
        previous_orientation = self.orientation
        previous_x = self.x
        previous_y = self.y
        self.orientation = (self.orientation-1)%4
        if not self.is_collide():
            self.lastmove = 'x'
            return True
        kick_table = jltsz_anticlockwise_kick_table if self.tetramino in 'JLTSZ' else i_anticlockwise_kick_table
        for idx, kick in enumerate(kick_table[self.orientation]):
            x, y = kick
            self.x -= x
            self.y -= y
            if not self.is_collide():
                self.lastmove = 'xkick' + str(idx+1)
                return True
            self.x = previous_x
            self.y = previous_y
        self.orientation = previous_orientation

        return False
    def rotate_180(self):
        previous_orientation = self.orientation
        self.orientation = (self.orientation-2)%4
        
        if not self.is_collide():
            self.lastmove = 'a'
            return True

        self.orientation = previous_orientation
        return False
        
    def drop(self, factor = 20):
        for _ in range(factor):
            previous_y = self.y
            self.y -= 1
            if self.is_collide():
                self.y = previous_y
                return False
            self.lastmove = 'drop'
        return True
    def lock(self):
        for col, row in self.to_shape():
            self.board[row][col] = self.tetramino
    def clear_line(self) -> int: 
        lines = []
        for row in range(19, -1, -1):
            if all(self.board[row][col] != 'N' for col in range(10)):
                lines.append(row)

        for line in lines:
            self.board.pop(line)
            self.board.append(['N' for _ in range(10)])
        return len(lines)
    def hold(self):
        temp = self.holdmino
        self.holdmino = self.bag[0]
        self.bag = temp + self.bag[1:]
        self.update()
    def push(self, generate_flag = True):
        self.bag = self.bag[1:]
        if generate_flag:
            self.generate()
        self.update()
    def generate(self):
        if len(self.bag)<7:
            random.shuffle(self.std_bag)
            self.bag += ''.join(self.std_bag)

    def update(self):
        self.tetramino = self.bag[0]
        self.x = 4
        self.y = 18
        self.orientation = 0
        self.lastmove = ''
    def softdrop(self):
        self.drop()
        
    def harddrop(self):
        self.drop()
        tspin_flag = self.is_tspin()
        
        self.lock()
        self.push()
        line_clear = self.clear_line()
        self.line_clear = line_clear
        self.total_piece += 1
        if line_clear > 0:
            
            if line_clear == 4 or tspin_flag:
                self.b2b += 1
            else:
                self.b2b = -1
            self.combo += 1
            combo = self.combo
            
            self.total_line_clear += line_clear
            
            attack = line_clear_table[tspin_flag][line_clear] 
            if attack >0:
                attack += (self.b2b >0)

            if combo >=12:
                attack += 5
            else:
                attack += combo_table[combo]

            if self.is_pc():
                attack += 10
                self.pc = True
            self.line_sent = attack
            self.total_line_sent += self.line_sent
        else:
            self.combo = -1
            self.line_sent = 0
            self.pc = False
        
        if self.is_collide():
            self.__init__()

        
    def is_tspin(self):
        test1 = self.tetramino == 'T'
        test2 = 0
        for x, y in tspin_test2_table[self.orientation]:
            testx = self.x+x
            testy = self.y+y
            if testx in [-1, 10] or testy in [-1, 20] or self.board[testy][testx] != 'N':
                test2 += 1

        test3 = 0
        for x, y in tspin_test3_table:
            testx = self.x+x
            testy = self.y+y
            if testx in [-1, 10] or testy in [-1, 20] or self.board[testy][testx] != 'N':
                test3 += 1
        if test1 and test2 == 2 and test3 >= 3:
            return True
        elif test1 and test2 == 1 and test3 >= 3:
            if self.lastmove[1:] == 'kick4' and self.orientation in [1,3]:
                return True
            elif self.lastmove[0] in 'axz':
                return 'tspinmini'
        return False
    

    def is_pc(self) -> bool:
        for row in range(20):
            for col in range(10):
                if self.board[row][col] != 'N':
                    return False
        return True

    def get_max_height(self):
        heights = []
        for col in range(10):
            height = -1
            for row in range(20):
                if self.board[row][col] != 'N':
                    height = row
            heights.append(height)
        return max(heights)

    def is_exposed(self):
        '''return whether garbage not on top'''
        for col, row in self.to_shape():
            for j in range(row+1, 20):
                if self.board[j][col] == 'G':
                    return False
        return True


