# train.py

from agent import Agent
from snake import SnakeGame, Direction, Point  # Corrigido o import

import matplotlib.pyplot as plt
# from IPython import display  # Remover se não estiver no Jupyter
import os
import random
import numpy as np

# AQUI VAI A FUNÇÃO `plot_scores` QUE PLOTA OS RESULTADOS
def plot_scores(scores, mean_scores):
    # Se não estiver no Jupyter, use uma versão simplificada
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores, label='Scores')
    plt.plot(mean_scores, label='Mean Scores')
    plt.ylim(ymin=0)
    plt.legend()
    if len(scores) > 0:
        plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    if len(mean_scores) > 0:
        plt.text(len(mean_scores)-1, mean_scores[-1], str(int(mean_scores[-1])))
    plt.pause(0.1)
    plt.show(block=False)

def train():
    plot_scores_list = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    
    # Corrigindo a criação do Agent
    agent = Agent(q_table={}, alpha=0.1, gamma=0.9, epsilon=0.8)
    game = SnakeGame()

    while True:
        # Pega o estado atual
        state_old = game.get_state()

        # Agente decide qual ação tomar
        final_move = agent.get_action(state_old)

        # Executa um passo do jogo
        reward, game_over, score = game.play_step(final_move)
        
        # Pega o novo estado do jogo
        state_new = game.get_state()

        # Treina o agente, ajustando a tabela Q
        agent.train_step(state_old, final_move, reward, state_new, game_over)

        # Quando o jogo acaba
        if game_over:
            # Reinicia o jogo 
            game = SnakeGame()  # Criar nova instância em vez de reset()
            agent.n_games += 1

            # Plota os resultados
            if score > record:
                record = score
            plot_scores_list.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            
            # Plot a cada 10 jogos para não sobrecarregar
            if agent.n_games % 10 == 0:
                plot_scores(plot_scores_list, plot_mean_scores)

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

# Bloco para começar a rodar o script
if __name__ == '__main__':
    train()