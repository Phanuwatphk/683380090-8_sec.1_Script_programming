# Script Programming

Repository สำหรับเก็บแบบฝึกหัด กิจกรรม และงาน Lab ในรายวิชา **Script Programming CP352301** ภาคการศึกษา 1/2026

ครอบคลุมการเขียน Python พื้นฐาน และงานอัตโนมัติระดับ Basic / Advance ตั้งแต่ Web Scraping ไปจนถึงการจัดการข้อมูล เอกสาร อีเมล และ SMS โดยมีงานถึง **LabX 12**

## Course

- **Course:** Script Programming CP352301
- **Student ID:** 683380090-8
- **Section:** 1

## Labs

### แบบฝึกหัดพื้นฐาน

| Lab | Description |
|---|---|
| [Lab 2](./Lab_2) | รับข้อมูลจากผู้ใช้และเขียนเงื่อนไขเพื่อเลือกการทำงาน |
| [Lab 3](./Lab_3) | การวนซ้ำ ตารางสูตรคูณ การนับถอยหลัง และเกมทายตัวเลข พร้อมกิจกรรมใน Jupyter Notebook |
| [Lab 4](./Lab_4) | การใช้ List และ Tuple รวมถึงโปรแกรมจัดการรายการและโจทย์ Challenge |
| [Lab 5](./Lab_5) | การจัดการข้อมูลผู้ติดต่อและประมวลผลข้อความ |
| [Lab 6](./Lab_6) | ฟังก์ชัน พารามิเตอร์ และการสร้างโมดูล Python |

### LabX: งานอัตโนมัติ

| LabX | Basic | Advance |
|---|---|---|
| 1 — Web Scraping | [ดึงข้อมูลจากเว็บด้วย Requests และ Beautiful Soup](./LabX_Basic_1) | [ดึงข้อมูลด้วย Selenium พร้อม config และการเปลี่ยนหน้า](./LabX_Advance_1) |
| 8 — CSV / JSON | [อ่าน เขียน กรองข้อมูลยอดขาย และปรับปรุงสินค้าคงคลัง](./LabX_Basic_8) | [ประมวลผลข้อมูลตาม pipeline ใน config พร้อมแปลง CSV / JSON และบันทึก audit report](./LabX_Advance_8) |
| 10 — Excel | [คำนวณยอดขายและสร้างรายงาน Excel พร้อมจัดรูปแบบ](./LabX_Basic_10) | [สร้างสูตร Conditional Formatting และกราฟตาม config พร้อม audit log](./LabX_Advance_10) |
| 11 — PDF / Word | [อ่านข้อความจาก PDF สร้างรายงาน Word และรวม PDF](./LabX_Basic_11) | [สร้างรายงานจาก Word template ใส่ลายน้ำ รวม PDF และสกัดข้อความตาม config](./LabX_Advance_11) |
| 12 — Email / SMS | [ส่งอีเมลพร้อมไฟล์แนบ ส่ง SMS ผ่าน email gateway และอ่านอีเมลผ่าน IMAP](./LabX_Basic_12) | [ทำงานตาม communication pipeline ใช้ข้อความ template และกฎประมวลผลอีเมล พร้อมการตอบกลับและแจ้งเตือน](./LabX_Advance_12) |

## Project Structure

```text
Script Programming Lab/
├── Lab_2/ ... Lab_6/       # แบบฝึกหัดและกิจกรรม Python
├── LabX_Basic_1/           # Web Scraping
├── LabX_Advance_1/
├── LabX_Basic_8/           # CSV / JSON
├── LabX_Advance_8/
├── LabX_Basic_10/          # Excel
├── LabX_Advance_10/
├── LabX_Basic_11/          # PDF / Word
├── LabX_Advance_11/
├── LabX_Basic_12/          # Email / SMS
├── LabX_Advance_12/
└── README.md
```

งาน LabX แยกจุดเริ่มต้นไว้ใน `main.py` และโมดูลใน `src/` ส่วนไฟล์ข้อมูลใช้โฟลเดอร์ `data/` หรือ `documents/` ตามประเภทงาน งาน Advance มี `configs/` สำหรับกำหนดขั้นตอนการทำงาน และบางงานมี `templates/`, `reports/` หรือภาพผลลัพธ์ประกอบ

