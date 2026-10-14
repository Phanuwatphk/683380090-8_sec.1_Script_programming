# 📚 Learning Log — Gaming Statistics Dashboard

## Final Term Project — CP352301 Script Programming

Learning Log นี้ใช้สำหรับบันทึกสิ่งที่สมาชิกในกลุ่ม
ได้เรียนรู้จากการพัฒนา Gaming Statistics Dashboard
ในแต่ละ Sprint ตั้งแต่ Sprint 1 จนถึง Sprint สุดท้าย

เนื้อหาจะถูก Update หลังจากจบแต่ละ Sprint
เพื่อบันทึกทั้ง Technical Learning, Project Management,
Teamwork, Problems และ Lessons Learned

---

# 📌 Learning Log Structure

ในแต่ละ Sprint จะบันทึกหัวข้อหลักดังนี้:

1. Sprint Overview
2. What We Did
3. What We Learned
4. Problems & Challenges
5. How We Solved Them
6. Teamwork & Process Learning
7. Technical Learning
8. Instructor / Team Feedback
9. Lessons Learned
10. How We Will Apply This Learning

---

# 🚀 Sprint 1 — Application Foundation

**Period:** 10–15 September 2026  
**Status:** ✅ Completed

## 1. Sprint Overview

Sprint 1 เป็นช่วงเริ่มต้นของการพัฒนา Project
โดยมีเป้าหมายเพื่อสร้าง Application Foundation
และทำความเข้าใจกระบวนการทำงานของทีม

ใน Sprint นี้ทีมพัฒนา Application ในรูปแบบ CLI
เพื่อทดลองโครงสร้างการทำงานของระบบ
ก่อนนำไปพัฒนาเป็น Web Application ใน Sprint ถัดไป

---

## 2. What We Did

สิ่งที่ทีมดำเนินการใน Sprint 1:

- กำหนด Sprint Goal
- กำหนด Scope และ Requirements
- แบ่ง Role ของสมาชิก
- ออกแบบ CLI Flow
- พัฒนา Main Menu
- พัฒนา Menu Navigation
- พัฒนา View Games
- พัฒนา Search Game
- พัฒนา Statistics
- พัฒนา Genre
- พัฒนา Top Rated Games
- เพิ่ม Input Validation
- เพิ่ม Exception Handling
- ทดสอบ Normal Cases
- ทดสอบ Invalid Inputs
- ทดสอบ Edge Cases
- จัดทำ Documentation
- จัดทำ GitHub Repository

---

## 3. What We Learned

### Project Planning

ทีมได้เรียนรู้ว่าการกำหนด Scope และ Requirements
ก่อนเริ่มพัฒนา ช่วยให้สมาชิกเข้าใจเป้าหมายเดียวกัน
และช่วยป้องกันการทำงานเกินขอบเขตของ Sprint

### Python Development

ทีมได้เรียนรู้การแบ่ง Program ออกเป็น Function
ตามหน้าที่ เช่น:

```text
display_main_menu()
get_menu_choice()
view_games()
search_game()
view_statistics()
````

การแยก Function ทำให้ Code อ่านง่าย
ทดสอบง่าย และสามารถแก้ไขเฉพาะส่วนได้

### Input Validation

ทีมได้เรียนรู้ว่าข้อมูลจากผู้ใช้ไม่สามารถคาดหวัง
ได้ว่าจะถูกต้องเสมอ จึงต้องมีการตรวจสอบ Input
ก่อนนำไปประมวลผล

### Exception Handling

ทีมได้เรียนรู้การใช้ `try-except`
เพื่อจัดการ Error ที่เกิดจาก Input
และป้องกันไม่ให้ Application Crash

### QA & Testing

ทีมได้เรียนรู้ว่าการทดสอบไม่ควรทดสอบเฉพาะ
กรณีที่ผู้ใช้กรอกข้อมูลถูกต้อง
แต่ควรทดสอบ Invalid Input และ Edge Cases ด้วย

---

## 4. Problems & Challenges

ปัญหาหลักที่พบใน Sprint 1:

### Problem 1 — Non-numeric Input

การรับ Input ที่เป็นข้อความ เช่น:

```text
abc
```

ในตำแหน่งที่ต้องการตัวเลข
สามารถทำให้เกิด `ValueError`

### Problem 2 — Invalid User Input

ผู้ใช้อาจกรอก:

```text
99
-1
[Blank]
```

ซึ่งอยู่นอกขอบเขตของตัวเลือกที่ระบบรองรับ

### Problem 3 — Project Scope

ในช่วงเริ่มต้นมีแนวทางที่สามารถพัฒนาได้หลายส่วน
เช่น API, Database และ Web UI
จึงต้องกำหนด Scope ของ Sprint 1
ให้ชัดเจนเพื่อไม่ให้ Development เกินขอบเขต

---

## 5. How We Solved Them

### Solution 1 — Exception Handling

ใช้ `try-except` เพื่อจัดการ `ValueError`

```python
try:
    choice = int(user_input)
except ValueError:
    print("Invalid input.")
