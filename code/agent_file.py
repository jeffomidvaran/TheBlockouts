import random

class TabQAgent(object):
    """Tabular Q-learning agent for discrete state/action spaces."""

    def __init__(self, actions=[], epsilon=0.1, alpha=0.1, gamma=1.0):
        #initializing all relevant variables for q learning
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

        self.actions = actions
        self.q_table = {}

        self.prev_s = None
        self.prev_a = None

        self.total_reward = 0


    def choose_action(self, current_s, current_r):
        "Q Learning implementation for our Agent"

        #Records total reward earned in the game
        self.total_reward += current_r

        #add state/action to q_table if not already inside
        if current_s not in self.q_table:
            self.q_table[current_s] = {}
            for action in self.actions:
                self.q_table[current_s][action] = 0


        # update Q values with our update function using our alpha and gamma 
        max_value = 0
        for action in self.q_table[current_s]:
            if self.q_table[current_s][action] > max_value:
                max_value = self.q_table[current_s][action]

        if self.prev_s and self.prev_a:
            old_q = self.q_table[self.prev_s][self.prev_a]
            self.q_table[self.prev_s][self.prev_a] = old_q + self.alpha * (current_r
                + self.gamma * max_value - old_q)

        #choose either a random action with some probability (epsilon) or any move with the highest q value
        a = 0
        rnd = random.random()
        if rnd < self.epsilon:
            a = self.actions[random.randint(0, len(self.actions) - 1)]
        else:
            max_value = -1 * float("inf")
            for action in self.q_table[current_s]:
                if self.q_table[current_s][action] > max_value:
                    max_value = self.q_table[current_s][action]

            best_actions = []
            for action in self.actions:
                if self.q_table[current_s][action] == max_value:
                    best_actions.append(action)

            a = best_actions[random.randint(0, len(best_actions) - 1)]


        self.prev_s = current_s
        self.prev_a = a

        return a