## Getting Started

เปิด terminal ที่โฟลเดอร์หลักของ repository แล้วสร้าง virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

ติดตั้ง dependencies ของ Lab ที่ต้องการรันจาก `requirements.txt` ของ Lab นั้น ตัวอย่างสำหรับ LabX Basic 10:

```bash
python -m pip install -r LabX_Basic_10/requirements.txt
python LabX_Basic_10/main.py
```

พาธข้อมูล config รายงาน และ `.env` อ้างอิงโฟลเดอร์ของแต่ละ Lab จากตำแหน่งไฟล์ Python จึงไม่ต้องเปลี่ยน working directory เข้าไปในโฟลเดอร์ของงานก่อนรัน หากรันจากโฟลเดอร์อื่น ให้ระบุพาธไปยังไฟล์สคริปต์ให้ถูกต้อง ส่วนพาธสัมพัทธ์ใน config อ้างอิงโฟลเดอร์ของ Lab และพาธแบบ absolute ใช้ตำแหน่งที่ระบุไว้

ตัวอย่างรัน Advance 1 จากโฟลเดอร์หลัก:

```bash
python LabX_Advance_1/main.py
```

ก่อนรัน ให้เตรียมข้อมูลต้นฉบับและไฟล์แนบตามพาธของ Lab ที่เลือก

### ตั้งค่า LabX 12

ทั้ง Basic และ Advance ใช้ environment variables สำหรับบัญชีผู้ส่ง ได้แก่ `SENDER_EMAIL`, `SENDER_APP_PASSWORD`, `SMTP_SERVER`, `SMTP_PORT` และ `IMAP_SERVER` โดยใส่ค่าใน `.env` ของ Lab หรือกำหนดผ่าน environment ของเครื่อง

- **Basic 12:** ใช้ `TEST_RECIPIENT_EMAIL`, `TEST_SMS_PHONE_NUMBER` และ `TEST_SMS_CARRIER` เพิ่มเติมสำหรับผู้รับตัวอย่าง
- **Advance 12:** ผู้รับ เนื้อหา ไฟล์แนบ และกฎประมวลผลกำหนดใน [comm_pipeline_config.json](./LabX_Advance_12/configs/comm_pipeline_config.json) โดย `to`, `cc` และ `bcc` เป็นรายการอีเมล

แต่ละ Lab มี `.env.example` สำหรับใช้เป็นต้นแบบ ตั้งค่าบัญชีและผู้รับก่อนรัน เพราะโปรแกรมส่งอีเมลจริงตามที่กำหนด ส่วนไฟล์ `.env` ถูกละเว้นจาก Git

### ทดสอบ LabX Basic 12

ชุดทดสอบใช้ `unittest` และ mock การเชื่อมต่ออีเมล เพื่อทดสอบแบบออฟไลน์:

```bash
python -m unittest discover -s LabX_Basic_12/tests -v
```

### ทดสอบพาธของทุก LabX

ชุดทดสอบใช้สำเนา Lab ในโฟลเดอร์ชั่วคราว ตรวจการรันไฟล์สคริปต์จากโฟลเดอร์อื่นและการรันด้วย `python -m` รวมถึงตำแหน่งไฟล์ผลลัพธ์ โดยจำลองบริการเว็บ เบราว์เซอร์ และอีเมล:

```bash
python -m unittest discover -s tests -v
```

ชุดทดสอบนี้ใช้ dependencies ของ LabX ทั้งหมดที่นำมาทดสอบ

## Technologies

- Python
- Jupyter Notebook
- Requests / Beautiful Soup — Web Scraping
- Selenium / WebDriver Manager — Browser Automation
- CSV / JSON — Data Processing
- openpyxl — Excel Automation
- PyPDF2 / python-docx / ReportLab — PDF และ Word Automation
- smtplib / imaplib / email — Email Automation
- python-dotenv — Environment Configuration
- unittest / unittest.mock — Automated Testing
