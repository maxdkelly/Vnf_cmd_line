from game import Game
import time



while True:
    game_length = input("Game lenghth(In points): ")
    if not game_length.isdigit():
        print("Not a digit")
        continue
    game_length = int(game_length)
    if game_length <= 0:
        print("Length needs to be greater than zero")
        continue
    else:
        break

player_score = 0
AI_score = 0

      
while player_score < game_length and AI_score < game_length:

    game = Game()

    game.deal_player()
    game.deal_AI()
    while True:
        if game.play_hand() == False:
             break
        print("***************************************************************************************")
        if game.play_AI_hand() == False:
            break
        print("***************************************************************************************")
    
    player_score += game.return_player_score()
    AI_score += game.return_AI_score()
    print("Player total score: " + str(player_score))
    print("AI total score: " + str(AI_score))
    

time.sleep(10)