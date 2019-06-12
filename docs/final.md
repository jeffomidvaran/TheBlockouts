---
layout: default
title:  Final Report
---

## Video
<iframe width="560" height="315" src="https://www.youtube.com/embed/uEv_zd5c7fE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


## Project Summary
<p>
The idea of our project is to create a counter siege AI that learns to both demarcate between "enemy" and "good" entities as well as using its knowledge of its weapon inventory to kill as many enemies as possible. The agent will start on one side of a clay barrier and be equipped with a bow (and arrow) and sword. The side of the barrier opposite to the agent will be filled with "enemy" entities, specifically endermen and zombies. Zombies will look for holes in the barrier to rush created by the Endermen who will randomly remove block pieces from the from the barrier. On the same side of the barrier as the agent will be "good" entities, specifically villagers. The agent should learn not kill any villagers.
<br>
While our agent can eventually implicitly differentiate between an enemy and good entity, the focus of the project is to have the agent demonstrate weapon-use intelligence as noted in the first paragraph. When the agent determines which entity should be classified as a threat, it must know how to respond. A sword swing for example, is the much preferred choice when directly in front of an enemy because a sword swipe can damage multiple enemies. A bow is less preferable because it can only strike a single entity at a time. It does become preferable, however, when its target entity is far enough away. These 2 weapon-use ideas (sword and bow) would be tedious, but possible to implement explicitly. However, explicit implementation becomes impractical quickly when adding more weapons. </p>
[Code Repository](https://github.com/jeffomidvaran/TheBlockouts)


## Approach
<br><br>
<img src="images/reinforcement_learning1.jpg">
<br><br>
<img src="images/markovtest.jpg">
<br><br>


Our update function is based on the Bellman Equation for Q learning. 
<br>
$$ \quad Q^\pi(s_t, a_t) = E[R_{t+1} + \gamma R_{t+2} +  \gamma^2 R_{t+3}... + [s_t, a_t]] $$ 

For our project we are implementing a q-tabular reinforcement learning system inspired by assignment_2. The table is implemented as a 2-level python dictionary for states-actions and their assigned reward; any unseen state will be initialized to 0. The update function for the q-table is as follows:

$$ \text{old_q_value} + [$$\alpha \times $$ (\text{current_reward} + $$\gamma \times$$ \text{max_q_value_for_state_x} - \text{old_q_value})] $$

<strong>old_q_value</strong> represents the old value our function assigned to the previous state and action
<br>
<strong>alpha $$\alpha$$</strong> represents the learning rate; how fast our function picks up on and incorporates what it observes
<br>
<strong>gamma $$\gamma$$</strong> represents the discount factor; how much importance we want to give to future rewards
<br>
<strong>max_q_value_for_state_x</strong> represents the maximum assigned value for the current state and all possible actions for that state.
<br>

We have set both our alpha and gamma to 1 as we were satisfied with the performance of our agent with those values. Our agent will choose the best action for the given state (or any of the best actions at random if there are multiple best actions); an action being the best means that it has the highest assigned value for the state. We will, with some probability, epsilon, choose a random action for a state. This is to simulate an exploration of the space and fight against reach some local maxima of understanding. Our epsilon is set to 0.1 as we are satisfied with the agent's performance with that value. 


<!-- ENTERING CODE TEST  -->
<code>
import math
for i in range(10):
    print("yes")
</code>


<h4> Our states will consist of the following: </h4>
<ul>
    <li>Are there currently any zombies, endermen, or villagers alive (boolean)</li>
    <li>What type of entity is in the agent’s line of sight (entity_dictionary)</li>
</ul>


<h4>Our action states will consist of the following:</h4>
<ul>
    <li>Attacking with the swing of a bow (the agent will move to the entity in line of sight and start swiping at it with a bow)</li>
    <li>Attacking by shooting an arrow (the agent will move to the entity in the line of sight and start shooting arrows)</li>
    <li>Targeting a random entity (the agent will switch focus to an entity in the current line of sight)</li>
    <li>Doing nothing (the agent will wait for the next agent action sequence)</li>
</ul>


<h4> Terminating States: </h4>
<ul>
    <li>Time runs out</li>
    <li>Agent dies</li>
</ul>


<h4>Rewards:</h4>
<ul>
    <li>Dealing damage to a zombie: 10</li>
    <li>Dealing damage to an endermen: 1</li>
    <li>Dealing damage to a villager: -10</li>
</ul>


<h4>Goal:</h4>
<p>Kill as many bad entities as possible (Zombies and Enderman) while leaving Villagers unharmed. Learn effective attacks with a bow and arrow and sword factoring in distance from harmful entities. </p>


<h4>Environment: </h4>
<p>The environment will be set as a box-like cave with a barrier separating the Agent and Villagers from the Zombies and Enderman. Enderman have the ability to remove blocks from the barrier protecting the Agent and Villagers. The Agent will be equipped with a bow-and-arrow and will have the ability to swipe the bow and fire arrows. The environment will have a set number of Zombies, Endermen, and Villagers. </p>



## Evaluation
<p>
ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
</p>

$$ v $$ = number of attacks needed to kill villager * reward for hitting villager<br>
$$ z $$ = number of attacks needed to kill zombie * reward for hitting zombie<br>
$$ e $$ = number of attacks needed to kill Endermen * reward for hitting Endermen<br>

$$ n_v = $$ total number of villagers<br>
$$ n_z = $$ total number of zombies<br>
$$ n_e = $$ total number of Endermen<br>

$$ n_{vk} = $$ total number of villagers killed<br>
$$ n_{zk} = $$ total number of zombies killed<br>
$$ n_{ek} = $$ total number of Endermen killed<br>

$$ \text{successful reward percentage} = P =  \frac{|vn_v| + vn_{vk} + zn_{zk} + en_{ek}} {vn_{v} + zn_{z} + en_{e}} $$ 

<br> <br>
<img src="images/reward_percentage_graphic1.jpg">
<br> <br>

## Resources Used 
- [Minecraft Wiki](https://minecraft.gamepedia.com/)
- [AI inspiration](https://github.com/Microsoft/malmo-challenge/tree/master/malmopy)
- [tabular_q_learning.py](https://github.com/microsoft/malmo/blob/master/Malmo/samples/Python_examples/tabular_q_learning.py)
- [hit_test.py](https://github.com/microsoft/malmo/blob/master/Malmo/samples/Python_examples/hit_test.py)
- [Microsoft XML Schema documentation](https://microsoft.github.io/malmo/0.30.0/Schemas/MissionHandlers.html)
