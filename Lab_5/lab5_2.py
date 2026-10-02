python_students = {"S001", "S003", "S005", "S007", "S009"}
java_students = {"S002", "S003", "S006", "S007", "S010"}

print(f"Students who enrolled in both courses: {python_students & java_students}")
print(f"Every students: {python_students | java_students}")
print(f"Students in Python but not in Java: {python_students - java_students}")
print(f"Students enrolled in Python or Java, but not both: {python_students ^ java_students}")

all_students_list = list(python_students) + list(java_students)
all_students_set = set(all_students_list)
print(f"Original: {all_students_list}\nSet: {all_students_set}")