```

### Solution 2 — Input Validation

เพิ่มการตรวจสอบ:

* Blank Input
* Non-numeric Input
* Negative Number
* Out-of-range Number
* Empty Search
* Unknown Game

### Solution 3 — Sprint Scope

กำหนดให้ Sprint 1 เน้น:

```text
CLI
Menu
Input
Validation
Core Features
QA
```

ส่วน Web UI, API และ Database
จะนำไปพัฒนาใน Sprint ถัดไป

---

## 6. Teamwork & Process Learning

จากการแบ่ง Role เป็น:

| Role     | Responsibility                 |
| -------- | ------------------------------ |
| Planner  | Planning และ Documentation     |
| Coder    | Development และ Implementation |
| Debugger | Testing และ QA                 |

ทีมได้เรียนรู้ว่าการแบ่งหน้าที่อย่างชัดเจน
ช่วยให้สมาชิกสามารถรับผิดชอบงานของตนเอง
และสามารถตรวจสอบงานระหว่างกันได้

นอกจากนี้ยังได้เรียนรู้ว่าการสื่อสารระหว่าง
Planner, Coder และ Debugger มีความสำคัญ
ต่อการทำให้ Requirements, Code และ QA
สอดคล้องกัน

---

## 7. Technical Learning

### Python

* Functions
* Loops
* Conditional Statements
* Exception Handling
* Input Validation
* Basic Data Processing

### Application Development

* CLI Application
* Menu Navigation
* Search
* Basic Statistics
* Error Handling

### Testing

* Test Cases
* Normal Cases
* Invalid Cases
* Edge Cases

### Git / GitHub

ทีมได้เรียนรู้ Workflow พื้นฐาน:

```text
Modify
  ↓
Git Add
  ↓
Git Commit
  ↓
Git Push
  ↓
Pull Request
  ↓
Review
  ↓
