while True:
    age = int(input("Enter you age : "))
    if age >= 0:
        break

if age < 5:
    print("You're too young for movies! Enjoy cartoons.")
elif 5 <= age <= 12:
    print("G-rated or PG-rated movies.")
elif 13 <= age <= 17:
    print("PG-13 or R-rated (with parental guidance).")
else:
    print("Any movie rating.")

option = input("Do you like action movie? (yes/no) : ")
if option == "yes" and age >= 18:
    print("You might enjoy the latest action blockbuster!")