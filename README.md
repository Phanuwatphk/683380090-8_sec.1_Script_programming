# Script Programming

Repository สำหรับเก็บแบบฝึกหัด กิจกรรม และงาน Lab ในรายวิชา **Script Programming CP352301** ภาคการศึกษา 1/2026

ครอบคลุมการเขียน Python พื้นฐาน และงานอัตโนมัติระดับ Basic / Advance ตั้งแต่ Web Scraping ไปจนถึงการจัดการข้อมูล เอกสาร อีเมล และ SMS โดยมีงานถึง **LabX 12** รวมถึงกิจกรรมพัฒนาโปรแกรม CLI, **Mini Project — PyPocket** และ **Final Project — Gaming Statistics Dashboard**

## Course

- **Course:** Script Programming CP352301
- **Student ID:** 683380090-8
- **Section:** 1

## Projects

| งาน | รายละเอียด | GitHub |
|---|---|---|
| [Mini Project — PyPocket](./Mini_Project/PyPocket) | โปรแกรมบันทึกรายรับ–รายจ่ายผ่าน CLI เก็บข้อมูลใน JSON | [เปิดโปรเจกต์](https://github.com/Phanuwatphk/PyPocket) |
| [Final Project — Gaming Statistics Dashboard](./Final_Project/Gaming-Statistics-Dashboard) | เว็บแอป Streamlit สำหรับค้นหาและวิเคราะห์ข้อมูลเกมจาก RAWG และ Steam | [เปิดโปรเจกต์](https://github.com/Phanuwatphk/Gaming-Statistics-Dashboard) |

## Activities

| งาน | หัวข้อ |
|---|---|
| [Activity 1](./Activity_1/my-task-manager) | Task Manager CLI และการจัดการข้อผิดพลาด |
| [Activity 2](./Activity_2/my-oop-task-manager) | ปรับ Task Manager เป็น OOP ด้วยคลาส Task และ TaskManager |
| [Activity 3](./Activity_3/my-api-fetcher) | ดึงข้อมูลจาก Web API และประมวลผล JSON |
| [Activity 4](./Activity_4/enhanced-task-manager-design) | วางแผนและออกแบบ Enhanced Task Manager |

## Labs

| งาน | หัวข้อ |
|---|---|
| [Lab 2](./Lab_2) | รับข้อมูลและใช้เงื่อนไข |
| [Lab 3](./Lab_3) | การวนซ้ำและเกมทายตัวเลข |
| [Lab 4](./Lab_4) | List, Tuple และโจทย์ Challenge |
| [Lab 5](./Lab_5) | จัดการข้อมูลผู้ติดต่อและข้อความ |
| [Lab 6](./Lab_6) | ฟังก์ชันและโมดูล Python |
| [Lab 12 — Final Project Development](./Lab_12_Final_Project_Development) | พัฒนาและทดสอบ Enhanced Task Manager พร้อมเตรียมนำเสนอ |

## LabX

| หัวข้อ | Basic | Advance |
|---|---|---|
| 1 — Web Scraping | [Requests / Beautiful Soup](./LabX_Basic_1) | [Selenium](./LabX_Advance_1) |
| 8 — CSV / JSON | [อ่านและเขียนข้อมูล](./LabX_Basic_8) | [Data Pipeline](./LabX_Advance_8) |
| 10 — Excel | [สร้างรายงาน Excel](./LabX_Basic_10) | [สูตรและกราฟตาม config](./LabX_Advance_10) |
| 11 — PDF / Word | [อ่านและสร้างเอกสาร](./LabX_Basic_11) | [Template และลายน้ำ](./LabX_Advance_11) |
| 12 — Email / SMS | [ส่งและอ่านอีเมล / ส่ง SMS](./LabX_Basic_12) | [Communication Pipeline](./LabX_Advance_12) |

## เริ่มใช้งาน

แต่ละงานแยกโฟลเดอร์ไว้ ติดตั้ง dependencies จาก `requirements.txt` หากมี แล้วรันไฟล์เริ่มต้นของงาน ตัวอย่างจากโฟลเดอร์หลัก:

```bash
python -m pip install -r LabX_Basic_10/requirements.txt
python LabX_Basic_10/main.py
```

สำหรับ Activities และ Projects เปิดโฟลเดอร์ของงานจากตารางด้านบน แล้วดูวิธีรันและการตั้งค่าใน README ของแต่ละงาน ส่วน LabX 12 ให้ตั้งค่าบัญชีและผู้รับจาก `.env.example` ก่อนรัน เพราะมีการส่งอีเมลและ SMS จริง
