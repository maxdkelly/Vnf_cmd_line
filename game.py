import json
import random
from src.card import Card
from src.AI import AI

class Game:

    def __init__(self):
        self._deck = []
        self._player_cards = []
        self._AI_cards = []
        self._pile_cards = []
        self._AI = AI()
        self.full_deck = []
        self.load_deck()
        self._view_cards = []
        self.animation_render = True
        
       
        
    @property
    def player_cards (self):
        return self._player_cards   

    @property
    def view_cards(self):
        return self._view_cards

    @property
    def AI_cards(self):
        return self._AI_cards

    @property
    def pile_cards(self):
        return self._pile_cards

    def len_player_cards(self):
        return len(self._player_cards)

    def set_AI_cards(self, a): 
         self._AI_cards.clear()
         self._AI_cards += a

    def load_deck(self):
        with open('src/cards.json','r') as json_file:
            data = json.load(json_file)
            for card_json in data['cards']:
                card = Card(card_json['name'],card_json['colour'],card_json['value'])
                self._deck.append(card)
        self._AI.load_possible_cards(self._deck)

        self.full_deck += self._deck

    def deal_player(self):

        
       # self._player_cards.append(self.return_card(self._deck,"King [hearts]"))
        for i in range(7):
            card = self._deck.pop(int(random.random() * len(self._deck)))
            self._player_cards.append(card)
  

    def deal_AI(self):
   
        # self._AI_cards.append(self.return_card(self._deck,"Jack [hearts]"))
        # self._AI_cards.append(self.return_card(self._deck,"Jack [diamonds]"))
        # self._AI_cards.append(self.return_card(self._deck,"Jack [spades]"))
        for i in range(7):
            card = self._deck.pop(int(random.random() * len(self._deck)))
            self._AI_cards.append(card)


    def check_card(self, name, curr_cards):
        for c in curr_cards:
            if c.name == name:
                return c

        return None

    def get_hand(self, hand_names):
        cards = []
        for name in hand_names:
            for c in self.full_deck:
                if c.name == str(name):
                    cards.append(c)


       # cards.append(self.full_deck[0])   
        return cards

    def check_duplicates_colour(self,curr_cards):


        for c in curr_cards:
            for c1 in curr_cards:
                if c1.value == c.value and c.name != c1.name and c.value != 0:
                    return True
                if c1.colour != c.colour and c.value != 0 and c1.value != 0:
                    return True
    
        return False

    def get_player_card_names(self):
        card_string = []

        for c in self._player_cards:
            card_string.append(c.name)
        return card_string

    def get_pile_card_names(self):
        card_string = []

        for c in self._pile_cards:
            card_string.append(c.name)
        return card_string


    def get_max(self, curr_cards):

        max_val = 0
        for c in curr_cards:
            if c.value > max_val:
                max_val = c.value
        return max_val

    def get_min(self, curr_cards):

        min_val = 13
        for c in curr_cards:
            if c.value < min_val and c.value != 0:
                min_val = c.value
        return min_val

    def change_min(self, curr_cards):

        min_val = 13
        val = None
        for c in curr_cards:
            if c.value < min_val and c.value != 0:
                val = c
                min_val = c.value

        if val != None:
            val.value = val.value + 13
        return min_val

    def check_wrapping(self, curr_cards, max):


        while self.change_min(curr_cards) != max:
            min_val = self.get_min(curr_cards)
            max_val =self. get_max(curr_cards)

            if max_val - min_val == len(curr_cards)  - 1:
                return True   

        return False

    def pick_up_from_deck(self):
        return self._deck.pop(int(random.random() * len(self._deck)))

    def validate_cards(self, curr_cards):

        if len(curr_cards) == 0:
            return False
        if len(curr_cards) == 1:
            return True
        value = -1
        for c in curr_cards:
            if value == -1:
                value = c.value
            else:
                if value != c.value:
                    value = -10

        if value != - 10:
            return True

        if self.check_duplicates_colour(curr_cards):
            return False
    
        min_val = self.get_min(curr_cards)
        max_val = self.get_max(curr_cards)

        if max_val - min_val == len(curr_cards)  - 1:
            return True

   
        #if self.check_wrapping(curr_cards.copy(), max_val):
         #   return True

        return False

    def remove_cards(self, curr_cards, sub_cards):
        for c in sub_cards:
            if c in curr_cards:
                curr_cards.remove(c)

    def print_cards(self, curr_cards):

        if curr_cards == None:
            return 

        i = 0
        for card in curr_cards:
            print(card.name, end = '')
            if i != len(curr_cards) - 1:
                print(", ", end = '')
            else:
                print()
            i += 1  

    def return_card(self, curr_cards, card_name):

        card = None
        for c in curr_cards:
            if c.name == card_name:
                card = c
    
        if card != None:
            curr_cards.remove(card)

        return card

    def return_AI_score(self):
        return self.sum_cards(self._AI_cards)

    def return_player_score(self):
        return self.sum_cards(self._player_cards)

    def get_AI_len(self):
        return len(self._AI_cards)

    def call_vnf(self):
        ret = None
        if self.sum_cards(self._player_cards) > self.sum_cards(self._AI_cards):
            print("you lose")
            ret = True
            
            
        else:
            print('you win')
            ret = False
        
        
        print("You had: " + str(self.sum_cards(self._player_cards)) + ", AI had: " + str(self.sum_cards(self._AI_cards))) 
        return ret

    def pick_up(self):
        print("Pick up options: [deck], ", end = "")
        self.print_cards(self._pile_cards)
        while True:
            user_input = input("Pick card: ")
            if user_input == 'deck':
                print("Picking up from deck...", end = "")
                card = self._deck.pop(int(random.random() * len(self._deck)))
                print("...." + card.name)
                self._player_cards.append(card)
                return
            c = self.check_card(user_input, self._pile_cards)
            if c == None:
                print("Not a valid pick up option")
            elif c.value == 0:
                print("Cannot pick up a Joker")
                continue
            else:
                print("Picking up " + c.name)
                self._view_cards.append(c)
                self._pile_cards.remove(c)
                self._player_cards.append(c)
                return


    def sum_cards(self, curr_cards):
        sum = 0
        for c in curr_cards:
            sum += c.value

        return sum

    def sum_square(self, curr_cards):
        sum = 0
        for c in curr_cards:
            sum += c.value * c.value

        return sum

    def change_pile(self, hand_cards):
        self._pile_cards.clear()
        self._pile_cards += hand_cards

        self._pile_cards.sort(key=lambda x: x.value)

    def play_hand_frontend(self, hand_cards, pile_card_name):
        self.remove_cards(self._view_cards, hand_cards)
        self.remove_cards(self._player_cards, hand_cards)

        if pile_card_name == 'deck_card':
               
            card = self._deck.pop(int(random.random() * len(self._deck)))
            self._player_cards.append(card)

        else:
            c = self.check_card(pile_card_name, self._pile_cards)
            self._player_cards.append(c)
        
        self.change_pile(hand_cards)






    def play_hand(self):

        print("Player cards: ", end = "")
        self.print_cards(self._player_cards)

        hand_cards = []

        card_name = None
        valid_hand = False

        while not valid_hand:
            while True:
                card_name = input("Choose cards to play (enter 'finish' to continue or 'vnf' to call vnf): ")
                if card_name == "finish":
                    break

                if card_name == "vnf":
                    if self.sum_cards(self._player_cards) > 7:
                        print("Too high a hand to call [need 7 or less]")
                        continue
                    else:
                        return self.call_vnf()


                c = self.check_card(card_name, self._player_cards)
                if c == None:
                    print("Not a valid card from your deck")
                else:
                    hand_cards.append(c)


            if self.validate_cards(hand_cards):
                valid_hand = True
                print("Hand accepted")
            else:
                print("Invalid hand")
                hand_cards.clear()

        self.remove_cards(self._view_cards, hand_cards)
        self.remove_cards(self._player_cards, hand_cards)

        self.pick_up()

        self.change_pile(hand_cards)

       

      

    def play_AI_hand(self):

        return self._AI.decide_hand(self)

      
        
        
    
