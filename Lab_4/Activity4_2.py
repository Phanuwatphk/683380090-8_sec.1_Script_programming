todo_list = []
flag = True

def printlist():
    for i in range(len(todo_list)):
        print(f"{i+1}. {todo_list[i]}")

while flag:
    choice = input("Menu:\n1. Add task\n2. View tasks\n3. Mark as done\n4. Exit\nselect : ")
    print()
    match choice:
        case "1":
            todo_list.append(input("Enter task : "))
            print("Task has been saved.\n")
        case "2":
            print("Task:")
            printlist()
            print()
        case "3":
            printlist()
            index = int(input("Enter number to mark as done : ")) - 1
            todo_list.pop(index)
            print("mark as done successfully.\n")
        case "4":
            flag = False
        case _:
            print("Please enter only 1-4\n")