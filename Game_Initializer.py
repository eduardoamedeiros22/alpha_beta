# We'll use the time module to measure the time of evaluating
# game tree in every move. It's a nice way to show the
# distinction between the basic Minimax and Minimax with
# alpha-beta pruning :)
import time


class Game:
    def __init__(self):
        self.result = None
        self.player_turn = None
        self.current_state = None
        self.initialize_game()

    def initialize_game(self):

        # O primeiro a jogar sempre será o X
        self.player_turn = 'X'

        self.current_state = [['.', '.', '.'],
                              ['.', '.', '.'],
                              ['.', '.', '.']]

    def draw_game(self):
        for i in range(0, 3):
            for j in range(0, 3):
                print('{}|'.format(self.current_state[i][j]), end=" ")
            print()
        print()

    # Validando movimento
    def is_valid(self, px, py):
        if px < 0 or px > 2 or py < 0 or py > 2:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    # Verifica se o jogo chegou ao final, seja por vitória (horizontal, vertical ou nas diagonais)
    # ou se o tabuleiro está cheio.
    def is_end(self):

        # Tabuleiro está cheio
        for i in range(0, 3):
            for j in range(0, 3):
                # There's an empty field, we continue the game
                if self.current_state[i][j] == '.':
                    return None

        # Diagonal Principal
        if (self.current_state[0][0] != '.' and
                self.current_state[0][0] == self.current_state[1][1] and
                self.current_state[0][0] == self.current_state[2][2]):
            return self.current_state[0][0]

        # Diagonal Secundária
        if (self.current_state[0][2] != '.' and
                self.current_state[0][2] == self.current_state[1][1] and
                self.current_state[0][2] == self.current_state[2][0]):
            return self.current_state[0][2]

        # Vertical
        for i in range(0, 3):
            if (self.current_state[0][i] != '.' and
                    self.current_state[0][i] == self.current_state[1][i] and
                    self.current_state[1][i] == self.current_state[2][i]):
                return self.current_state[0][i]

        # Horizontal
        for i in range(0, 3):
            if self.current_state[i] == ['X', 'X', 'X']:
                return 'X'
            elif self.current_state[i] == ['O', 'O', 'O']:
                return 'O'

        # Empatou!
        return '.'

    # O player com '0' é o max, no caso a IA
    def max(self):

        # Possíveis valores para a variável maxv
        # -1 - Derrota
        # 0  - Empate
        # 1  - Vitória

        # Inicializando a variável com -2 que é menor que o pior caso:
        max_value = -2

        px = None
        py = None

        result = self.is_end()

        # Se o jogo chegar no final, a função precisará
        # retornar o valor do final, que pode ser:
        # -1 - Derrota
        # 0  - Empate
        # 1  - Vitória
        if result == 'X':
            return -1, 0, 0
        elif result == 'O':
            return 1, 0, 0
        elif result == '.':
            return 0, 0, 0

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    # Em um espaço vazio '0' realiza um movimento e chama a função Min
                    # Esse é um galho da árvore do jogo.
                    self.current_state[i][j] = 'O'
                    (m, min_i, min_j) = self.min()
                    # Consertando o valor de maxv se necessário
                    if m > max_value:
                        max_value = m
                        px = i
                        py = j
                    # Voltando o campo para vazio
                    self.current_state[i][j] = '.'
        return max_value, px, py

        # Jogador 'X' é o min, nesse caso o humano (porém o algoritmo calcula a jogada ideal)

    def min(self):

        # Possíveis valores para a variável minv
        # -1 - Vitória
        # 0  - Empate
        # 1  - Derrota

        # Inicializando a variável com o valor 2 que é pior que o pior caso
        min_value = 2

        qx = None
        qy = None

        result = self.is_end()

        if result == 'X':
            return -1, 0, 0
        elif result == 'O':
            return 1, 0, 0
        elif result == '.':
            return 0, 0, 0

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max()
                    if m < min_value:
                        min_value = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'

        return min_value, qx, qy

    def max_alpha_beta(self, alpha, beta):
        max_value = -2
        px = None
        py = None

        result = self.is_end()

        if result == 'X':
            return -1, 0, 0
        elif result == 'O':
            return 1, 0, 0
        elif result == '.':
            return 0, 0, 0

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                    if m > max_value:
                        max_value = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'

                    # Esses 2 "ifs" são a única diferença entre um algoritmo regular minimax e o alfa beta
                    if max_value >= beta:
                        return max_value, px, py

                    if max_value > alpha:
                        alpha = max_value

        return max_value, px, py

    def min_alpha_beta(self, alpha, beta):

        min_value = 2

        qx = None
        qy = None

        result = self.is_end()

        if result == 'X':
            return -1, 0, 0
        elif result == 'O':
            return 1, 0, 0
        elif result == '.':
            return 0, 0, 0

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max_alpha_beta(alpha, beta)
                    if m < min_value:
                        min_value = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'

                    if min_value <= alpha:
                        return min_value, qx, qy

                    if min_value < beta:
                        beta = min_value

        return min_value, qx, qy

    def play(self):
        while True:
            self.draw_game()
            self.result = self.is_end()

            # Imprimindo a mensagem correta de acordo com o resultado.
            if self.result is not None:
                if self.result == 'X':
                    print('O vencedor é X!')
                elif self.result == 'O':
                    print('O vencedor é O!')
                elif self.result == '.':
                    print("Empatou!")

                self.initialize_game()
                return

            # Turno do player
            if self.player_turn == 'X':

                while True:

                    start = time.time()
                    (m, qx, qy) = self.min()
                    end = time.time()
                    print('Tempo de validação: {}s'.format(round(end - start, 7)))
                    # print('Movimento Recomendado: X = {}, Y = {}'.format(qx, qy))
                    #
                    # px = int(input('Insira a coordenada X: '))
                    # py = int(input('Insira a coordenada Y: '))
                    #
                    # (qx, qy) = (px, py)
                    #
                    #
                    # if self.is_valid(px, py):
                    #     self.current_state[px][py] = 'X'
                    #     self.player_turn = 'O'
                    #     break
                    if self.is_valid(qx, qy):
                        self.current_state[qx][qy] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('Movimento Inválido, tente denovo')

            # Turno da IA
            else:
                (m, px, py) = self.max()
                self.current_state[px][py] = 'O'
                self.player_turn = 'X'

    def play_alpha_beta(self):
        while True:
            self.draw_game()
            self.result = self.is_end()

            if self.result is not None:
                if self.result == 'X':
                    print('O vencedor é X!')
                elif self.result == 'O':
                    print('O vencedor é O!')
                elif self.result == '.':
                    print("Empatou!")

                self.initialize_game()
                return

            if self.player_turn == 'X':

                while True:
                    start = time.time()
                    (m, qx, qy) = self.min_alpha_beta(-2, 2)
                    end = time.time()
                    print('Tempo de validação: {}s'.format(round(end - start, 7)))
                    print('Movimento Recomendado: X = {}, Y = {}'.format(qx, qy))

                    px = int(input('Insira a coordenada X: '))
                    py = int(input('Insira a coordenada Y: '))

                    qx = px
                    qy = py

                    if self.is_valid(px, py):
                        self.current_state[px][py] = 'X'
                        self.player_turn = 'O'
                        break
                    # if self.is_valid(qx, qy):
                    #     self.current_state[qx][qy] = 'X'
                    #     self.player_turn = 'O'
                    #     break
                    else:
                        print('Movimento Inválido, tente denovo')

            else:
                (m, px, py) = self.max_alpha_beta(-2, 2)
                self.current_state[px][py] = 'O'
                self.player_turn = 'X'
