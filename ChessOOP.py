import copy


class Figure(object):
    def __init__(self, pos: str, color: str, kind=None, possible_moves=[], possible_takes=[], flagok=0) -> None:
        self.pos = pos
        self.color = color
        self.kind = kind
        self.possible_moves = possible_moves
        self.possible_takes = possible_takes
        self.flagok = flagok

    def calculate_possible_moves(self, field, all_moves_in_game, all_possible_takes, flagok) -> None:
        pass

    def make_move(self, new_pos: str, field: list, color_now: str, all_moves_in_game: list, all_possible_takes,
                  flagok) -> None or bool:
        self.calculate_possible_moves(field, all_moves_in_game, all_possible_takes, flagok)
        if new_pos in self.possible_moves and self.color == color_now:
            if field[new_pos[0]][new_pos[1]] == ' ':
                all_moves_in_game.append(self.pos + '-' + new_pos)
            else:
                all_moves_in_game.append(self.pos + ':' + new_pos)
            if self.kind in 'Pp':
                if self.pos[0] == new_pos[0] or field[new_pos[0]][new_pos[1]] != ' ':
                    field[self.pos[0]][self.pos[1]] = ' '
                    field[new_pos[0]][new_pos[1]] = self
                    self.pos = new_pos[0] + new_pos[1]
                else:
                    temp = 1 if self.color == 'White' else -1
                    field[self.pos[0]][self.pos[1]] = ' '
                    field[new_pos[0]][new_pos[1]] = self
                    self.pos = new_pos[0] + new_pos[1]
                    field[new_pos[0]][chr(ord(new_pos[1]) - temp)] = ' '
                    all_moves_in_game.insert(-1, '*')
            if self.kind in 'Kk':
                if abs(ord(self.pos[0]) - ord(new_pos[0])) == 2:
                    if new_pos[0] == 'C':
                        field[self.pos[0]][self.pos[1]] = ' '
                        field[new_pos[0]][new_pos[1]] = self
                        self.pos = new_pos[0] + new_pos[1]
                        field['D'][self.pos[1]] = field['A'][self.pos[1]]
                        field['A'][self.pos[1]] = ' '
                        field['D'][self.pos[1]].pos = 'D' + self.pos[1]
                        all_moves_in_game.insert(-1, '{')
                    else:
                        field[self.pos[0]][self.pos[1]] = ' '
                        field[new_pos[0]][new_pos[1]] = self
                        self.pos = new_pos[0] + new_pos[1]
                        field['F'][self.pos[1]] = field['H'][self.pos[1]]
                        field['H'][self.pos[1]] = ' '
                        field['F'][self.pos[1]].pos = 'F' + self.pos[1]
                        all_moves_in_game.insert(-1, '}')
                else:
                    field[self.pos[0]][self.pos[1]] = ' '
                    field[new_pos[0]][new_pos[1]] = self
                    self.pos = new_pos[0] + new_pos[1]
            else:
                field[self.pos[0]][self.pos[1]] = ' '
                field[new_pos[0]][new_pos[1]] = self
                self.pos = new_pos[0] + new_pos[1]

            return False
        else:
            return True

    def calculated(self, field, moves, all_moves_in_game, all_possible_takes, flagok):
        for dx, dy in moves:
            for i in range(1, 8):
                if 65 <= (ord(self.pos[0]) + dx * i) <= 72 and 1 <= (int(self.pos[1]) + dy * i) <= 8:
                    if field[chr(ord(self.pos[0]) + dx * i)][str(int(self.pos[1]) + dy * i)] == ' ':
                        self.possible_moves.append(chr(ord(self.pos[0]) + dx * i) + str(int(self.pos[1]) + dy * i))
                        self.possible_takes.append(chr(ord(self.pos[0]) + dx * i) + str(int(self.pos[1]) + dy * i))
                    elif field[chr(ord(self.pos[0]) + dx * i)][str(int(self.pos[1]) + dy * i)].color != \
                            field[self.pos[0]][self.pos[1]].color:
                        self.possible_moves.append(chr(ord(self.pos[0]) + dx * i) + str(int(self.pos[1]) + dy * i))
                        self.possible_takes.append(chr(ord(self.pos[0]) + dx * i) + str(int(self.pos[1]) + dy * i))
                        break
                    else:
                        break

    def visual_moves(self, field, all_moves_in_game, all_possible_takes, flagok):
        self.calculate_possible_moves(field, all_moves_in_game, all_possible_takes, flagok)
        v_field = copy.deepcopy(field)
        for i in self.possible_moves:
            if v_field[i[0]][i[1]] == ' ':
                v_field[i[0]][i[1]] = '◦'
            else:
                v_field[i[0]][i[1]] = '🕱'
        print('  A B C D E F G H')
        print(' +---+---+---+---+')
        for row in range(8, 0, -1):
            print(row, end=' ')
            for i in v_field.keys():
                print(v_field[i][str(row)], end=' ')
            print('|')
        print('  +---+---+---+---+')
        print('  A B C D E F G H')

    def __str__(self):
        return self.kind


