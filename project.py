import requests
import random
import html
import sys
import os
from tabulate import tabulate
from pyfiglet import Figlet

# Initialize figlet which is for the stylized titles
figlet = Figlet()

# Setfont for figlet. "slant" is the name of the font
figlet.setFont(font = "slant")

# Relative file path for correct placement and reading of leaderboard file
base_dir = os.path.dirname(os.path.abspath(__file__))
leaderboard_file = os.path.join(base_dir, "leaderboard.txt")


def main_menu():
    # Main menu options table
    game_modes = [["1.", "PLAY!"],
                  ["2.", "LEADERBOARD"],
                  ["3.", "EXIT GAME"]]
    print("\n"*35)
    # Print stylized title
    print(figlet.renderText("Brainstorm Blitz!"))

    # Print main menu options table in 'pretty' format using tabulate
    print(tabulate(game_modes, headers=["Choice No.", "Main Menu"], tablefmt="rounded_grid", colalign=("center","center")))
    
    # Main menu logic 
    while True:
        menu_choice = input("Select from the menu: ")

        # Try-except for input validation
        try:

            # Match case for option select.
            match int(menu_choice):
                case 1:
                    # Launches game and exits out of main menu loop
                    start_game()
                    break
                
                case 2:
                    # Displays leaderboard and reprompts user for main menu option select.
                    display_leaderboard()
                
                case 3:
                    while True:
                        # Prompts the user for confirmation to exit the game and reprompts if invalid input
                        confirmation = input("Are you sure you want to exit? (Y/N): ").strip().upper()
                        
                        if confirmation == "Y":
                            sys.exit("Goodbye! Thanks for playing!")
                            
                        elif confirmation == "N":
                            break  
                        else:
                            print("Invalid choice. Please enter Y or N.")
                            
        except ValueError:
            print("Please enter a valid number.")


# Start game logic
def start_game():

    # Prompts the user for a category choice
    category = get_category()

    # The get_category function will return None if the user chooses to return to main menu
    # The main menu is started, and returns out of the start_game logic
    if category is None:
        main_menu()
        return

    # Prompts the user for amount of questions, difficulty, and question type
    question_amount = get_questions_amount()
    difficulty = get_difficulty()
    question_type = get_question_type()

    # Default structuring for the API URL, plugging in the values from the user prompts
    url = f"https://opentdb.com/api.php?amount={question_amount}&difficulty={difficulty}&type={question_type}"

    # If the user selects 'All categories', it will use the default URL. 
    # No specified category, the API will return questions from all categories
    # But if the user selects a category, concatenate the category parameter onto the URL, pluggin in the category ID
    if category != "all categories":
        url += f"&category={category}"

    # Get the json response with the URL and extract the questions and answers
    json_url = requests.get(url).json()
    questions = get_questions(json_url)
    all_answers = get_answers(json_url)
    
    print("\n"*20)

    # After all the user prompting, display quiz
    print(figlet.renderText("Quiz Started!"))
    display_quiz(questions, all_answers, question_type)


# Prompts user for question amount they want to play for. 1 to 50 is the hard limit set by the API.
def get_questions_amount():
    while True:
        # Prompts the user, validates the input and returns the question amount
        try:
            amount = int(input("How many questions would you like to play for (1 - 50)? "))
            if 1 <= amount <= 50:
                return amount
            else:
                raise ValueError
            
        except Exception:
            print("Invalid amount")
            continue


