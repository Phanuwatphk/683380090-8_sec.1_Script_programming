student_names = []

student_names.append("Phanuwat")
student_names.append("Alfred ")
student_names.append("Jenny")
student_names.append("David")
student_names.append("Robert")

#print student's name in list
for i in student_names:
    print(i)
print()

#search for student's name in list
name = input("Enter a student's name to search for : ")
if name in student_names:
    print(f"index of \"{name}\" = {student_names.index(name)}\n")
else:
    print(f"Not found \"{name}\" in the list\n")

#delete student's name in list
name = input("Enter a student's name to delete : ")
if name in student_names:
    student_names.remove(name)
else:
    print(f"Not found \"{name}\" in the list")

#print student's name in list
for i in student_names:
    print(i)
print()

student_names.sort()

print(f"Number of student in list = {len(student_names)}\n")