import copy

class Figure(object):
    def __init__(self, pos: str, color: str, kind=None, possible_moves=[], possible_takes=[], flagok=0) -> None:
        self.pos = pos
        self.color = color
        self.kind = kind
        self.possible_moves = possible_moves
        self.possible_takes = possible_takes
        self.flagok = flagok

    def calculate_possible_moves(self, field, all_moves_in_game=[], all_possible_takes=[], flagok = 0) -> None:
        pass

    def make_move(self, new_pos: str, field: list, color_now: str, all_moves_in_game=[], all_possible_takes=[],
                  flagok=0) -> None or bool:
        self.calculate_possible_moves(field, all_moves_in_game, all_possible_takes, flagok)
        if (new_pos in self.possible_moves and self.color == color_now) or (self.kind in 'Cc' and new_pos in self.possible_takes):
            if self.kind not in 'cC':
                if field[new_pos[0]][new_pos[1]] == ' ':
                    all_moves_in_game.append(self.pos + '-' + new_pos)
                else:
                    all_moves_in_game.append(self.pos + ':' + new_pos)



                if self.kind in 'Pp' or self.kind in 'Gg':
                    if new_pos[1] in '18':
                        fig = input('Выберите фигурy R, N, B, Q: ').upper()
                        fig.upper()
                        field[self.pos[0]][self.pos[1]] = ' '
                        if fig == 'R':
                            field[new_pos[0]][new_pos[1]] = Rook(new_pos, self.color)
                        elif fig == 'N':
                            field[new_pos[0]][new_pos[1]] = Norse(new_pos, self.color)
                        elif fig == 'B':
                            field[new_pos[0]][new_pos[1]] = Bishop(new_pos, self.color)
                        elif fig == 'Q':
                            field[new_pos[0]][new_pos[1]] = Queen(new_pos, self.color)
                        else:
                            print('Нет такой фигуры')
                        all_moves_in_game.insert(-1, '123')

                    elif self.pos[0] == new_pos[0] or field[new_pos[0]][new_pos[1]] != ' ':
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
                elif self.kind in 'Kk':
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
            else:
                if len(self.possible_takes) == 0:
                    field[self.pos[0]][self.pos[1]] = ' '
                    field[new_pos[0]][new_pos[1]] = self
                    self.pos = new_pos[0] + new_pos[1]
                else:
                    field[self.pos[0]][self.pos[1]] = ' '
                    field[chr(ord(new_pos[0]) - ord(self.pos[0]) + (1 if ord(new_pos[0]) - ord(self.pos[0]) < 0 else -1) + ord(self.pos[0]))]\
                        [chr(ord(new_pos[1]) - ord(self.pos[1]) + (1 if ord(new_pos[1]) - ord(self.pos[1]) < 0 else -1) + ord(self.pos[1]))]= ' '
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

    def visual_moves(self, field, all_moves_in_game=[], all_possible_takes=[], flagok=0):
        self.calculate_possible_moves(field, all_moves_in_game, all_possible_takes, flagok)
        v_field = copy.deepcopy(field)
        if self.kind not in 'Cc' or len(self.possible_takes) == 0:
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
        else:
            for i in self.possible_takes:
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


class Gleb(Figure):
    def __init__(self, pos: str, color: str, possible_moves=[], all_possible_takes=[], flagok=0) -> None:
        kind = 'g' if color == "Black" else 'G'
        super().__init__(pos, color, kind, possible_moves, all_possible_takes, flagok)
    def calculate_possible_moves(self, field, all_moves_in_game, all_possible_takes, flagok) -> None:
        self.possible_moves = []
        self.possible_takes = []
        moves = [(-1, 1), (0, 1), (1,1)]
        temp = 1 if self.color == 'White' else -1
        for dx, dy in moves:
            if 65 <= (ord(self.pos[0]) + dx * temp) <= 72 and 1 <= (int(self.pos[1]) + dy * temp)<= 8:
                if field[chr(ord(self.pos[0]) + dx * temp)][chr(ord(self.pos[1]) + dy * temp)] == ' ' or \
                        field[chr(ord(self.pos[0]) + dx * temp)][chr(ord(self.pos[1]) + dy * temp)].color != field[self.pos[0]][self.pos[1]].color:
                    self.possible_moves.append(chr(ord(self.pos[0]) + dx * temp)+chr(ord(self.pos[1]) + dy * temp))
                    self.possible_takes.append(chr(ord(self.pos[0]) + dx * temp)+chr(ord(self.pos[1]) + dy * temp))


