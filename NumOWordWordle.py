"""
Created By: Matthew Govia
This is a small python project that is wordle and user can set either number version or word version

"""

from csv import Dialect
import curses
import random
from sys import stderr
import pyautogui as py


NUM_DIGITS = -1  
MAX_GUESSES = 10
GAME_VERSION = ''
DIFFICULTY = ''

def oop():
    global GAME_VERSION


menu = ["Number", "Words"]
diff_choices = ["Easy", "Medium", "Hard"]
def main(stdscr): #
    #game loop
    stdscr.clear()
    stdscr.refresh()
    while True:
        gameMode = ''
        gameDiff = ''
        global GAME_VERSION
        global NUM_DIGITS
        global DIFFICULTY
        global MAX_GUESSES
        #GAME_VERSION = 'Number'
        #DIFFICULTY = 'Easy'
        NUM_DIGITS = 4
        #MAX_GUESSES = 10
        curses.curs_set(0)  # Hide the cursor
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        
        current_row = 0
        difficulty_row = 0
        

        #this while statement is to get the game version (numbers or words)
        print_menu(stdscr, current_row)
        while True:
            key = stdscr.getch()
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
                #print('up')
            elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
                current_row += 1
                #print('down')
            elif key == 10:  
                stdscr.clear()
                GAME_VERSION = menu[current_row]
                stdscr.refresh()
                break
            print_menu(stdscr, current_row)
        #now we will pick gamemode (easy, medium, hard)
        print_difficulty(stdscr, difficulty_row)
        while True:
            keyo = stdscr.getch()
            if(keyo == curses.KEY_UP and difficulty_row > 0):
                difficulty_row -= 1
            elif (keyo == curses.KEY_DOWN and difficulty_row < len(diff_choices) - 1):
                difficulty_row += 1
            elif (keyo == 10):
                stdscr.clear()
                DIFFICULTY = diff_choices[difficulty_row]
                stdscr.refresh()
                break
            print_difficulty(stdscr, difficulty_row)
        stdscr.clear()
        stdscr.refresh()
        stdscr.addstr("-------------------------------------------------------------------------------------------------------------\n")
        stdscr.addstr("Hello and Welcome to my version of Wordle that can either be with numbers or with actual words.\n")
        stdscr.addstr("\n")
        stdscr.addstr("Under each secret word will show words giving hints on how many you have correct\n")
        stdscr.addstr("\n")
        stdscr.addstr("opo: One index is the correct value & in the correct space\n")
        stdscr.addstr("iti: One index is the correct value & NOT in the correct space\n")
        stdscr.addstr("womp: Index is incorrect value and incorrect index")
        stdscr.addstr("\n")
        stdscr.addstr("\n")
        stdscr.addstr("For example, if the secret number was 248 and your guess was 843, the ")
        stdscr.addstr("hints would be womp opo iti.")
        stdscr.addstr("\n")
        stdscr.addstr("-------------------------------------------------------------------------------------------------------------")
        stdscr.addstr("(press any key to continue...)")
        stdscr.refresh()
        stdscr.getch()
        stdscr.clear()
        stdscr.addstr("")
        stdscr.addstr("You have selected to play '" + GAME_VERSION + "' with the difficulty as '" + DIFFICULTY + "'. ")
        stdscr.addstr("")
        stdscr.addstr("(press any key to continue...)")
        stdscr.refresh()
        stdscr.getch()
        

        #this is where I will decide of word or number 
        
        """
        EASY: 3-5 characters
        MEDIUM: 6-8 characters
        HARD: 9-12 characters
        """
  
        extra_Hard_Word = ''
        if(DIFFICULTY.lower() == 'easy'):
            NUM_DIGITS = random.randint(3,4)
            MAX_GUESSES = 10
        elif(DIFFICULTY.lower()  == 'medium'):
            NUM_DIGITS = random.randint(5,8)
            MAX_GUESSES = 15
        else:
            #NUM_DIGITS = random.randint(9,12)
            maxNum = 0
            weightNum = 0
            extra_Hard_Word = ", You're gonna need it"
            if(GAME_VERSION == 'Number'):
                maxNum = 12
                weightNum = 12
            else:
                maxNum = 24
                weightNum = 16
            possible_values = list(range(9, maxNum))
            #This section was to weigh more towards the lower numbers 
            #weights_distribution = [i for i in range(1, weightNum)]
            #weights_distribution = weights_distribution + [1] * (len(possible_values) - len(weights_distribution))
            #NUM_DIGITS = random.choices(possible_values, weights=weights_distribution)[0]
            NUM_DIGITS = random.randint(9,maxNum)
            MAX_GUESSES = random.randint(17,22)
        
        secretNum = getSecret()
        stdscr.clear()
        
        stdscr.addstr("\n")
        stdscr.addstr('I have thought up a secret code with length of (' + str(NUM_DIGITS) + ').')
        stdscr.addstr("\n")
        #stdscr.addstr('code is ' + str(secretNum))
        #stdscr.addstr("\n")
        stdscr.addstr("You have ("+ str(MAX_GUESSES)+") guesses to get it, Good Luck" + extra_Hard_Word + "!")
        stdscr.addstr("\n")
        stdscr.refresh()
        
        numOfGuessed = 1
        curses.curs_set(1)
        height, width = stdscr.getmaxyx()       #this is for the max height of the terminal and to check if putting a string would be too much for it
        while (numOfGuessed <= MAX_GUESSES):
            myGuess = ''
            #loop until answer is valid
            while len(myGuess) != NUM_DIGITS:
                myGuess = ''
                stdscr.addstr('Guess #'+str(numOfGuessed)+':')
                stdscr.refresh()
                stdscr.addstr('>')
                key=0
                current_y, _ = stdscr.getyx()    
                if(current_y +1 > height):
                    stdscr.clear()
                    stdscr.refresh()
                while True:  
                    key = stdscr.getch()

                    # Check if the key is a printable character
                    if 32 <= key <= 126:
                        myGuess += chr(key)
                        stdscr.addstr(chr(key))  # Display the entered character
                    elif key == curses.KEY_BACKSPACE or key == 8:  # Backspace key
                        if myGuess:
                            myGuess = myGuess[:-1]  # Remove the last character
                            y, x = stdscr.getyx()
                            stdscr.move(y, x - 1)
                            stdscr.addch(' ')  # Clear the last character on the screen
                            stdscr.move(y, x - 1)
                    elif key == 10:  # Enter key
                        if(current_y +1 > height):
                            stdscr.clear()
                            stdscr.refresh()
                        break    
                
                """if current_y + 1 < height:
                    stdscr.addstr(current_y + 1, current_x, newline)
                    pass
                else:
                    stdscr.clear()
                    stdscr.refresh()
                    stdscr.addstr("\n")"""
                
            clues = getClues(myGuess, secretNum)
            if(current_y +4 > height):
                stdscr.clear()
                stdscr.refresh()
            stdscr.addstr("\n")
            stdscr.addstr(clues)
            stdscr.refresh()
            numOfGuessed += 1

            if myGuess == secretNum:
                break  # They're correct, so break out of this loop.
            if numOfGuessed > MAX_GUESSES:
                stdscr.clear()
                stdscr.addstr('You ran out of guesses.')
                stdscr.addstr("\n")
                stdscr.addstr("The answer was '"+ secretNum + "'\n")
        # Ask player if they want to play again.
        stdscr.addstr('Do you want to play again? (yes or no): ')
        stdscr.refresh()
        userInp = ''
        key=0
        while key != 10:  # Enter key
            key = stdscr.getch()

            # Check if the key is a printable character
            if 32 <= key <= 126:
                userInp += chr(key)
                stdscr.addstr(chr(key))  # Display the entered character
            elif key == curses.KEY_BACKSPACE or key == 8:  
                if userInp:
                    userInp = userInp[:-2]  # Remove the last character
                    y, x = stdscr.getyx()
                    stdscr.move(y, x - 1)  
                    stdscr.addch(' ')  # Clear the last character on the screen
                    stdscr.move(y, x - 1)  
        if not userInp.startswith('y'):
            break
    stdscr.addstr('\nThank you for playing!')
    stdscr.refresh()
    stdscr.getch()

