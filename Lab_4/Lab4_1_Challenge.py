list = []
flag = True
choice = 0
text = ""

def print_list():
    for i in list:
        print(i)
    
while flag:
    choice = input("Menu:\n1. Add\n2. Delete\n3. Search\n4. Sort\n5. Exit\nSelect : ")
    print()
    match choice:
        case "1":
            text = input("Enter text to add to list : ")
            list.append(text)
            print(f"Add {text} successfully.")
            print_list()
        case "2":
            text = input("Enter text to delete : ")
            if text in list:
                list.remove(text)
                print(f"Remove {text} successfully.")
            else:
                print(f"Not found {text} in list.")
            print_list()
        case "3":
            text = input("Enter text to search : ")
            if text in list:
                print(f"Index of {text} = {list.index(text)}")
            else:
                print(f"Not found {text} in list.")
        case "4":
            list.sort()
            print_list()
        case "5":
            flag = False
        case _:
            print("Please enter only 1-5")
    print()