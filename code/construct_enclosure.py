from __future__ import print_function
from builtins import range
from past.utils import old_div
import MalmoPython
import os
import sys
import time
import json
import random
import errno
import math
import malmoutils


if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

###################### USER ADDED FUNCTIONS ####################
def move(speed):
  if(speed > 1 or speed < -1):
    raise ValueError("Invalid speed entered")
  agent_host.sendCommand("move " + str(speed))


def attack():
  agent_host.sendCommand("attack 1")


def shoot_arrow(cock_time=1):
  agent_host.sendCommand("use 1")
  time.sleep(cock_time)
  agent_host.sendCommand("use 0")
  
def place_block():
  agent_host.sendCommand("hotbar.3 1")


def spawn_enemies(*args):
    result_string = ""
    for enemy in args:
        entity = """
        <DrawEntity
        x="{}" 
        y="{}"
        z="{}"
        type="{}"
        yaw="{}"
        pitch="{}"
        xVel="{}"
        yVel="{}"
        zVel="{}"/>
        """.format(enemy[0],enemy[1],enemy[2],enemy[3],enemy[4],enemy[5],
            enemy[6],enemy[7],enemy[8])
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

# Task parameters:
malmoutils.fix_print()

agent_host = MalmoPython.AgentHost()
malmoutils.parse_command_line(agent_host)
recordingsDirectory = malmoutils.get_recordings_directory(agent_host)
video_requirements = '<VideoProducer><Width>860</Width><Height>480</Height></VideoProducer>' if agent_host.receivedArgument("record_video") else ''

ARENA_WIDTH = 20
ARENA_BREADTH = 20

def getCorner(index,top,left,expand=0,y=0):
    ''' Return part of the XML string that defines the requested corner'''
    x = str(-(expand+old_div(ARENA_WIDTH,2))) if left else str(expand+old_div(ARENA_WIDTH,2))
    z = str(-(expand+old_div(ARENA_BREADTH,2))) if top else str(expand+old_div(ARENA_BREADTH,2))
    return 'x'+index+'="'+x+'" y'+index+'="' +str(y)+'" z'+index+'="'+z+'"'

def getSpawnEndTag(i):
    return ' type="mob_spawner" variant="' + ["Sheep", "Pig"][i % 2] + '"/>'