class Pawn(Figure):
    def __init__(self, pos: str, color: str, possible_moves=[], all_possible_takes=[], flagok=0) -> None:
        kind = 'p' if color == "Black" else 'P'
        super().__init__(pos, color, kind, possible_moves, all_possible_takes, flagok)

    def calculate_possible_moves(self, field, all_moves_in_game, all_possible_takes, flagok) -> None:
        self.possible_moves = []
        self.possible_takes = []
        temp = 1 if self.color == 'White' else -1

        try:
            if self.pos[1] in '27' and field[self.pos[0]][str(int(self.pos[1]) + temp)] == ' ' and field[self.pos[0]][
                str(int(self.pos[1]) + temp * 2)] == ' ':
                self.possible_moves.append(self.pos[0] + str(int(self.pos[1]) + temp * 2))
        except:
            pass

        try:
            if field[self.pos[0]][str(int(self.pos[1]) + temp)] == ' ':
                self.possible_moves.append(self.pos[0] + str(int(self.pos[1]) + temp))
        except:
            pass

        try:
            if field[chr(ord(self.pos[0]) + 1)][str(int(self.pos[1]) + temp)].color != field[self.pos[0]][
                self.pos[1]].color:
                self.possible_moves.append(chr(ord(self.pos[0]) + 1) + str(int(self.pos[1]) + temp))
                self.possible_takes.append(chr(ord(self.pos[0]) + 1) + str(int(self.pos[1]) + temp))
        except:
            pass
        try:
            if field[chr(ord(self.pos[0]) - 1)][str(int(self.pos[1]) + temp)].color != field[self.pos[0]][
                self.pos[1]].color:
                self.possible_moves.append(chr(ord(self.pos[0]) - 1) + str(int(self.pos[1]) + temp))
                self.possible_takes.append(chr(ord(self.pos[0]) - 1) + str(int(self.pos[1]) + temp))
        except:
            pass
        try:
            if '-' in all_moves_in_game[-1]:
                if self.pos[1] == all_moves_in_game[-1].split('-')[1][1] and all_moves_in_game[-1].split('-')[0][
                    1] in '27' and all_moves_in_game[-1].split('-')[1][1] in '45' \
                        and chr(ord(self.pos[0]) + 1) == all_moves_in_game[-1].split('-')[0][0]:
                    if field[chr(ord(self.pos[0]) + 1)][str(int(self.pos[1]) + temp)] == ' ':
                        self.possible_moves.append(chr(ord(self.pos[0]) + 1) + str(int(self.pos[1]) + temp))
                        self.possible_takes.append(chr(ord(self.pos[0]) + 1) + str(int(self.pos[1]) + temp))
        except:
            pass
        try:
            if '-' in all_moves_in_game[-1]:
                if self.pos[1] == all_moves_in_game[-1].split('-')[1][1] and all_moves_in_game[-1].split('-')[0][
                    1] in '27' and all_moves_in_game[-1].split('-')[1][1] in '45' \
                        and chr(ord(self.pos[0]) - 1) == all_moves_in_game[-1].split('-')[0][0]:
                    if field[chr(ord(self.pos[0]) - 1)][str(int(self.pos[1]) + temp)] == ' ':
                        self.possible_moves.append(chr(ord(self.pos[0]) - 1) + str(int(self.pos[1]) + temp))
                        self.possible_takes.append(chr(ord(self.pos[0]) - 1) + str(int(self.pos[1]) + temp))
        except:
            pass


