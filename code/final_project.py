from __future__ import print_function
from __future__ import division
from builtins import range
from past.utils import old_div
import MalmoPython
import os
import sys
import time
import json
import math
import random
import agent_file
import entity_functions
import world_builder
# import evaluation_graphs

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

################################################################
###################### USER ADDED FUNCTIONS ####################
################################################################


###### CHANGE VARIABLE FOR MULTIPLE GAMES ################################
# NUMBER_OF_REPS = 1
##########################################################################

MAX_LIFE_DICT = {"Villager":20, "Zombie":20, "Enderman":40, "Creeper":20, "ourAgent":100}
villager_view_count_list = [] 
enderman_view_count_list = [] 
zombie_view_count_list = [] 

villager_view_count = 0
enderman_view_count = 0
zombie_view_count  = 0


def switch_to_item(hotslot_number):
    '''Not 0 indexed 1 is the first item in the hotbar'''
    agent_host.sendCommand("hotbar." + str(hotslot_number) + " 1") #Press the hotbar key
    time.sleep(0.2)
    agent_host.sendCommand("hotbar." + str(hotslot_number) + " 0") 
    time.sleep(0.05)


def attack():
  agent_host.sendCommand("attack 1")
  time.sleep(0.03)
  agent_host.sendCommand("attack 0")
  time.sleep(0.05)


def shoot_arrow(ob, cock_time=0.3):
  # check if arrow is current item else switch
  if(ob['currentItemIndex'] != 0):
    switch_to_item(1)
  agent_host.sendCommand("use 1")
  time.sleep(cock_time)
  agent_host.sendCommand("use 0")
  time.sleep(0.05)


def attack_with_sword(ob):
  if(ob['currentItemIndex'] != 1):
    switch_to_item(2)
  attack()


def attack_with_bow_swing(ob):
  if(ob['currentItemIndex'] != 0):
    switch_to_item(1)
  attack()


def get_agent_position(ob):
  if u'Yaw' in ob:
      current_yaw = ob[u'Yaw']
  if u'XPos' in ob:
      self_x = ob[u'XPos']
  if u'ZPos' in ob:
      self_z = ob[u'ZPos']
  return current_yaw, self_x, self_z


def get_agent_dict(ob):
    ''' returns the 0th index entity which is always the agent '''
    entities = ob["entities"]
    return entities[0]


def determine_direction(x_pull, z_pull, current_yaw):
  ''' Determine the direction we need to turn in order to head towards point with most zombies '''
  yaw = -180 * math.atan2(x_pull, z_pull) / math.pi
  difference = yaw - current_yaw;
  while difference < -180:
      difference += 360;
  while difference > 180:
      difference -= 360;
  difference /= 180.0;
  return difference


def get_pull_dist_weight(e_dict, self_x, self_z):
    x_pull = 0
    z_pull = 0
    dist = 0 
    weight = 0
    if(e_dict != None):
      dist = max(0.0001, (e_dict["x"] - self_x) * (e_dict["x"] - self_x) + (e_dict["z"] - self_z) * (e_dict["z"] - self_z))
      weight = MAX_LIFE_DICT[e_dict["name"]]+1 - e_dict["life"] 
      x_pull += weight * (e_dict["x"] - self_x) / dist
      z_pull += weight * (e_dict["z"] - self_z) / dist
    return x_pull, z_pull, dist, weight


def move_toward_entity(e_dict, current_yaw, self_x, self_z):
    x_pull, z_pull, dist, weight = get_pull_dist_weight(e_dict, self_x, self_z)
    difference = determine_direction(x_pull, z_pull, current_yaw)
    agent_host.sendCommand("turn " + str(difference))
    # move slower when turning faster - helps with "orbiting" problem
    move_speed = 1.0 if abs(difference) < 0.5 else 0  
    agent_host.sendCommand("move " + str(move_speed))


def move_away_from_entity(e_dict, current_yaw, self_x, self_z):
    x_pull, z_pull, dist, weight = get_pull_dist_weight(e_dict, self_x, self_z)
    difference = determine_direction(x_pull, z_pull, current_yaw)
    agent_host.sendCommand("turn " + str(difference))
    # move slower when turning faster - helps with "orbiting" problem
    move_speed = 1.0 if abs(difference) < 0.5 else 0  
    agent_host.sendCommand("move " + str(-move_speed))


def number_enemies(ob):
    "returns the number of Zombies and Endermen in existence"
    count = 0
    for item in ob["entities"]:
        if item["name"] == "Zombie" or item["name"] == "Enderman" or item["name"] == "Creeper":
          count += 1
    return count

def get_entity_dict(ob, id):
  for dic in ob["entities"]:
    if dic["id"] == id:
      return dic
  return None


