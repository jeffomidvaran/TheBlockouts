---
layout: default
title: Status
---

## Video
brief description of problem
example capture of a run that is working. How you did it failures

<iframe width="560" height="315" src="https://www.youtube.com/embed/wnPaqCjGIgA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Project Summary
The main idea of The Blockouts project is to create a counter siege AI. Counter siege, in this context, means the AI will try to survive as long as possible while trying to preventing enemies from crossing its border. The AI will take as input enemy locations, and enemy types. As output the AI will decide between moving, fighting, which enemy to attack and which weapon to use. We plan to add more input and output information as our project grows...


## Approach
For our project we are implementing a q-tabular reinforcement learning system inspired by assignment_2. 
<br><br>
<img src="images/reinforcement_learning1.jpg">
<br><br>
Our update function is based on the Bellman Equation for Q learning. 
$$ \quad Q^\pi(s_t, a_t) = E[R_{t+1} + \gamma R_{t+2} +  \gamma^2 R_{t+3}... + [s_t, a_t]] $$ 
<br>
<!-- $$ \text{oldQValue} + [\alpha \times (\text{currentReward} + \gamma * \text{maxQValueForStateX} - \text{oldQValue})] $$ -->


##### Our states will consist of the following:
<ul>
    <li>Are there currently any zombies, endermen, or villagers alive (boolean)</li>
    <li>What type of entity is in the agent’s line of sight (entity_dictionary)</li>
</ul>


##### Our action states will consist of the following:
<ul>
    <li>Attacking with the swing of a bow (the agent will move to the entity in line of sight and start swiping at it with a bow)</li>
    <li>Attacking by shooting an arrow (the agent will move to the entity in the line of sight and start shooting arrows)</li>
    <li>Targeting a random entity (the agent will switch focus to an entity in the current line of sight)</li>
    <li>Doing nothing (the agent will wait for the next agent action sequence)</li>
</ul>


##### Terminating States:
<ul>
    <li>Time runs out</li>
    <li>Agent dies</li>
</ul>


#### Rewards:
<ul>
    <li>Dealing damage to a zombie: 10</li>
    <li>Dealing damage to an endermen: 1</li>
    <li>Dealing damage to a villager: -10</li>
    <li>Surviving until end of game: 100</li>
    <li>Dying before the game time has ended: -100</li>
</ul>


#### Goal:
<p>Kill as many bad entities as possible (Zombies and Enderman) while leaving Villagers unharmed. </p>


#### Environment:
<p>The environment will be set as a box-like cave with a barrier separating the Agent and Villagers from the Zombies and Enderman. Enderman have the ability to remove blocks from the barrier protecting the Agent and Villagers. The Agent will be equipped with a bow-and-arrow and will have the ability to swipe the bow and fire arrows. The environment will have a set number of Zombies, Endermen, and Villagers. </p>



## Evaluation 
evaluate project. Present results to show reader that this is a working implementation. Plot charts tables etc... Few paragraphs

## Remaining Goal and Challenges
few paragraphs, goals for the next 2-3 weeks. Describe how you consider your prototype to be limited, and what you want to add.



<h2>Resources Used</h2>
- [Source code](https://github.com/jeffomidvaran/TheBlochttps://github.com/Microsoft/malmo-challenge/tree/master/malmopykouts)
- [Minecraft Wiki](https://minecraft.gamepedia.com/)
- [AI inspiration](https://github.com/Microsoft/malmo-challenge/tree/master/malmopy)

code documentation
AI/ML libraries, stackoverflow