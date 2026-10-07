# create_dummy_data.py
import openpyxl
import os

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(data_dir, exist_ok=True)
output_path = os.path.join(data_dir, 'input_data.xlsx')

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "SalesData"

ws.append(["Product Name", "Quantity", "Unit Price"])

data = [
    ["Laptop", 2, 1200.50], ["Mouse", 5, 25.00], ["Keyboard", 3, 75.99],
    ["Monitor", 1, 300.00], ["Projector", 1, 850.00], ["Webcam", 10, 45.00],
    ["Headset", 4, 99.99], ["SSD", 2, 180.00], ["Router", 1, 70.00]
]
for row in data:
    ws.append(row)

wb.save(output_path)
print(f"✅ สร้างไฟล์ {output_path} สำเร็จ!")
