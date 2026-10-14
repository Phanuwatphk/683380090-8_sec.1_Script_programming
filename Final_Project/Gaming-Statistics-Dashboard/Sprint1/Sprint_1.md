# 🎮 Gaming Statistics Dashboard — Sprint 1 Report

> บันทึกประวัติตามช่วง Sprint: โครงสร้างและพฤติกรรมบางส่วนเปลี่ยนในรุ่นส่งมอบ ให้ใช้ [README](../README.md) สำหรับการติดตั้ง/ใช้งานปัจจุบัน และ [Final QA](../docs/FINAL_QA.md) สำหรับผลตรวจล่าสุด

## Final Term Project — CP352301 Script Programming

**Sprint:** Sprint 1 — Application Foundation  
**Period:** Week 12  
**Presentation:** 15–16 September 2026  
**Due Date:** 18 September 2026  
**Status:** ✅ Completed

**Repository:** https://github.com/Phanuwatphk/Gaming-Statistics-Dashboard

**Pull Request:** https://github.com/Phanuwatphk/Gaming-Statistics-Dashboard/pull/2


---

# 1. Sprint Overview

Sprint 1 เป็น Sprint แรกของโปรเจกต์ Gaming Statistics Dashboard
มีเป้าหมายเพื่อสร้าง Foundation ของระบบ และทดสอบโครงสร้างการทำงานหลัก
ก่อนนำไปพัฒนาเป็น Web Application ใน Sprint ถัดไป

ใน Sprint นี้ทีมพัฒนา Application ในรูปแบบ **Command Line Interface (CLI)**
เพื่อสร้างและทดสอบโครงสร้างพื้นฐานของระบบ เช่น Menu Navigation,
User Input, Input Validation, Search และ Statistics

Sprint 1 ยังไม่เชื่อมต่อ RAWG API, SQLite หรือ Web UI จริง
โดยใช้ Local Sample Dataset สำหรับการพัฒนาและทดสอบระบบ

---

# 2. Sprint Goal

> สร้าง Application Foundation ของ Gaming Statistics Dashboard
> ที่สามารถรับ Input จากผู้ใช้ แสดงข้อมูลเกม ค้นหาเกม
> แสดง Statistics และจัดการ Input ที่ไม่ถูกต้องได้อย่างปลอดภัย

เมื่อจบ Sprint 1 ระบบสามารถ:

- เริ่มต้น Application ได้
- แสดง Welcome Message
- แสดง Main Menu
- รับ Menu Input
- แสดงข้อมูลเกม
- ค้นหาเกม
- แสดง Statistics
- แสดง Genre
- แสดง Top Rated Games
- ตรวจสอบ Input ที่ไม่ถูกต้อง
- กลับไปยัง Main Menu
- ออกจาก Application อย่างถูกต้อง

---

# 3. Team Members & Roles

| สมาชิก | ชื่อเล่น | Role | หน้าที่หลัก |
|---| --- |---|---|
| นายชิษณุพงศ์ ซู | คิม | Planner | Planning, Requirements, Scope และ Documentation |
| นายภานุวัฒน์ ผองแก้ว | ฟลุ๊ค | Coder | Application Development และ Implementation |
| นายเดโชชิต โตวินัส | ออม | Debugger | Testing, QA, Edge Cases และ Bug Verification |

> Role ดังกล่าวเป็น Role ที่ใช้ในการทำงานของ Sprint 1
> โดยสมาชิกสามารถหมุนเวียน Role ใน Sprint ถัดไปได้

---

# 4. Sprint 1 Scope

## In Scope

สิ่งที่พัฒนาใน Sprint 1:

- Command Line Interface (CLI)
- Welcome Message
- Main Menu
- Menu Navigation
- User Input
- Input Validation
- Exception Handling
- View Games
- Search Game
- View Statistics
- View Genres
- View Top Rated Games
- Local Sample Dataset
- QA Testing
- Edge Case Testing

## Out of Scope

สิ่งที่ยังไม่พัฒนาใน Sprint 1:

- RAWG API Integration
- SQLite Database
- Web UI
- Streamlit Dashboard
- Advanced Data Processing
- Advanced Search / Filter / Sort
- Automated Testing
- GitHub Actions
- CI/CD
- AI Integration

---

# 5. Sprint 1 Functional Requirements

## FR-01 — Welcome Message

เมื่อเริ่มต้น Application
ระบบต้องแสดงข้อความต้อนรับผู้ใช้

---

## FR-02 — Main Menu

ระบบต้องแสดง Main Menu พร้อมตัวเลือก:

