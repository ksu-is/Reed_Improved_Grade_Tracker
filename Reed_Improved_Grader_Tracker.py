
## Global Data Structure
# The main data structure is a nested dictionary to store courses, their grades, and category weights.
# Structure:
# grades = {
#     'CourseName': {
#         'grades': [(score1, category1), (score2, category2), ...],
#         'weights': {'CategoryName': weight, ...}
#     },
#     ...

grades = {} ##this is the global grades dictionary that I will keep referring to in order to store data globally instead of locally within a function.
FILE_NAME = 'grades_data.txt'
DELETE_PASSCODE = '1234' ## Simple passcode for course deletion confirmation


## Data Persistence Functions

def load_grades():
    ##loads grades data from a plain text file, rebuilding the nested structure.
    global grades ## This stores the grades information in the function to the grades dictionary globally instead of locally.

    try:
        with open(FILE_NAME, 'r') as file:
            grades = {}
            for line in file:
                ##Format: CourseName, Score, CategoryName, CategoryWeight
                parts = line.strip().split(',')
                if len(parts) == 4:
                    course, score_str, category, weight_str = parts
                    score = float(score_str)
                    weight = float(weight_str)
                    course = course.title()
                    category = category.title()

                    ##Rebuild the nested dictionary structure
                    if course not in grades:
                        grades[course] = {'grades': [], 'weights': {}}

                    grades[course]['grades'].append((score, category))
                    grades[course]['weights'][category] = weight

            print(f"Loaded {len(grades)} courses from {FILE_NAME}.")

    except FileNotFoundError:
        print("No existing grades file found. Starting fresh.")
    except Exception:
        print("Error reading grades file. Data might be corrupt. Starting fresh.")
        

def save_grades():
    ##saves all courses, grades, and their course_specific weights to one text file.
    global grades ## This stores the grades information in the function to the grades dictionary globally instead of locally.

    try:
        with open(FILE_NAME, 'w') as file:
            for course, data in grades.items():
                course_weights = data['weights']

                if data['grades']:
                    for score, category in data['grades']:
                        weight = course_weights[category]
                        ##Write in the format: CourseName, Score, CategoryName, CategoryWeight
                        file.write(f"{course},{score},{category},{weight}\n")
        print(f"Grades and course_specific weights saved to {FILE_NAME}.")
    except Exception as e:
        print(f"Error saving grades: {e}")

##-----------------------------------------------------------------------------------------------------------

## Core Functionality

def add_course(course_name):
    ##adds a new course and initializes data structure
    course_name = course_name.title()
    if course_name not in grades:
        grades[course_name] = {'grades': [], 'weights': {}}
        print(f"Course '{course_name}' added.")
    else:
        print(f"Course '{course_name}' already exists.")

def delete_course(course_name):
    ## Deletes a specified course and all of its grades/ weights.
    global grades ## This stores the grades information in the function to the grades dictionary globally instead of locally.
    global DELETE_PASSCODE

    course_name = course_name.title()

    if course_name in grades:
        ## Ask for passcode confirmation
        entered_code = input(f"Are you sure you want to DELETE '{course_name}'? Enter the 4-digit security code to confirm: ")

        ## Check if the passcode matched the global code
        if entered_code == DELETE_PASSCODE:
            del grades[course_name]
            print(f" Course '{course_name}' has been deleted. (Remember to save before exiting!)")
        else:
            print(" Security code inccorrect. Deletion Cancelled.")
    else:
        print(f"Error: Course '{course_name}' not found.")   

##    if course_name in grades:
##        del grades[course_name]
##        print(f"Course '{course_name}' has been deleted. (remember to save before exiting!)")
##    else:
##        print(f"Error: Course '{course_name}' not found.")



def add_grade(course_name, score, category_name):
    ##adds a grade, checks for the course specific weight, and prompts if needed.
    course_name = course_name.title()
    category_name = category_name.title()

    if course_name not in grades:
        print(f"Error: Course '{course_name}' not found. Please add the course first (Menu 1).")
        return
    
    course_weights = grades[course_name]['weights']

    ## handle new category type and its course specific weight

    if category_name not in course_weights:
        print(f"'{category_name}' is NEW assignment type for {course_name}.")
        while True:
            try:
                weight = float(input(f"enter the percentage weight for ALL '{category_name}' assignments in {course_name} (e.g., 20): "))
                if 0 <= weight <= 100:
                    course_weights[category_name] = weight
                    print(f"Category '{category_name}' weight set to {weight}% for {course_name}.")
                    break
                else:
                    print("Weight must be between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a number for the weight.")

    ## add the grade to the course's grades list
    grades[course_name]['grades'].append((score, category_name))
    print(f"Grade {score}% added to {course_name} under category '{category_name}'.")

