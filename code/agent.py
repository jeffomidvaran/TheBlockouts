class FighterAgent(object):
    def __init__(self, alpha=0.3, gamma=1, n=1):
        """Constructing an RL agent.

        Args
            alpha:  <float>  learning rate      (default = 0.3)
            gamma:  <float>  value decay rate   (default = 1)
            n:      <int>    number of back steps to update (default = 1)
        """
        self.epsilon = 0.2  # chance of taking a random action instead of the best
        self.q_table = {}
        self.n, self.alpha, self.gamma = n, alpha, gamma
        

    def get_possible_actions(self, agent_host, ob):
        """Returns all possible actions that can be done at the current state. """
        action_list = ["swingBow","shootArrow","randomTarget","nothing"]

        return action_list

    def get_curr_state(entities,ob):
        """Creates a unique identifier for a state.

        entities is a list of entities

        lineOfSight tells us what entity is currently seen
        
        ob is needed to see 


        """
        living_entities_list = []
        liveEnemies = 0

        for e in entities:
            if "life" in e:
                living_entities_list.append(e)

        for e in living_entities_list:
            if "Zombie" in e:
                liveEnemies +=1
            if "Enderman" in e:
                liveEnemies +=1

        los = ob[u'LineOfSight']
        seenEntity=los["type"]
        
        ret = (seenEntity, liveEnemies) 




        return ret


        #return submission.get_curr_state(self.inventory.items())

    def choose_action(self, curr_state, possible_actions, eps):
        """Chooses an action according to eps-greedy policy. """
        if curr_state not in self.q_table:
            self.q_table[curr_state] = {}
        for action in possible_actions:
            if action not in self.q_table[curr_state]:
                self.q_table[curr_state][action] = 0


        rnd = random.random()
        a = random.randint(0, len(possible_actions) - 1)
        
        if(rnd > eps):
            maxVal = max(q_table[curr_state].values())
            
            maxValActions = []
            for action,value in q_table[curr_state].items():
                if(value == maxVal):
                    maxValActions.append(action)

            return random.choice(maxValActions)


        return possible_actions[a]

    def update_q_table(self, tau, S, A, R, T):
        """Performs relevant updates for state tau.

        Args
            tau: <int>  state index to update
            S:   <dequqe>   states queue
            A:   <dequqe>   actions queue
            R:   <dequqe>   rewards queue
            T:   <int>      terminating state index
        """
        curr_s, curr_a, curr_r = S.popleft(), A.popleft(), R.popleft()
        G = sum([self.gamma ** i * R[i] for i in range(len(S))])
        if tau + self.n < T:
            G += self.gamma ** self.n * self.q_table[S[-1]][A[-1]]

        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)


    def best_policy(self, agent_host,entities):
        """Reconstructs the best action list according to the greedy policy. """
        self.clear_inventory()
        policy = []
        current_r = 0
        #is_first_action = True
        #next_a = ""
        while len(entities) != 0:
            curr_state = self.get_curr_state()
            possible_actions = self.get_possible_actions(agent_host, ob)
            next_a = self.choose_action(curr_state, possible_actions, 0)
            policy.append(next_a)
            #is_first_action = False
            current_r = self.act(agent_host, next_a)
        print(' with reward %.1f' % (current_r))
        return self.is_solution(current_r)
        #print 'Best policy so far is %s with reward %.1f' % (policy, current_r)


    def run(self, agent_host,entities):
        """Learns the process to compile the best gift for dad. """
        S, A, R = deque(), deque(), deque()
        #present_reward = 0
        done_update = False
        while not done_update:
            s0 = self.get_curr_state()
            possible_actions = self.get_possible_actions(agent_host, True)
            a0 = self.choose_action(s0, possible_actions, self.epsilon)
            S.append(s0)
            A.append(a0)
            R.append(0)

            T = sys.maxsize
            for t in range(sys.maxsize):
                time.sleep(0.1)
                if t < T:
                    current_r = self.act(agent_host, A[-1])
                    R.append(current_r)

                    if len(entities) == 0:
                        # Terminating state
                        T = t + 1
                        S.append('Term State')
                        present_reward = current_r
                        print("Reward:", present_reward)
                    else:
                        s = self.get_curr_state()
                        S.append(s)
                        possible_actions = self.get_possible_actions(agent_host)
                        next_a = self.choose_action(s, possible_actions, self.epsilon)
                        A.append(next_a)

                tau = t - self.n + 1
                if tau >= 0:
                    self.update_q_table(tau, S, A, R, T)

                if tau == T - 1:
                    while len(S) > 1:
                        tau = tau + 1
                        self.update_q_table(tau, S, A, R, T)
                    done_update = True
                    break