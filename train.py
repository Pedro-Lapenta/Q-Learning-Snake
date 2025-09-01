# train.py

from agent import Agent
from snake import SnakeGame, Direction, Point

import matplotlib.pyplot as plt
import os
import random
import numpy as np
import time

def plot_scores(scores, mean_scores):
    plt.clf()
    plt.title('Training Progress')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores, label='Scores', color='blue', alpha=0.7)
    plt.plot(mean_scores, label='Mean Scores', color='red', linewidth=2)
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
    
    # Criar agente e jogo
    agent = Agent(q_table={}, alpha=0.1, gamma=0.9, epsilon=0.8)
    game = SnakeGame()
    
    print("Treinamento iniciado!")
    print("Interface gráfica aparecerá a cada 50 jogos")
    print("=" * 50)

    while True:
        # Pega o estado atual
        current_state = game.get_state()

        # Agente decide qual ação tomar
        final_move = agent.get_action(current_state)

        # Executa um passo do jogo
        # Mostrar interface gráfica apenas a cada 50 jogos
        show_ui = (agent.n_games % 50 == 0 and agent.n_games > 0) or agent.n_games == 0
        reward, game_over, score = game.play_step(final_move, show_ui)
        
        # Pega o novo estado do jogo
        state_new = game.get_state()

        # Treina o agente, ajustando a tabela Q
        agent.train_step(current_state, final_move, reward, state_new, game_over)
        
        # Quando o jogo acaba
        if game_over:
            # Reinicia o jogo 
            game.reset()
            agent.n_games += 1

            # Plota os resultados
            if score > record:
                record = score
                print(f"🎉 NEW RECORD: {record}")
            
            plot_scores_list.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            
            # Plot a cada 5 jogos (voltando ao original)
            if agent.n_games % 5 == 0:
                plot_scores(plot_scores_list, plot_mean_scores)

            # Estatísticas detalhadas a cada 10 jogos
            if agent.n_games % 10 == 0:
                epsilon_current = max(0.01, agent.epsilon - agent.n_games * 0.01)
                print(f"Game {agent.n_games:4d} | Score: {score:2d} | Record: {record:2d} | "
                      f"Mean: {mean_score:.1f} | Epsilon: {epsilon_current:.3f} | "
                      f"Q-States: {len(agent.q_table)}")
            else:
                print(f"Game {agent.n_games:4d} | Score: {score:2d}")

        # Pausa apenas quando mostrando a UI
        if show_ui:
            time.sleep(0.01)

    # Limpeza
    game.close()
    plt.close('all')

if __name__ == '__main__':
    train()