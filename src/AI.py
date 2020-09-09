from itertools import combinations
from src.decisionTree import DecisionTree
from src.state import State
import math

class AI:

    def __init__(self):
        self._start_state = []
        self._state = []
        self._decision_tree = None
        self._possible_cards = []

    def load_possible_cards(self, possible_cards):
        self._possible_cards += possible_cards

    def decide_hand(self, game):

        #print(self.calculate_reward(self._start_state))

        self._decision_tree = DecisionTree()
        self._decision_tree.state = self.create_state(game.AI_cards, game.pile_cards)

        self.remove_cards(self._possible_cards, game.AI_cards)
        self.remove_cards(self._possible_cards, game.pile_cards)

        if game.sum_cards(game.AI_cards) < self.model_player_hand(game) and game.sum_cards(game.AI_cards) <= 7:
            print("AI calling vnf.....")
            return game.call_vnf()

       # game.remove_cards()
        self.create_moves(game.AI_cards, game.pile_cards, game)

    def remove_cards(self, curr_cards, sub_cards):
        for c in sub_cards:
            if c in curr_cards:
                curr_cards.remove(c)

    def create_state(self, hand_cards, pile_cards):
        return State(hand_cards, pile_cards)

    def fill_start_state(self, game):
        self._start_state.append(game.AI_cards)
        self._start_state.append(game.pile_cards)

    def calculate_reward(self, prev_state, state):
        sum = 0
        for card in state.hand_cards:
            sum += card.value

        prev_sum = 0
        for card in prev_state.hand_cards:
            prev_sum += card.value

        
        return prev_sum - sum

    def model_player_hand(self, game):
        player_len = game.len_player_cards()
        len_unknown = player_len - len(game.view_cards)

        sum_cards = 0
        if len(game.view_cards) != 0:
            sum_cards += game.sum_cards(game.view_cards)

        expected_value = game.sum_cards(self._possible_cards) / len(self._possible_cards)
        variance = game.sum_square(self._possible_cards) / len(self._possible_cards) - expected_value * expected_value
        
        sum_cards += expected_value * len_unknown
        variance = variance * len_unknown


        return sum_cards - math.sqrt(variance)



    def calculate_deck_node(self, hand_cards, game, pile_cards, tree_node, end_game):
       # print("")
        expected_values = []

      
        state = None

        for card in self._possible_cards:
            probability = 1 / len(self._possible_cards)
            hand_cards.append(card)
            reward = -100
            
          #  print(str(card.name)+ ": ", end = "") 
            if not end_game:
                for i in range(len(hand_cards)):
                    for combo in combinations(hand_cards, i+1):
                        if not game.validate_cards(list(combo)):
                            continue
                        hand_cards_copy = hand_cards.copy()
                        self.remove_cards(hand_cards_copy,list(combo))

                        decision_node = DecisionTree()
                        decision_node.state = self.create_state(hand_cards_copy, pile_cards)
                        decision_node.reward = self.calculate_reward(tree_node.state, decision_node.state)

                        if decision_node.reward > reward:
                            state = decision_node.state.hand_cards
                            reward = decision_node.reward                     
            else:

                decision_node = DecisionTree()
                decision_node.state = self.create_state(hand_cards, pile_cards)
                decision_node.reward = self.calculate_reward(tree_node.state, decision_node.state)  
                reward = decision_node.reward

            #print(str(state) + ", " + str(reward)+ ", ", end = "")   
           
            expected_values.append(reward)
            hand_cards.remove(card)      

        #print(expected_values)
    #    print("---------------------------------")
        node = DecisionTree()
        node.state = self.create_state([], [])
        node.reward = sum(expected_values) / len(expected_values)
        node.state.pick_up = "deck"
        
        tree_node.children.append(node)


        return sum(expected_values) / len(expected_values)
            




    def create_moves(self, hand_cards, pile_cards, game):

       # print(hand_cards)
       # print(game.view_cards)
       
        min = 100
        best_state = None
        list_combo = None
        pick_up = None
        hand = None
        end_game = False
        # if game.sum_cards(hand_cards) <= 5 or len(hand_cards) <= 1:
        #     end_game = True

        max_sum = 0
        for i in range(len(hand_cards)):
            for combo in combinations(hand_cards, i+1):
                
                if not game.validate_cards(list(combo)):
                   continue

                hand_sum = game.sum_cards(list(combo))
                if hand_sum > max_sum:
                    max_sum = hand_sum
                    
                

        if game.sum_cards(hand_cards) - max_sum <= 2:
            end_game = True

        for i in range(len(hand_cards)):
            for combo in combinations(hand_cards, i+1):
                
                if not game.validate_cards(list(combo)):
                   continue
                
                
                hand_cards_copy = hand_cards.copy()

                game.remove_cards(hand_cards_copy, list(combo))
                decision_node = DecisionTree()
                decision_node.state = self.create_state(hand_cards_copy, pile_cards)
                decision_node.reward = self.calculate_reward(self._decision_tree.state, decision_node.state)
                decision_node.state.put_down = list(combo)

                self._decision_tree.children.append(decision_node)

               
                for card in pile_cards:
                
                    if card.value == 0:
                        continue

                    hand_cards_cop = hand_cards_copy.copy()
                    pile_cards_copy = pile_cards.copy()
                    pile_cards_copy.remove(card)
                    hand_cards_cop.append(card)


                    state = self.create_state(list(hand_cards_cop), list(pile_cards_copy))
                    #state.pick_up += card
                    decision_child = DecisionTree()
                    decision_child.state = state
                    decision_child.state.pick_up = card
                    decision_child.reward = self.calculate_reward(decision_node.state, decision_child.state)
                    decision_node.children.append(decision_child)
                    reward = game.sum_cards(state.hand_cards)

                    if not end_game:
                       # print("hello")
                        for i in range(len(hand_cards_cop)):
                            for combo_child in combinations(hand_cards_cop, i+1):
                                if not game.validate_cards(list(combo_child)):
                                    continue
                                hand_cards_copy_copy = hand_cards_cop.copy()

                                game.remove_cards(hand_cards_copy_copy, list(combo_child))
                                decision_node_child = DecisionTree()
                                decision_node_child.state = self.create_state(hand_cards_copy_copy, pile_cards)
                                decision_node_child.reward = self.calculate_reward(decision_child.state, decision_node_child.state)
                                decision_node_child.state.put_down = list(combo_child)
                                decision_child.children.append(decision_node_child)

                self.calculate_deck_node(hand_cards_copy.copy(), game, pile_cards, decision_node, end_game)

        #self._decision_tree.print()     
        self._decision_tree.get_max_reward_parent()
        put_down_cards = self._decision_tree.put_down
        self.remove_cards(hand_cards,put_down_cards)
        pick_up = self._decision_tree.pick_up

        if pick_up == "deck":
            hand_cards.append(game.pick_up_from_deck())
        else:
            hand_cards.append(pick_up)

        game.change_pile(put_down_cards)
       
        hand = hand_cards.copy()
        game.set_AI_cards(hand)



        print("AI Played: " + str(put_down_cards) + ", Picked up: " + str(pick_up)  + ", Currently has " + str(len(hand)) + " cards in hand")



            