class Rook(Figure):
    def __init__(self, pos: str, color: str, possible_moves=[], all_possible_takes=[], flagok=0) -> None:
        kind = 'r' if color == "Black" else 'R'
        super().__init__(pos, color, kind, possible_moves, all_possible_takes, flagok)

    def calculate_possible_moves(self, field, all_moves_in_game, all_possible_takes, flagok) -> None:
        self.possible_moves = []
        self.possible_takes = []
        moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.calculated(field, moves, all_moves_in_game, all_possible_takes, flagok)


class Norse(Figure):
    def __init__(self, pos: str, color: str, possible_moves=[], all_possible_takes=[], flagok=0) -> None:
        kind = 'n' if color == "Black" else 'N'
        super().__init__(pos, color, kind, possible_moves, all_possible_takes, flagok)

    def calculate_possible_moves(self, field, all_moves_in_game, all_possible_takes, flagok=0) -> None:
        self.possible_moves = []
        self.possible_takes = []
        letters = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}
        un_letters = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'}
        moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dx, dy in moves:
            if 1 <= int(self.pos[1]) + dx <= 8 and 1 <= letters[self.pos[0]] + dy <= 8:
                if field[un_letters[letters[self.pos[0]] + dy]][str(int(self.pos[1]) + dx)] == ' ' or \
                        field[self.pos[0]][self.pos[1]].color != field[un_letters[letters[self.pos[0]] + dy]][
                    str(int(self.pos[1]) + dx)].color:
                    self.possible_moves.append(un_letters[letters[self.pos[0]] + dy] + str(int(self.pos[1]) + dx))
                    self.possible_takes.append(un_letters[letters[self.pos[0]] + dy] + str(int(self.pos[1]) + dx))


class Bishop(Figure):
    def __init__(self, pos: str, color: str, possible_moves=[], all_possible_takes=[], flagok=0) -> None:
        kind = 'b' if color == "Black" else 'B'
        super().__init__(pos, color, kind, possible_moves, all_possible_takes, flagok)

    def calculate_possible_moves(self, field, all_moves_in_game, all_possible_takes, flagok=0) -> None:
        self.possible_moves = []
        self.possible_takes = []
        moves = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
        self.calculated(field, moves, all_moves_in_game, all_possible_takes, flagok)


