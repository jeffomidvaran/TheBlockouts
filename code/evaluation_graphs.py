import numpy as np
import matplotlib.pyplot as plt


##### code for part 1 evaluation #######
'''
Grading Agent's choice of who to attack:

We take multiple instances of states and resulting actions to see what was in the agent’s line of sight when they chose to attack. We grade the agent on the percentage of times a harmful entity was in the line of sight vs a non-harmful entity. This is to show that the agent learns to prioritize harmful_entities while avoiding non-harmful entities.
'''


number_of_games = 20
graph_size_array = np.arange(number_of_games)


zombie = np.array([8, 21, 26, 52, 33, 58, 51, 54, 66, 65, 73, 67, 76, 66, 53, 55, 46, 48, 67, 56])
villager = np.array([0, 1, 3, 0, 3, 0, 1, 12, 7, 2, 0, 1, 0, 0, 0, 6, 1, 2, 0, 0])
enderman = np.array([13, 9, 5, 7, 2, 22, 3, 2, 9, 10, 7, 8, 12, 4, 3, 2, 5, 1, 10, 6])
shotsfired = np.array([28, 30, 15, 65, 29, 58, 47, 64, 56, 72, 61, 53, 81, 62, 62, 48, 44, 47, 49, 47])
swordSwings = np.array([17, 18, 26, 25, 18, 31, 34, 20, 36, 18, 30, 42, 36, 22, 16, 23, 16, 13, 41, 27])
bowSwings = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


#reward_percentages = np.array([0.30321, 0.36434, 0.34214, 0.40398, 0.56786, 0.66545, 0.68934, 0.68932, 0.75476, 0.74353])

reward_per_mission = np.array([116.93, 92.08999999999999, 78.35, 373.2699999999999, 67.01999999999998, 244.01999999999967, 395.0300000000002, 282.2199999999999, 233.9899999999998, 280.39999999999975, 317.3699999999999, 344.68000000000006, 325.7200000000001, 340.63999999999993, 359.3299999999998, 174.91999999999987, 142.54999999999993, 150.60999999999987, 258.79999999999995, 213.65999999999985])
cumulative_reward = np.array([116.93, 209.01999999999992, 287.3699999999999, 660.640000000001, 727.6600000000017, 971.6800000000028, 1366.7100000000019, 1648.929999999998, 1882.9199999999926, 2163.319999999987, 2480.689999999982, 2825.3699999999776, 3151.0899999999733, 3491.729999999968, 3851.059999999964, 4025.97999999996, 4168.529999999963, 4319.13999999998, 4577.940000000007, 4791.600000000029])

#plt.subplot(4, 1, 1)
plt.figure(1)
plt.plot(graph_size_array, zombie, label="Zombies")
plt.plot(graph_size_array, villager, label="Villagers")
plt.plot(graph_size_array, enderman, label="Endermen")
plt.legend(loc="upper left")
plt.title('Line of Site Count')
plt.xlabel('Number of Games')
plt.ylabel('Entitiy In Focus per Game')

#plt.subplot(4, 1, 2)
plt.figure(2)
plt.plot(graph_size_array, cumulative_reward, '.-')
plt.xlabel('Number of Games')
plt.ylabel('cumulative reward')
plt.title('Cumulative Reward vs Game')

#plt.subplot(4, 1, 3)
plt.figure(3)
plt.plot(graph_size_array, reward_per_mission, '.-')
plt.xlabel('Number of Games')
plt.ylabel('reward')
plt.title('Reward per Game')


#plt.subplot(4,1,4)
plt.figure(4)
plt.plot(graph_size_array,shotsfired,label="Arrows Fired")
plt.plot(graph_size_array,swordSwings,label="Sword Swings")
#plt.plot(graph_size_array,bowSwings,label="Bow Swings")
plt.legend(loc="upper left")
plt.title('Attacks per Game')
plt.xlabel('Number of Games')
plt.ylabel('Times Agent Tried to Attack')

plt.show()


##### code for part 2 evaluation #######
'''
Grading Reward: 
    these functions below should help implementing this 
        get_number_of_killed_entites()
        successful_reward_percentage()


FROM THE STATUS PAGE(see webpage for full details)
    The reward metric is a percentage. Where the Agent receives a 100% if all of the harmful entities are killed and all of the non-harmful entities are left unharmed. To calculate this metric, the following formula is applied.

    v = number of attacks needed to kill villager * reward for hitting villager
    z = number of attacks needed to kill zombie * reward for hitting zombie
    e = number of attacks needed to kill Endermen * reward for hitting Endermen

    nv = total number of villagers
    nz = total number of zombies
    ne = total number of Endermen

    nvk = total number of villagers killed
    nzk = total number of zombies killed 
    nek = total number of Endermen killed

'''
def get_number_of_killed_entities(entities, 
                                  num_of_villagers, 
                                  num_of_zombies, 
                                  num_of_enderman, 
                                  num_of_creepers):

    current_villagers = 0
    current_zombies = 0
    current_enderman = 0
    current_creepers = 0

    for e in entities:
        if e['name'] == "Villager":
            current_villagers+=1
        if e['name'] == "Zombie":
            current_zombies+=1
        if e['name'] == "Enderman":
            current_enderman+=1
        if e['name'] == "Creeper":
            current_creepers+=1

    return  {
                "Villager": num_of_villagers-current_villagers, 
                "Zombie": num_of_zombies-current_zombies,
                "Enderman": num_of_enderman-current_enderman,
                "Creeper": num_of_creepers-current_creepers 
            }


def successful_reward_percentage(v,z,e,nv,nz,ne,nvk,nzk,nek):
    numerator = abs(v*nv) + v*nvk + z*nzk + e*nek 
    denominator = v*nv + z*nz + e*ne
    return numerator/denominator