def take_action(ob, action, extra):
    "Calls for the action the agent requested"
    if action == "bow_swipe_forward":
        attack_entity_with_bow_swing_move_forward(extra[0], extra[1], extra[2], extra[3], extra[4])
    elif action == "arrow_shot_forward":
        attack_entity_by_shooting_arrow_move_forward(extra[0], extra[1], extra[2], extra[3], extra[4])
    elif action == "sword_swipe_forward":
        attack_entity_with_sword_move_forward(extra[0], extra[1], extra[2], extra[3], extra[4])
    elif action == "bow_swipe_backward":
        attack_entity_with_bow_swing_move_backward(extra[0], extra[1], extra[2], extra[3], extra[4])
    elif action == "sword_swipe_backward": 
        attack_entity_with_sword_move_backward(extra[0], extra[1], extra[2], extra[3], extra[4])
    elif action == "arrow_shot_backward":
        attack_entity_by_shooting_arrow_move_backward(extra[0], extra[1], extra[2], extra[3], extra[4])
    elif action == "change_target":
        return entity_functions.switch_to_random_entity(ob)
        time.sleep(0.03)
    elif action == "do_nothing":
        time.sleep(0.03)
    return extra[1]


def give_reward(state, action):
  "returns the respective rewards for whoever the agent attacks"
  if action == "bow_swipe" or action == "arrow_shot":
      if state[1] == "Zombie":
        return 10
      elif state[1] == "Enderman":
        return 1
      elif state[1] == "Villager":
        return -10
  return 0

def give_reward_updated(state, action, d_ene, d_good, d_neu):
  reward = 0
  reward += (10 * d_ene)
  reward += (-10 * d_good)
  reward += (1 * d_neu)

  if action in ["arrow_shot_forward", "sword_swipe_forward", 
    "arrow_shot_backward", "sword_swipe_backward"]:
    if state[1] == "Zombie":
      reward += 0.1
    elif state[1] == "Enderman":
      reward += 0.01
    elif state[1] == "Villager":
      reward += -0.1

  if action == "change_target":
    reward -= 2

  return reward


def how_many_damaged(ob, dr, kind):
  damaged = 0
  for ent in dr:
    if entity_functions.get_entity_type(ent, ob) == kind:
      damaged += 1
  return damaged


def handle_line_of_site(attack_function, ob):
    if u'LineOfSight' in ob:
      los = ob[u'LineOfSight']
      if(los["type"] == "Villager"):
        global villager_view_count
        villager_view_count += 1 
      elif(los["type"] == "Zombie"):
        global zombie_view_count
        zombie_view_count +=1
      elif(los["type"] == "Enderman"):
        global enderman_view_count
        enderman_view_count += 1
      hitType=los["hitType"]
      if hitType == "entity":
        attack_function(ob)


def attack_entity_with_bow_swing_move_forward(ob, entity_dict, current_yaw, self_x, self_z):
    move_toward_entity(entity_dict, current_yaw, self_x, self_z)
    handle_line_of_site(attack_with_bow_swing, ob)
      

def attack_entity_by_shooting_arrow_move_forward(ob, entity_dict, current_yaw, self_x, self_z):
    move_toward_entity(entity_dict, current_yaw, self_x, self_z)
    handle_line_of_site(shoot_arrow, ob)


def attack_entity_with_sword_move_forward(ob, entity_dict, current_yaw, self_x, self_z):
    move_toward_entity(entity_dict, current_yaw, self_x, self_z)
    handle_line_of_site(attack_with_sword, ob)


def attack_entity_with_bow_swing_move_backward(ob, entity_dict, current_yaw, self_x, self_z):
    move_away_from_entity(entity_dict, current_yaw, self_x, self_z)
    handle_line_of_site(attack_with_bow_swing, ob)
      

def attack_entity_by_shooting_arrow_move_backward(ob, entity_dict, current_yaw, self_x, self_z):
    move_away_from_entity(entity_dict, current_yaw, self_x, self_z)
    handle_line_of_site(shoot_arrow, ob)


def attack_entity_with_sword_move_backward(ob, entity_dict, current_yaw, self_x, self_z):
    move_away_from_entity(entity_dict, current_yaw, self_x, self_z)
    handle_line_of_site(attack_with_sword, ob)




################################################################
#################### END USER DEFINED FUNCTIONS ################
################################################################


if __name__  == '__main__':
    random.seed(0)

    agent_host = MalmoPython.AgentHost()
    try:
        agent_host.parse( sys.argv )
    except RuntimeError as e:
        print('ERROR:',e)
        print(agent_host.getUsage())
        exit(1)
    if agent_host.receivedArgument("help"):
        print(agent_host.getUsage())
        exit(0)

  
