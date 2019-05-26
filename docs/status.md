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
few paragrahs. Detailed description of approach. Summarize main algorithm
<br>
Bellman Equation for Q learning
<br>
$$ Q^\pi(s_t, a_t) = E[R_{t+1} + \gamma R_{t+2} +  \gamma^2 R_{t+3}... + [s_t, a_t] $$

<img src="images/reinforcement_learning1.jpg">


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