# Prompts the user for category selection
def get_category():
    
    # Main category table
    top_level_categories = [["1.", "Animals"], 
                            ["2.", "Art"], 
                            ["3.", "Celebrities"], 
                            ["4.", "Entertainment +"], 
                            ["5.", "General Knowledge"], 
                            ["6.", "Geography"], 
                            ["7.", "History"], 
                            ["8.", "Mythology"], 
                            ["9.", "Politics"], 
                            ["10.", "Science +"], 
                            ["11.", "Science & Nature"], 
                            ["12.", "Sports"], 
                            ["13.", "Vehicles"],
                            ["14.", "All Categories"],
                            ["15.", "One Random Category"],
                            ["0.", "Back to Menu"]]
    
    # ID dictionary for main category choices. (Ex: if user selects Animals(1) the ID for that within the database API is 27)
    top_level_id_dict = {"1":"27", "2":"25", "3":"26", "5":"9", "6":"22", "7":"23",
                         "8":"20", "9":"24", "11":"17", "12":"21", "13":"28"}
    
    # Entertainment sub-categories table
    entertainment = [["1.","Board Games"],
                     ["2.","Books"],
                     ["3.","Cartoon & Animations"],
                     ["4.","Comics"],
                     ["5.","Film"],
                     ["6.","Japanese Anime & Manga"],
                     ["7.","Musicals & Theatres"],
                     ["8.","Music"],
                     ["9.","Television"],
                     ["10.","Video Games"],
                     ["0.", "Back to Categories"]]
    
    # ID conversion again
    entertainment_id_dict = {"1":"16", "2":"10", "3":"32", "4":"29", "5":"11", 
                             "6":"31", "7":"13", "8":"12", "9":"14", "10":"15"}
    
    # Science sub-categories table
    science = [["1.","Computers"],
               ["2.","Gadgets"],
               ["3.","Mathematics"],
               ["0.", "Back to Categories"]]
    
    # ID conversion again
    science_id_dict = {"1":"18", "2":"30", "3":"19"}
    
    while True:
        print("\n"*10)
        # Print Categories with figlet styling
        print(figlet.renderText('Categories'))
        
        # Prints the categories table
        print(tabulate(top_level_categories, headers=["Choice No.", "Category Name"], tablefmt="rounded_grid", colalign=("center","center")))
        print("Categories with '+' have more subcategories to choose from :D\n")
        
        try:
            selection = input("Desired Category Number: ").strip().strip(".")
            
            # Returns None, goes back to the main menu, and exits the loop
            if selection == "0":
                return None
            
            # Input validation
            if int(selection) > 15 or int(selection) < 0:
                raise ValueError
            
            # If user input is in the category dict, return the corresponding value (the category ID)
            elif selection in top_level_id_dict.keys():

                # Prints the current available amounts of questions. total, easy, medium, and hard
                print(question_count(top_level_id_dict.get(selection)))
                return top_level_id_dict.get(selection)
            
            else:
                match int(selection):
                    # If the user inputs 4, the entertainment category has subcategories within it.
                    case 4:
                        while True:
                            # Input validation, table printing, and appropriate category ID return
                            print('\n' * 20)
                            print(figlet.renderText('Entertainment'))
                            print("Entertainment Sub-categories:")
                            print(tabulate(entertainment, headers=["Choice No.", "Category Name"], tablefmt="rounded_grid", colalign=("center","center")))
                            sub_selection = input("Desired Category Number: ").strip().strip(".")
                            try:
                                if int(sub_selection) > 10 or int(sub_selection) < 0:
                                    raise ValueError
                                
                                if sub_selection == "0":
                                    break
                                else:
                                    print(question_count(entertainment_id_dict.get(sub_selection)))
                                    return entertainment_id_dict.get(sub_selection)
                            except ValueError:
                                print("Invalid subcategory selection. Please choose a valid option.")
                    
                    # Same as entertainment, science also has subcategories within
                    case 10:
                        while True:
                            # Input validation, table printing, and appropriate category ID return
                            print('\n' * 40)
                            print(figlet.renderText('Science'))
                            print("Science Sub-categories:")
                            print(tabulate(science, headers=["Choice No.", "Category Name"], tablefmt="rounded_grid", colalign=("center","center")))
                            sub_selection = input("Desired Category Number: ").strip().strip(".")
                            try:
                                if int(sub_selection) > 3 or int(sub_selection) < 0:
                                    raise ValueError
                                if sub_selection == "0":
                                    break
                                else:
                                    print(question_count(science_id_dict.get(sub_selection)))
                                    return science_id_dict.get(sub_selection)
                            except ValueError:
                                print("Invalid subcategory selection. Please choose a valid option.")

                    # return the string 'all categories' back to the start game function to use the correct URL structure
                    case 14:
                        return "all categories"
                    
                    # Randomly chooses a category ID and returns it.
                    case 15:
                        random_category = random.choice(["9", "10", "11", "12", "13", "14", "15", 
                                            "16", "17", "18", "19", "20", "21", "22",
                                            "23", "24", "25", "26", "27", "28", "29",
                                            "30", "31", "32"])
                        print(question_count(random_category))
                        return random_category
            
        except ValueError:
            print("Invalid Category Selection.")
            continue