class What_is_love(Figure):
    def __init__(self, pos: str, color: str, possible_moves=[], all_possible_takes=[], flagok=0) -> None:
        kind = 'w' if color == "Black" else 'W'
        super().__init__(pos, color, kind, possible_moves, all_possible_takes, flagok)
    def calculate_possible_moves(self, field, all_moves_in_game, all_possible_takes, flagok) -> None:
        self.possible_moves = []
        self.possible_takes = []
        moves = [(2,0), (0, 2), (-2,0), (0, -2)]
        self.calculated(field, moves, all_moves_in_game, all_possible_takes, flagok)


class Vova(Figure):
    def __init__(self, pos: str, color: str, possible_moves=[], all_possible_takes=[], flagok=0) -> None:
        kind = 'v' if color == "Black" else 'V'
        super().__init__(pos, color, kind, possible_moves, all_possible_takes, flagok)
    def calculate_possible_moves(self, field, all_moves_in_game, all_possible_takes, flagok) -> None:
        self.possible_moves = []
        self.possible_takes = []
        moves = [(2,0), (0, 2), (-2,0), (0, -2), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        self.calculated(field, moves, all_moves_in_game, all_possible_takes, flagok)


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
                if ((field[chr(ord(self.pos[0]) + dx)][str(int(self.pos[1]) + dy)] == ' ' \
                    or field[chr(ord(self.pos[0]) + dx)][str(int(self.pos[1]) + dy)].color != \
                    field[self.pos[0]][self.pos[1]].color) and \
                        all(chr(ord(self.pos[0]) + dx) + str(int(self.pos[1]) + dy) not in i \
                            for i in all_possible_takes['Black' if self.color == 'White' else 'White'])) or \
                        (field[chr(ord(self.pos[0]) + dx)][str(int(self.pos[1]) + dy)] != ' ' and \
                         field[chr(ord(self.pos[0]) + dx)][str(int(self.pos[1]) + dy)].color != field[self.pos[0]][self.pos[1]].color):
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


class Checkers(Figure):
    def __init__(self, pos: str, color: str, possible_moves=[], all_possible_takes=[], flagok=0) -> None:
        kind = 'c' if color == "Black" else 'C'
        super().__init__(pos, color, kind, possible_moves, all_possible_takes, flagok)
    def calculate_possible_moves(self, field, all_moves_in_game=[], all_possible_takes=[], flagok=0) -> None:
        self.possible_moves = []
        self.possible_takes = []
        temp = -1 if self.color == 'Black' else 1
        moves = [(1*temp,1*temp), (-1*temp, 1*temp)]
        f = 0
        for dx, dy in moves:
            if 'A' <= chr(ord(self.pos[0]) + dx) <= 'H' and '1' <= chr(ord(self.pos[1]) + dy) <= '8':
                    if field[chr(ord(self.pos[0]) + dx)][chr(ord(self.pos[1]) + dy)] == ' ':
                        self.possible_moves.append(chr(ord(self.pos[0]) + dx) + chr(ord(self.pos[1]) + dy))
                    elif field[chr(ord(self.pos[0]) + dx)][chr(ord(self.pos[1]) + dy)].color != self.color:
                        f = 1
        if f != 0:
            moves = [(1*temp,1*temp), (-1*temp, 1*temp), (1*temp, -1*temp), (-1*temp, -1 * temp)]
            for dx, dy in moves:
                if 'A' <= chr(ord(self.pos[0]) + dx*2) <= 'H' and '1' <= chr(ord(self.pos[1]) + dy*2) <= '8':
                    if field[chr(ord(self.pos[0]) + dx)][chr(ord(self.pos[1]) + dy)] != ' ' and field[chr(ord(self.pos[0]) + dx)][chr(ord(self.pos[1]) + dy)].color != self.color and \
                            field[chr(ord(self.pos[0]) + dx*2)][chr(ord(self.pos[1]) + dy*2)] == ' ':
                        self.possible_takes.append(chr(ord(self.pos[0]) + dx*2)+chr(ord(self.pos[1]) + dy*2))
        if len(self.possible_takes) != 0:
            self.possible_moves = []

class ChessGame(object):
    print(
        'режимы игры:'
    )
    print(
        '1. Обычка'
    )
    print(
        '2. С новыми фигурами'
    )
    print(
        '3. Шашхи'
    )
    x = input ('Выберите режим: ')
    turn_move = 0
    all_moves_in_game = []
    taken_now = []
    all_takes = {
        'White': [],
        'Black': []
    }
    if x in '12':
        if x == '2':
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
                    '2': What_is_love('B2', 'White'),
                    '3': Vova('B3', 'White'),
                    '4': ' ',
                    '5': ' ',
                    '6': Vova('B6', 'Black'),
                    '7': What_is_love('B7', 'Black'),
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
                    '2': Gleb('D2', 'White'),
                    '3': ' ',
                    '4': ' ',
                    '5': ' ',
                    '6': ' ',
                    '7': Gleb('D7', 'Black'),
                    '8': Queen('D8', 'Black')
                },
                'E': {
                    '1': King('E1', 'White'),
                    '2': Gleb('E2', 'White'),
                    '3': ' ',
                    '4': ' ',
                    '5': ' ',
                    '6': ' ',
                    '7': Gleb('E7', 'Black'),
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
                    '2': What_is_love('G2', 'White'),
                    '3': Vova('G3', 'White'),
                    '4': ' ',
                    '5': ' ',
                    '6': Vova('G6', 'Black'),
                    '7': What_is_love('G7', 'Black'),
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
        else:
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
        all_figure = 32
        pos_king = ['E1', 'E8']
        flagok = [0, pos_king[0], pos_king[1]]
        check_mate_possible_moves = []
    else:
        start_field = {
            'A': {
                '1': Checkers('A1', 'White'),
                '2': '□',
                '3': Checkers('A3', 'White'),
                '4': '□',
                '5': ' ',
                '6': '□',
                '7': Checkers('A7', 'Black'),
                '8': '□'
            },
            'B': {
                '1': '□',
                '2': Checkers('B2', 'White'),
                '3': '□',
                '4': ' ',
                '5': '□',
                '6': Checkers('B6', 'Black'),
                '7': '□',
                '8': Checkers('B8', 'Black'),
            },
            'C': {
                '1': Checkers('C1', 'White'),
                '2': '□',
                '3': Checkers('C3', 'White'),
                '4': '□',
                '5': ' ',
                '6': '□',
                '7': Checkers('C7', 'Black'),
                '8': '□'
            },
            'D': {
                '1': '□',
                '2': Checkers('D2', 'White'),
                '3': '□',
                '4': ' ',
                '5': '□',
                '6': Checkers('D6', 'Black'),
                '7': '□',
                '8': Checkers('D8', 'Black'),
            },
            'E': {
                '1': Checkers('E1', 'White'),
                '2': '□',
                '3': Checkers('E3', 'White'),
                '4': '□',
                '5': ' ',
                '6': '□',
                '7': Checkers('E7', 'Black'),
                '8': '□'
            },
            'F': {
                '1': '□',
                '2': Checkers('F2', 'White'),
                '3': '□',
                '4': ' ',
                '5': '□',
                '6': Checkers('F6', 'Black'),
                '7': '□',
                '8': Checkers('F8', 'Black'),
            },
            'G': {
                '1': Checkers('G1', 'White'),
                '2': '□',
                '3': Checkers('G3', 'White'),
                '4': '□',
                '5': ' ',
                '6': '□',
                '7': Checkers('G7', 'Black'),
                '8': '□'
            },
            'H': {
                '1': '□',
                '2': Checkers('H2', 'White'),
                '3': '□',
                '4': ' ',
                '5': '□',
                '6': Checkers('H6', 'Black'),
                '7': '□',
                '8': Checkers('H8', 'Black'),
            },
        }
        fig_white = 12
        fig_black = 12


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

    game_over = True

    def play(self) -> int:
        if self.x in '12':
            while self.game_over:
                self.all_taken()
                print(f'Количество ходов в партии: {self.turn_move}')
                print(f'Ход игрока номер {self.turn_move % 2 + 1}')
                print('Если хотите вернуть ход, напишите: <- или количество ходов')

                if any(self.pos_king[self.turn_move % 2] == i for j in
                       self.all_takes[('Black' if self.turn_move % 2 == 0 else 'White')] for i in j):
                    print('Шах')
                    if self.check_mate():
                        print('и', 'Мат', sep=' \n')
                        self.game_over = False
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
                    self.all_taken()
                    if any(self.pos_king[self.turn_move % 2] == i for j in
                           self.all_takes[('Black' if self.turn_move % 2 == 0 else 'White')] for i in j):
                        print('Фигура под шахом')
                        if self.field[new_possition[0]][new_possition[1]] != ' ':
                            self.taken_now.pop()
                        self.reverse_stroke()
                        self.turn_move += 1
                    else:
                        self.print_field()
                        self.all_taken()
                        self.turn_move += 1
        else:
            while self.fig_white > 0 and self.fig_black > 0:
                print(f'Ходит игрок: {1 if self.turn_move%2 == 0 else 2}')
                must_be_pos = []
                for row in range(1, 9):
                    for i in self.field.keys():
                        if self.field[i][str(row)] != ' ' and self.field[i][str(row)] != '□':
                            self.field[i][str(row)].calculate_possible_moves(self.field)
                            if len(self.field[i][str(row)].possible_takes) != 0:
                                if self.field[i][str(row)].color == 'White' if self.turn_move%2==0 else 'Black':
                                    must_be_pos.append(i + str(row))

                if len(must_be_pos) != 0:
                    print('Возможные шашки: ', *must_be_pos)
                    start_pos = input('Введите, позицию шашки: ').upper()
                    while start_pos not in must_be_pos:
                        print('Ошибка')
                        start_pos = input('Введите, позицию шашки: ').upper()
                else:
                    start_pos = input('Введите, позицию шашки: ').upper()
                self.field[start_pos[0]][start_pos[1]].visual_moves(self.field)
                new_pos = input('Куда хотите пойти: ').upper()

                if self.field[start_pos[0]][start_pos[1]].make_move(new_pos, self.field, 'White' if self.turn_move%2==0 else 'Black'):
                    print('Ошибка')
                else:
                    self.print_field()
                    self.turn_move += 1

                    count_w = 0
                    count_b = 0
                    for row in range(1, 9):
                        for i in self.field.keys():
                            if self.field[i][str(row)] != ' ' and self.field[i][str(row)] != '□':
                                count_w += (1 if self.field[i][str(row)].color == 'White' else 0)
                                count_b += (1 if self.field[i][str(row)].color == 'Black' else 0)


                    if count_b != self.fig_black or count_w != self.fig_white:
                        self.fig_white = count_w
                        self.fig_black = count_b

                        while True:
                            self.field[new_pos[0]][new_pos[1]].calculate_possible_moves(self.field)
                            start_pos = new_pos
                            if len(self.field[new_pos[0]][new_pos[1]].possible_takes) != 0:
                                self.turn_move -= 1
                                print('варианты хода: ', *self.field[new_pos[0]][new_pos[1]].possible_takes)
                                pos_in_while = input('Ваш ход: ').upper()
                                if pos_in_while in self.field[new_pos[0]][new_pos[1]].possible_takes:
                                    start_pos, new_pos = new_pos, pos_in_while
                                    if self.field[start_pos[0]][start_pos[1]].make_move(new_pos, self.field, 'White' if self.turn_move%2==0 else 'Black'):
                                        print('Ошибка')
                                    else:
                                        self.turn_move += 1
                                        self.print_field()
                                else:
                                    print('Ошибка')
                            else:
                                break

            if self.fig_white == 0:
                print('Победа черных')

            else:
                print('Победа белых')






    def check_mate(self):
        temp = True
        self.all_taken()
        self.field[self.pos_king[0 if self.turn_move % 2 == 0 else 1][0]][
            self.pos_king[0 if self.turn_move % 2 == 0 else 1][1]].calculate_possible_moves(self.field,
                                                                                            self.all_moves_in_game,
                                                                                            self.all_takes, self.flagok)

        if self.field[self.pos_king[0 if self.turn_move % 2 == 0 else 1][0]][self.pos_king[0 if self.turn_move % 2 == 0 else 1][1]].possible_moves != []:
            return False

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
            elif self.all_moves_in_game[-2] == '123':
                flag = 4
            else:
                flag = 0
        except:
            pass
        if flag == 4:
            self.field[rev[-2]][rev[-1]] = Pawn(rev[-2:], 'Black' if self.turn_move else 'White')
            flag = 0
            self.all_moves_in_game.remove('123')
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
