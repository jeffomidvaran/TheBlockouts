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

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

################################################################
###################### USER ADDED FUNCTIONS ####################
################################################################

ARENA_WIDTH = 20
ARENA_BREADTH = 20
NUMBER_OF_REPS = 1
GAME_SECONDS = 100
MAX_LIFE_DICT = {"Villager":20, "Zombie":20, "Enderman":40, "Creeper":20}

villager_view_count_list = [] 
enderman_view_count_list = [] 
zombie_view_count_list = [] 

villager_view_count = 0
enderman_view_count = 0
zombie_view_count  = 0


class Timer:
    def __init__(self, run_time):
        self.start_time = time.time()
        self.run_time = run_time
        self.stop_time = self.start_time + run_time
    
    def time_elapsed(self):
        if(self.stop_time <= time.time()):
            self.start_time = time.time()
            self.stop_time = self.start_time + self.run_time
            return True
        else:
            return False


class RL:
    ''' Reinforcement Learner ''' 
    def __init__(self):
      self.reward = 0


def game_time(seconds):
    return str(seconds * 1000)


def switch_to_item(hotslot_number):
    '''Not 0 indexed 1 is the first item in the hotbar'''
    agent_host.sendCommand("hotbar." + str(hotslot_number) + " 1") #Press the hotbar key
    time.sleep(0.2)
    agent_host.sendCommand("hotbar." + str(hotslot_number) + " 0") 


def shoot_arrow(cock_time=0.3):
  # agent_host.sendCommand("use 1")
  # time.sleep(cock_time)
  # agent_host.sendCommand("use 0")
  # time.sleep(0.05)
  pass


def attack():
  agent_host.sendCommand("attack 1")


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


def get_agent_position(ob):
  if u'Yaw' in ob:
      current_yaw = ob[u'Yaw']
  if u'XPos' in ob:
      self_x = ob[u'XPos']
  if u'ZPos' in ob:
      self_z = ob[u'ZPos']
  return current_yaw, self_x, self_z


def spawn_enemies(*args):
    result_string = ""
    for enemy in args:
        entity = """ <DrawEntity x="{}" y="{}" z="{}" type="{}" yaw="{}" pitch="{}" xVel="{}" yVel="{}" zVel="{}"/>
        """.format(enemy[0],enemy[1],enemy[2],enemy[3],enemy[4],enemy[5], enemy[6],enemy[7],enemy[8])
        result_string += entity
    return result_string


def spawn_multiple_enemies(ememy_list):
  result_string = ""
  for e in ememy_list:
    for _ in range(e[1]):
      if(e[0] == "Creeper"):
        result_string +=  '''<DrawEntity x="10" y="227" z="10" type="{}" yaw="0" xVel="{}" yVel="{}" zVel="{}"/>'''.format(e[0],1,1,1)
      elif(e[0] == "Villager" or e[0] == "Sheep"):
        result_string +=  '''<DrawEntity x="4" y="227" z="4" type="{}" yaw="0" />'''.format(e[0])
      else:
        result_string +=  '''<DrawEntity x="10" y="227" z="10" type="{}" yaw="0" />'''.format(e[0])
  return result_string



def move_and_turn_agent(e_dict, current_yaw, self_x, self_z):
    x_pull = 0
    z_pull = 0

    dist = max(0.0001, (e_dict["x"] - self_x) * (e_dict["x"] - self_x) + (e_dict["z"] - self_z) * (e_dict["z"] - self_z))

    weight = MAX_LIFE_DICT[e_dict["name"]]+1 - e_dict["life"] #
    
    x_pull += weight * (e_dict["x"] - self_x) / dist
    z_pull += weight * (e_dict["z"] - self_z) / dist

    difference = determine_direction(x_pull, z_pull, current_yaw)
    agent_host.sendCommand("turn " + str(difference))
    # move slower when turning faster - helps with "orbiting" problem
    move_speed = 1.0 if abs(difference) < 0.5 else 0  
    agent_host.sendCommand("move " + str(move_speed))


