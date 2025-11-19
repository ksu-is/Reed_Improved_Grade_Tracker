grades = {}
FILE_NAME = 'grades_data.txt'

def load_grades():
    ##loads grades data from a plain text file, rebuilding the nested structure.
    global grades ## This stores the grades information in the function to the grades list globally instead of locally.

    try:
        with open(FILE_NAME, 'r') as file:
            grades = {}
            for line in file:
                ##Format: CourseName, Score, CategoryName, CategoryWeight
                parts = line.strip(',')
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
    global grades ## This stores the grades information in the function to the grades list globally instead of locally.

    try:
        with open(FILE_NAME, 'w') as file:
            for course, data in grades.items():
                course_weights = data['weights']

                if data['grades']:
                    for score, category in data['grades']:
                        weight = course_weights[category]
                        ##Write in the format: CourseName, Score, CategoryName, CategoryWeight
                        file.write(f"{course},{category},{weight}\n")
        print(f"Grades and course_specific weights saved to {FILE_NAME}.")
    except Exception as e:
        print(f"Error saving grades: {e}")


def add_course(course_name):
    ##adds a new course and initializes data structure
    course_name = course_name.title()
    if course_name not in grades:
        grades[course_name] = {'grades': [], 'weights': {}}
        print(f"Course '{course_name}' added.")
    else:
        print(f"Course '{course_name}' already exists.")

def delete_course(course_name):
    ##Deletes a specified course and all its grades and weights
    global grades ##This stores the grades information in the function to the grades list globally instead of locally.
    course_name = course_name.title()

    if course_name in grades:
        del grades[course_name]
        print(f"Course '{course_name}' has been deleted. (Remember to save before exiting!)")
    else:
        print(f"Error: Course '{course_name}' not found.")


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
    ##Calculates and prints the weighted average GPA for all stored courses.
    global grades ## This stores the grades information in the function to the grades list globally instead of locally.
    
    if not grades:
        print("no courses added yet.")
        return
    
    print("\n--- Summary of All Course GPAs 📈 ---")
    print("-------------------------------------")

    for course_name in grades.keys():
        ## Call calculate_gpa with show_breakdown=Flase to avoid clutter
        gpa_result = calculate_gpa(course_name, show_breakdown=False)
        print(f"   >{course_name}: {gpa_result}")

    print("------------------------------------")

 ## Main Application Loop
 
def grade_tracker_app():
    ## This is the main user interface for the application
    load_grades() ##This is important to load the data first

    while True:
        print("\n--- Grade Tracker Menu ---")
        print("1. Add a New Course")
        print("2. Add a Grade (Score and Category)")
        ## Other items will be added as they are built
        print("7. Save and Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            name = input("Enter the course name: ")
            add_course(name)

        elif choice == '2':
            if grades:
                print("\nAvailable Courses:", ", ".join(grades.keys()))
                course = input("Enter the course name to add grade: ")
                category = input("Enter assignment type (e.g., Quiz, Test, Homework): ")
                try: 
                    score = float(input(f"Enter score for {category} (e.g., 92.5): "))
                    add_grade(course, score, category)
                except ValueError:
                    print("invalid input for score. Please use a number.")
            else:
                print("Please add a course first (Menu 1).")

        ## Space to add other elif choices
        ##
        ##

        elif choice == "7":
            save_grades() ##This is to save data on exit
            print("Exiting the application. Goodbye")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 7")


if __name__ == "__main__":
    grade_tracker_app()