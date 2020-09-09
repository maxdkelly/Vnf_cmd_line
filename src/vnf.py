import json
import random
from card import Card



cards = []
player_cards = []
AI_cards = []

def check_card(name, curr_cards):
    for c in curr_cards:
        if c.name == name:
            return c

    return None


def check_duplicates(curr_cards):

    for c in curr_cards:
        for c1 in curr_cards:
            if c1.value == c.value and c.name != c1.name:
                return True
    
    return False

def get_max(curr_cards):

    max_val = 0
    for c in curr_cards:
        if c.value > max_val:
            max_val = c.value
    return max_val

def get_min(curr_cards):

    min_val = 13
    for c in curr_cards:
        if c.value < min_val and c.value != 0:
            min_val = c.value
    return min_val

def change_min(curr_cards):

    min_val = 13
    val = None
    for c in curr_cards:
        if c.value < min_val and c.value != 0:
            val = c
            min_val = c.value

    if val != None:
        val.value = val.value + 13
    return min_val

def check_wrapping(curr_cards, max):


    while change_min(curr_cards) != max:
        min_val = get_min(curr_cards)
        max_val = get_max(curr_cards)

        if max_val - min_val == len(curr_cards)  - 1:
            return True   

    return False



def validate_cards(curr_cards):

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

    if check_duplicates(curr_cards):
        return False
    
    min_val = get_min(curr_cards)
    max_val = get_max(curr_cards)

    if max_val - min_val == len(curr_cards)  - 1:
        return True

   
    if check_wrapping(curr_cards.copy(), max_val):
        return True

    return False

def remove_cards(curr_cards, sub_cards):
    for c in sub_cards:
        curr_cards.remove(c)

def print_cards(curr_cards):

    if curr_cards == None:
        return 

    i = 0
    for card in curr_cards:
        print(card.name, end = '')
        if i != len(curr_cards) - 1:
            print(", ", end = '')
        else:
            print()
        i = i+1   

def return_card(curr_cards, card_name):
    for c in curr_cards:
        if c.name == card_name:
            return c
    
    return None

def pick_up(curr_cards,player_cards,deck):
    print("Pick up options: [deck], ", end = "")
    print_cards(curr_cards)
    while True:
        user_input = input()
        if user_input == 'deck':
            print("Picking up from deck...")
            card = deck.pop(int(random.random() * len(deck)))
            player_cards.append(card)
            return
        c = check_card(card_name, curr_cards)
        if c == None:
            print("Not a valid pick up option")
        else:
            print("Picking up " + card_name)
            curr_cards.remove(c)
            player_cards.append(c)
            return



with open('cards.json','r') as json_file:
    data = json.load(json_file)
    for card_json in data['cards']:
        card = Card(card_json['name'],card_json['colour'],card_json['value'])
        cards.append(card)

print("Player cards: ", end = '')       
for i in range(7):
    card = cards.pop(int(random.random() * len(cards)))
    player_cards.append(card)

print_cards(player_cards)

for i in range(7):
    card = cards.pop(int(random.random() * len(cards)))
    AI_cards.append(card)
   

while True:
    hand_cards = []

    card_name = None
    valid_hand = False

    while not valid_hand:
        while True:
            card_name = input("Choose cards to play (enter 'finish' to continue): ")
            if card_name == "finish":
                break

            c = check_card(card_name, player_cards)
            if c == None:
                print("Not a valid card from your deck")
            else:
                hand_cards.append(c)


        if validate_cards(hand_cards):
            valid_hand = True
            print("Hand accepted")
        else:
            print("Invalid hand")

    remove_cards(player_cards, hand_cards)
    pick_up(None,player_cards,cards)
    print("Player cards: ", end = "")
    print_cards(player_cards)





