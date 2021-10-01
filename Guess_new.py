import random
import os
clear = lambda: os.system('cls')



#Create game 

class GuessNumber():
    
    def __init__(self,player_name):
        
        self.player_name = player_name
        self.level = int(input(f"""Hello {self.player_name}. Here is a guessing game. Choose the level you would like to play. \n
         Key in the digit level:\n
                               '1' - Easy | Choose one number between 1 - 5\n
                               '2' - Medium | Choose two numbers between 1 - 5\n"""))
        self.first_number = random.choice(range(6))
        self.second_number = random.choice(range(6))
        self.attempts = 0

    def first_level(self):
   
        print("Ok. Pick up the number bwtween 1 - 5?")

        while True:
            player_guess = int(input("What is your guess: "))
            self.attempts += 1

            if player_guess == self.first_number:
                print(f"YOU WON in {self.attempts} attepmts. Your guesse was {player_guess} and PC guess was {self.first_number}\n")
                break
            else:
                if player_guess > self.first_number:
                    
                    print(f"Too high. You had {self.attempts} attempts. Keep trying...\n")
                else:
                    print(f"Too low. You had {self.attempts} attempts. Keep trying...\n")
    
                        
    def second_level(self):
        
        print("Ok. Pick up the number bwtween 1 - 5?")

        while True:
            
            first_player_guess = int(input("What is your first guess: "))
            self.attempts += 1
            
            if first_player_guess == self.first_number and first_player_guess is not str:
                print(f"Your FIRST guesse is CORRECT!!!: {first_player_guess}")
                break
            else:
                if first_player_guess > self.first_number:
                    
                    print(f"Too high. You had {self.attempts} attempts. Keep trying...")
                else:
                    print(f"Too low. You had {self.attempts} attempts. Keep trying...")

        print("Wrong Number")
              
        while True:

            second_player_guess = int(input("What is your second guess: "))
            self.attempts += 1

            if second_player_guess == self.second_number:
                    
                print(f"YOU WON!!!!. Your SECOND guesse is CORRECT!!! {second_player_guess}.\n You  did it in {self.attempts} attempts!\n")
                break
            else:
                if second_player_guess > self.second_number:
                    
                    print(f"Too high. You had {self.attempts} attempts. Keep trying...")
                else:
                    print(f"Too low. You had {self.attempts} attempts. Keep trying...")                
            
            
            
        
        

    


name = input("What is you name?")
while True:

    game = GuessNumber(name)
    if game.level == 1:
        game.first_level()
        play_on = input("Do you want to play again? Y or N: ")
        if play_on.upper() == "N" or play_on.upper() == '':
                break
    elif game.level == 2:
        game.second_level()
        play_on = input("Do you want to play again? Y or N: ")
        if play_on.upper() == "N" or play_on.upper() == ''::
            break
   
        