def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    stdscr.addstr('Please select a gamemode:')

    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()

def print_difficulty(stdscr, select_row):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    stdscr.addstr('Please select difficulty')

    for idx, row in enumerate(diff_choices):
        x = w //2-len(row) // 2
        y = h//2 -len(diff_choices) // 2 + idx
        if idx == select_row:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def getClues(myGuess, actualAns):
    """Returns string form opo, iti, womp"""
    if(myGuess == actualAns):
        return "\nCorrect! You Win!!\n"
    clues = []
    for i in range(len(myGuess)):
        if myGuess[i] == actualAns[i]:
            # correct dig in corrct place
            clues.append('opo')
        elif myGuess[i] in actualAns:
            # correct dig in wrong place
            clues.append('iti')
    if len(clues) == 0:
        return 'womp\n'
    else:
        clues.sort()    #this is so location of where it is doesnt give it away
        clues.append('\n')
        return ' '.join(clues)

def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

def getSecret():
    """Returns a string made up of NUM_DIGITS unique random digits."""
    secretNum = ''
    
    global GAME_VERSION
    global NUM_DIGITS
    
    if(GAME_VERSION == 'Number'):
        numbers = list('0123456789')  # Create a list of digits 0 to 9.
        random.shuffle(numbers)  # Shuffle them into random order.

        # Get the first NUM_DIGITS digits in the list for the secret number:
        
        for i in range(NUM_DIGITS):
            secretNum += str(numbers[i%9])
        return secretNum
    else:
        #else grab a random word from the wordList
        return getRandom_FromLength(load_words(), NUM_DIGITS)

def getRandom_FromLength(strings, length):
    # this list only has those of the length 
    valid_strings = [s for s in strings if len(s) == length]
    random_string = random.choice(valid_strings)

    return random_string

if __name__ == '__main__':
    curses.wrapper(main) 
    #main()
    