def number_enemies(ob):
    "returns the numbber o Zombies and Endermen in existence"
    count = 0
    for item in ob["entities"]:
        if item["name"] == "Zombie" or item["name"] == "Enderman":
          count += 1
    return count


def take_action(action, extra):
    "Calls for the action the agent requested"
    if action == "bow_swipe":
        attack_entity_with_bow_swing(extra[0], extra[1], extra[2], extra[3], extra[4])
    elif action == "arrow_shot":
        attack_entity_by_shooting_arrow(extra[0], extra[1], extra[2], extra[3], extra[4])
    elif action == "change_target":
        return entity_functions.switch_to_random_entity(ob)
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
        attack_function()


def attack_entity_with_bow_swing(ob, entity_dict, current_yaw, self_x, self_z):
    move_and_turn_agent(entity_dict, current_yaw, self_x, self_z)
    life_before_attack = entity_dict["life"]
    handle_line_of_site(attack, ob)
      

def attack_entity_by_shooting_arrow(ob, entity_dict, current_yaw, self_x, self_z):
    move_and_turn_agent(entity_dict, current_yaw, self_x, self_z)
    handle_line_of_site(shoot_arrow, ob)


def get_agent_dict(ob):
    ''' returns the 0th index entity which is always the agent '''
    entities = ob["entities"]
    return entities[0]


def make_enclosure(start_x, start_z, end_x, end_z, height, barrier_type="clay", wall_type="bedrock", barrier=True):
    result_string = ""
    ''' start x and start z will start building from the upper left corner''' 

    # BUILD THE CEILING
    for x in range(start_x, end_x):
      for z in range(start_z, end_z+2):
        #CEILING
        result_string += '''<DrawBlock x="{}" y="{}" z="{}" type="glowstone" />'''.format(x,227+height-2, z)  
        result_string += '''<DrawBlock x="{}" y="{}" z="{}" type="{}" />'''.format(x,227+height-1, z, wall_type)  

        #FLOOR
        result_string += '''<DrawBlock x="{}" y="{}" z="{}" type="glowstone" />'''.format(x,227-1, z)  
        result_string += '''<DrawBlock x="{}" y="{}" z="{}" type="{}" />'''.format(x,227-2, z, wall_type)  

    # BUILD THE WALLS 
    for h in range(227, 227+height-1):
      for x in range(start_x, end_x):
        result_string += '''<DrawBlock x="{}" y="{}" z="{}" type="{}" />'''.format(x, h, start_z, wall_type)  
        result_string += '''<DrawBlock x="{}" y="{}" z="{}" type="{}" />'''.format(x, h, end_z+1, wall_type)  

      for z in range(start_z, end_z):
        result_string += '''<DrawBlock x="{}" y="{}" z="{}" type="{}" />'''.format(start_x, h, z+1, wall_type)  
        result_string += '''<DrawBlock x="{}" y="{}" z="{}" type="{}" />'''.format(end_x-1, h, z+1, wall_type)  

    # BUILD THE BARRIER
    if(barrier == True):
      for x in range(start_x, end_x):
        # LOWER BARRIER
        result_string += '''<DrawBlock x="{}" y="{}" z="{}" type="{}" />'''.format(x, 227, start_z+5, barrier_type)  

        # UPPER BARRIER
        for h in range(227+2, 227+height-1):
          result_string += '''<DrawBlock x="{}" y="{}" z="{}" type="{}" />'''.format(x, h, start_z+5,barrier_type)  
  
    return result_string


def getCorner(index,top,left,expand=0,y=0):
    ''' Return part of the XML string that defines the requested corner'''
    x = str(-(expand+old_div(ARENA_WIDTH,2))) if left else str(expand+old_div(ARENA_WIDTH,2))
    z = str(-(expand+old_div(ARENA_BREADTH,2))) if top else str(expand+old_div(ARENA_BREADTH,2))
    return 'x'+index+'="'+x+'" y'+index+'="' +str(y)+'" z'+index+'="'+z+'"'


################################################################
#################### END USER DEFINED FUNCTIONS ################
################################################################

missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
            <ServerSection>
              <ServerInitialConditions>
                <Time>
                    <StartTime>1000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <AllowSpawning>true</AllowSpawning>
                <Weather>clear</Weather>
              </ServerInitialConditions>
              <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" forceReset="1"/>
                <DrawingDecorator>
                   ''' + make_enclosure(0,0,20,20,12, barrier = True) + ''' 
                   ''' + spawn_multiple_enemies([["Villager", 2], ["Zombie", 2], ["Enderman", 2], ["Creeper", 0]]) + ''' 
                </DrawingDecorator>
                <ServerQuitFromTimeUp timeLimitMs="''' + game_time(GAME_SECONDS) + '''"/>
                <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>ourAgent</Name>
                <AgentStart>
                    <Placement x="4" y="227" z="4" pitch="0" yaw="-40"/>
                    <Inventory>
                        <InventoryItem slot="1" type="diamond_sword"/>
                        <InventoryItem slot="0" type="bow"/>
                        <InventoryItem slot="2" type="arrow" quantity="64"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromHotBar/>
                  <ObservationFromFullStats/>
                  <ObservationFromRay/>
                  <ObservationFromFullInventory/>
                  <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="'''+str(ARENA_WIDTH)+'''" yrange="2" zrange="'''+str(ARENA_BREADTH)+'''" />
                  </ObservationFromNearbyEntities>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                  <InventoryCommands/>
                  <AgentQuitFromTouchingBlockType>
                      <Block type="diamond_block" />
                  </AgentQuitFromTouchingBlockType>
                  <RewardForDamagingEntity>
                    <Mob type="Villager" reward="-10"/>
                    <Mob type="Enderman" reward="1"/>
                    <Mob type="Zombie" reward="10"/>
                  </RewardForDamagingEntity>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''


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
    agent_brain = agent_file.TabQAgent(actions = ["bow_swipe", "arrow_shot", "change_target"])
    for repeat in range(NUMBER_OF_REPS):
      villager_view_count = 0
      enderman_view_count = 0
      zombie_view_count  = 0
      my_mission = MalmoPython.MissionSpec(missionXML, True)
      my_mission_record = MalmoPython.MissionRecordSpec()

      # Attempt to start a mission:
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
      prev_ob = None

      while world_state.is_mission_running:
          time.sleep(0.1)
          world_state = agent_host.getWorldState()
          for error in world_state.errors:
              print("Error:",error.text)
          if world_state.number_of_observations_since_last_state > 0:
              msg = world_state.observations[-1].text    
              # ob is the data from the changing world
              # prev_ob is the word data from the previous loop 
              ob = json.loads(msg) 

              current_yaw, self_x, self_z = get_agent_position(ob)
              if target == None:
                target = entity_functions.switch_to_random_entity(ob)



              ##### used to switch something every n number of seconds #########
              ##### an alternate to sleep when you don't want to freeze the agent's actions 
              # t = Timer(1)
              # while(True):
              #     if(t.time_elapsed() == True):
              current_s = (number_enemies(ob), entity_functions.entity_in_sight(ob))
              current_a = agent_brain.choose_action(current_s, current_r)
              current_r = give_reward(current_s, current_a)
              extra = [ob, target, current_yaw, self_x, self_z]
              target = take_action(current_a, extra)

              if target is None:
                break
              # print("the end")


              ####### FUNCTIONS TO BE USED BY THE RL CLASS #################
              # agent_dict = get_agent_dict(ob)
              # entity_dict = switch_to_random_entity(ob)

              # if(entity_dict != None):
              #   attack_entity_with_bow_swing(ob, entity_dict, current_yaw, self_x, self_z)
              #   # attack_entity_by_shooting_arrow(ob, entity_dict, current_yaw, self_x, self_z)
              #   # do_nothing()
              #   # entity_died(entity_dict)
              # else: 
              #   # this will be reached when there are no living entities left 
              #   # except for the agent 
              #   break

              
              # damage_report = entity_functions.get_entity_damage_report(ob, prev_ob)
              # if(len(damage_report) > 0): 
              #   print("\tdamage report = {}".format(damage_report))

              prev_ob = ob # KEEP THIS AT THE END OF THE WHILE LOOP !!!! 


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