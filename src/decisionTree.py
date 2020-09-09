class DecisionTree:
    def __init__(self):
        self.children  = []
        self.state = None
        self.reward = None
        self.max_child = None

        self.put_down = None
        self.pick_up = None

    def print(self):
        self.print_tree("--")
        # self.state.print()
        # print(", reward: " + str(self.reward))
        # print(" -- ", end = "")


        # for i in self.children:
        #     i.print()
            
    def print_tree(self, string):
        print(string, end = "")
        self.state.print()
        print(", reward: " + str(self.reward))
       

        string += "--"

        for i in self.children:
            i.print_tree(string)

    def get_max_reward_parent(self):
        if len(self.children) == 0:
            return self.reward

        max_reward = -100
        node = None
        for c in self.children:
            
            reward = c.get_max_reward()
           
            if reward > max_reward:
                max_reward = reward
                node = c

    #        print("reward: " + str(max_reward) + " put down: " + str(c.state.put_down))

        
        self.put_down = node.state.put_down
       # print(max_reward)
        self.pick_up = node.max_child.state.pick_up

    def get_max_reward(self):
        if len(self.children) == 0:
            return self.reward

        node = None
        max_reward = -100
        for c in self.children:
            reward = c.get_max_reward()
            if reward > max_reward:
                max_reward = reward
                node = c
        
        self.max_child = node
        return max_reward + self.reward
