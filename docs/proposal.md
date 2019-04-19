---
layout: default
title:  Proposal
---

## Summary of the Project
The main idea of our project is to create a counter siege AI. Counter siege, in this context, means the ai will try to survive as long as possible while maintaining a structure or at least preventing enemies from crossing its border. The ai will take as input enemy locations, enemy types, the ideal state of its structure, and the current state of the structure. As output the AI will decide between moving, fighting, and placing blocks. 

## AI/ML Algorithms
We plan to use reinforcement learning as the basis for our AI agent.

## Evaluation Plan
The evaluation of our AI's success will be length of time surviving, the integrity of the structure(how many blocks are missing at the end of the siege), and if the agent survives to the end of the siege. The AI will start with a predefined structure which it will know all the block types and block positions of as its baseline structural integrity and border position. Failure states will constitute dying, total loss of the structure(could be changed to percentage loss of structure depending on mission), or enemies crossing the border of the structure.<br/> 

Sanity cases will be surviving to the end of siege with no border crossings and the structure surviving.<br/>

Our moonshot goal will be to get the ai to succeed in these tasks without being immediately aware of enemy positions(meaning it will have to see enemies approach before reacting to them) and structural damage (meaning it will have to check its structure for holes and vulnerabilities).<br/> 

## Appointment with the Instructor
Appointment set for 3:15pm - 3:30pm, Thursday, April 25, 2019
https://calendly.com/sameersingh/office-hours