Merge
```

---

## 8. Instructor / Team Feedback

หลังจากนำเสนอ Sprint 1
ทีมได้รับ Feedback ให้ปรับปรุง:

* Project Pitch
* Project Plan
* Project Timeline
* Task Allocation
* Change Log
* Learning Log
* Contribution Metrics

ทีมจึงนำ Feedback ดังกล่าวมาใช้ปรับปรุง
Project Documentation และ Repository Structure

---

## 9. Lessons Learned

สิ่งสำคัญที่ทีมได้เรียนรู้จาก Sprint 1:

1. ควรกำหนด Scope ก่อนเริ่ม Development
2. ควรแบ่งงานตามหน้าที่อย่างชัดเจน
3. Code ควรแบ่งเป็น Function ตาม Responsibility
4. User Input ต้องได้รับการ Validation
5. ควรทดสอบ Invalid Input และ Edge Cases
6. Documentation ควร Update ไปพร้อมกับ Development
7. Git/GitHub ควรใช้เป็นส่วนหนึ่งของ Development Workflow
8. Feedback จากการ Review สามารถนำมาใช้ปรับปรุง Project ได้

---

## 10. How We Will Apply This Learning

สิ่งที่เรียนรู้จาก Sprint 1
จะถูกนำไปใช้ใน Sprint ถัดไป โดยเฉพาะ:

* ใช้ Modular Design ในการพัฒนา Web Application
* ใช้ Input Validation กับ Web UI
* ใช้ Error Handling กับ API และ Database
* ใช้ Git/GitHub Workflow ต่อเนื่อง
* ทำ QA ระหว่าง Development
* Update Documentation อย่างต่อเนื่อง
* ใช้ Task Allocation เพื่อติดตามงานของสมาชิก

---

## 11. Sprint 1 Learning Summary

| Learning Area      | Status    |
| ------------------ | --------- |
| Project Planning   | ✅ Learned |
| Python Functions   | ✅ Learned |
| CLI Development    | ✅ Learned |
| Input Validation   | ✅ Learned |
| Exception Handling | ✅ Learned |
| Search Logic       | ✅ Learned |
| Basic Statistics   | ✅ Learned |
| QA / Testing       | ✅ Learned |
| Edge Case Testing  | ✅ Learned |
| Git / GitHub       | ✅ Learned |
| Teamwork           | ✅ Learned |
| Documentation      | ✅ Learned |
| Feedback Handling  | ✅ Learned |

---

# 🚀 Sprint 2 — Web UI, API & Database

**Period:** 20–24 September 2026
**Status:** ✅ Completed

> Sprint 2 เป็นช่วงที่ทีมพัฒนาระบบจาก CLI ใน Sprint 1
> ให้เป็น Web Application และเชื่อมต่อข้อมูลจริงจาก API
> พร้อมจัดเก็บข้อมูลผ่าน SQLite Database

## 1. Sprint Overview

**Sprint Goal:**

พัฒนา Gaming Statistics Dashboard ให้สามารถใช้งานผ่าน Web Browser
โดยเชื่อมต่อข้อมูลเกมจริงจาก RAWG API และจัดเก็บข้อมูลผ่าน SQLite Database
พร้อมพัฒนา Backend / Data Flow ให้สามารถนำข้อมูลไปแสดงผลบน Web UI ได้

**Main Focus:**

* Web UI
* Dashboard Layout
* RAWG API
* SQLite Database
* Backend / Data Flow

---

## 2. What We Did

ทีมพัฒนา Streamlit Web Application สำหรับ
Gaming Statistics Dashboard
โดยเปลี่ยนจาก CLI ใน Sprint 1 มาเป็น Web Application
ที่สามารถใช้งานผ่าน Web Browser

มีการเชื่อมต่อ RAWG API เพื่อดึงข้อมูลเกมจริง เช่น:

* Game Name
* Rating
* Released Date
* Genres
* Platforms
* Metacritic Score
* Image

นอกจากนี้ยังเพิ่ม Steam API สำหรับข้อมูลจำนวนผู้เล่นออนไลน์
และ Steam Top 100 / Live Players

ทีมพัฒนา SQLite Database สำหรับจัดเก็บข้อมูลเกม
และสร้าง Game Service เพื่อจัดการ Application Logic

รวมถึงเพิ่ม Data Processing และ Data Normalization
ก่อนนำข้อมูลไปใช้งานใน Web Application

ในส่วนของ Web UI มีการพัฒนา:

* Game Library
* Search
* Genres
* Top Rated
* Live Players
* Game Detail
* Filter
* Pagination
* Error Handling
* Empty State

มีการจัดทำ Automated Tests สำหรับ:

* API
* Database
* Service
* Data Processing

---

## 3. What We Learned

### Web Development

ทีมได้เรียนรู้การพัฒนา Web Application ด้วย Streamlit
และการออกแบบ Dashboard สำหรับแสดงข้อมูลเกมในรูปแบบ
ที่ผู้ใช้สามารถค้นหา กรอง และดูรายละเอียดข้อมูลได้

นอกจากนี้ยังได้เรียนรู้การจัดการ:

* Page Navigation
* Pagination
* Filter
* Error State
* Empty State

บน Web UI

### API Integration

ทีมได้เรียนรู้การเชื่อมต่อ REST API และการทำงานกับ JSON Response
โดยใช้ RAWG API เป็นแหล่งข้อมูลหลักของเกม

ทีมยังได้เรียนรู้การจัดการ API Key ผ่าน Environment Variable
รวมถึงการตรวจสอบ API Response, API Error
และข้อมูลที่อาจไม่ครบถ้วน

นอกจากนี้ยังได้เรียนรู้การเชื่อมต่อ Steam API
เพื่อดึงข้อมูลเกี่ยวกับจำนวนผู้เล่นและ Steam Top 100

### Database

ทีมได้เรียนรู้การใช้ SQLite Database
สำหรับจัดเก็บและจัดการข้อมูลเกมภายในระบบ

รวมถึงการออกแบบการเชื่อมต่อระหว่าง Application
กับ Database และการใช้ Database Layer
แยกออกจากส่วนอื่นของระบบ

### Data Management

ทีมได้เรียนรู้การทำ Data Processing และ Data Normalization
เพื่อแปลงข้อมูลจาก API ให้อยู่ในรูปแบบที่เหมาะสมกับการนำไปใช้งาน

นอกจากนี้ยังได้เรียนรู้การจัดการข้อมูลที่มี Missing Values
และข้อมูลที่อาจมีรูปแบบแตกต่างกันจาก API

---

## 4. Problems & Challenges

| Problem                                      | Impact                                                     | Solution                                                 | Result                                                  |
| -------------------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------- |
| API Response มีข้อมูลซ้อนกันหลายระดับ        | นำข้อมูลไปใช้งานโดยตรงได้ยาก                               | สร้าง Data Processing และ Data Normalization             | ข้อมูลอยู่ในรูปแบบที่ระบบนำไปใช้งานต่อได้               |
| RAWG และ Steam ใช้ข้อมูลระบุตัวเกมต่างกัน    | ไม่สามารถเชื่อมข้อมูลเกมจากทั้งสอง API ได้โดยตรง           | จัดการ Steam App ID Mapping                              | สามารถเชื่อมข้อมูลเกมกับ Steam ได้ในส่วนที่รองรับ       |
| API อาจตอบกลับช้าหรือเกิด Error              | Web Application อาจแสดงผลผิดพลาดหรือไม่สามารถโหลดข้อมูลได้ | เพิ่ม Error Handling และ Empty State                     | ระบบสามารถจัดการกรณี API ใช้งานไม่ได้หรือไม่มีข้อมูล    |
| จำนวนข้อมูลเกมมีมาก                          | แสดงข้อมูลทั้งหมดในหน้าเดียวได้ยาก                         | เพิ่ม Pagination                                         | ผู้ใช้สามารถดูข้อมูลเป็นหน้าได้                         |
| ข้อมูล Steam Player มีการเปลี่ยนแปลงตลอดเวลา | ต้องเรียก API ซ้ำบ่อยเพื่อให้ข้อมูลเป็นปัจจุบัน            | ใช้ระบบ Refresh และ Snapshot                             | ลดการเรียก API ซ้ำและสามารถจัดเก็บข้อมูลล่าสุดไว้ใช้งาน |
| การพัฒนาหลายส่วนพร้อมกัน                     | อาจทำให้ Code และ Module เชื่อมต่อกันผิดพลาด               | แบ่ง API, Database, Service, Processing และ UI ออกจากกัน | สามารถพัฒนาและตรวจสอบแต่ละส่วนได้ง่ายขึ้น               |

---

## 5. How We Solved Them

ทีมแก้ไขปัญหาโดยแบ่งระบบออกเป็นหลาย Layer
เพื่อให้แต่ละส่วนมีหน้าที่ชัดเจน ได้แก่

```text
Web UI
   ↓