```text
1. View Games
2. Search Game
3. View Statistics
4. View Genres
5. View Top Rated Games
0. Exit
````

---

## FR-03 — Menu Input

ระบบต้องรับค่าตัวเลือกจากผู้ใช้
และตรวจสอบว่าค่าที่รับเข้ามาอยู่ในช่วงที่ระบบรองรับ

---

## FR-04 — Input Validation

ระบบต้องสามารถจัดการ Input ที่ไม่ถูกต้อง เช่น:

* Blank Input
* Non-numeric Input
* Negative Number
* Number นอกช่วงที่กำหนด
* Invalid Input

โดย Application ต้องไม่ Crash

---

## FR-05 — Search Game

ระบบต้องสามารถ:

* รับชื่อเกมจากผู้ใช้
* ค้นหาแบบ Case-insensitive
* ค้นหาแบบ Partial Match
* แจ้งเตือนเมื่อไม่พบเกม
* ป้องกัน Empty Search

---

## FR-06 — Return to Main Menu

หลังจากทำ Function เสร็จ
ระบบต้องสามารถกลับไปยัง Main Menu ได้

---

## FR-07 — Safe Exit

เมื่อผู้ใช้เลือก `0`
ระบบต้องออกจาก Application อย่างถูกต้อง

---

# 6. Local Sample Dataset

เนื่องจาก Sprint 1 ยังไม่เชื่อมต่อ RAWG API
จึงใช้ Local Sample Dataset จำนวน 8 เกม

| Game                | Rating | Genre      | Platform        |
| ------------------- | -----: | ---------- | --------------- |
| Portal 2            |    4.6 | Puzzle     | PC              |
| The Witcher 3       |    4.8 | RPG        | PC              |
| Minecraft           |    4.5 | Sandbox    | Multi-platform  |
| Hades               |    4.7 | Action     | Nintendo Switch |
| God of War          |    4.7 | Action     | PlayStation     |
| Stardew Valley      |    4.4 | Simulation | PC              |
| Mario Kart 8 Deluxe |    4.5 | Racing     | Nintendo Switch |
| Baldur's Gate 3     |    4.9 | RPG        | PC              |

---

# 7. Application Flow

โครงสร้างการทำงานของ Sprint 1:

```text
User
  ↓
CLI Application
  ↓
Main Menu
  ↓
Input Validation
  ↓
Selected Function
  ↓
Local Sample Dataset
  ↓
Display Result
  ↓