# Prompts the user for difficulty selection
def get_difficulty():
    
    print()
    difficulty_table = [["1.", "Easy"],
                        ["2.", "Medium"],
                        ["3.","Hard"]]
    
    # Prints the formatted difficulty table
    print(tabulate(difficulty_table, headers=["Choice No.", "Difficulty"], tablefmt="rounded_grid", colalign=("center","center")))
    while True:
        # Prompts and if needed, reprompts the user for difficulty selection, and giving multiple options for user input
        # Try-except for input validation
        try:
            difficulty = input("Select a difficulty: ").lower().strip().strip(".")
            if difficulty in ["1", "low", "easy", "beginner", "ez"]:
                return "easy"
            elif difficulty in ["2","mid", "med", "middle", "medium", "intermediate", "normal"]:
                return "medium"
            elif difficulty in ["3", "hard", "tough", "challenge", "difficult", "max"]:
                return "hard"
            else:
                raise ValueError
            
        except Exception:
            print("Invalid difficulty.")
            continue

# Prompts the user for question type
def get_question_type():

    # Prompt user, validate input, and return either: Boolean for T/F questions or Multiple for multiple choice questions
    while True:
        try:
            print()
            choice = input("What type of questions would you like? Mutliple choice (M), or True/False (T): ").strip().upper()
            print("\n" * 2)
            if choice in ["M", "T"]:
                match choice:
                    case "M":
                        return "multiple"
                    case "T":
                        return "boolean"
            else:
                raise Exception
        except Exception:
            print("Invalid Question Type")
            continue

# Display the quiz itself
def display_quiz(questions, all_answers, question_type):

    # Tracker variables to keep track of updating values
    score = 0
    streak = 0
    highest_streak = 0
    total_hints_used = 0
    
    # List of praises to later be used
    praises_list = ["Good Job!", "Nice Work!", "You're A Genius!!", "Wow!", 
                    "OMG!", "Amazing!", "Spectacular!", "Really Nice!",
                    "Are You Cheating?!", "No Way!", "Insane!", "Outstanding!"]
    
    # Loop to iterate through each question
    for i in range(len(questions)):
        # Hint used will stay false until the user uses a hint
        hint_used = False

        # Prints the dynamic question number. Ex: Question 4/11. Displays current question number and total no. of questions
        print(f"\nQuestion {i + 1}/{len(questions)}: {questions[i]}")
        
        # Split the passed in answer list into 2 variables. The 3 wrong answers and the one correct answer
        answers = all_answers[i][0]
        correct_answer = all_answers[i][1]
        
        # Changes the option labels depending on question type 
        if question_type == "boolean":
            option_labels = ["A", "B"]
            answers = ["True", "False"]
        elif question_type == "multiple":
            option_labels = ["A", "B", "C", "D"]

        # Zips together the answers with the labels. Ex: (A., Option A), (B., Option B).
        answer_table = list(zip(option_labels, answers))
        
        print(tabulate(answer_table, headers=["Option", "Answer"], tablefmt="rounded_grid"))
        
        # User answer selection and input validation
        # Hint system 
        while True:
            user_input = input(f"Please enter your answer ({', '.join(option_labels)}). Enter 'H' for a hint(-10 Pts.): ").strip().upper()
            
            # Hint option if user inputs 'H'. Hint only available for multiple choice questions (MCQ). 1 hint per question
            if user_input == 'H' and question_type == "multiple" and not hint_used:

                # Leaderboard number of hints used tracker
                total_hints_used += 1

                # Apply hint is called and returns the updated score (-10pts), hint_used is True, option labels and answers with 1 removed
                score, hint_used, option_labels, answers = apply_hint(answers, correct_answer, option_labels, score)
                
                # Combines the updated option labels with the asnwers
                answer_table = list(zip(option_labels, answers))
                print(tabulate(answer_table, headers=["Option", "Answer"], tablefmt="rounded_grid", colalign=("center","center")))
            elif user_input in option_labels:
                break
            else:
                print(f"Invalid input. Please choose one of {option_labels}.")
        
        # Gets the index of the answer of the user input, and matches the answer at that index to the correct answer.
        # If user choice is correct, +1 to streak, add to score based off of current score multiplier, display current score. 
        if answers[option_labels.index(user_input)] == correct_answer:
            streak += 1
            score += score_multiplier(streak)
            print("\n"*30)
            print(f"{'='*30}")
            print(f"\nCorrect! {random.choice(praises_list)}\n")
            print(f"Current streak: 🔥 {streak}")
            print(f"+{score_multiplier(streak)} points!\n")
            print(f"CURRENT SCORE: {score} points\n")
            print(f"{'='*30}")
            
            # Keeps track of what was the highest streak that the user achieved.
            if streak > highest_streak:
                highest_streak = streak

        # If answer is wrong, reset streak, display correct answer, and current score        
        else:
            streak = 0
            print("\n"*30)
            print(f"\n\n{'='*45}")
            print(f"\nWhoops! That was wrong. Streak Reset! 🔥 {streak}")
            print(f"The correct answer was: {correct_answer}\n")
            print(f"CURRENT SCORE: {score} points\n")
            print(f"{'='*45}")

    # After quiz is complete, display final score        
    print(f"\n\nQuiz complete! Your final score: {score} points!")
    
    # Prompt user to add score to leaderboard
    add_to_leaderboard_prompt(score, highest_streak, len(questions), total_hints_used)
    
    # Prompt if user wants to play again. If yes, go back to main menu. If no, exit program.
    while True:
        replay = input("Would you like to play again? (Y/N): ").strip().upper()
        if replay == "Y":
            main_menu()
            
        elif replay == "N":
            print("Goodbye! Thanks for playing!")
            break
        
        else:
            print("\nInvalid Input. Please enter Y or N")
            continue