missionXML = '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>CS175 Project</Summary>
        </About>

        <ModSettings>
            <MsPerTick>50</MsPerTick>
        </ModSettings>
        <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>1000</StartTime>
                    <AllowPassageOfTime>true</AllowPassageOfTime>
                </Time>
                <AllowSpawning>true</AllowSpawning>
                <AllowedMobs>Pig Sheep</AllowedMobs>
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" forceReset="1"/>
                <DrawingDecorator>
                   ''' + make_enclosure(0,0,30,30,12) + ''' 
                   ''' + spawn_multiple_enemies([["Sheep", 1], ["Zombie", 4], ["Enderman", 4], ["Creeper", 0], ["Spider", 0]]) + '''
                </DrawingDecorator>
                <AnimationDecorator ticksPerUpdate="10">
                <Linear>
                    <CanvasBounds>
                        <min x="''' + str(old_div(-ARENA_BREADTH,2)) + '''" y="205" z="''' + str(old_div(-ARENA_BREADTH,2)) + '''"/>
                        <max x="''' + str(old_div(ARENA_WIDTH,2)) + '''" y="217" z="''' + str(old_div(ARENA_WIDTH,2)) + '''"/>
                    </CanvasBounds>
                    <InitialPos x="0" y="207" z="0"/>
                    <InitialVelocity x="0" y="0.025" z="0"/>
                </Linear>
                <DrawingDecorator>
                    <DrawLine ''' + getCorner("1",True,True,expand=-2) + " " + getCorner("2",True,False,expand=-2) + getSpawnEndTag(1) + '''
                    <DrawLine ''' + getCorner("1",True,True,expand=-2) + " " + getCorner("2",False,True,expand=-2) + getSpawnEndTag(1) + '''
                    <DrawLine ''' + getCorner("1",False,False,expand=-2) + " " + getCorner("2",True,False,expand=-2) + getSpawnEndTag(1) + '''
                    <DrawLine ''' + getCorner("1",False,False,expand=-2) + " " + getCorner("2",False,True,expand=-2) + getSpawnEndTag(1) + '''
                    <DrawLine ''' + getCorner("1",True,True,expand=-3) + " " + getCorner("2",True,False,expand=-3) + getSpawnEndTag(2) + '''
                    <DrawLine ''' + getCorner("1",True,True,expand=-3) + " " + getCorner("2",False,True,expand=-3) + getSpawnEndTag(2) + '''
                    <DrawLine ''' + getCorner("1",False,False,expand=-3) + " " + getCorner("2",True,False,expand=-3) + getSpawnEndTag(2) + '''
                    <DrawLine ''' + getCorner("1",False,False,expand=-3) + " " + getCorner("2",False,True,expand=-3) + getSpawnEndTag(2) + '''
                </DrawingDecorator>
                </AnimationDecorator>
               <ServerQuitWhenAnyAgentFinishes />
               <ServerQuitFromTimeUp timeLimitMs="110000"/>
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>The Hunter</Name>
            <AgentStart>
                <Placement x="4" y="227" z="4" pitch="20" yaw="-40"/>
                <Inventory>
                    <InventoryItem slot="0" type="diamond_pickaxe" />
                    <InventoryItem slot="1" type="bow" />
                    <InventoryItem slot="2" type="arrow" quantity="64" />
                    <InventoryItem slot="3" type="dirt" quantity="64" />
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <ContinuousMovementCommands turnSpeedDegs="420"/>
                <ObservationFromRay/>
                <RewardForDamagingEntity>
                    <Mob type="Sheep" reward="1"/>
                    <Mob type="Enderman" reward="1"/>
                    <Mob type="Pig" reward="-1"/>
                    <Mob type="Zombie" reward="1"/>
                </RewardForDamagingEntity>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="'''+str(ARENA_WIDTH)+'''" yrange="2" zrange="'''+str(ARENA_BREADTH)+'''" />
                </ObservationFromNearbyEntities>
                <ObservationFromFullStats/>''' + video_requirements + '''
            </AgentHandlers>
        </AgentSection>

    </Mission>'''
    

# mission loop will start here
agent_host = MalmoPython.AgentHost()
my_mission = MalmoPython.MissionSpec(missionXML, True)

# Set up recording
my_mission_record = MalmoPython.MissionRecordSpec()

try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

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


############ Loop while mission is starting: ############
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    time.sleep(0.1)
    world_state = agent_host.getWorldState()

total_reward = 0
sheep_population = 0
zombie_population = 0
self_x = 0
self_z = 0
current_yaw = 0

###################################################### 
###################################################### 

# Loop until mission ends:
while world_state.is_mission_running:
    world_state = agent_host.getWorldState()
    if(world_state.number_of_observations_since_last_state > 0):
        msg = world_state.observations[-1].text
        ob = json.loads(msg)

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
            if type == "Enderman":
                agent_host.sendCommand("attack 1")
                agent_host.sendCommand("attack 0")
            if type == "Zombie":
                agent_host.sendCommand("attack 1")
                agent_host.sendCommand("attack 0")

        # Use the nearby-entities observation to decide which way to move
        # keep track of population sizes 
        if u'entities' in ob:
            entities = ob["entities"]
            num_sheep = 0
            num_zombies = 0
            num_enderman = 0 
            x_pull = 0
            z_pull = 0
 
            for e in entities:
                if e["name"] == "Sheep":
                    num_sheep += 1
                elif e["name"] == "Zombie":
                    num_zombies += 1
                    # move toward the Zombie
                    dist = max(0.0001, (e["x"] - self_x) * (e["x"] - self_x) + (e["z"] - self_z) * (e["z"] - self_z))
                    weight = 21.0 - e["life"]
                    x_pull += weight * (e["x"] - self_x) / dist
                    z_pull += weight * (e["z"] - self_z) / dist
                elif e["name"] == "Enderman":
                    num_enderman = 0
                    dist = max(0.0001, (e["x"] - self_x) * (e["x"] - self_x) + (e["z"] - self_z) * (e["z"] - self_z))
                    weight = 41.0 - e["life"]
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

# mission loop will end here
for error in world_state.errors:
    print("Error:",error.text)

print()
print("Mission ended")
# Mission has ended.