Return to Main Menu
```

---

# 8. Main Functions

ระบบ Sprint 1 แบ่ง Function ตามหน้าที่หลักดังนี้:

| Function                    | Responsibility           |
| --------------------------- | ------------------------ |
| `display_welcome_message()` | แสดงข้อความต้อนรับ       |
| `display_main_menu()`       | แสดง Main Menu           |
| `get_menu_choice()`         | รับและตรวจสอบ Menu Input |
| `view_games()`              | แสดงข้อมูลเกม            |
| `search_game()`             | ค้นหาเกม                 |
| `view_statistics()`         | แสดง Statistics          |
| `view_genres()`             | แสดง Genre               |
| `view_top_games()`          | แสดงเกมที่มี Rating สูง  |
| `main()`                    | ควบคุม Main Program Flow |

การแยก Function ตามหน้าที่ช่วยให้ Code สามารถอ่าน,
ทดสอบ และแก้ไขได้ง่ายขึ้น

---

# 9. Sprint 1 Work Plan

## Phase 1 — Planning

### Planner — คิม (นายชิษณุพงศ์ ซู)

* กำหนด Sprint Goal
* กำหนด Scope
* กำหนด Functional Requirements
* กำหนด Definition of Done
* ออกแบบ CLI Flow
* กำหนด Main Menu
* กำหนด Local Sample Dataset
* จัดทำ Documentation

### Coder — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

* ตรวจสอบ Requirements
* ตรวจสอบความเป็นไปได้ของโครงสร้าง CLI
* วางโครงสร้าง Function

### Debugger — ออม (นายเดโชชิต โตวินัส)

* ตรวจสอบ Requirements
* ระบุ Edge Cases
* เตรียม Test Cases
* วางแนวทาง QA

---

# 10. Development Phase

## Coder — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

พัฒนา:

* Main Program
* Main Menu
* Menu Navigation
* View Games
* Search Game
* Statistics
* Genres
* Top Rated Games
* Input Validation
* Exception Handling

## Planner — คิม (นายชิษณุพงศ์ ซู)

* ตรวจสอบ Scope
* ตรวจสอบ Requirements
* ติดตามความคืบหน้า
* ตรวจสอบ Documentation
* ตรวจสอบว่า Implementation สอดคล้องกับ Sprint Goal

## Debugger — ออม (นายเดโชชิต โตวินัส)

* ตรวจสอบ Function ที่พัฒนา
* เตรียม Test Cases
* ทดสอบ Normal Cases
* ทดสอบ Invalid Inputs
* ทดสอบ Edge Cases

---

# 11. Sprint 1 Daily Task Allocation & Update

Sprint 1 ดำเนินงานระหว่างวันที่ **10–15 กันยายน 2569**
โดยแบ่งงานตาม Role ของสมาชิก และมีการ Update ความคืบหน้าในแต่ละวันดังนี้

| วันที่ | Planner — คิม (นายชิษณุพงศ์ ซู) | Coder — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว) | Debugger — ออม (นายเดโชชิต โตวินัส) | Daily Update |
|---|---|---|---|---|
| **10 ก.ย. 2569** | กำหนด Sprint Goal, Scope และ Requirements | ศึกษา Requirements และวางโครงสร้าง Code | วิเคราะห์ Test Cases และ Edge Cases ที่ต้องทดสอบ | **เริ่ม Sprint 1 และกำหนดขอบเขตการทำงานของทีม** |
| **11 ก.ย. 2569** | ออกแบบ CLI Flow, Main Menu และกำหนด Local Dataset | เตรียมโครงสร้าง Function และ Main Program | ออกแบบแนวทางการทดสอบ Function และ Input Validation | **ได้โครงสร้างการทำงานของ CLI และแนวทางการพัฒนา** |
| **12 ก.ย. 2569** | ตรวจสอบ Scope และติดตามความคืบหน้าการพัฒนา | พัฒนา Main Menu, Navigation และ View Games | ตรวจสอบ Function ที่พัฒนาและเริ่มทดสอบการทำงาน | **เริ่มได้ CLI Foundation และสามารถแสดงข้อมูลเกมได้** |
| **13 ก.ย. 2569** | ตรวจสอบ Requirements และปรับรายละเอียด Sprint Documentation | พัฒนา Search, Statistics, Genres และ Top Rated Games | ทดสอบ Core Features และตรวจสอบผลลัพธ์ | **Core Features ของ Sprint 1 เริ่มทำงานครบตาม Scope** |
| **14 ก.ย. 2569** | ตรวจสอบ Definition of Done และเตรียมเอกสาร Sprint Report | ปรับปรุง Input Validation และแก้ไข Bug จากการทดสอบ | ทดสอบ Invalid Input และ Edge Cases ทั้งหมด | **ระบบผ่านการทดสอบด้าน Input Validation และ Edge Cases** |
| **15 ก.ย. 2569** | สรุปผล Sprint, จัดทำ Documentation และเตรียมการนำเสนอ | ตรวจสอบ Code และเตรียม Version สำหรับส่งมอบ | สรุป QA Result และตรวจสอบ Test Cases รอบสุดท้าย | **สรุปผล Sprint 1, ตรวจสอบงานร่วมกัน และเตรียมส่งมอบ/นำเสนอ** |

---

## Daily Update Summary

### 📅 10 กันยายน 2569 — Planning

**Update:**
- กำหนดเป้าหมายของ Sprint 1
- กำหนด Scope และ Out of Scope
- กำหนด Functional Requirements
- แบ่ง Role ของสมาชิกเป็น Planner, Coder และ Debugger
- กำหนดแนวทางการทดสอบเบื้องต้น

**สถานะ:** 🟡 Planning Started

---

### 📅 11 กันยายน 2569 — Design

**Update:**
- ออกแบบโครงสร้าง CLI
- กำหนด Main Menu
- กำหนด Local Sample Dataset
- ออกแบบ Function หลัก
- กำหนด Test Cases และ Edge Cases

**สถานะ:** 🟡 Design Completed

---

### 📅 12 กันยายน 2569 — CLI Foundation

**Update:**
- เริ่มพัฒนา Main Program
- เพิ่ม Welcome Message
- เพิ่ม Main Menu
- เพิ่ม Menu Navigation
- เพิ่ม View Games
- เริ่มทดสอบการทำงานของ CLI

**สถานะ:** 🟡 Core Foundation In Progress

---

### 📅 13 กันยายน 2569 — Core Features

**Update:**
- เพิ่ม Search Game
- เพิ่ม View Statistics
- เพิ่ม View Genres
- เพิ่ม View Top Rated Games
- ทดสอบการทำงานของแต่ละ Feature

**สถานะ:** 🟡 Core Features Completed

---

### 📅 14 กันยายน 2569 — Validation & QA

**Update:**
- เพิ่มและปรับปรุง Input Validation
- จัดการ Non-numeric Input
- จัดการ Blank Input
- จัดการ Negative Input
- จัดการ Out-of-range Input
- ทดสอบ Empty Search
- ทดสอบ Unknown Game
- ตรวจสอบ Edge Cases
- แก้ไขปัญหาที่พบจากการทดสอบ

**สถานะ:** 🟢 QA In Progress

---

### 📅 15 กันยายน 2569 — Review & Handoff

**Update:**
- ทดสอบระบบรอบสุดท้าย
- ตรวจสอบ Test Cases ทั้งหมด
- สรุป QA Result
- ตรวจสอบ Definition of Done
- จัดทำ Sprint 1 Documentation
- ตรวจสอบ Code และ Repository
- เตรียมการนำเสนอ Sprint 1
- เตรียมส่งมอบงานผ่าน GitHub

**สถานะ:** 🟢 Sprint 1 Ready for Review / Handoff

---

## Sprint 1 Progress

```text
10 Sep  → Planning
11 Sep  → Design
12 Sep  → CLI Foundation
13 Sep  → Core Features
14 Sep  → Validation & QA
15 Sep  → Review & Handoff
```

---

# 12. Implemented Features

## 12.1 View Games

แสดงข้อมูลเกมทั้งหมดจาก Local Sample Dataset

จำนวนเกมทั้งหมด:

```text
8 Games
```

---

## 12.2 Search Game

รองรับ:

* Full Name
* Partial Name
* Case-insensitive Search

ตัวอย่าง:

```text
Search: Portal
→ Portal 2
```

และ:

```text
Search: portal
→ Portal 2
```

---

## 12.3 View Statistics

จาก Dataset จำนวน 8 เกม:

```text
Total Games     : 8
Average Rating  : 4.64
Highest Rating  : 4.9
```

เกมที่มี Rating สูงสุด:

```text
Baldur's Gate 3 — 4.9
```

---

## 12.4 View Genres

ระบบสามารถแสดง Genre ที่มีอยู่ใน Dataset

ตัวอย่าง:

```text
Action
Puzzle
RPG
Sandbox
Simulation
Racing
```

---

## 12.5 View Top Rated Games

ระบบสามารถเรียงเกมตาม Rating จากสูงไปต่ำ
และแสดงเกมที่มี Rating สูงสุด

---

# 13. Input Validation

ระบบถูกออกแบบให้รองรับ Input ที่ผิดพลาด
โดยไม่ทำให้ Application Crash

## Case 1 — Blank Menu Input

```text
Input:
[Enter]