Game Service
   ↓
Data Processing
   ↓
API / Database
```

สำหรับข้อมูลจาก API ทีมสร้าง Data Processing Layer
เพื่อจัดรูปแบบและ Normalize ข้อมูลก่อนนำไปใช้งาน

สำหรับปัญหาการเชื่อมต่อข้อมูลจาก RAWG และ Steam
ทีมใช้ข้อมูลที่เกี่ยวข้องกับ Steam App ID
เพื่อเชื่อมข้อมูลเกมในส่วนที่สามารถรองรับได้

สำหรับ API Error และข้อมูลที่ไม่มี
ทีมเพิ่ม Error Handling และ Empty State
เพื่อให้ Application สามารถทำงานต่อได้โดยไม่ Crash

สำหรับข้อมูลจำนวนมาก ทีมเพิ่ม Pagination
เพื่อช่วยลดปริมาณข้อมูลที่แสดงในแต่ละหน้า

สำหรับ Steam Player Data ทีมเพิ่มระบบ Refresh และ Snapshot
เพื่อจัดการข้อมูลที่เปลี่ยนแปลงตลอดเวลาและลดการเรียก API ซ้ำ

---

## 6. Teamwork & Process Learning

ใน Sprint 2 ทีมมีการหมุนเวียน Role ตามที่กำหนด โดยแบ่งเป็น:

| สมาชิก | Role     | Member | Responsibility                                         |
| -------------------- | -------- | ------ | ------------------------------------------------------ |
| นายภานุวัฒน์ ผองแก้ว | Planner  | ฟลุ๊ค  | Planning, Requirements, Architecture และ Documentation |
| นายเดโชชิต โตวินัส | Coder    | ออม    | Web UI, API, Database, Service และ Data Processing     |
| นายชิษณุพงศ์ ซู | Debugger | คิม    | Testing, QA, Error Handling และ Edge Cases             |

ทีมได้เรียนรู้ว่าการแบ่งงานตาม Role
ช่วยให้แต่ละคนมีความรับผิดชอบที่ชัดเจนมากขึ้น

Planner ต้องทำความเข้าใจ Scope และ Requirements
ก่อนส่งต่อให้ Coder

Coder ต้องพัฒนา Code ให้สอดคล้องกับ Requirements
และแบ่ง Module ให้สามารถทำงานร่วมกับส่วนอื่นได้

Debugger ต้องตรวจสอบทั้ง Normal Cases,
Invalid Cases และ Error Cases

การทำงานร่วมกันทำให้ทีมเห็นความสำคัญของการสื่อสาร
ระหว่าง Planning, Development และ Testing
เพื่อให้แต่ละส่วนของระบบสามารถทำงานร่วมกันได้

---

## 7. Technical Learning

### Web UI

เรียนรู้การพัฒนา Web Application และ Dashboard ด้วย Streamlit
รวมถึง Navigation, Pagination, Filter และ Empty State

### API

เรียนรู้ REST API, JSON Response, RAWG API,
Steam API, API Key และ API Error Handling

### SQLite

เรียนรู้การสร้าง Database, การจัดเก็บข้อมูล
และการเชื่อมต่อ Application กับ SQLite

### Data Processing

เรียนรู้ Data Cleaning, Data Normalization
และการจัดรูปแบบข้อมูลจาก API ก่อนนำไปใช้งาน

### Git / GitHub

เรียนรู้การทำงานร่วมกันผ่าน Git/GitHub
และการแบ่งงานระหว่างสมาชิกตาม Role

---

## 8. Instructor / Team Feedback

ใน Sprint 2 ยังไม่มี Instructor Feedback เพิ่มเติม
เนื่องจากเป็นส่วนที่ทีมพัฒนาต่อจาก Feedback ของ Sprint 1

ทีมจึงนำ Feedback จาก Sprint 1
เกี่ยวกับ Project Pitch, Project Plan, Timeline,
Task Allocation, Change Log, Learning Log
และ Contribution Metrics
มาใช้ในการทำงานและปรับปรุง Documentation ของ Project

---

## 9. Lessons Learned

1. Web Application ที่ใช้ External API จำเป็นต้องมี Error Handling และ Empty State เพื่อรองรับกรณี API ไม่สามารถใช้งานได้หรือไม่มีข้อมูล
2. การแยกระบบออกเป็น API, Database, Service, Data Processing และ UI ช่วยให้ Code มีโครงสร้างชัดเจนและสามารถพัฒนาแต่ละส่วนได้ง่ายขึ้น
3. การใช้ Database ช่วยให้ Application สามารถจัดเก็บและจัดการข้อมูลได้อย่างเป็นระบบ
4. API Data อาจมีโครงสร้างและข้อมูลที่ไม่สมบูรณ์ จึงต้องมี Data Processing และ Data Normalization ก่อนนำไปใช้งาน
5. ข้อมูลที่เปลี่ยนแปลงตลอดเวลา เช่น Steam Player Data ต้องมีการจัดการ Refresh และการจัดเก็บ Snapshot
6. Pagination มีความสำคัญเมื่อ Application ต้องแสดงข้อมูลจำนวนมากบน Web UI
7. การทดสอบควรทำควบคู่กับการพัฒนา เพื่อช่วยค้นหา Error และปัญหาจากการเชื่อมต่อระหว่างแต่ละ Module

---

## 10. How We Will Apply This Learning

สิ่งที่เรียนรู้จาก Sprint 2
จะถูกนำไปใช้ในการพัฒนา Sprint ถัดไป โดยเฉพาะ:

* ใช้ Modular Architecture ต่อในการพัฒนา Features ใหม่
* ใช้ Data Processing และ Data Normalization กับข้อมูลที่จะนำมาวิเคราะห์
* ใช้ SQLite และ Service Layer เป็นส่วนหนึ่งของ Data Flow
* ใช้ Error Handling กับ External API และ Database อย่างต่อเนื่อง
* ใช้ Pagination และ Filtering เพื่อปรับปรุง User Experience
* ทำ Automated Testing ควบคู่กับการพัฒนา Features
* ใช้ Git/GitHub Workflow และการแบ่ง Role ต่อเนื่อง
* Update Documentation ให้สอดคล้องกับการพัฒนาในแต่ละ Sprint

---

## 11. Sprint 2 Learning Summary

| Learning Area   | Status    |
| --------------- | --------- |
| Web UI          | ✅ Learned |
| Dashboard       | ✅ Learned |
| API Integration | ✅ Learned |
| SQLite          | ✅ Learned |
| Data Processing | ✅ Learned |
| Testing         | ✅ Learned |
| Teamwork        | ✅ Learned |

---

# 🚀 Sprint 3 — Data Analysis, Visualization & Advanced Features

**Period:** 25–29 September 2026
**Duration:** 5 Days
**Status:** ✅ Completed

## 1. Sprint Overview

Sprint 3 เป็นช่วงที่ทีมพัฒนาต่อยอดจากระบบ Web Application,
API, Database และ Game Service ที่สร้างไว้ใน Sprint 2

เป้าหมายของ Sprint นี้คือการนำข้อมูลเกมที่มีอยู่ในระบบ
มาจัดการ เตรียมข้อมูล วิเคราะห์ และนำเสนอผ่าน Statistics
และ Data Visualization

นอกจากนี้ยังเพิ่มความสามารถในการสำรวจข้อมูลเกม
ผ่าน Advanced Filtering, Sorting และ Game Comparison

**Sprint Goal:**

> พัฒนา Gaming Statistics Dashboard ให้สามารถนำข้อมูลเกม
> มาวิเคราะห์และนำเสนอในรูปแบบ Statistics และ Data Visualization
> พร้อมเพิ่มความสามารถในการสำรวจ เปรียบเทียบ และกรองข้อมูลเกมได้สะดวกขึ้น

**Main Focus:**

* Data Cleaning
* Data Preparation
* Data Normalization
* Exploratory Data Analysis (EDA)
* Statistical Analysis
* Dashboard Statistics
* Data Visualization
* Advanced Filtering
* Advanced Sorting
* Game Comparison
* Integration Testing

---

## 2. What We Did

ใน Sprint 3 ทีมดำเนินงานตามลำดับตั้งแต่
Data Processing ไปจนถึงการแสดงผลบน Dashboard

งานหลักที่ดำเนินการ:

* เตรียมข้อมูลเกมสำหรับการวิเคราะห์
* ตรวจสอบและจัดการข้อมูลที่ไม่สมบูรณ์
* Normalize ข้อมูลจาก RAWG และข้อมูลที่เกี่ยวข้อง
* ทำ Exploratory Data Analysis (EDA)
* เพิ่ม Descriptive Statistics
* เพิ่ม Statistics Dashboard
* เพิ่ม Data Visualization
* เพิ่มการวิเคราะห์ Genre
* เพิ่มการวิเคราะห์ Platform
* เพิ่มการวิเคราะห์ Rating
* เพิ่มการวิเคราะห์ Release Year
* เพิ่มการวิเคราะห์ Metacritic
* เพิ่มการวิเคราะห์ Steam Live Players
* เพิ่ม Advanced Filtering
* เพิ่ม Advanced Sorting
* เพิ่ม Game Comparison
* ตรวจสอบ Empty State
* ตรวจสอบการเชื่อมต่อระหว่าง Analysis และ Dashboard
* ทดสอบ Features และ Integration

---

## 3. What We Learned

### Data Preparation

ทีมได้เรียนรู้ว่าการวิเคราะห์ข้อมูลไม่ควรเริ่มจากการคำนวณ
ทันที แต่ควรเตรียมและตรวจสอบข้อมูลก่อน

ขั้นตอนสำคัญ ได้แก่:

```text
Raw Data
   ↓
