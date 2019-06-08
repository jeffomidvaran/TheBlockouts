
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


def get_entity_damage_report(ob, prev_ob):
    ''' 
        returns empty dict if no damage is done 
        damage_report = dict{agent_id: damage_taken}
    '''
    damage_report = dict()

    if (prev_ob == None):
        return damage_report

    current_entities = ob['entities']
    prev_entities = prev_ob['entities']

    if(len(current_entities) == len(prev_entities)): # O(n) 
        for i in range(0, len(current_entities)):
            if('life' in current_entities[i] and 'life' in prev_entities[i] and current_entities[i]['life'] != prev_entities[i]['life']):
                changed = prev_entities[i]['life'] - current_entities[i]['life'] 
                damage_report[current_entities[i]['id']] = changed

    else: # O(n^2) handles case where an entity dies       
        for ce in current_entities:
            for pe in prev_entities:
                
                if('life' in ce and 'life' in pe and ce["id"] == pe["id"]) and ce['life'] != pe['life']:
                    changed = pe['life'] - ce['life'] 
                    damage_report[ce['id']] = changed

    return damage_report