Expected:
Warning message และกลับไปให้ผู้ใช้เลือกใหม่
```

## Case 2 — Non-numeric Input

```text
Input:
abc

Expected:
แจ้งเตือน Invalid Input และ Application ไม่ Crash
```

## Case 3 — Out-of-range Input

```text
Input:
99

Expected:
แจ้งเตือน Invalid Choice
```

## Case 4 — Negative Input

```text
Input:
-1

Expected:
แจ้งเตือน Invalid Choice
```

## Case 5 — Empty Search

```text
Search:
[Enter]

Expected:
แจ้งเตือนให้กรอกชื่อเกม
```

## Case 6 — Unknown Game

```text
Search:
XYZXYZ

Expected:
Game not found
```

---

# 14. QA Test Cases

Sprint 1 มี Test Cases ทั้งหมด **14 Cases**

|  # | Test Case         | Expected Result            | Status |
| -: | ----------------- | -------------------------- | ------ |
|  1 | Application Start | แสดง Welcome และ Main Menu | ✅ PASS |
|  2 | View Games        | แสดงเกมทั้งหมด 8 เกม       | ✅ PASS |
|  3 | Search `Portal`   | พบ Portal 2                | ✅ PASS |
|  4 | Search `portal`   | พบ Portal 2                | ✅ PASS |
|  5 | View Statistics   | แสดง Statistics ถูกต้อง    | ✅ PASS |
|  6 | View Genres       | แสดง Genre ถูกต้อง         | ✅ PASS |
|  7 | View Top Games    | เรียง Rating จากสูงไปต่ำ   | ✅ PASS |
|  8 | Input `99`        | แจ้ง Invalid Choice        | ✅ PASS |
|  9 | Input `-1`        | แจ้ง Invalid Choice        | ✅ PASS |
| 10 | Input `abc`       | ไม่เกิด Crash              | ✅ PASS |
| 11 | Blank Menu Input  | แจ้งเตือนและรับใหม่        | ✅ PASS |
| 12 | Empty Search      | แจ้งเตือน                  | ✅ PASS |
| 13 | Search `XYZXYZ`   | แสดง Game not found        | ✅ PASS |
| 14 | Input `0`         | ออกจาก Application         | ✅ PASS |

---

# 15. QA Summary

จากการทดสอบ Sprint 1:

```text
Total Test Cases : 14
Passed           : 14
Failed           : 0
Critical Bugs    : 0
```

### Test Pass Rate

```text
14 / 14 × 100 = 100%
```

ผลการทดสอบแสดงว่า Function ที่กำหนดไว้สำหรับ Sprint 1
สามารถทำงานตาม Expected Result และ Application สามารถจัดการ
Input ที่ไม่ถูกต้องได้โดยไม่ Crash

---

# 16. Contribution Matrix — Member Performance

ส่วนนี้ใช้สำหรับประเมินการทำงานของสมาชิกแต่ละคน
โดยพิจารณาจากงานที่ได้รับผิดชอบและผลลัพธ์ที่ส่งมอบใน Sprint 1

**เกณฑ์คะแนน:** งานแต่ละส่วนเต็ม 10 คะแนน

* 10 = ทำครบตามหน้าที่และส่งมอบงานเรียบร้อย
* 8–9 = ทำได้เกือบครบ มีการแก้ไขหรือปรับปรุงเล็กน้อย
* 6–7 = ทำได้บางส่วน แต่ยังต้องมีการช่วยเหลือหรือแก้ไขเพิ่มเติม
* 1–5 = ทำงานไม่ครบตามหน้าที่
* 0 = ไม่ได้ดำเนินงานในส่วนดังกล่าว

---

## 16.1 Planner — คิม (นายชิษณุพงศ์ ซู)

| งานที่รับผิดชอบ            | รายละเอียด                                           |     คะแนน |
| -------------------------- | ---------------------------------------------------- | --------: |
| Project / Sprint Planning  | กำหนด Goal, Scope และแนวทางการทำงาน                  | **10/10** |
| Requirements & DoD         | กำหนด Functional Requirements และ Definition of Done | **10/10** |
| Project Documentation      | จัดทำและปรับปรุง Project Documentation               | **10/10** |
| Timeline & Task Allocation | จัดทำ Project Timeline และแบ่งงานตามหน้าที่          | **10/10** |
| Review & Feedback          | ตรวจสอบงานและนำ Feedback มาปรับปรุง Documentation    | **10/10** |
| **Total**                  |                                                      | **50/50** |

### Planner Contribution

รับผิดชอบด้านการวางแผนและ Documentation ของ Sprint
รวมถึงการประสานงานและตรวจสอบให้งานที่พัฒนาสอดคล้องกับ Scope
และ Sprint Goal

---

## 16.2 Coder — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

| งานที่รับผิดชอบ               | รายละเอียด                                                 |     คะแนน |
| ----------------------------- | ---------------------------------------------------------- | --------: |
| CLI Foundation                | พัฒนาโครงสร้างหลักของ CLI                                  | **10/10** |
| Main Menu & Navigation        | พัฒนา Menu และ Main Program Flow                           | **10/10** |
| Core Features                 | View Games, Search, Statistics, Genres และ Top Rated Games | **10/10** |
| Input Validation              | จัดการ Blank, Non-numeric, Negative และ Invalid Input      | **10/10** |
| Code Improvement & Bug Fixing | ปรับปรุง Code และแก้ปัญหาจากการทดสอบ                       | **10/10** |
| **Total**                     |                                                            | **50/50** |

### Coder Contribution

รับผิดชอบการพัฒนา Source Code หลักของ Sprint 1
ตั้งแต่โครงสร้าง CLI ไปจนถึง Core Features และ Input Validation

---

## 16.3 Debugger — ออม (นายเดโชชิต โตวินัส)

| งานที่รับผิดชอบ    | รายละเอียด                         |     คะแนน |
| ------------------ | ---------------------------------- | --------: |
| Test Case Design   | ออกแบบ Test Cases สำหรับ Sprint 1  | **10/10** |
| Functional Testing | ทดสอบ Function หลักของ Application | **10/10** |
| Edge Case Testing  | ทดสอบ Invalid Input และ Edge Cases | **10/10** |
| Bug Verification   | ตรวจสอบ Bug และผลลัพธ์หลังแก้ไข    | **10/10** |
| QA Report          | สรุปผลการทดสอบและจัดทำ QA Summary  | **10/10** |
| **Total**          |                                    | **50/50** |

### Debugger Contribution

รับผิดชอบการทดสอบระบบและตรวจสอบความถูกต้องของ Application
โดยครอบคลุมทั้ง Normal Cases, Invalid Inputs และ Edge Cases

---

# 17. Contribution Summary

| สมาชิก | ชื่อเล่น | Role     | คะแนนที่ได้รับ | คะแนนเต็ม | Completion |
| --------- | --- | -------- | -------------: | --------: | ---------: |
| นายชิษณุพงศ์ ซู | คิม | Planner  |             50 |        50 |   **100%** |
| นายภานุวัฒน์ ผองแก้ว | ฟลุ๊ค | Coder    |             50 |        50 |   **100%** |
| นายเดโชชิต โตวินัส | ออม | Debugger |             50 |        50 |   **100%** |

### Team Contribution

```text
Planner  : 50/50
Coder    : 50/50
Debugger : 50/50

