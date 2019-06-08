''' FUNCTIONS USED TO BUILD THE CUSTOM MINECRAFT WORLD ''' 


def game_time(seconds):
    return str(seconds * 1000)


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


def create_missionXML(num_villagers, num_zombies, num_enderman, num_creepers, game_length):
    result='''
      <?xml version="1.0" encoding="UTF-8" standalone="no" ?>
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
                   ''' + spawn_multiple_enemies([["Villager", num_villagers], ["Zombie", num_zombies], ["Enderman", num_enderman], ["Creeper", num_creepers]]) + ''' 
                </DrawingDecorator>
                <ServerQuitFromTimeUp timeLimitMs="''' + game_time(game_length) + '''"/>
                <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>ourAgent</Name>
                <AgentStart>
                    <Placement x="4" y="227" z="4" pitch="0" yaw="-40"/>
                    <Inventory>
                        <InventoryItem slot="0" type="bow"/>
                        <InventoryItem slot="1" type="diamond_sword"/>
                        <InventoryItem slot="2" type="arrow" quantity="64"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromHotBar/>
                  <ObservationFromFullStats/>
                  <ObservationFromRay/>
                  <ObservationFromFullInventory/>
                  <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="20" yrange="2" zrange="20" />
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
    return result













############# UNUSED ################# 
# def getCorner(index,top,left,expand=0,y=0):
#     ''' Return part of the XML string that defines the requested corner'''
#     x = str(-(expand+old_div(ARENA_WIDTH,2))) if left else str(expand+old_div(ARENA_WIDTH,2))
#     z = str(-(expand+old_div(ARENA_BREADTH,2))) if top else str(expand+old_div(ARENA_BREADTH,2))
#     return 'x'+index+'="'+x+'" y'+index+'="' +str(y)+'" z'+index+'="'+z+'"'


# def spawn_enemies(*args):
#     result_string = ""
#     for enemy in args:
#         entity = """ <DrawEntity x="{}" y="{}" z="{}" type="{}" yaw="{}" pitch="{}" xVel="{}" yVel="{}" zVel="{}"/>
#         """.format(enemy[0],enemy[1],enemy[2],enemy[3],enemy[4],enemy[5], enemy[6],enemy[7],enemy[8])
#         result_string += entity
#     return result_string
