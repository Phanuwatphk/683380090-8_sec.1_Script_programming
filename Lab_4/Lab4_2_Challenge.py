import math

p1 = (float(input("Enter x1 : ")), float(input("Enter y1 : ")))
p2 = (float(input("Enter x2 : ")), float(input("Enter y2 : ")))

distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
print(f"Distance = {distance}")