Data Cleaning
   ↓
Data Validation
   ↓
Data Preparation
   ↓
Analysis
```

การเตรียมข้อมูลช่วยลดปัญหาที่อาจเกิดขึ้น
จาก Missing Values, Data Type และข้อมูลที่ไม่อยู่ในรูปแบบเดียวกัน

### Exploratory Data Analysis

ทีมได้เรียนรู้ว่า EDA ช่วยให้เข้าใจภาพรวมของ Dataset
ก่อนที่จะสร้าง Statistics และ Visualization

การดู Distribution, Frequency และ Summary Statistics
ช่วยให้เห็นลักษณะของข้อมูลและช่วยเลือกวิธีนำเสนอข้อมูล
ให้เหมาะสมมากขึ้น

### Statistical Analysis

ทีมได้เรียนรู้การใช้ Descriptive Statistics
เพื่อสรุปลักษณะของข้อมูล เช่น:

* Count
* Mean
* Median
* Minimum
* Maximum
* Standard Deviation

และเรียนรู้ว่าการคำนวณ Statistics ต้องพิจารณา
ชนิดของข้อมูลและข้อมูลที่สามารถนำมาคำนวณได้จริง

### Data Visualization

ทีมได้เรียนรู้ว่าการสร้าง Chart
ไม่ใช่เพียงการนำข้อมูลมาแสดงผล
แต่ต้องเลือก Visualization ให้เหมาะสมกับข้อมูล

ตัวอย่างเช่น:

* Genre → Distribution
* Platform → Distribution
* Rating by Genre → Comparison
* Release Year → Distribution
* Metacritic → Distribution
* Steam Players → Ranking / Comparison

### Dashboard Integration

ทีมได้เรียนรู้ว่าการสร้าง Analysis Layer
ต้องคำนึงถึงการนำผลลัพธ์ไปเชื่อมกับ Dashboard
เพื่อให้ข้อมูลที่ผู้ใช้เห็นสอดคล้องกับข้อมูลที่นำมาคำนวณ

---

## 4. Problems & Challenges

### Problem 1 — Data Quality

ข้อมูลจาก External API อาจมีข้อมูลบางส่วนที่ไม่ครบ
หรือมี Data Type ที่ไม่เหมาะกับการคำนวณ

**Impact:**

อาจทำให้ Statistics หรือ Visualization
ไม่สามารถคำนวณหรือแสดงผลได้อย่างถูกต้อง

**Approach:**

ตรวจสอบ Data Type, Missing Values
และเตรียมข้อมูลก่อนนำเข้าสู่ Analysis

---

### Problem 2 — Statistics กับ Dashboard ต้องสอดคล้องกัน

ผลลัพธ์จาก Analysis ต้องสอดคล้องกับข้อมูล
ที่นำมาแสดงบน Dashboard

**Impact:**

หาก Filter หรือ Data Processing ทำงานไม่ตรงกัน
Statistics และ Chart อาจแสดงผลไม่ตรงกับข้อมูลที่ผู้ใช้เลือก

**Approach:**

ตรวจสอบ Data Flow ตั้งแต่ Data Processing
จนถึง Analysis และ Dashboard

---

### Problem 3 — Visualization ต้องรองรับข้อมูลที่ไม่มี

เมื่อผู้ใช้ Filter ข้อมูล อาจไม่มีข้อมูลเหลืออยู่

**Impact:**

Chart หรือ Statistics อาจไม่สามารถแสดงผลได้

**Approach:**

เพิ่ม Empty-State Handling
เพื่อให้ระบบสามารถแจ้งผู้ใช้เมื่อไม่มีข้อมูลที่ตรงกับเงื่อนไข

---

### Problem 4 — การเพิ่ม Features หลายส่วนพร้อมกัน

Sprint 3 มีทั้ง Analysis, Visualization,
Filtering, Sorting และ Comparison

**Impact:**

แต่ละ Feature ต้องทำงานร่วมกับระบบเดิม
โดยไม่ทำให้ Features ที่มีอยู่เดิมเสียหาย

**Approach:**

แบ่งการพัฒนาออกเป็นส่วนย่อย
และใช้ Testing / Integration Testing
เพื่อตรวจสอบการทำงานร่วมกัน

---

## 5. How We Solved Them

ทีมใช้แนวทางแบ่งงานออกเป็น Layer
และตรวจสอบข้อมูลก่อนส่งต่อไปยังขั้นตอนถัดไป

```text
SQLite / API Data
       ↓
