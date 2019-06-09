import numpy as np
import matplotlib.pyplot as plt

''' 
If you can turn the following into functions that are usable
in final_project.py that would be super helpful
If there any other evaluations that you can think of that would be awesome 
as well. 
''' 

##### code for part 1 evaluation #######
'''
Grading Agent's choice of who to attack:

We take multiple instances of states and resulting actions to see what was in the agent’s line of sight when they chose to attack. We grade the agent on the percentage of times a harmful entity was in the line of sight vs a non-harmful entity. This is to show that the agent learns to prioritize harmful_entities while avoiding non-harmful entities.
'''


number_of_games = 10
graph_size_array = np.arange(number_of_games)


zombie = np.array([90, 114, 170, 201, 211, 230, 241, 240, 245, 242])
villager = np.array([60, 54, 35, 40, 33, 17, 21, 18, 19 , 20])
enderman = np.array([40, 36, 25, 30, 24, 10, 19, 16, 14, 13])

reward_percentages = np.array([0.30321, 0.36434, 0.34214, 0.40398, 0.56786, 0.66545, 0.68934, 0.68932, 0.75476, 0.74353])

plt.subplot(2, 1, 1)
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


##### code for part 2 evaluation #######
'''
Grading Reward: 
    these functions below should help implementing this 
        get_number_of_killed_entites()
        successful_reward_percentage()


THIS HAS NOT YET BEEN IMPLEMENTED OR TESTED (it's more of an idea)
if you can get it to work great or if you have other ideas that's great too


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

