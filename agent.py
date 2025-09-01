import numpy as np
import random

class Agent:
    def __init__(self, q_table, alpha, gamma, epsilon):
        self.q_table = q_table if q_table is not None else {}
        self.alpha = alpha  # Use os parâmetros passados
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_games = 0    # ERRO: Este atributo estava faltando

    def train_step(self, state_old, action, reward, state_new, game_over):
        # 1. Converte os estados para tuplas para que possam ser chaves no dicionário
        state_old_key = tuple(state_old)
        state_new_key = tuple(state_new)

        # 2. Inicializa o estado se ele for novo na tabela Q
        if state_old_key not in self.q_table:
            self.q_table[state_old_key] = [0, 0, 0] # 3 valores, um para cada ação

        if not game_over:
            # 3. Calcula o valor Q da próxima ação
            if state_new_key not in self.q_table:
                self.q_table[state_new_key] = [0, 0, 0]
            
            target = reward + self.gamma * max(self.q_table[state_new_key])
        else:
            target = reward

        # 4. Atualiza o valor Q do estado antigo
        action_index = np.argmax(action) # Pega o índice da ação tomada
        
        # A fórmula de atualização:
        # q_novo = q_velho + alpha * (target - q_velho)
        q_old = self.q_table[state_old_key][action_index]
        self.q_table[state_old_key][action_index] = q_old + self.alpha * (target - q_old)

    def get_action(self, state):
        state_key = tuple(state)

        # EXPLORATION - ERRO: Lógica do epsilon estava errada
        epsilon_threshold = max(0.01, self.epsilon - self.n_games * 0.01)  # Decaimento gradual
        
        if random.random() < epsilon_threshold:  # Use random.random() em vez de randint
            move = random.randint(0, 2)
            final_move = [0, 0, 0]
            final_move[move] = 1
            return final_move
        
        # EXPLOITATION
        if state_key in self.q_table:
            # Pega os Q-values para o estado atual
            q_values = self.q_table[state_key]
            # Escolhe a ação com o maior Q-value
            action_index = np.argmax(q_values)
            
            final_move = [0, 0, 0]
            final_move[action_index] = 1
            return final_move
        else:
            # Se o estado for novo, toma uma ação aleatória para começar a exploração
            move = random.randint(0, 2)
            final_move = [0, 0, 0]
            final_move[move] = 1
            return final_move