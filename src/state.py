
class State:
    def __init__(self, hand_cards, pile_cards):
        self.hand_cards = hand_cards
        self.pile_cards = pile_cards
        self.put_down = None
        self.pick_up = None

    

    def print(self):
        print("put down: " + str(self.put_down) + ", pick up: " + str(self.pick_up), end = "")
       # print("hand: " + str(self.hand_cards) + ", pile: " + str(self.pile_cards), end = "")