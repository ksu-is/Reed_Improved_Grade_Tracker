grades = {}
FILE_NAME = 'grdes_data.txt'

def add_course(course_name):
    ##adds a new course and initializes data structure
    course_name = course_name.title()
    if course_name not in grades:
        grades[course_name] = {'grades': [], 'weights': {}}
        print(f"Course '{course_name}' added.")
    else:
        print(f"Course '{course_name}' already exists.")

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