def calculate_gpa(course_name, show_breakdown=True):
    ##Calcualtes the weighted average grade for a single course
    ## If show_breakdown is True, it prints the average for each category.
    course_name = course_name.title()
    if course_name not in grades or not grades[course_name]['grades']:
        return "N/A"

    course_data = grades[course_name]
    course_weights = course_data['weights']

    category_scores = {}

    ##1. Organize scores by cateogry
    for score, category in course_data['grades']:
        category = str(category).title()
        if category not in category_scores:
            category_scores[category] = []
        category_scores[category].append(score)
    
    total_weighted_sum = 0
    total_category_weight = 0

    ##2. Calcualte the average for each category and apply the course's specific weight
    for category, scores in category_scores.items():
        if category in course_weights:
            category_weight = course_weights[category]
            category_average = sum(scores) / len(scores)

            total_weighted_sum += (category_average * category_weight)
            total_category_weight += category_weight

            if show_breakdown:
                print(f"  > {category} Avg: {category_average:.2f}% (Weight: {category_weight}%)")

    ##3. Final GPA calculation
    if total_category_weight > 0:
        final_gpa = total_weighted_sum / total_category_weight
        return f"{final_gpa:.2f}%"
    else:
        return "No grades in weighted categories"
    
def calculate_all_gpas():
    ##Calculates and prints the weighted GPA for all stored course.
    global grades ## This stores the grades information in the function to the grades dictionary globally instead of locally.

    if not grades:
        print("No courses added yet.")
        return

    print("\n--- Summary of All Course GPAs 📈 ---")
    print("--------------------------------------")

    for course_name in grades.keys(): ## this extracts all course names and creates a sequence of them for hte loop to process.
        ## iterate through every course in the grade tracker and print the final GPA for each one, without showing the detailed category breakdown.
        gpa_result = calculate_gpa(course_name, show_breakdown=False)
        print(f"  > {course_name}: {gpa_result}")

    print("--------------------------------")


 ## Main Application Loop
 
def grade_tracker_app():
    ## This is the main user interface for the application
    load_grades() ##This is important to load the data first

    while True:
        print("\n--- Grade Tracker Menu ---")
        print("1. Add a New Course.")
        print("2. Add a Grade (Score and Category).")
        print("3. View GPA for ALL Course.")
        print("4. View GPA for a SINGLE Course (with Breakdown).")
        print("5. View course cateogry weights.")
        print("6. Delete a course.")
        ## Other items can be added as they are built
        print("7. Save and Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            name = input("Enter the course name: ")
            add_course(name)

        elif choice == '2':
            if grades:
                print("\nAvailable Courses:", ", ".join(grades.keys()))
                course = input("Enter the course name to add grade to: ")
                category = input("Enter assignment type (e.g., Quiz, Test, Homework): ")
                try: 
                    score = float(input(f"Enter score for {category} (e.g., 92.5): "))
                    add_grade(course, score, category)
                except ValueError:
                    print("invalid input for score. Please use a number.")
            else:
                print("Please add a course first (Menu 1).")

        elif choice == '3':
            calculate_all_gpas()

        elif choice == '4':
            if grades:
                print("\nAvailable courses: ", ", ".join(grades.keys()))
                course = input("Enter course name to view GPA: ")
                print(f"\n--- GPA Calculation for {course.title()} ---")
                ## Call the calculate_gpa function with default show_breakdown=True
                gpa = calculate_gpa(course)
                print(f"\nFinal GPA for {course.title()}: **{gpa}**")
            else:
                print("No available courses to calculate GPA. Please add a course first (Menu 1).")

        elif choice == '5':
            if grades:
                print("\nAvailable Courses: ", ", ".join(grades.keys()))
                course_to_view = input("Enter course name to view weights: ").title()

                if course_to_view in grades:
                    weights = grades[course_to_view]['weights']
                    print(f"\n--- {course_to_view} Category Weights ---")
                    if weights:
                        for cat, weight in weights.items():
                            print(f"  > {cat}: {weight}%")
                    else:
                        print(f"No categories defined for {course_to_view} yet.")
                else:
                    print(f"Error: Course '{course_to_view}' not found.")
            else:
                print("No courses availabale to view weights.")

        elif choice == '6':
            if grades:
                print("\nAvailabel courses:", ", ".join(grades.keys()))
                course_to_delete = input("Enter the course name to DELETE: ")
                delete_course(course_to_delete)
            else:
                print("No course available to delete.")
                
            

        ## Space to add other elif choices
        ##
        ##

        elif choice == "7":
            save_grades() ##This is to save data on exit
            print("Exiting the application. Goodbye")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 7")

##Run the application
if __name__ == "__main__":
    grade_tracker_app()

