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

def game_time(seconds):
    return str(seconds * 1000)


def shoot_arrow(cock_time=1):
  agent_host.sendCommand("use 1")
  time.sleep(cock_time)
  agent_host.sendCommand("use 0")


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
      else:
        result_string +=  '''<DrawEntity x="10" y="227" z="10" type="{}" yaw="0" />'''.format(e[0])
  return result_string


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
                   ''' + make_enclosure(0,0,30,30,12) + ''' 
                   ''' + spawn_multiple_enemies([["Sheep", 0], ["Zombie", 1], ["Enderman", 1], ["Creeper", 0], ["Spider", 0]]) + '''
                </DrawingDecorator>
                <ServerQuitFromTimeUp timeLimitMs="''' + game_time(10) + '''"/>
                <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="4" y="227" z="4" pitch="0" yaw="-40"/>
                    <Inventory>
                        <InventoryItem slot="0" type="diamond_pickaxe"/>
                        <InventoryItem slot="1" type="bow"/>
                        <InventoryItem slot="2" type="arrow" quantity="64"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ObservationFromRay/>
                  <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="'''+str(ARENA_WIDTH)+'''" yrange="2" zrange="'''+str(ARENA_BREADTH)+'''" />
                  </ObservationFromNearbyEntities>
                  <ObservationFromGrid>
                      <Grid name="floor3x3">
                        <min x="-1" y="-1" z="-1"/>
                        <max x="1" y="-1" z="1"/>
                      </Grid>
                  </ObservationFromGrid>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                  <InventoryCommands/>
                  <AgentQuitFromTouchingBlockType>
                      <Block type="diamond_block" />
                  </AgentQuitFromTouchingBlockType>
                  <RewardForDamagingEntity>
                    <Mob type="Sheep" reward="1"/>
                    <Mob type="Enderman" reward="1"/>
                    <Mob type="Zombie" reward="1"/>
                  </RewardForDamagingEntity>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''


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

######################################################### 
############ loop while mission is starting: ############
######################################################### 
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)


# Loop until mission ends:
while world_state.is_mission_running:
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)
    if world_state.number_of_observations_since_last_state > 0: # Have any observations come in?
        msg = world_state.observations[-1].text                 # Yes, so get the text
        ob = json.loads(msg)                          # and parse the JSON
        # grid = ob.get(u'floor3x3', 0)                 # and get the grid we asked for


##########################################################
############ ADDED CODE FROM 1ST FILE ################### 
##########################################################
        # Get Avatar position/orientation:
        if u'Yaw' in ob:
            current_yaw = ob[u'Yaw']
        if u'XPos' in ob:
            self_x = ob[u'XPos']
        if u'ZPos' in ob:
            self_z = ob[u'ZPos']
        # Use the line-of-sight observation to determine when to hit and when not to hit:
        if u'LineOfSight' in ob:
            los = ob[u'LineOfSight']
            type=los["type"]
            if type == "Zombie":
                # when a zombie is in front of you release the arrow 
                agent_host.sendCommand("hotbar.2 1")
                agent_host.sendCommand("hotbar.2 0") 
                time.sleep(0.001)
                agent_host.sendCommand("use 1")
                agent_host.sendCommand("move 0")
                time.sleep(0.1)
                agent_host.sendCommand("use 0")
            if type == "Enderman":
                print("enderman seen")


        # Use the nearby-entities observation to decide which way to move
        if u'entities' in ob:
            entities = ob["entities"]
            num_zombies = 0
            num_enderman = 0 
            x_pull = 0
            z_pull = 0

            for e in entities:
                if e["name"] == "Zombie":
                    num_zombies += 1
                    # move toward the Zombie
                    dist = max(0.0001, (e["x"] - self_x) * (e["x"] - self_x) + (e["z"] - self_z) * (e["z"] - self_z))
                    weight = 21.0 - e["life"] #
                    x_pull += weight * (e["x"] - self_x) / dist
                    z_pull += weight * (e["z"] - self_z) / dist

        # Determine the direction we need to turn in order to head towards point with most zombies
            yaw = -180 * math.atan2(x_pull, z_pull) / math.pi
            difference = yaw - current_yaw;
            while difference < -180:
                difference += 360;
            while difference > 180:
                difference -= 360;
            difference /= 180.0;
            agent_host.sendCommand("turn " + str(difference))
            move_speed = 1.0 if abs(difference) < 0.5 else 0  # move slower when turning faster - helps with "orbiting" problem
            agent_host.sendCommand("move " + str(move_speed))


##########################################################
##########################################################
##########################################################


print()
print("Mission ended")
# Mission has ended.
