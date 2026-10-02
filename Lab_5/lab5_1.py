contacts = {}

def print_info(info):
    print(f"Name: {info["name"]}\nPhone number: {info["phone"]}\nEmail: {info["email"]}\n")

while True:
    print(f"{"-"*50}\nMenu\n1. Add/Update Contact\n2. View Contact Details\n3. List All Contacts\n4. Delete Contact\n5. Exit")
    choice = input("Please enter choice (1-5) : ")
    print()

    if choice == '1':#Add/Update Contact
        name = input("Enter name : ")
        phone = input("Enter phone number : ")
        email = input("Enter email : ")

        contacts[name.lower()] = {}
        contacts[name.lower()]["phone"] = phone
        contacts[name.lower()]["email"] = email
        contacts[name.lower()]["name"] = name
        print("Write sucessfully!!!\n")

    elif choice == '2':#View Contact Details
        name = input("Enter name to find contact : ")
        info = contacts.get(name.lower(), None)
        print()
        if len(contacts) == 0 or info == None:
            print("Contact not found.\n")
        else:
            print("information:")
            print_info(info)

    elif choice == '3':#List All Contacts
        if len(contacts) == 0:
            print("There is no any contact in the list.\n")
            continue

        print("information:")
        for name, value in contacts.items():
            print_info(value)

    elif choice == '4':#Delete Contact
        name = input("Enter name to delete : ")
        print()
        try:
            del contacts[name.lower()]
        except KeyError:
            print(f"There is no {name} in contacts list.\n")
        else:
            print("Remove sucessfully!!!\n")

    elif choice == '5':#Exit
        print("Thank You\n")
        exit()
        
    else:
        print("**Please enter number 1-5**\n")