# Prompts user to add their score to leaderboard
def add_to_leaderboard_prompt(score, highest_streak, num_questions, total_hints_used):
    
    while True:
        add_prompt = input("\nWould you like to add your score to the leaderboard? (Y/N): ").strip().upper()
        if add_prompt == 'Y':
            # If yes then prompt user for their name
            name = input("\nEnter your name: ").strip()
            add_to_leaderboard(name, score, highest_streak, num_questions, total_hints_used)
            display_leaderboard()
            break
        elif add_prompt == "N":
            print("No entry added to the leaderboard.")
            break
        
        else:
            print("Invalid Input. Please enter Y or N")
            continue
            

# Add to leaderboard function
def add_to_leaderboard(name, score, highest_streak, num_questions, total_hints_used):
    leaderboard = []
    
    # if file exists, open in read mode
    # This section is for existing leaderboard entries
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, 'r') as file:

            # The leaderboard file is structured with '=' on the top and bottom of the header, 
            #   thus the next line after the first is the header
            header = next(file)
            
            # Strip every line in the file except for the decoration '=' seperators.
            for line in file:
                line = line.strip()
                if not line or line.startswith("="):
                    continue
                
                # Split the line into parts, if there arent 5 parts, move onto the next line. It is probably the seperator line.
                parts = line.split()
                if len(parts) != 5:
                    continue
                try:
                    # Assign each part that was split to a variable and catch the error to move on to another line
                    player_name = parts[0]
                    player_score = int(parts[1])
                    player_streak = int(parts[2])
                    questions_played = int(parts[3])
                    player_total_hints_used = int(parts[4])

                    # Append each line as one element(each line containing 5 parts) to the leaderboard list
                    leaderboard.append((player_name.strip(), player_score, player_streak, questions_played, player_total_hints_used))
                except ValueError:
                    continue

    # Append the current playing users statistics to the leaderboard list              
    leaderboard.append((name.strip(), score, highest_streak, num_questions, total_hints_used))

    # Sort the leaderboard list by the SCORE of each entry, and in descending order
    leaderboard.sort(key=lambda leaderboard_entry: leaderboard_entry[1], reverse=True)

    # Open the file in write mode, write the header, followed my the '=' seperator
    # This will also create the file if it doesnt exist
    with open(leaderboard_file, 'w') as file:
        header = f"{'Name':<15} {'Score':<10} {'Highest Streak':<22} {'Questions Played':<20} {'Hints Used':<10}\n"
        file.write(header)
        file.write("=" * len(header) + "\n")
        
        # Loop to write each entry stored (current playing user and exisitng user) back to the leaderboard.txt file
        # Writes each entry in one line, following the same spacing (Ex: ':<20') as the header to ensure correct formatting
        for player_name, player_score, player_streak, questions_played, player_total_hints_used in leaderboard:
            file.write(f"{player_name:<15} {player_score:<10} {player_streak:<22} {questions_played:<20} {player_total_hints_used:<10}\n")


