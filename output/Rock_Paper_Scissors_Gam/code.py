import random

def ai_choice():
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def get_user_input():
    while True:
        user_input = input("Enter 'rock', 'paper' or 'scissors': ").lower()
        if user_input in ['rock', 'paper', 'scissors']:
            return user_input
        else:
            print("Invalid input. Please try again.")
    
def game_result(user, ai):
    if user == ai:
        return "It's a tie!"
    elif (user == 'rock' and ai == 'scissors') or (user == 'scissors' and ai == 'paper') or (user == 'paper' and ai == 'rock'):
        return 'You win!'
    else:
        return 'You lose!'

if __name__ == "__main__":
    print("Rock-Paper-Scissors Game")
    
    user_input = get_user_input()
    ai_input = ai_choice()
    print(f'You chose: {user_input}, AI chose: {ai_input}')
    result = game_result(user_input, ai_input)
    print(result)