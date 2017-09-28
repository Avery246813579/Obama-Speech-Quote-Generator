class Hangman:


    pass

def ask_play_again():
    play_again = input("Do you want to play again? (Y/n)").upper()
    if play_again == "Y":
        return True
    elif play_again == "N":
        return False
    else:
        print("I don't understand the input: " + play_again)
        ask_play_again()


while True:
    if not ask_play_again():
        break