Total Team Score = 150/150
Team Completion  = 100%
```

---

# 18. Definition of Done

Sprint 1 ถือว่าเสร็จเมื่อ:

### Application

* [x] CLI สามารถเริ่มทำงานได้
* [x] Welcome Message ทำงานได้
* [x] Main Menu ทำงานได้
* [x] Menu Navigation ทำงานได้
* [x] View Games ทำงานได้
* [x] Search Game ทำงานได้
* [x] View Statistics ทำงานได้
* [x] View Genres ทำงานได้
* [x] View Top Rated Games ทำงานได้
* [x] Exit ทำงานได้

### Input Validation

* [x] Blank Input
* [x] Non-numeric Input
* [x] Negative Input
* [x] Out-of-range Input
* [x] Empty Search
* [x] Unknown Game
* [x] Case-insensitive Search

### Code Quality

* [x] แยก Function ตามหน้าที่
* [x] Function มีชื่อที่สื่อความหมาย
* [x] มี Docstring
* [x] มี Exception Handling
* [x] Code สามารถอ่านและแก้ไขต่อได้

### QA

* [x] Normal Case Testing
* [x] Invalid Input Testing
* [x] Edge Case Testing
* [x] Application ไม่ Crash
* [x] QA Result ถูกบันทึก

### Documentation

* [x] Project Pitch
* [x] Project Plan
* [x] Sprint 1 Report
* [x] Contribution Matrix
* [x] QA Summary
* [x] Wow!
* [x] Whoops!

### GitHub / Handoff

* [x] GitHub Repository
* [x] Code ถูกจัดเก็บใน Repository
* [x] Pull Request สำหรับ Sprint 1
* [x] ใส่ Pull Request URL ในเอกสาร

---

# 19. Wow! — สิ่งที่ทำได้ดี

### 1. Modular CLI Structure

ระบบถูกแบ่งออกเป็น Function ตามหน้าที่
ทำให้สามารถอ่าน Code และแก้ไขแต่ละส่วนได้ง่าย

### 2. Input Validation

ระบบสามารถจัดการ Input ที่ไม่ถูกต้องได้หลายรูปแบบ
โดยไม่ทำให้ Application Crash

### 3. Search Function

Search รองรับทั้ง Case-insensitive และ Partial Search
ทำให้ผู้ใช้สามารถค้นหาเกมได้สะดวกขึ้น

### 4. QA Coverage

ทีมทดสอบทั้ง Normal Cases และ Invalid / Edge Cases
รวมทั้งหมด 14 Test Cases

### 5. Clear Sprint Scope

ทีมสามารถกำหนดขอบเขตของ Sprint 1
โดยยังไม่ดึง API, Database หรือ Web UI เข้ามาปนกับงานของ Sprint นี้

---

# 20. Whoops! — ปัญหาและการแก้ไข

## Problem

ในช่วงเริ่มต้นของการพัฒนา
การรับ Menu Input ที่เป็น Non-numeric เช่น:

```text
abc
```

สามารถทำให้เกิด `ValueError`

## Cause

การแปลง Input เป็น Integer โดยตรง
โดยยังไม่มีการจัดการ Exception

## Solution

เพิ่ม `try-except` เพื่อจัดการ `ValueError`
และเพิ่มการตรวจสอบ:

* Blank Input
* Numeric Range
* Negative Number
* Invalid Choice

## Result

หลังจากปรับปรุงแล้ว:

```text
abc
↓
Invalid Input
↓
Application ยังทำงานต่อ
↓
กลับไป Main Menu
```

Application ไม่ Crash จาก Input ประเภทดังกล่าว

---

# 21. Sprint Review

หลังจากพัฒนาและทดสอบ Sprint 1
ทีมตรวจสอบผลลัพธ์เทียบกับ Sprint Goal

### Sprint Goal

> สร้าง Application Foundation ที่สามารถรับ Input,
> แสดงข้อมูลเกม, ค้นหาเกม, แสดง Statistics
> และจัดการ Invalid Input ได้

### Result

**Sprint Goal: Achieved ✅**

ระบบสามารถทำงานตามขอบเขตที่กำหนดไว้ใน Sprint 1
และผ่าน Test Cases ที่วางแผนไว้ทั้งหมด

---

# 22. Instructor Feedback & Improvement

หลังจากนำเสนอ Sprint 1
ทีมได้รับ Feedback จากอาจารย์ให้ปรับปรุงและเพิ่มเติม
ในส่วนของ Project Pitch, Plan, Documentation และ Metrics

ทีมจึงดำเนินการแก้ไขและเพิ่มเติมดังนี้

---

## 22.1 Project Pitch

### Feedback

เพิ่มคำอธิบาย Project ให้ชัดเจนขึ้น เช่น:

* รูปแบบของ Application
* วิธีการใช้งาน
* เครื่องมือที่ใช้
* Architecture
* Data Source
* แนวทางการพัฒนา

### สิ่งที่กลุ่มแก้ไข

ปรับ `docs/Project_Pitch.md` ให้ระบุชัดเจนว่า:

* Final Project เป็น **Web Application**
* ผู้ใช้สามารถเข้าถึงระบบผ่าน **Web Browser**
* ใช้ **Python** เป็นภาษาหลัก
* ใช้ **Streamlit** สำหรับ Web Dashboard
* ใช้ **RAWG API** เป็น External Data Source
* ใช้ **Pandas** สำหรับ Data Processing
* ใช้ **SQLite** สำหรับ Database
* ใช้ **Git และ GitHub** สำหรับ Version Control
* มีการวาง System Architecture และ Data Flow ของ Final Project
* แยกสิ่งที่ทำใน Sprint 1 ออกจากสิ่งที่จะพัฒนาใน Sprint ถัดไป

### Status

**✅ Updated**

---

# 23. Project Plan Improvement

### Feedback

เพิ่ม:

* ตารางกำหนดเวลาของ Project
* ตารางงานของสมาชิก
* การแจกแจงงานตามหน้าที่
* Metrics สำหรับติดตามงาน

### สิ่งที่กลุ่มแก้ไข

ปรับ `docs/Plan.md` ให้เป็น **Master Plan ของทั้ง Project**
โดยแบ่งการพัฒนาออกเป็น:

```text
Sprint 1
   ↓
