import random

def switch_to_random_entity(ob):
    entities = ob["entities"]
    living_entities_list = []
    for e in entities:
      if "life" in e and e["life"] > 0: 
        living_entities_list.append(e)
    num_of_entities = len(living_entities_list) 
    if(num_of_entities > 1):
        random_index = random.randrange(1,num_of_entities)
        return living_entities_list[random_index]
    else:
      return None


def entity_in_sight(ob):
    "returns the the entity(or block) in the agent's line of sight"
    return ob["LineOfSight"]["type"]


def entity_died(entity_dict):
    if(entity_dict["life"] == 0):
      return True
    else: 
      return False

###################################################
############### NEWLY ADDED FUNCTIONS ############# 
###################################################

def get_entity_type(entity_id, ob):
    for entity in ob['entities']:
        if(entity['id'] == entity_id):
            return entity['name']
    return None 


def get_distance_from_entity_in_line_of_site(ob):
  return ob['LineOfSight']['distance'] 


def entity_within_swipe_range(ob):
  # sword/bow swipe range = 3
  if(ob['LineOfSight']['type'] == "Zombie" or
    ob['LineOfSight']['type'] == "Villager" or
    ob['LineOfSight']['type'] == "Enderman" or
    ob['LineOfSight']['type'] == "Creeper"):

    if(ob['LineOfSight']['distance'] <= 3.05):
      return True
  return False


def filter_entities(entity_dict):
    result = list()
    for e in entity_dict:
        if(e['name'] == 'Zombie' or 
           e['name'] == 'Villager' or 
           e['name'] == 'Enderman' or 
           e['name'] == 'Creeper'):
            result.append(e)
    return result


def get_entity_damage_report(ob, prev_ob):
    ''' 
        returns empty dict if no damage is done otherwise 
        damage_report = dict{agent_id: damage_taken}
    '''
    damage_report = dict()

    if (prev_ob == None):
        return damage_report

    current_entities = filter_entities(ob['entities'])
    prev_entities = filter_entities(prev_ob['entities'])

    if(len(current_entities) == len(prev_entities)): # O(n) 
        for i in range(0, len(current_entities)):
            if(current_entities[i]['life'] != prev_entities[i]['life']):
                changed = prev_entities[i]['life'] - current_entities[i]['life'] 
                damage_report[current_entities[i]['id']] = changed

    else: # O(n^2) handles case where lists are uneven (entity dies)
        for ce in current_entities:
            for pe in prev_entities:
                if(ce["id"] == pe["id"]) and ce['life'] != pe['life']:
                    changed = pe['life'] - ce['life'] 
                    damage_report[ce['id']] = changed

    return damage_report


