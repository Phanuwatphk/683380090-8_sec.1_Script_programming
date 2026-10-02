def add(a, b):
    """It is used to add two numbers together"""
    return a + b

def subtract(a, b):
    """It is used to subtract two numbers"""
    return a - b

def multiply(a, b):
    """It is used to multiply two numbers"""
    return a * b

def divide(a, b):
    """It is used to divide two numbers"""
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Division by zero"

def power(base, exponent = 2):
    """It is used to raise a number to a power"""
    return base ** exponent

while True:
    print(f"{"-"*50}\nMenu\n1. Add\n2. Subtract\n3. mulitply\n4. divide\n5. Power\n6. Exit")
    choice = input("Enter choice : ")
    if choice not in ["1", "2", "3", "4", "5", "6"]:
        print("\nPlease enter 1-6\n")
        continue
    elif choice == "6":
        exit()

    a, b = input("Format: a b\nEnter two number : ").split()
    a = int(a)
    b = int(b)
    print()

    match choice:
        case "1":
            print(f"{a} + {b} = {add(a, b)}")
        case "2":
            print(f"{a} - {b} = {subtract(a, b)}")
        case "3":
            print(f"{a} * {b} = {multiply(a, b)}")
        case "4":
            print(f"{a} / {b} = {divide(a, b)}")
        case "5":
            print(f"{a} ^ {b} = {power(a, b)}")
    
    print()