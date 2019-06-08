
import numpy as np
import matplotlib.pyplot as plt

number_of_games = 10
graph_size_array = np.arange(number_of_games)


zombie = np.array([90, 114, 170, 201, 211, 230, 241, 240, 245, 242])
villager = np.array([60, 54, 35, 40, 33, 17, 21, 18, 19 , 20])
enderman = np.array([40, 36, 25, 30, 24, 10, 19, 16, 14, 13])

reward_percentages = np.array([0.30321, 0.36434, 0.34214, 0.40398, 0.56786, 0.66545, 0.68934, 0.68932, 0.75476, 0.74353])

plt.subplot(2, 1, 1)
# plt.plot(x1, y1, 'o-')
plt.plot(graph_size_array, zombie, label="Zombies")
plt.plot(graph_size_array, villager, label="Villagers")
plt.plot(graph_size_array, enderman, label="Endermen")
plt.legend(loc="upper left")
plt.title('Line of Site Count')
plt.xlabel('Number of Games')
plt.ylabel('Number Of Times Entitiy In Focus in a 1 Minute Game')

plt.subplot(2, 1, 2)
plt.plot(graph_size_array, reward_percentages, '.-')
plt.xlabel('Number of Games')
plt.ylabel('Reward Percentage')
plt.title('Reward Percentage Over Game')

plt.show()