############################################################# 
#################  Start of mission #########################
############################################################# 

    ########################################################################
    ####### ADD GAME SETTINGS HERE #########################################
    ########################################################################

    num_of_villagers = 4
    num_of_zombies = 4
    num_of_enderman = 2
    num_of_creepers = 0
    game_time = 60
    number_of_games = 10

    agent_brain = agent_file.TabQAgent(actions = ["change_target", "arrow_shot_forward", "sword_swipe_forward", "do_nothing"])


    ########################################################################
    ####### END ADD GAME SETTINGS HERE #####################################
    ########################################################################

    for repeat in range(number_of_games):
      villager_view_count = 0
      enderman_view_count = 0
      zombie_view_count  = 0

      missionXML = world_builder.get_XML(num_of_villagers, 
                                         num_of_zombies, 
                                         num_of_enderman,
                                         num_of_creepers, 
                                         game_time)


      my_mission = MalmoPython.MissionSpec(missionXML, True)
      my_mission_record = MalmoPython.MissionRecordSpec()

      ######## Attempt to start a mission ################################
      max_retries = 3
      for retry in range(max_retries):
          try:
              agent_host.startMission( my_mission, my_mission_record )
              break
          except RuntimeError as e:
              if retry == max_retries - 1:
                  print("Error starting mission:",e)
                  exit(1)
              else:
                  time.sleep(2)


      ####### LOOP WHILE MISSION IS STARTING: SETUP #################
      world_state = agent_host.getWorldState()
      while not world_state.has_mission_begun:
          time.sleep(0.1)
          world_state = agent_host.getWorldState()
          for error in world_state.errors:
              print("Error:",error.text)


      ####### LOOP UNTIL MISSION ENDS ##############################
      current_r = 0
      target = None
      target_id = ""
      prev_ob = None
      iterations = 0

      while world_state.is_mission_running:
          time.sleep(0.1)
          world_state = agent_host.getWorldState()
          for error in world_state.errors:
              print("Error:",error.text)
          if world_state.number_of_observations_since_last_state > 0:
              msg = world_state.observations[-1].text    
              ob = json.loads(msg) 

              # print(iterations)
              ########## AI CODE #####################################
              current_yaw, self_x, self_z = get_agent_position(ob)
              if target == None:
                target = entity_functions.switch_to_random_entity(ob)

              if(iterations > 7): 
                  swipe_range = entity_functions.entity_within_swipe_range(ob)

                  current_s = (number_enemies(ob), entity_functions.entity_in_sight(ob), swipe_range)

                  current_a = agent_brain.choose_action(current_s, current_r)

                  prev_ob = ob

                  extra = [ob, target, current_yaw, self_x, self_z]
                  target = take_action(ob, current_a, extra)


                  #####Begin refresh frame###############
                  world_state = agent_host.getWorldState()
                  if world_state.number_of_observations_since_last_state > 0:
                    msg = world_state.observations[-1].text 
                    ob = json.loads(msg)
                  #####End refresh frame################

                  dr = entity_functions.get_entity_damage_report(ob, prev_ob)
                  damaged_enemies = sum([how_many_damaged(prev_ob, dr, x) for x in ["Zombie", "Creeper"]])
                  damaged_good = how_many_damaged(prev_ob, dr, "Villager")
                  damaged_neutrals = how_many_damaged(prev_ob, dr, "Enderman")

                  current_r = give_reward_updated(current_s, current_a, damaged_enemies, damaged_good, damaged_neutrals)
              ########## END AI CODE ##################################



              ##### THESE 2 UPDATES NEED TO HAPPEN AT THE END OF EVERY LOOP !!!!!!
              ##### SO BE CAREFUL ADDING BREAKS CAUSE IT CAN CAUSE ISSUES !!!!!
              iterations += 1
              ################################################################


      ##### EXAMPLE OF HOW TO USE THIS FUNCTION FROM EVALUATION GRAPHS
      ##### CAN BE REMOVED
      # result = evaluation_graphs.get_number_of_killed_entities(prev_ob['entities'],
      #                                                 num_of_villagers, 
      #                                                 num_of_zombies, 
      #                                                 num_of_enderman, 
      #                                                 num_of_creepers)

      print()
      print("Mission {} ended".format(repeat))
      villager_view_count_list.append(villager_view_count)
      enderman_view_count_list.append(enderman_view_count) 
      zombie_view_count_list.append(zombie_view_count)

      print("Villager views = {}".format(villager_view_count_list))
      print("Enderman views = {}".format(enderman_view_count_list))
      print("Zombie views = {}".format(zombie_view_count_list))
      ##########################################################
      ###################### END OF MISSION ####################
      ##########################################################