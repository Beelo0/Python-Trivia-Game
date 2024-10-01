import requests
import random
import html
import sys
import os
from tabulate import tabulate
from pyfiglet import Figlet

figlet = Figlet()
figlet.setFont(font = "slant")
base_dir = os.path.dirname(os.path.abspath(__file__))
leaderboard_file = os.path.join(base_dir, "leaderboard.txt")

def main_menu():
    game_modes = [["1.", "PLAY!"],
                  ["2.", "LEADERBOARD"],
                  ["3.", "EXIT GAME"]]
    print("\n"*35)
    print(figlet.renderText("Brainstorm Blitz!"))
    print(tabulate(game_modes, headers=["Choice No.", "Main Menu"], tablefmt="rounded_grid", colalign=("center","center")))
    
    while True:
        menu_choice = input("Select from the menu: ")
        try:
            match int(menu_choice):
                case 1:
                    start_game()
                    break
                
                case 2:
                    display_leaderboard()
                    break
                
                case 3:
                    while True:
                        confirmation = input("Are you sure you want to exit? (Y/N): ").strip().upper()
                        
                        if confirmation == "Y":
                            sys.exit("Goodbye! Thanks for playing!")
                            
                        elif confirmation == "N":
                            break  
                        else:
                            print("Invalid choice. Please enter Y or N.")
                            
        except ValueError:
            print("Please enter a valid number.")


def start_game():
    category = get_category()

    if category is None:
        main_menu()
        return

    question_amount = get_questions_amount()
    difficulty = get_difficulty()
    question_type = get_question_type()

    url = f"https://opentdb.com/api.php?amount={question_amount}&difficulty={difficulty}&type={question_type}"
    if category != "all categories":
        url += f"&category={category}"

    json_url = requests.get(url).json()
    questions = get_questions(json_url)
    all_answers = get_answers(json_url)

    display_quiz(questions, all_answers, question_type)

def get_questions_amount():
    while True:
        try:
            amount = int(input("How many questions would you like to play for (1 - 50)? "))
            if 1 <= amount <= 50:
                return amount
            else:
                raise ValueError
            
        except Exception:
            print("Invalid amount")
            continue


def get_category():
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
    
    top_level_id_dict = {"1":"27", "2":"25", "3":"26", "5":"9", "6":"22", "7":"23",
                         "8":"20", "9":"24", "11":"17", "12":"21", "13":"28"}
    
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
    
    entertainment_id_dict = {"1":"16", "2":"10", "3":"32", "4":"29", "5":"11", 
                             "6":"31", "7":"13", "8":"12", "9":"14", "10":"15"}
    
    science = [["1.","Computers"],
               ["2.","Gadgets"],
               ["3.","Mathematics"],
               ["0.", "Back to Categories"]]
    
    science_id_dict = {"1":"18", "2":"30", "3":"19"}
    
    while True:
        print("\n"*10)
        print(figlet.renderText('Categories'))
        print(tabulate(top_level_categories, headers=["Choice No.", "Category Name"], tablefmt="rounded_grid", colalign=("center","center")))
        print("Categories with '+' have more subcategories to choose from :D\n")
        
        try:
            selection = input("Desired Category Number: ").strip().strip(".")
            
            if selection == "0":
                return None
            
            if int(selection) > 15 or int(selection) < 0:
                raise ValueError
            
            elif selection in top_level_id_dict.keys():
                print(question_count(top_level_id_dict.get(selection)))
                return top_level_id_dict.get(selection)
            
            else:
                match int(selection):
                    case 4:
                        while True:
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
                    
                    case 10:
                        while True:
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
                
                    case 14:
                        return "all categories"
                    
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
        
        
def get_difficulty():
    
    print()
    difficulty_table = [["1.", "Easy"],
                        ["2.", "Medium"],
                        ["3.","Hard"]]
    
    print(tabulate(difficulty_table, headers=["Choice No.", "Difficulty"], tablefmt="rounded_grid", colalign=("center","center")))
    while True:
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


def get_question_type():
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

    
def display_quiz(questions, all_answers, question_type):
    score = 0
    streak = 0
    highest_streak = 0
    
    praises_list = ["Good Job!", "Nice Work!", "You're A Genius!!", "Wow!", 
                    "OMG!", "Amazing!", "Spectacular!", "Really Nice!",
                    "Are You Cheating?!", "No Way!", "Insane!", "Outstanding!"]
    
    for i in range(len(questions)):
        hint_used = False
        print(f"\nQuestion {i + 1}/{len(questions)}: {questions[i]}")
        
        answers = all_answers[i][0]
        correct_answer = all_answers[i][1]
        
        if question_type == "boolean":
            option_labels = ["A", "B"]
            answers = ["True", "False"]
        elif question_type == "multiple":
            option_labels = ["A", "B", "C", "D"]

        answer_table = list(zip(option_labels, answers))
        
        print(tabulate(answer_table, headers=["Option", "Answer"], tablefmt="rounded_grid"))
        
        while True:
            user_input = input(f"Please enter your answer ({', '.join(option_labels)}). Enter 'H' for a hint(-10 Pts.): ").strip().upper()
            if user_input == 'H' and question_type == "multiple" and not hint_used:
                score, hint_used, option_labels, answers = apply_hint(answers, correct_answer, option_labels, score)
                answer_table = list(zip(option_labels, answers))
                print(tabulate(answer_table, headers=["Option", "Answer"], tablefmt="rounded_grid", colalign=("center","center")))
            elif user_input in option_labels:
                break
            else:
                print(f"Invalid input. Please choose one of {option_labels}.")
        
        if answers[option_labels.index(user_input)] == correct_answer:
            streak += 1
            score += score_multiplier(streak)
            print(f"\n\n{'='*30}")
            print(f"\nCorrect! {random.choice(praises_list)}\n")
            print(f"Current streak: 🔥 {streak}")
            print(f"+{score_multiplier(streak)} points!\n")
            print(f"CURRENT SCORE: {score} points\n")
            print(f"{'='*30}")
            
            if streak > highest_streak:
                highest_streak = streak
                
        else:
            streak = 0
            print(f"\n\n{'='*45}")
            print(f"\nWhoops! That was wrong. Streak Reset! 🔥 {streak}")
            print(f"The correct answer was: {correct_answer}\n")
            print(f"CURRENT SCORE: {score} points\n")
            print(f"{'='*45}")
            
    print(f"Quiz complete! Your final score: {score} points!")
    
    add_to_leaderboard_prompt(score, highest_streak, len(questions))