Data Processing
       ↓
Data Preparation
       ↓
Analysis / Statistics
       ↓
Visualization
       ↓
Dashboard
```

สำหรับข้อมูลที่ไม่สมบูรณ์
ทีมตรวจสอบและจัดการข้อมูลก่อนนำไปคำนวณ

สำหรับ Statistics
ทีมแยก Logic การวิเคราะห์ออกจาก UI
เพื่อให้สามารถตรวจสอบผลลัพธ์ได้ง่ายขึ้น

สำหรับ Visualization
ทีมตรวจสอบข้อมูลที่ใช้สร้าง Chart
และรองรับกรณีที่ไม่มีข้อมูล

สำหรับ Advanced Features
ทีมตรวจสอบ Filter, Sort และ Comparison
ร่วมกับ Dashboard เพื่อให้การทำงานสอดคล้องกัน

---

## 6. Teamwork & Process Learning

Sprint 3 มีการหมุนเวียน Role ของสมาชิกดังนี้:

| สมาชิก               | ชื่อเล่น | Role     | หน้าที่หลัก                                                                                   |
| -------------------- | -------- | -------- | --------------------------------------------------------------------------------------------- |
| นายเดโชชิต โตวินัส   | ออม      | Planner  | กำหนด Sprint Goal, Scope, Requirements, Definition of Done, แบ่งงาน และติดตามความคืบหน้า      |
| นายชิษณุพงศ์ ซู      | คิม      | Coder    | พัฒนา Data Processing, Analysis, Statistics, Visualization และ Advanced Features              |
| นายภานุวัฒน์ ผองแก้ว | ฟลุ๊ค    | Debugger | ทดสอบ Data Quality, Statistics, Visualization, Filtering, Sorting, Comparison และ Integration |

ทีมได้เรียนรู้ว่าการหมุนเวียน Role
ทำให้สมาชิกได้เข้าใจงานในมุมมองที่แตกต่างกัน

Planner ต้องเข้าใจทั้ง Requirements และผลลัพธ์ที่ต้องการ

Coder ต้องเข้าใจทั้ง Data Flow และผลกระทบของการแก้ไข Code

Debugger ต้องเข้าใจ Requirements เพื่อสามารถตรวจสอบ
ว่าระบบทำงานตรงตามที่กำหนดหรือไม่

---

## 7. Technical Learning

### Data Processing

เรียนรู้การเตรียมข้อมูลก่อนนำไปวิเคราะห์
รวมถึงการจัดการ Data Type, Missing Values
และข้อมูลที่มีรูปแบบแตกต่างกัน

### EDA

เรียนรู้การสำรวจ Dataset
เพื่อทำความเข้าใจ Distribution, Frequency
และลักษณะของข้อมูลก่อนทำ Statistics

### Statistics

เรียนรู้การคำนวณ Descriptive Statistics
และการเลือกข้อมูลที่เหมาะสมสำหรับการคำนวณ

### Visualization

เรียนรู้การเลือก Chart ให้เหมาะสมกับข้อมูล
และตรวจสอบความถูกต้องของข้อมูลที่นำไปแสดงผล

### Filtering & Sorting

เรียนรู้การเพิ่มเงื่อนไขการค้นหาและการจัดเรียงข้อมูล
โดยต้องคำนึงถึง Missing Values และ Data Types

### Game Comparison

เรียนรู้การนำข้อมูลของเกมหลายรายการมาเปรียบเทียบ
ผ่านตัวแปรที่ระบบรองรับ

### Testing

เรียนรู้การทดสอบ Features ที่เชื่อมต่อกันหลาย Module
แทนการทดสอบเฉพาะ Function ใด Function หนึ่ง

---

## 8. Instructor / Team Feedback

ใน Sprint 3 เน้นการนำ Requirements
และ Feedback จาก Sprint ก่อนหน้ามาปรับใช้กับการพัฒนา

ทีมให้ความสำคัญกับ:

* Scope Control
* Task Allocation
* Definition of Done
* Data Quality
* Testing
* Documentation

หากมี Instructor Feedback เพิ่มเติมหลังการ Review
สามารถ Update ในส่วนนี้ได้

---

## 9. Lessons Learned

สิ่งสำคัญที่ทีมได้เรียนรู้จาก Sprint 3:

1. Data Analysis ที่ดีต้องเริ่มจาก Data Preparation
2. EDA ช่วยให้เข้าใจ Dataset ก่อนทำ Statistical Analysis
3. Statistics ต้องคำนวณจากข้อมูลที่ผ่านการตรวจสอบแล้ว
4. Visualization ต้องเลือกให้เหมาะสมกับชนิดและวัตถุประสงค์ของข้อมูล
5. Filter และ Sorting ต้องคำนึงถึง Data Type และ Missing Values
6. Dashboard ที่มีหลาย Feature ต้องตรวจสอบ Integration ระหว่าง Module
7. Empty State เป็นส่วนสำคัญของ Data-driven Application
8. การแยก Analysis Logic ออกจาก UI ช่วยให้พัฒนาและทดสอบได้ง่ายขึ้น
9. การทดสอบควรครอบคลุมทั้ง Individual Features และ Integration
10. Documentation ควร Update ให้ตรงกับสิ่งที่พัฒนาจริงหลังจบ Sprint

---

## 10. How We Will Apply This Learning

ความรู้จาก Sprint 3 จะถูกนำไปใช้ใน Final Sprint
โดยเฉพาะ:

* ตรวจสอบระบบทั้งหมดแบบ End-to-End
* ตรวจสอบ Data Flow ตั้งแต่ API / Database ถึง Dashboard
* ทำ Regression Testing
* ตรวจสอบ Edge Cases
* ปรับปรุง Error Handling
* ตรวจสอบความถูกต้องของ Statistics และ Visualization
* ตรวจสอบ Documentation ให้สอดคล้องกับ Source Code
* เตรียม Project สำหรับ Final Presentation

---

## 11. Sprint 3 Learning Summary

| Learning Area             | Status    |
| ------------------------- | --------- |
| Data Processing           | ✅ Learned |
| Data Cleaning             | ✅ Learned |
| Data Preparation          | ✅ Learned |
| Exploratory Data Analysis | ✅ Learned |
| Statistical Analysis      | ✅ Learned |
| Data Visualization        | ✅ Learned |
| Advanced Filtering        | ✅ Learned |
| Advanced Sorting          | ✅ Learned |
| Game Comparison           | ✅ Learned |
| Dashboard Integration     | ✅ Learned |
| Testing                   | ✅ Learned |
| Teamwork                  | ✅ Learned |
| Documentation             | ✅ Learned |

---

# Final Sprint — Integration, Reliability and Delivery

**ช่วงตามแผน:** 2–6 October 2026
**รอบตรวจส่งมอบ:** 13 October 2026

## สิ่งที่ตรวจและปรับปรุง

รอบตรวจครอบคลุม API clients, SQLite, normalization, service, UI, statistics, config, import scripts, tests, CI และเอกสาร โดยยืนยันพฤติกรรมจาก tests และ source ปัจจุบัน

- แยก RAWG popularity cache 24 ชั่วโมงจาก Steam player cache 15 นาที
- ดึงผู้พัฒนาเฉพาะ Details และ cache ผลว่างที่สำเร็จด้วย
- เก็บคะแนนที่ยังไม่มีค่าเฉลี่ยเป็น missing แทนการตีความว่าได้คะแนน 0
- ใช้ SQL LIMIT ก่อนแปลง records และใช้ DataFrame ร่วมกันใน Statistics
- ปิด connections หลัง transaction และตรวจ rollback
- ใช้พาธจากตำแหน่งไฟล์แทน current working directory
- ตรวจชุดไฟล์ส่งมอบที่ไม่มี .env หรือ virtualenv และรวม source ที่ tests ต้องใช้

## บทเรียนจากผลตรวจ

| ประเด็น | บทเรียน |
|:--|:--|
| จำนวน requests | Parallel ลดเวลารอ แต่ไม่ลดจำนวนคำขอ; lazy loading ลดคำขอที่ไม่จำเป็น |
| Missing values | 0, None และผลว่างจาก API ไม่ได้มีความหมายเดียวกัน |
| Cache | ต้องแยกผลสำเร็จที่ว่างจากคำขอล้มเหลว เพื่อให้ retry ถูกจังหวะ |
| Data loading | Pagination ใน UI ยังช้าได้หาก query/decode ทั้งฐานก่อนแบ่งหน้า |
| SQLite | Connection context จัดการ transaction แต่ต้องปิด connection ด้วย |
| Paths/imports | ต้องตรวจทั้ง package mode และ script mode จากโฟลเดอร์อื่น |
| Repository | Tests ผ่านในเครื่องไม่พอ หากต้องใช้ไฟล์ที่ไม่รวมใน Git |
| Documentation | ควรมีแหล่งเดียวสำหรับผล QA และแยกแผนเดิมจากสิ่งที่ตรวจแล้ว |

## การนำไปใช้ต่อ

เริ่มจากอ่านเส้นทางข้อมูลจริง วัดงานที่ช้า แก้เฉพาะจุดที่มีหลักฐาน แล้วใช้ regression tests ตรวจผล การตรวจ clean checkout ช่วยพบ dependency ที่ถูกซ่อนไว้ในเครื่องนักพัฒนา

ผล QA และขอบเขตที่ตรวจอยู่ใน [Final QA](FINAL_QA.md) รายละเอียดงานอยู่ใน [Final Sprint](<../Final Sprint/Final_Sprint.md>) การ commit/push, presentation และ submission ไม่ได้ถูกยืนยันว่าดำเนินการแล้วในรอบนี้

## สรุป

Sprint 1–3 ให้พื้นฐาน CLI, Web/API/SQLite และ Analysis/Visualization ส่วนรอบ final เพิ่ม reliability, request efficiency, performance และเอกสารใช้งานที่ทำตามได้ บันทึกประวัติด้านบนเก็บตามช่วงเดิม; ใช้ [README](../README.md) สำหรับพฤติกรรมปัจจุบัน