# Displays the content from the leaderboard file
# If file does not exist then print 'no data...'
def display_leaderboard():
    print("\n\nLeaderboard:\n")
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, 'r') as file:
            for line in file:
                print(line, end="")
        print()
    else:
        print("\nNo leaderboard data available.\n")
        
# Hint system logic
def apply_hint(answers, correct_answer, option_labels, score):

    # Append passed-in wrong answers to a list
    incorrect_answers = [ans for ans in answers if ans != correct_answer]
    if incorrect_answers:
        removed_answer = random.choice(incorrect_answers) # Randomly select one of the wrong answer
        answers.remove(removed_answer) # Remove the randomly selected wrong answer
        option_labels = option_labels[:len(answers)] # Shorten the option labels to only 3 options
        print(f"Hint used! One wrong answer removed (cost: -10 points).")
        score -= 10 # Cost of 1 hint
        return score, True, option_labels, answers # Returns the updated score, option labels, answers and set 'hint used' to True
    else:
        print("No incorrect answers available to remove.")
        return score, False, option_labels, answers
    

# Retrieve questions from API       
def get_questions(url):
    questions = []
    for i in range(len(url["results"])):
        questions.append(text_cleanup(url["results"][i]["question"]))
        i += 1
        
    return questions


# Retrieve corresponding answers from API, keeps track of correct answer and wrong answers
def get_answers(url):
    all_answers = []
    for i in range(len(url["results"])):
        correct_answer = text_cleanup(url["results"][i]["correct_answer"])
        incorrect_answers = [text_cleanup(ans) for ans in url["results"][i]["incorrect_answers"]]
        answers = [correct_answer] + incorrect_answers
        random.shuffle(answers)
        all_answers.append([answers, correct_answer])
    
    return all_answers


# Score multiplier system.
# Points per question scale with current streak of the player
def score_multiplier(current_streak):
    if 0 <= current_streak <= 2:
        return 10
    elif 3 <= current_streak <= 5:
        return 12
    elif 6 <= current_streak <= 8:
        return 15
    elif 9 <= current_streak <= 11:
        return 20
    elif current_streak >= 12:
        return 30


# Simple text cleanup function
def text_cleanup(text):
    text = (html.unescape(text)).replace("\\'", "'")
    return text

# Displays total currently available number of question from specified category
def question_count(category_id):
    category_dict = {"9":"General Knowledge", "10":"Books", "11":"Film", "12":"Music", "13": "Musicals & Theatres",
                     "14":"Television", "15":"Video Games", "16":"Board Games", "17":"Science & Nature",
                     "18":"Computers", "19":"Mathematics", "20":"Mythology", "21":"Sports",
                     "22":"Geography", "23":"History", "24":"Politics", "25":"Art", "26":"Celebrities",
                     "27":"Animals", "28":"Vehicles", "29":"Comics", "30":"Gadgets", 
                     "31":"Japanese Anime & Manga", "32":"Cartoon & Animations"}
    url = f"https://opentdb.com/api_count.php?category={category_id}"
    questions = requests.get(url).json()

    # Retrieves the total no. of questions, along with questions per difficulty, and prints
    total_category_questions = questions["category_question_count"]["total_question_count"]
    total_easy = questions["category_question_count"]["total_easy_question_count"]
    total_medium = questions["category_question_count"]["total_medium_question_count"]
    total_hard = questions["category_question_count"]["total_hard_question_count"]
    return f"\nTime To Do A Quiz About {category_dict.get(category_id)}!\nTotal Questions About This Category: {total_category_questions}\nTotal Easy Questions: {total_easy}\nTotal Medium Questions: {total_medium}\nTotal Hard Questions: {total_hard}\n"
 

if __name__ == "__main__":
    main_menu()