def add_to_leaderboard_prompt(score, highest_streak, num_questions):
    add_prompt = input("Would you like to add your score to the leaderboard? (Y/N): ").strip().upper()
    if add_prompt == 'Y':
        name = input("Enter your name: ").strip()
        add_to_leaderboard(name, score, highest_streak, num_questions)
        display_leaderboard()
    else:
        print("No entry added to the leaderboard.")


def add_to_leaderboard(name, score, highest_streak, num_questions):
    leaderboard = []
    
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, 'r') as file:
            header = next(file)
            
            for line in file:
                line = line.strip()
                if not line or line.startswith("="):
                    continue
                
                parts = line.split()
                if len(parts) != 4:
                    continue
                try:
                    player_name = parts[0]
                    player_score = int(parts[1])
                    player_streak = int(parts[2])
                    questions_played = int(parts[3])
                    leaderboard.append((player_name.strip(), player_score, player_streak, questions_played))
                except ValueError:
                    continue

    leaderboard.append((name.strip(), score, highest_streak, num_questions))

    leaderboard.sort(key=lambda leaderboard_entry: leaderboard_entry[1], reverse=True)

    with open(leaderboard_file, 'w') as file:
        header = f"{'Name':<15} {'Score':<10} {'Streak':<10} {'Questions Played':<20}\n"
        file.write(header)
        file.write("=" * len(header) + "\n")
        
        for player_name, player_score, player_streak, questions_played in leaderboard:
            file.write(f"{player_name:<15} {player_score:<10} {player_streak:<10} {questions_played:<20}\n")

    
def display_leaderboard():
    print("\n\nLeaderboard:\n")
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, 'r') as file:
            for line in file:
                print(line, end="")
        print()
    else:
        print("\nNo leaderboard data available.\n")
        

def apply_hint(answers, correct_answer, option_labels, score):
    incorrect_answers = [ans for ans in answers if ans != correct_answer]
    if incorrect_answers:
        removed_answer = random.choice(incorrect_answers)
        answers.remove(removed_answer)
        option_labels = option_labels[:len(answers)]
        print(f"Hint used! One wrong answer removed (cost: -10 points).")
        score -= 10
        return score, True, option_labels, answers
    else:
        print("No incorrect answers available to remove.")
        return score, False, option_labels, answers
    
       
def get_questions(url):
    questions = []
    for i in range(len(url["results"])):
        questions.append(text_cleanup(url["results"][i]["question"]))
        i += 1
        
    return questions

 
def get_answers(url):
    all_answers = []
    for i in range(len(url["results"])):
        correct_answer = text_cleanup(url["results"][i]["correct_answer"])
        incorrect_answers = [text_cleanup(ans) for ans in url["results"][i]["incorrect_answers"]]
        answers = [correct_answer] + incorrect_answers
        random.shuffle(answers)
        all_answers.append([answers, correct_answer])
    
    return all_answers


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


def text_cleanup(text):
    text = (html.unescape(text)).replace("\\'", "'")
    return text


def question_count(category_id):
    category_dict = {"9":"General Knowledge", "10":"Books", "11":"Film", "12":"Music", "13": "Musicals & Theatres",
                     "14":"Television", "15":"Video Games", "16":"Board Games", "17":"Science & Nature",
                     "18":"Computers", "19":"Mathematics", "20":"Mythology", "21":"Sports",
                     "22":"Geography", "23":"History", "24":"Politics", "25":"Art", "26":"Celebrities",
                     "27":"Animals", "28":"Vehicles", "29":"Comics", "30":"Gadgets", 
                     "31":"Japanese Anime & Manga", "32":"Cartoon & Animations"}
    url = f"https://opentdb.com/api_count.php?category={category_id}"
    questions = requests.get(url).json()
    total_category_questions = questions["category_question_count"]["total_question_count"]
    total_easy = questions["category_question_count"]["total_easy_question_count"]
    total_medium = questions["category_question_count"]["total_medium_question_count"]
    total_hard = questions["category_question_count"]["total_hard_question_count"]
    return f"\nTime To Do A Quiz About {category_dict.get(category_id)}!\nTotal Questions About This Category: {total_category_questions}\nTotal Easy Questions: {total_easy}\nTotal Medium Questions: {total_medium}\nTotal Hard Questions: {total_hard}\n"
 

if __name__ == "__main__":
    main_menu()