Sprint 2
   ↓
Sprint 3
   ↓
Final Sprint
```

และเพิ่ม:

* Project Timeline
* Sprint Overview
* Sprint Objectives
* Main Scope
* Deliverables
* Technology Roadmap
* Project Status
* Team Planning
* Documentation Structure

ส่วนรายละเอียดของแต่ละ Sprint
จะแยกออกไปอยู่ในไฟล์ของ Sprint นั้น ๆ

### Status

**✅ Updated**

---

# 24. Documentation Improvement

### Feedback

เพิ่ม Documentation:

* Change Log
* Learning Log

### สิ่งที่กลุ่มเพิ่มเติม

เพิ่มไฟล์:

```text
docs/
├── Change_Log.md
└── Learning_Log.md
```

โดยมีหน้าที่:

### Change Log

บันทึกการเปลี่ยนแปลงของ Project
เช่น:

* การเปลี่ยน Project Direction
* การเปลี่ยน Architecture
* การเพิ่ม Feature
* การแก้ไขตาม Instructor Feedback

### Learning Log

บันทึกสิ่งที่ทีมเรียนรู้จากการทำ Project
เช่น:

* การวางแผน Sprint
* การแบ่งหน้าที่
* การพัฒนา CLI
* Input Validation
* QA และ Edge Case Testing
* Git / GitHub Workflow

### Status

**✅ Added**

---

# 25. Metrics Improvement

### Feedback

เพิ่ม Metrics สำหรับการให้คะแนนและติดตามการทำงานของสมาชิกในกลุ่ม

### สิ่งที่กลุ่มเพิ่มเติม

เพิ่ม **Contribution Matrix**
เพื่อแสดง:

* สมาชิกแต่ละคน
* Role ที่รับผิดชอบ
* งานที่ได้รับมอบหมาย
* ผลงานที่ดำเนินการ
* คะแนนของแต่ละส่วน
* คะแนนรวมของสมาชิก

ตัวอย่าง:

```text
Planner
50 / 50

