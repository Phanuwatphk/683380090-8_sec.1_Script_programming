import math

p1 = (3, 4)
p2 = (6, 8)

# p1[0] = 5
# Traceback (most recent call last):
#   File "/home/phanuwat/Desktop/Code/Script Programming/Lab_4/Lab4_2.py", line 4, in <module>
#     p1[0] = 5
#     ~~^^^
# TypeError: 'tuple' object does not support item assignment
'''
สาเหตุที่มี Error เกิดขึ้นเพราะว่าชนิดข้อมูล Tuple ไม่สามารถทำการเปลี่ยนค่าได้
'''

distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
print(f"Distance = {distance}")