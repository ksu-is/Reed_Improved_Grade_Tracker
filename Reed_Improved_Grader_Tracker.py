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