Coder
50 / 50

Debugger
50 / 50
```

Metrics นี้ใช้เป็นการประเมิน Contribution
ภายในกลุ่มของ Sprint 1

### Status

**✅ Added**

---

# 26. Repository Structure Improvement

หลังจากได้รับ Feedback และวางแผน Project ใหม่
ทีมปรับโครงสร้าง Repository ให้แยก Documentation,
Source Code และ Sprint Documentation ออกจากกัน

โครงสร้างปัจจุบัน:

```text
Gaming-Statistics-Dashboard/
│
├── README.md
│
├── docs/
│   ├── Project_Pitch.md
│   ├── Plan.md
│   ├── Change_Log.md
│   └── Learning_Log.md
│
├── src/
│   ├── ...
│   └── ...
│
├── Sprint1/
│   └── Sprint_1.md
│
├── Sprint2/
│   └── Sprint_2.md
│
├── Sprint3/
│   └── ...
│
└── ...
```

แนวทางนี้ช่วยแยก:

* Project-level Documentation
* Source Code
* Sprint-level Documentation

ออกจากกันอย่างชัดเจน

### Status

**✅ Structure Updated**

---

# 27. Comment / Feedback Summary

หลังจากนำเสนอ Sprint 1
กลุ่มได้นำ Feedback ของอาจารย์มาปรับปรุง Project
โดยไม่ได้เปลี่ยนเป้าหมายหลักของ Sprint 1
แต่เน้นการทำให้ Project Documentation และ Project Planning
มีความชัดเจนและเป็นระบบมากขึ้น

สิ่งที่กลุ่มได้ **แก้ไขและเพิ่มเติม** ได้แก่:

1. **Project Pitch**

   * เพิ่มรายละเอียดว่า Final Project จะเป็น Web Application
   * ระบุการใช้งานผ่าน Web Browser
   * เพิ่ม Technology Stack
   * เพิ่ม Architecture และ Data Flow
   * ระบุ Data Source และแนวทางการพัฒนาในแต่ละ Sprint

2. **Project Plan**

   * ปรับ `Plan.md` ให้เป็น Master Plan ของทั้ง Project
   * เพิ่ม Project Timeline
   * เพิ่ม Sprint Overview
   * เพิ่ม Deliverables ของแต่ละ Sprint
   * เพิ่ม Technology Roadmap
   * เพิ่มการแบ่งหน้าที่ของสมาชิกในภาพรวม

3. **Sprint 1 Documentation**

   * เพิ่มรายละเอียดงานของ Planner, Coder และ Debugger
   * เพิ่ม Task Allocation
   * เพิ่ม QA Test Cases
   * เพิ่ม Definition of Done
   * เพิ่ม Contribution Matrix

4. **Documentation**

   * เพิ่ม `Change_Log.md`
   * เพิ่ม `Learning_Log.md`

5. **Metrics**

   * เพิ่ม Contribution Matrix สำหรับประเมินการทำงานของสมาชิก
   * แสดงงานที่แต่ละคนรับผิดชอบ
   * แสดงคะแนนรายงานตามหน้าที่
   * แสดงคะแนนรวมของแต่ละสมาชิก

6. **Repository Structure**

   * แยก `docs/` สำหรับ Project Documentation
   * เพิ่ม `src/` สำหรับ Source Code
   * แยก Documentation ของแต่ละ Sprint ไว้ใน Folder ของ Sprint นั้น ๆ

การปรับปรุงทั้งหมดนี้มีเป้าหมายเพื่อให้ Project
มีโครงสร้างที่ชัดเจนขึ้น สามารถติดตามความคืบหน้าได้ง่ายขึ้น
และสามารถนำไปใช้เป็นพื้นฐานในการพัฒนา Sprint ถัดไปได้

---

# 28. Sprint 1 Final Status

```text
╔══════════════════════════════════════╗
║       SPRINT 1 — COMPLETED           ║
╚══════════════════════════════════════╝
```

### Sprint 1 Summary

**Application**

* ✅ CLI Foundation
* ✅ Main Menu
* ✅ Menu Navigation
* ✅ View Games
* ✅ Search Game
* ✅ Statistics
* ✅ Genres
* ✅ Top Rated Games
* ✅ Input Validation
* ✅ Exception Handling

**QA**

* ✅ 14 Test Cases
* ✅ 14 Passed
* ✅ 100% Test Pass Rate
* ✅ 0 Critical Bugs

**Documentation**

* ✅ Project Pitch Updated
* ✅ Project Plan Updated
* ✅ Sprint 1 Report
* ✅ Change Log Added
* ✅ Learning Log Added
* ✅ Contribution Matrix Added

**GitHub**

* ✅ Repository
* ✅ Sprint 1 Code
* ✅ Sprint 1 Documentation
* ⏳ Pull Request URL จะเพิ่มภายหลัง

---

## Current Sprint Status

**Sprint 1: ✅ Completed**

**Next Step: Sprint 2 Planning**

```
```
