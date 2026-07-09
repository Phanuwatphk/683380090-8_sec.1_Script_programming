num = int(input("Enter number : "))

print("The number is ", end="")
if num > 0:
    print("positive and ", end = "")
elif num < 0:
    print("negative and ", end = "")
else:
    print("zero and ", end = "")

if num % 2 == 0:
    print("even")
else:
    print("odd")