class Queen(Figure):
    def __init__(self, pos: str, color: str, possible_moves=[], all_possible_takes=[], flagok=0) -> None:
        kind = 'q' if color == "Black" else 'Q'
        super().__init__(pos, color, kind, possible_moves, all_possible_takes, flagok)

    def calculate_possible_moves(self, field, all_moves_in_game, all_possible_takes, flagok) -> None:
        self.possible_moves = []
        self.possible_takes = []
        moves = [(-1, -1), (1, 1), (-1, 1), (1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
        self.calculated(field, moves, all_moves_in_game, all_possible_takes, flagok)


class King(Figure):
    def __init__(self, pos: str, color: str, possible_moves=[], all_possible_takes=[], flagok=0) -> None:
        kind = 'k' if color == "Black" else 'K'
        super().__init__(pos, color, kind, possible_moves, all_possible_takes, flagok)

    def calculate_possible_moves(self, field, all_moves_in_game, all_possible_takes, flagok) -> None:
        self.possible_moves = []
        self.possible_takes = []
        moves = [(-1, -1), (1, 1), (-1, 1), (1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
        for dx, dy in moves:
            if 65 <= (ord(self.pos[0]) + dx) <= 72 and 1 <= (int(self.pos[1]) + dy) <= 8:
                if (field[chr(ord(self.pos[0]) + dx)][str(int(self.pos[1]) + dy)] == ' ' \
                    or field[chr(ord(self.pos[0]) + dx)][str(int(self.pos[1]) + dy)].color != \
                    field[self.pos[0]][self.pos[1]].color) and \
                        all(chr(ord(self.pos[0]) + dx) + str(int(self.pos[1]) + dy) not in i \
                            for i in all_possible_takes['Black' if self.color == 'White' else 'White']):
                    self.possible_moves.append(chr(ord(self.pos[0]) + dx) + str(int(self.pos[1]) + dy))
                    self.possible_takes.append(chr(ord(self.pos[0]) + dx) + str(int(self.pos[1]) + dy))
                else:
                    pass
        # Рокировка
        if (all('A1' not in i and 'E1' not in i for i in all_moves_in_game) and self.color == 'White' and \
            field['B']['1'] == ' ' and field['C']['1'] == ' ' and field['D']['1'] == ' ' and \
            all('B1' not in i and 'E1' not in i and 'C1' not in i and 'D1' not in i for i in
                all_possible_takes['Black'])) or \
                (all('A8' not in i and 'E8' not in i for i in all_moves_in_game) and self.color == 'Black' and \
                 field['B']['8'] == ' ' and field['C']['8'] == ' ' and field['D']['8'] == ' ' and \
                 all('B8' not in i and 'E8' not in i and 'C8' not in i and 'D8' not in i for i in
                     all_possible_takes['White'])):
            self.possible_moves.append(chr(ord(self.pos[0]) - 2) + self.pos[1])
        if (all('H1' not in i and 'E1' not in i for i in all_moves_in_game) and self.color == 'White' and \
            field['F']['1'] == ' ' and field['G']['1'] == ' ' and \
            all('F1' not in i and 'E1' not in i and 'G1' not in i for i in all_possible_takes['Black'])) or \
                (all('H8' not in i and 'E8' not in i for i in all_moves_in_game) and self.color == 'Black' and \
                 field['F']['8'] == ' ' and field['G']['8'] == ' ' and \
                 all('F8' not in i and 'E8' not in i and 'G8' not in i for i in all_possible_takes['White'])):
            self.possible_moves.append(chr(ord(self.pos[0]) + 2) + self.pos[1])


class ChessGame(object):
    start_field = {
        'A': {
            '1': Rook('A1', 'White'),
            '2': Pawn('A2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('A7', 'Black'),
            '8': Rook('A8', 'Black')
        },
        'B': {
            '1': Norse('B1', 'White'),
            '2': Pawn('B2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('B7', 'Black'),
            '8': Norse('B8', 'Black'),
        },
        'C': {
            '1': Bishop('C1', 'White'),
            '2': Pawn('C2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('C7', 'Black'),
            '8': Bishop('C8', 'Black'),
        },
        'D': {
            '1': Queen('D1', 'White'),
            '2': Pawn('D2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('D7', 'Black'),
            '8': Queen('D8', 'Black')
        },
        'E': {
            '1': King('E1', 'White'),
            '2': Pawn('E2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('E7', 'Black'),
            '8': King('E8', 'Black')
        },
        'F': {
            '1': Bishop('F1', 'White'),
            '2': Pawn('F2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('F7', 'Black'),
            '8': Bishop('F8', 'Black'),
        },
        'G': {
            '1': Norse('G1', 'White'),
            '2': Pawn('G2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('G7', 'Black'),
            '8': Norse('G8', 'Black'),
        },
        'H': {
            '1': Rook('H1', 'White'),
            '2': Pawn('H2', 'White'),
            '3': ' ',
            '4': ' ',
            '5': ' ',
            '6': ' ',
            '7': Pawn('H7', 'Black'),
            '8': Rook('H8', 'Black'),
        },
    }
    turn_move = 0
    all_moves_in_game = []
    all_figure = 32
    taken_now = []
    all_takes = {
        'White': [],
        'Black': []
    }
    pos_king = ['E1', 'E8']
    flagok = [0, pos_king[0], pos_king[1]]
    check_mate_possible_moves = []

    def __init__(self, field=start_field) -> None:
        self.field = field

    def print_field(self):
        print('  A B C D E F G H')
        print(' +---+---+---+---+')
        for row in range(8, 0, -1):
            print(row, end=' ')
            for i in self.field.keys():
                print(self.field[i][str(row)], end=' ')
            print('|')
        print('  +---+---+---+---+')
        print('  A B C D E F G H')

    def play(self) -> int:
        game_over = True

        while game_over:
            self.all_taken()
            print(f'Количество ходов в партии: {self.turn_move}')
            print(f'Ход игрока номер {self.turn_move % 2 + 1}')
            print('Если хотите вернуть ход, напишите: <- или количество ходов')

            if any(self.pos_king[self.turn_move % 2] == i for j in
                   self.all_takes[('Black' if self.turn_move % 2 == 0 else 'White')] for i in j):
                print('Шах')
                if self.check_mate():
                    print('и', 'Мат', sep=' \n')
                    game_over = False
                    continue
                self.flagok = [1, self.pos_king[0], self.pos_king[1]]
            start_possition = input('Выберите фигуру: ').upper()
            try:
                start_possition = int(start_possition)
            except:
                pass
            if start_possition == '<-':
                if self.turn_move == 0:
                    print('Ошибка, ходов в игре еще нет')
                else:
                    self.reverse_stroke(start_possition)
            elif type(start_possition) == int:
                while start_possition > 0:
                    if self.turn_move == 0:
                        self.print_field()
                        break
                    else:
                        self.reverse_stroke(start_possition)
                    start_possition -= 1
            else:

                self.field[start_possition[0]][start_possition[1]].visual_moves(self.field, self.all_moves_in_game,
                                                                                self.all_takes, self.flagok)
                new_possition = input('Введите куда будете ходить: ').upper()
                try:
                    self.taken_now.append(self.field[new_possition[0]][new_possition[1]])
                except:
                    pass
                color = 'White' if self.turn_move % 2 == 0 else 'Black'
                if self.field[start_possition[0]][start_possition[1]].make_move(new_possition, self.field, color,
                                                                                self.all_moves_in_game, self.all_takes,
                                                                                self.flagok):
                    print('Ошибка')
                    if self.field[new_possition[0]][new_possition[1]] != ' ':
                        self.taken_now.pop()
                    self.play()
                else:
                    # Записываем позицию короля, если она была изменена
                    if start_possition == self.pos_king[0]:
                        self.pos_king[0] = new_possition
                    if start_possition == self.pos_king[1]:
                        self.pos_king[1] = new_possition
                self.print_field()
                self.all_taken()
                self.turn_move += 1

    def check_mate(self):
        temp = True
        self.all_taken()
        self.field[self.pos_king[0 if self.turn_move % 2 == 0 else 1][0]][
            self.pos_king[0 if self.turn_move % 2 == 0 else 1][1]].calculate_possible_moves(self.field,
                                                                                            self.all_moves_in_game,
                                                                                            self.all_takes, self.flagok)

        for row in range(1, 9):
            for column in self.field.keys():
                if self.field[column][str(row)] != ' ' and self.field[column][str(row)].color == (
                'White' if self.turn_move % 2 == 0 else 'Black'):
                    self.field[column][str(row)].calculate_possible_moves(self.field, self.all_moves_in_game,
                                                                          self.all_takes, self.flagok)
                    pos_move = self.field[column][str(row)].possible_moves
                    for x in pos_move:
                        flag = 0
                        if self.field[x[0]][x[1]] != ' ':
                            flag = 1
                        self.field[column][str(row)].make_move(x, self.field,
                                                               'White' if self.turn_move % 2 == 0 else 'Black',
                                                               self.all_moves_in_game, self.all_takes, self.flagok)
                        self.all_taken()

                        if any(self.pos_king[self.turn_move % 2] == i for j in
                               self.all_takes[('Black' if self.turn_move % 2 == 0 else 'White')] for i in j):
                            self.reverse_stroke()
                            self.turn_move += 1
                        else:
                            temp = False
                            self.reverse_stroke()
                            self.turn_move += 1
                            break
                if temp == False:
                    break
            if temp == False:
                break
        return temp

    def all_taken(self):
        self.all_takes['White'] = []
        self.all_takes['Black'] = []

        for row in range(1, 9):
            for i in self.field.keys():
                if self.field[i][str(row)] != ' ':
                    self.field[i][str(row)].calculate_possible_moves(self.field, self.all_moves_in_game, self.all_takes,
                                                                     self.flagok)
                    if self.field[i][str(row)].color == 'White':
                        self.all_takes['White'].append(self.field[i][str(row)].pos)
                        self.all_takes['White'].append(self.field[i][str(row)].possible_takes)
                    elif self.field[i][str(row)].color == 'Black':
                        self.all_takes['Black'].append(self.field[i][str(row)].pos)
                        self.all_takes['Black'].append(self.field[i][str(row)].possible_takes)

    def reverse_stroke(self, start_possition=0):
        self.turn_move -= 1
        rev = self.all_moves_in_game[-1]
        flag = 0
        try:
            if self.all_moves_in_game[-2] == '*':
                flag = 1
            elif self.all_moves_in_game[-2] == '{':
                flag = 2
            elif self.all_moves_in_game[-2] == '}':
                flag = 3
            else:
                flag = 0
        except:
            pass
        temp = -1 if self.turn_move % 2 == 0 else 1
        if '-' in rev and flag == 0:  # D7 - D5
            rev = rev.split('-')
            if self.field[rev[1][0]][rev[1][1]].__str__() in ('Kk'):
                self.pos_king[self.turn_move % 2] = rev[0]
            self.field[rev[0][0]][rev[0][1]] = self.field[rev[1][0]][rev[1][1]]
            self.field[rev[1][0]][rev[1][1]] = ' '
            self.field[rev[0][0]][rev[0][1]].pos = rev[0]
        elif flag == 1:
            rev = self.all_moves_in_game[-1].split(':')
            self.field[rev[0][0]][rev[0][1]] = self.field[rev[1][0]][rev[1][1]]
            self.field[rev[1][0]][rev[1][1]] = ' '
            self.field[rev[0][0]][rev[0][1]].pos = rev[0]
            self.field[rev[1][0]][chr(ord(rev[1][1]) + temp)] = Pawn(rev[1][0] + chr(ord(rev[1][1]) + temp),
                                                                     'Black' if self.turn_move % 2 == 0 else 'White')
            self.all_moves_in_game.pop()
            self.all_figure += 1
        elif flag == 2:
            rev = rev.split('-')
            self.field[rev[0][0]][rev[0][1]] = self.field[rev[1][0]][rev[1][1]]
            self.field[rev[1][0]][rev[1][1]] = ' '
            self.field[rev[0][0]][rev[0][1]].pos = rev[0]
            self.field['A'][rev[0][1]] = self.field['D'][rev[0][1]]
            self.field['D'][rev[0][1]] = ' '
            self.field['A'][rev[0][1]].pos = 'A' + rev[0][1]
            self.all_moves_in_game.pop()
        elif flag == 3:
            rev = rev.split('-')
            self.field[rev[0][0]][rev[0][1]] = self.field[rev[1][0]][rev[1][1]]
            self.field[rev[1][0]][rev[1][1]] = ' '
            self.field[rev[0][0]][rev[0][1]].pos = rev[0]
            self.field['H'][rev[0][1]] = self.field['F'][rev[0][1]]
            self.field['F'][rev[0][1]] = ' '
            self.field['H'][rev[0][1]].pos = 'H' + rev[0][1]
            self.all_moves_in_game.pop()
        else:  # E4:D5
            rev = rev.split(':')

            self.field[rev[0][0]][rev[0][1]] = self.field[rev[1][0]][rev[1][1]]
            self.field[rev[0][0]][rev[0][1]].pos = rev[0]
            self.field[rev[1][0]][rev[1][1]] = self.taken_now[-1]
            self.all_figure += 1
            self.taken_now.pop()
        self.all_moves_in_game.pop()
        self.all_taken()
        if type(start_possition) == int:
            if start_possition == 1:
                self.print_field()
        else:
            self.print_field()


ChessGame().print_field()
ChessGame().play()
