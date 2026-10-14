# 🎮 Gaming Statistics Dashboard — Sprint 3 Report

> บันทึกประวัติตามช่วง Sprint: โครงสร้างและพฤติกรรมบางส่วนเปลี่ยนในรุ่นส่งมอบ ให้ใช้ [README](../README.md) สำหรับการติดตั้ง/ใช้งานปัจจุบัน และ [Final QA](../docs/FINAL_QA.md) สำหรับผลตรวจล่าสุด

## Final Term Project — CP352301 Script Programming

**Sprint:** Sprint 3 — Data Analysis, Visualization & Advanced Features  
**Period:** 25–29 September 2026  
**Duration:** 5 Days  
**Status:** ✅ Completed

**Repository:** https://github.com/Phanuwatphk/Gaming-Statistics-Dashboard

---

# 1. Sprint Overview

Sprint 3 เป็นการพัฒนาต่อยอดจาก Sprint 2 ซึ่งทีมได้พัฒนา Web Application ด้วย Streamlit พร้อมเชื่อมต่อ RAWG API, Steam API และ SQLite Database

เป้าหมายหลักของ Sprint 3 คือการนำข้อมูลเกมที่มีอยู่ในระบบมาจัดเตรียม วิเคราะห์ และนำเสนอในรูปแบบ Statistics และ Data Visualization รวมถึงเพิ่มความสามารถในการ Filter, Sort และเปรียบเทียบข้อมูลเกม

ใน Sprint นี้มีการเพิ่ม **Analysis Layer** เข้ามาในระบบ โดยแยกส่วนการคำนวณและวิเคราะห์ข้อมูลออกจาก UI เพื่อให้สามารถนำข้อมูลจาก Game Service มาวิเคราะห์ด้วย Pandas และนำผลลัพธ์ไปแสดงบน Statistics Page ของ Streamlit Dashboard

งานที่พัฒนาใน Sprint 3 ประกอบด้วย:

- Data Processing และ Data Normalization
- Data Preparation สำหรับการวิเคราะห์
- Exploratory Data Analysis (EDA)
- Descriptive Statistics
- Frequency และ Proportion Analysis
- Genre / Platform Analysis
- Release Year Analysis
- Metacritic Analysis
- Steam Live Player Analysis
- Statistics Dashboard
- Data Visualization
- Game Comparison
- Advanced Filtering
- Advanced Sorting
- Dashboard Integration
- Unit Testing และ Integration Testing
- Empty State และ Missing Data Handling

---

# 2. Sprint Goal

> พัฒนา Gaming Statistics Dashboard ให้สามารถนำข้อมูลเกมจากระบบมาวิเคราะห์และนำเสนอในรูปแบบ Statistics และ Data Visualization พร้อมเพิ่มความสามารถในการสำรวจ เปรียบเทียบ และกรองข้อมูลเกมได้สะดวกขึ้น

เมื่อจบ Sprint 3 ระบบสามารถ:

- เตรียมและ Normalize ข้อมูลเกมจาก RAWG
- แปลงข้อมูลให้อยู่ในรูปแบบที่เหมาะสมต่อการวิเคราะห์
- จัดการข้อมูลที่ไม่มีค่าใน Optional Fields โดยไม่สร้างข้อมูลขึ้นมาแทนโดยไม่มีหลักเกณฑ์
- วิเคราะห์ข้อมูลด้วย Pandas
- คำนวณ Descriptive Statistics ของ Rating
- วิเคราะห์ Frequency และ Proportion ของ Genre และ Platform
- วิเคราะห์ Average Rating ตาม Genre
- วิเคราะห์จำนวนเกมตาม Release Year
- วิเคราะห์ Metacritic Score ที่มีอยู่ในระบบ
- วิเคราะห์ Current Steam Players ที่มีข้อมูล
- แสดง Statistics บนหน้า Statistics
- แสดง Visualization จำนวน 6 ส่วน
- เปรียบเทียบข้อมูลของเกม 2 เกม
- Filter เกมด้วยหลายเงื่อนไขพร้อมกัน
- Sort เกมตาม Rating, Release Date และ Name
- จัดการ Missing Values และ Empty Dataset ในส่วนที่เกี่ยวข้อง
- ทดสอบ Analysis Functions และ Dashboard Integration

---

# 3. Team Members & Roles

Sprint 3 ใช้ Role Rotation จาก Sprint ก่อนหน้า โดยแบ่งหน้าที่ดังนี้:

| สมาชิก | ชื่อเล่น | Role | หน้าที่หลัก |
|---| --- |---|---|
| นายเดโชชิต โตวินัส | ออม | Planner | กำหนด Sprint Goal, Scope, Requirements, Definition of Done, แบ่งงาน ติดตามความคืบหน้า และจัดทำ Documentation |
| นายชิษณุพงศ์ ซู | คิม | Coder | พัฒนา Data Processing, Analysis, Statistics, Visualization และ Features ที่อยู่ใน Scope ของ Sprint 3 |
| นายภานุวัฒน์ ผองแก้ว | ฟลุ๊ค | Debugger | ออกแบบและดำเนินการทดสอบ ตรวจสอบผลลัพธ์ วิเคราะห์ปัญหา และยืนยันการแก้ไข Bug |


---

# 4. Sprint 3 Scope

## 4.1 Data Processing & Data Preparation

สิ่งที่ดำเนินการจริง:

- Normalize ข้อมูลเกมจาก RAWG API
- แปลง Game ID เป็น Integer
- แปลง Rating เป็น Float
- แปลง Metacritic เป็น Integer
- แปลง Ratings Count เป็น Integer
- จัดการ Released Date ให้อยู่ในรูปแบบที่สามารถนำไปวิเคราะห์ได้
- แยก Release Year จาก Released Date
- Normalize Genre จาก Nested RAWG Data
- Normalize Platform จาก Nested RAWG Data
- ลบชื่อ Genre / Platform ที่ซ้ำกันภายในข้อมูลของเกมเดียวกัน
- เก็บ Optional Fields ที่ไม่มีข้อมูลเป็น `None`
- ข้ามข้อมูลที่ไม่มี Game ID ที่ใช้งานได้
- แปลงข้อมูล Numeric ใน Analysis Layer ด้วย Pandas
- รองรับข้อมูลที่ไม่สมบูรณ์โดยไม่ทำให้ Statistics Page เกิด Error

---

## 4.2 Exploratory Data Analysis (EDA)

ดำเนินการวิเคราะห์ข้อมูลเกมในหลายมิติ ได้แก่:

### Rating

- Count
- Mean
- Median
- Minimum
- Maximum
- Standard Deviation

### Genre

- Genre Frequency
- Genre Proportion
- Average Rating by Genre

### Platform

- Platform Frequency
- Platform Proportion

### Release Date

- Release Year Frequency

### Metacritic

- Numeric Value Extraction
- Distribution ของ Metacritic Score

### Steam

- Current Player Count
- Top Current Steam Players

---

## 4.3 Statistical Analysis

Sprint 3 ใช้ **Descriptive Statistics** เป็นหลัก

Statistics ที่คำนวณจริง ได้แก่:

| Statistic | การใช้งาน |
|---|---|
| Count | จำนวนเกมที่มี Rating ที่สามารถนำมาคำนวณได้ |
| Mean | ค่าเฉลี่ย Rating |
| Median | ค่ามัธยฐาน Rating |
| Minimum | Rating ต่ำสุด |
| Maximum | Rating สูงสุด |
| Standard Deviation | ส่วนเบี่ยงเบนมาตรฐานของ Rating |
| Frequency | จำนวนการปรากฏของ Genre / Platform |
| Proportion | สัดส่วนของ Genre / Platform |

### Rating Statistics

Descriptive Statistics ใน Summary ใช้ข้อมูล `Rating` เป็นตัวแปรหลัก

หากไม่มีเกมหรือไม่มี Rating ที่สามารถคำนวณได้ ระบบจะคืนค่า:

```text
Count = 0
Mean = None
Median = None
Minimum = None
Maximum = None
Standard Deviation = None
````

และหน้า Dashboard จะแสดง Empty / N/A State แทนการเกิด Error

---

# 5. Analysis Layer

Sprint 3 เพิ่ม Analysis Layer ใหม่เพื่อแยกส่วนการวิเคราะห์ข้อมูลออกจาก UI

โครงสร้างหลัก:

```text
src/
├── analysis/
│   ├── __init__.py
│   └── statistics.py
│
├── components/
│   ├── dashboard.py
│   └── statistics_page.py
│
├── services/
│   └── game_service.py
│
└── utils/
    └── data_processing.py
```

## `src/analysis/statistics.py`

Module นี้รับผิดชอบการวิเคราะห์ข้อมูลเกม เช่น:

* `games_to_dataframe()`
* `descriptive_statistics()`
* `genre_frequency()`
* `platform_frequency()`
* `genre_rating_mean()`
* `release_year_frequency()`
* `frequency_with_proportion()`
* `numeric_values()`
* `top_current_players()`
* `comparison_dataframe()`

การแยก Analysis Layer ช่วยให้:

```text
Game Data
    ↓
Analysis Functions
    ↓
Statistics / DataFrame
    ↓
Visualization
```

โดยไม่ต้องนำ Logic การคำนวณ Statistics ไปเขียนรวมอยู่ใน UI

---

# 6. System Architecture

Architecture ของ Sprint 3 ต่อเนื่องจาก Sprint 2 และเพิ่ม Analysis Layer เข้ามา

```text
                    ┌──────────────┐
                    │   RAWG API   │
                    └──────┬───────┘
                           ↓
                  ┌──────────────────┐
                  │ Data Processing  │
                  │  Normalization   │
                  └────────┬─────────┘
                           ↓
                  ┌──────────────────┐
                  │ SQLite Database  │
                  └────────┬─────────┘
                           ↓
                  ┌──────────────────┐
                  │   Game Service   │
                  └────────┬─────────┘
                           ↓
                ┌───────────────────────┐
                │   Analysis Layer      │
                │ Statistics / Pandas   │
                └───────────┬───────────┘
                            ↓
                ┌───────────────────────┐
                │ Visualization Layer   │
                │       Altair          │
                └───────────┬───────────┘
                            ↓
                ┌───────────────────────┐
                │ Streamlit Dashboard   │
                └───────────┬───────────┘
                            ↓
                       Web Browser
```

สำหรับ Steam:

```text
Steam API
    ↓
Steam Player Data
    ↓
Game Service
    ↓
SQLite
    ↓
Analysis Layer
    ↓
Statistics / Dashboard
```

---

# 7. Sprint 3 Data Flow

การทำงานของ Statistics Page:

```text
SQLite Database
       ↓
Game Service
       ↓
Game Records
       ↓
Analysis Layer
       ↓
Pandas DataFrame
       ↓
Statistics Functions
       ↓
Statistics / Frequency / Distribution
       ↓
Altair Visualization
       ↓
Streamlit Statistics Page
```

สำหรับ Game Comparison:

```text
Game Library
     ↓
Select Game A + Game B
     ↓
comparison_dataframe()
     ↓
Rating
Metacritic
Steam Players
     ↓
Comparison Table
```

---

# 8. Project Structure

โครงสร้าง Project หลัง Sprint 3:

```text
Gaming-Statistics-Dashboard/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env
├── .env.example
├── pytest.ini
│
├── data/
│   └── gaming_statistics.db
│
├── docs/
│   ├── Project_Pitch.md
│   ├── Plan.md
│   ├── CHANGELOG.md
│   └── LEARNINGLOG.md
│
├── src/
│   ├── __init__.py
│   ├── app.py
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── statistics.py
│   │
│   ├── api/
│   │   ├── rawg_api.py
│   │   └── steam_api.py
│   │
│   ├── components/
│   │   ├── dashboard.py
│   │   ├── statistics_page.py
│   │   └── styles.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── services/
│   │   └── game_service.py
│   │
│   └── utils/
│       ├── data_processing.py
│       └── time_utils.py
│
├── tests/
│   ├── test_dashboard.py
│   ├── test_data_processing.py
│   ├── test_database.py
│   ├── test_game_service.py
│   ├── test_rawg_api.py
│   ├── test_statistics.py
│   ├── test_steam_api.py
│   └── test_time_utils.py
│
├── Sprint1/
│   └── Sprint_1.md
│
├── Sprint2/
│   └── Sprint_2.md
│
└── Sprint3/
    └── Sprint_3.md
```

จุดสำคัญของ Sprint 3 คือการเพิ่ม:

```text
src/analysis/statistics.py
src/components/statistics_page.py
tests/test_statistics.py
```

รวมถึงการเพิ่ม Test Cases ที่เกี่ยวข้องกับ Statistics และ Dashboard Integration

---

# 9. Tools & Technologies

| Technology   | Purpose                                             |
| ------------ | --------------------------------------------------- |
| Python       | Programming Language                                |
| Streamlit    | Web Application และ Dashboard                       |
| Pandas       | DataFrame, Data Processing และ Statistical Analysis |
| SQLite       | Data Storage                                        |
| RAWG API     | Game Data Source                                    |
| Steam API    | Steam Player Data Source                            |
| Altair       | Data Visualization                                  |
| pytest       | Automated Testing                                   |
| Git + GitHub | Version Control และ Collaboration                   |

---

# 10. Data Processing & Data Preparation

## 10.1 RAWG Data Normalization

RAWG API ส่งข้อมูลบางส่วนในรูปแบบ Nested Structure เช่น:

```text
genres
platforms
```

จึงมีการแปลงข้อมูลให้อยู่ในรูปแบบที่ Application สามารถใช้งานได้ง่ายขึ้น

ตัวอย่าง:

```text
RAWG Nested Data
      ↓
process_game()
      ↓
Normalized Game Record
```

Normalized Game Record ประกอบด้วย:

```text
game_id
name
rating
released
genres
platforms
metacritic
ratings_count
image
```

---

## 10.2 Numeric Conversion

Analysis Layer แปลงข้อมูล Numeric ด้วย Pandas ได้แก่:

```text
rating
metacritic
current_players
```

โดยใช้ Numeric Coercion เพื่อรองรับกรณีข้อมูลไม่สามารถแปลงเป็นตัวเลขได้

ค่าที่ไม่สามารถแปลงได้จะถูกจัดการเป็น Missing Value แทนที่จะทำให้ Analysis Process หยุดทำงาน

---

## 10.3 Release Date Processing

ระบบแปลง:

```text
released
```

เป็น Datetime และสร้าง:

```text
release_year
```

เพื่อใช้วิเคราะห์จำนวนเกมตามปีที่วางจำหน่าย

---

## 10.4 Missing Data Handling

ระบบไม่ได้แทนค่า Missing ด้วย `0` โดยอัตโนมัติ

Optional Fields ที่ไม่มีข้อมูลสามารถถูกเก็บเป็น:

```text
None
```

และ Analysis Functions จะใช้เฉพาะค่าที่สามารถนำมาคำนวณได้

ตัวอย่าง:

```text
ไม่มี Rating
      ↓
ไม่รวมในการคำนวณ Rating Statistics
```

---

# 11. Exploratory Data Analysis

## 11.1 Genre Analysis

ระบบคำนวณ:

```text
Genre Frequency
Genre Proportion
Average Rating by Genre
```

เนื่องจากเกมหนึ่งเกมสามารถมีได้หลาย Genre การคำนวณ Frequency จะนับจำนวนการปรากฏของ Genre

ตัวอย่าง:

```text
Game A → Action, RPG
Game B → Action
```

จะได้:

```text
Action = 2
RPG    = 1
```

Proportion จึงคำนวณจากจำนวน Genre Assignments ทั้งหมด ไม่ใช่จำนวนเกมทั้งหมด

---

## 11.2 Platform Analysis

ระบบคำนวณ:

```text
Platform Frequency
Platform Proportion
```

โดยรองรับกรณีเกมหนึ่งเกมมีหลาย Platform

---

## 11.3 Rating Analysis

ระบบคำนวณ:

```text
Count
Mean
Median
Minimum
Maximum
Standard Deviation
```

และนำผลไปแสดงบน Statistics Dashboard

---

## 11.4 Rating by Genre

ระบบใช้ Genre ที่แตกออกจากรายการของแต่ละเกมเพื่อคำนวณ:

```text
Average Rating per Genre
```

จากนั้นเรียงค่าเฉลี่ย Rating จากสูงไปต่ำและนำเสนอเป็น Bar Chart

---

## 11.5 Release Year Analysis

ระบบแปลง Release Date เป็น Year และคำนวณ:

```text
Number of Games per Release Year
```

จากนั้นนำเสนอเป็น Line Chart

---

## 11.6 Metacritic Analysis

ระบบดึงค่าที่สามารถแปลงเป็น Numeric ได้จาก:

```text
metacritic
```

และนำเสนอ Distribution ด้วย Binned Bar Chart

---

## 11.7 Steam Player Analysis

ระบบใช้ข้อมูล:

```text
current_players
```

เพื่อหาเกมที่มีจำนวนผู้เล่นปัจจุบันสูงสุด

ผลลัพธ์ถูกนำเสนอเป็น:

```text
Top Live Steam Players
```

ในรูปแบบ Bar Chart

---

# 12. Dashboard Statistics

Statistics Page แสดง Summary Metrics จำนวน 5 รายการ:

| Metric         | Description                               |
| -------------- | ----------------------------------------- |
| Rated games    | จำนวนเกมที่มี Rating ที่สามารถใช้คำนวณได้ |
| Average Rating | ค่าเฉลี่ย Rating                          |
| Median Rating  | ค่ามัธยฐาน Rating                         |
| Highest Rating | Rating สูงสุด                             |
| Lowest Rating  | Rating ต่ำสุด                             |

ตัวอย่าง Flow:

```text
Game Records
     ↓
descriptive_statistics()
     ↓
Count / Mean / Median / Min / Max / Std
     ↓
Streamlit Metrics
```

---

# 13. Data Visualization

Statistics Page มี Visualization หลักทั้งหมด 6 ส่วน

## 13.1 Genre Distribution

แสดงจำนวนเกมในแต่ละ Genre

```text
Bar Chart
```

พร้อม Tooltip:

```text
Genre
Count
Share
```

---

## 13.2 Platform Distribution

แสดงจำนวนเกมในแต่ละ Platform

```text
Bar Chart
```

พร้อม Tooltip:

```text
Platform
Count
Share
```

---

## 13.3 Rating by Genre

แสดง Average Rating ของแต่ละ Genre

```text
Bar Chart
```

โดยกำหนด Rating Scale:

```text
0 – 5
```

---

## 13.4 Release Year Distribution

แสดงจำนวนเกมที่ออกในแต่ละปี

```text
Line Chart
```

พร้อม Point ในแต่ละปี

---

## 13.5 Metacritic Score Distribution

แสดงการกระจายตัวของ Metacritic Score

```text
Binned Bar Chart
```

โดยแบ่งข้อมูลเป็นช่วงเพื่อแสดง Distribution

---

## 13.6 Top Live Steam Players

แสดงเกมที่มีจำนวนผู้เล่น Steam ปัจจุบันสูงสุด

```text
Bar Chart
```

ข้อมูลใช้เฉพาะเกมที่มี Current Player Count

---

# 14. Advanced Features

## 14.1 Advanced Filtering

Game Library รองรับ Filter หลายเงื่อนไขพร้อมกัน:

* Genre
* Platform
* Minimum Rating
* Release Year

ตัวอย่าง:

```text
Genre = Action
Platform = PC
Minimum Rating >= 4.0
Release Year = 2020–2025
```

ระบบจะคืนเฉพาะเกมที่ผ่านเงื่อนไขทั้งหมด

---

## 14.2 Advanced Sorting

รองรับการ Sort ตาม:

```text
Rating
Release Date
Name
```

และเลือก Order ได้:

```text
Descending
Ascending
```

สำหรับ Rating และ Release Date ระบบจะแยกข้อมูลที่มีค่าออกจากข้อมูล Missing และวาง Missing Values ไว้ท้ายผลลัพธ์

---

## 14.3 Game Comparison

Sprint 3 เพิ่มความสามารถในการเลือกเกม 2 เกม:

```text
Game A
Game B
```

จากนั้นเปรียบเทียบ Metrics:

| Metric        |
| ------------- |
| Rating        |
| Metacritic    |
| Steam Players |

ผลลัพธ์แสดงในรูปแบบ Comparison Table

ตัวอย่างโครงสร้าง:

```text
Metric          Game A       Game B
------------------------------------
Rating          4.50         4.80
Metacritic      90           94
Steam Players   12000        8500
```

ค่าที่แสดงมาจากข้อมูลของเกมที่เลือกโดยตรง

---

# 15. Empty State & Error Handling

ระบบรองรับกรณีไม่มีข้อมูลใน Statistics Page

หากไม่มี Game Records ระบบจะแสดง:

```text
No data available.
Add games through Search before viewing statistics.
```

และไม่ทำการคำนวณหรือสร้าง Chart ต่อ

นอกจากนี้แต่ละ Visualization มีการตรวจสอบข้อมูลก่อนสร้าง Chart

ตัวอย่าง:

```text
No genre data available.
No platform data available.
No rating-by-genre data available.
No release-year data available.
No Metacritic data available.
No live Steam-player data available.
```

แนวทางนี้ช่วยป้องกันการเกิด Exception เมื่อข้อมูลบางส่วนไม่มีอยู่

---

# 16. Integration with Game Service

Sprint 3 ยังคงใช้ Game Service เป็นตัวกลางระหว่าง UI และ Data Layer

```text
Streamlit UI
      ↓
Game Service
      ↓
SQLite / API
```

Game Service รับผิดชอบการจัดการข้อมูลที่ Dashboard ต้องใช้ เช่น:

* Get Games
* Search Games
* Search and Import Games
* Import Search Page
* Steam Player Refresh
* Catalog Refresh
* Live Top Games Refresh

และส่งข้อมูลเกมที่พร้อมใช้งานให้ Dashboard และ Analysis Layer

---

# 17. Steam Data Integration

Steam Player Data ยังคงทำงานผ่าน Game Service และ SQLite

ระบบมีการจัดการ:

```text
Steam App ID
Current Players
Steam Lookup Status
Player Refresh Timestamp
```

และมีการใช้ Refresh Interval เพื่อหลีกเลี่ยงการเรียก Steam API ซ้ำโดยไม่จำเป็น

ระบบยังมี Shared Lock สำหรับการ Refresh ข้อมูล เพื่อป้องกันหลาย Streamlit Sessions ทำการ Refresh Database Snapshot พร้อมกัน

Lock ที่ใช้ใน Game Service ได้แก่:

```text
_LIVE_TOP_REFRESH_LOCK
_CATALOG_REFRESH_LOCK
_PLAYERS_REFRESH_LOCK
```

---

# 18. Development Tasks & Results

## Task 1 — Sprint Planning & Requirements

### Planner — ออม (นายเดโชชิต โตวินัส)

ดำเนินการ:

* กำหนด Sprint Goal
* กำหนด Scope
* กำหนด Requirements
* กำหนด Definition of Done
* แบ่งงาน
* ติดตามความคืบหน้า
* จัดทำ Documentation

**Result:** ✅ Completed

---

## Task 2 — Data Processing & Preparation

### Coder — คิม (นายชิษณุพงศ์ ซู)

ดำเนินการ:

* Normalize RAWG Game Data
* Handle Optional Fields
* Numeric Conversion
* Release Date Conversion
* Release Year Extraction
* Genre / Platform Normalization

### Debugger — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

ดำเนินการ:

* ตรวจสอบ Data Processing
* ตรวจสอบ Missing Data
* ตรวจสอบ Duplicate Game ID
* ตรวจสอบ Data Type

**Result:** ✅ Completed

---

## Task 3 — EDA & Statistical Analysis

### Coder — คิม (นายชิษณุพงศ์ ซู)

พัฒนา:

* DataFrame Conversion
* Descriptive Statistics
* Genre Frequency
* Platform Frequency
* Genre Rating Mean
* Release Year Frequency
* Frequency with Proportion
* Numeric Value Extraction
* Top Current Players
* Game Comparison

### Debugger — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

ตรวจสอบ:

* Statistics Calculation
* Empty Dataset
* Missing Values
* Frequency / Proportion
* Comparison Data

**Result:** ✅ Completed

---

## Task 4 — Dashboard Statistics & Visualization

### Coder — คิม (นายชิษณุพงศ์ ซู)

พัฒนา:

* Statistics Page
* Summary Metrics
* Genre Distribution
* Platform Distribution
* Rating by Genre
* Release Year Distribution
* Metacritic Distribution
* Top Live Steam Players
* Game Comparison Table

### Debugger — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

ตรวจสอบ:

* Dashboard Rendering
* Chart Rendering
* Empty State
* Statistics Integration
* Comparison Table

**Result:** ✅ Completed

---

## Task 5 — Advanced Features & Integration

### Coder — คิม (นายชิษณุพงศ์ ซู)

พัฒนา:

* Multi-condition Filtering
* Sorting
* Missing Value Sorting
* Game Comparison
* Analysis / Dashboard Integration

### Debugger — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

ตรวจสอบ:

* Filter Combination
* Sorting
* Missing Values
* Dashboard Integration
* Edge Cases

**Result:** ✅ Completed

---

# 19. Sprint 3 Daily Task Allocation & Actual Result

| วันที่           | Planner — ออม (นายเดโชชิต โตวินัส)                                           | Coder — คิม (นายชิษณุพงศ์ ซู)                                                                    | Debugger — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)                                                    | ผลการดำเนินงาน                         |
| ---------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------- | -------------------------------------- |
| **25 ก.ย. 2569** | กำหนด Sprint Goal, Scope, Requirements และแบ่งงาน       | ตรวจสอบโครงสร้างโค้ดและวิเคราะห์งานที่ต้องพัฒนาจาก Sprint 2                    | เตรียมแนวทาง Test Cases และตรวจสอบจุดที่ต้องทดสอบ                   | **Planning & Technical Preparation** ✅ |
| **26 ก.ย. 2569** | ติดตามความคืบหน้าและตรวจสอบขอบเขต Data Analysis         | พัฒนา Data Processing, Data Normalization และ Analysis Layer (`statistics.py`) | ทดสอบ Data Processing, Data Type และ Missing Data                   | **Data Processing & Analysis** ✅       |
| **27 ก.ย. 2569** | ตรวจสอบ Requirements ของ Statistics Dashboard           | พัฒนา Statistics Page, Summary Statistics และ Data Visualization               | ตรวจสอบ Statistics และการแสดงผล Charts                              | **Statistics & Visualization** ✅       |
| **28 ก.ย. 2569** | ติดตาม Advanced Features และ Integration                | พัฒนา Advanced Filtering, Sorting, Game Comparison และเชื่อมต่อกับ Dashboard   | ทดสอบ Filter, Sort, Comparison และ Integration                      | **Advanced Features & Integration** ✅  |
| **29 ก.ย. 2569** | ตรวจสอบ Definition of Done และจัดทำ Final Documentation | แก้ไข Bug และเตรียม Source Code สำหรับ Final Sprint                            | ทำ Final QA, Regression / Integration Testing และตรวจสอบ Test Cases | **Final QA & Documentation** ✅         |


---

# 20. Sprint Progress

| Task                           | Status      | Result                                                        |
| ------------------------------ | ----------- | ------------------------------------------------------------- |
| Sprint Planning & Requirements | ✅ Completed | Sprint Goal, Scope และ DoD                                    |
| Data Processing & Preparation  | ✅ Completed | Normalization และ Data Preparation                            |
| Exploratory Data Analysis      | ✅ Completed | Genre, Platform, Rating, Release Year และ Additional Analysis |
| Statistical Analysis           | ✅ Completed | Descriptive Statistics และ Frequency / Proportion             |
| Dashboard Statistics           | ✅ Completed | Summary Metrics                                               |
| Data Visualization             | ✅ Completed | 6 Visualization Sections                                      |
| Advanced Filtering             | ✅ Completed | Genre, Platform, Rating, Release Year                         |
| Advanced Sorting               | ✅ Completed | Rating, Release Date, Name                                    |
| Game Comparison                | ✅ Completed | Game A vs Game B                                              |
| Integration Testing            | ✅ Completed | Dashboard + Service + Analysis                                |
| Final QA                       | ✅ Completed | S3-TC-01 ถึง S3-TC-14 Pass                                    |
| Documentation                  | ✅ Completed | Sprint 3 Report และ Project Documentation                     |

---

# 21. QA Test Cases

Sprint 3 มี Test Cases สำหรับตรวจสอบ Data Processing, Analysis, Dashboard และ Advanced Features

| Test ID  | Test Case                              | Expected Result                                            |
| -------- | -------------------------------------- | ---------------------------------------------------------- |
| S3-TC-01 | ตรวจสอบ Dataset ที่มีข้อมูลครบถ้วน     | Data Processing ทำงานได้ถูกต้อง                            |
| S3-TC-02 | ตรวจสอบ Missing Values                 | ระบบจัดการ Optional / Missing Values ได้อย่างปลอดภัย       |
| S3-TC-03 | ตรวจสอบข้อมูลซ้ำ                       | Database ป้องกัน Duplicate Game ID                         |
| S3-TC-04 | ตรวจสอบ Data Type                      | Numeric Values ถูกแปลงเป็นชนิดที่เหมาะสม                   |
| S3-TC-05 | ตรวจสอบ Mean / Median                  | ผลคำนวณตรงกับค่าที่ตรวจสอบ                                 |
| S3-TC-06 | ตรวจสอบ Min / Max / Standard Deviation | ผลคำนวณถูกต้อง                                             |
| S3-TC-07 | ตรวจสอบ Genre / Platform Frequency     | จำนวนและ Proportion ถูกต้อง                                |
| S3-TC-08 | ตรวจสอบ Dataset ว่าง                   | ระบบไม่ Crash และแสดง Empty State                          |
| S3-TC-09 | ตรวจสอบ Statistics Visualization       | Statistics Page สามารถ Render Visualization ได้            |
| S3-TC-10 | ตรวจสอบ Filter หลายเงื่อนไข            | ผลลัพธ์ตรงตามเงื่อนไขที่เลือก                              |
| S3-TC-11 | ตรวจสอบ Sorting                        | ข้อมูลเรียงตามเงื่อนไขที่เลือกและ Missing Values ถูกจัดการ |
| S3-TC-12 | ตรวจสอบ Game Comparison                | ค่าตรงกับข้อมูลของเกมที่เลือก                              |
| S3-TC-13 | ตรวจสอบ Dashboard Integration          | UI แสดงผลจาก Service / Analysis ได้ถูกต้อง                 |
| S3-TC-14 | ตรวจสอบข้อมูลไม่เพียงพอสำหรับ Chart    | ระบบแสดง Empty / Informative State                         |

---

# 22. QA Result

ผลการทดสอบที่บันทึกใน Sprint 3:

| Test ID  | Result | Evidence / Notes                                                   |
| -------- | ------ | ------------------------------------------------------------------ |
| S3-TC-01 | ✅ Pass | `test_process_game_normalizes_nested_rawg_fields`                  |
| S3-TC-02 | ✅ Pass | Missing optional values และ empty statistics ถูกจัดการอย่างปลอดภัย |
| S3-TC-03 | ✅ Pass | `test_database_upsert_prevents_duplicate_game_ids`                 |
| S3-TC-04 | ✅ Pass | Numeric coercion ถูกครอบคลุมใน Analysis และ Processing Tests       |
| S3-TC-05 | ✅ Pass | `test_descriptive_statistics`                                      |
| S3-TC-06 | ✅ Pass | Min, Max และ Sample Standard Deviation ถูกตรวจสอบ                  |
| S3-TC-07 | ✅ Pass | Genre / Platform Frequency และ Proportion ถูกตรวจสอบ               |
| S3-TC-08 | ✅ Pass | `test_statistics_page_handles_an_empty_library`                    |
| S3-TC-09 | ✅ Pass | Statistics Page Render Visualization ทั้ง 6 Sections ได้           |
| S3-TC-10 | ✅ Pass | Multi-condition Genre / Platform / Rating / Year Filter Test       |
| S3-TC-11 | ✅ Pass | Rating และ Release Date Sorting รวมถึง Missing Values              |
| S3-TC-12 | ✅ Pass | `test_comparison_dataframe_uses_the_selected_games_values`         |
| S3-TC-13 | ✅ Pass | AppTest Render Statistics, Charts และ Comparison Table             |
| S3-TC-14 | ✅ Pass | Empty Library Chart Path แสดง Informative State                    |

### QA Summary

```text
Total Test Cases: 14
Passed:           14
Failed:            0
```

**QA Result: ✅ 14/14 Pass**

---

# 23. Automated Tests Added / Updated

Sprint 3 เพิ่ม:

```text
tests/test_statistics.py
```

โดยครอบคลุม:

* Descriptive Statistics
* Genre Frequency
* Platform Frequency
* Release Year Frequency
* Empty Statistics
* Frequency with Proportion
* Numeric Values
* Top Current Players
* Game Comparison

นอกจากนี้ `tests/test_dashboard.py` มีการเพิ่ม Test สำหรับ:

* Multi-condition Filtering
* Sorting
* Missing Values
* Statistics Page Rendering
* Game Comparison
* Empty Statistics Library

---

# 24. Sprint 3 Scope vs Actual Implementation

เพื่อให้ Documentation ตรงกับ Source Code จึงสรุปความแตกต่างระหว่าง Scope เดิมกับ Implementation จริงดังนี้:

| Planned Scope                 | Actual Result                                                                                   |
| ----------------------------- | ----------------------------------------------------------------------------------------------- |
| Data Cleaning / Preparation   | ✅ Implemented ในรูปแบบ Data Normalization, Type Conversion และ Missing Optional Fields Handling |
| Rating Analysis               | ✅ Implemented                                                                                   |
| Genre Analysis                | ✅ Implemented                                                                                   |
| Platform Analysis             | ✅ Implemented                                                                                   |
| Release Year Analysis         | ✅ Implemented                                                                                   |
| Metacritic Analysis           | ✅ Implemented                                                                                   |
| Steam Player Analysis         | ✅ Implemented                                                                                   |
| Descriptive Statistics        | ✅ Implemented                                                                                   |
| Frequency / Proportion        | ✅ Implemented                                                                                   |
| Rating Distribution Chart     | ⚠️ ไม่มี Chart แยกสำหรับ Rating Distribution โดยตรง แต่มี Rating Summary และ Rating by Genre    |
| Genre Distribution            | ✅ Implemented                                                                                   |
| Platform Distribution         | ✅ Implemented                                                                                   |
| Rating Comparison by Genre    | ✅ Implementedเป็น Average Rating by Genre                                                       |
| Rating Comparison by Platform | ⚠️ ไม่มี Visualization แยกตาม Platform                                                          |
| Release Year Distribution     | ✅ Implemented                                                                                   |
| Metacritic Visualization      | ✅ Implemented                                                                                   |
| Steam Player Visualization    | ✅ Implemented                                                                                   |
| Advanced Filtering            | ✅ Implemented                                                                                   |
| Advanced Sorting              | ✅ Implemented                                                                                   |
| Data Comparison               | ✅ Implementedเป็น Game A vs Game B                                                              |
| Statistical Group Testing     | ❌ ไม่ได้ Implement                                                                              |
| Machine Learning              | ❌ ไม่ได้อยู่ใน Sprint 3                                                                         |
| Authentication                | ❌ ไม่ได้อยู่ใน Sprint 3                                                                         |
| CI/CD                         | ❌ ไม่ได้อยู่ใน Sprint 3                                                                         |
| AI Integration                | ❌ ไม่ได้อยู่ใน Sprint 3                                                                         |

> การระบุรายการที่ไม่ได้ Implement มีไว้เพื่อให้ Sprint Report สะท้อน Source Code จริงและไม่กล่าวอ้าง Feature ที่ไม่มีในระบบ

---

# 25. Technical Challenges & Solutions

## 25.1 RAWG Nested Data

**Problem:**
ข้อมูล Genre และ Platform จาก RAWG API อยู่ในรูปแบบ Nested Structure

**Solution:**
สร้าง Data Processing Functions สำหรับ Normalize Nested Fields ให้อยู่ใน List ของชื่อ Genre และ Platform ที่ระบบใช้งานได้โดยตรง

**Result:**
Analysis Layer สามารถนำข้อมูลไปใช้กับ Pandas และ Frequency Analysis ได้

---

## 25.2 Missing Optional Data

**Problem:**
เกมบางรายการอาจไม่มี Rating, Metacritic หรือข้อมูล Steam Player

**Solution:**
เก็บ Optional Values เป็น `None` และให้ Analysis Functions กรองค่าที่ไม่สามารถใช้คำนวณได้

**Result:**
ระบบสามารถแสดงข้อมูลส่วนที่มีอยู่และแสดง Informative / Empty State เมื่อข้อมูลไม่เพียงพอ

---

## 25.3 Dynamic Steam Player Data

**Problem:**
Steam Player Count เป็นข้อมูล Dynamic และมีการเปลี่ยนแปลงตลอดเวลา

**Solution:**
ใช้ Game Service จัดการ Refresh และเก็บข้อมูลใน SQLite พร้อม Timestamp และ Refresh Interval

**Result:**
Dashboard สามารถนำ Current Player Data ที่มีอยู่ใน Database ไปใช้ต่อใน Statistics ได้

---

## 25.4 Multiple Streamlit Sessions

**Problem:**
หลาย Streamlit Sessions อาจพยายาม Refresh Database Snapshot พร้อมกัน

**Solution:**
Game Service ใช้ Shared Locks สำหรับการ Refresh:

```text
_LIVE_TOP_REFRESH_LOCK
_CATALOG_REFRESH_LOCK
_PLAYERS_REFRESH_LOCK
```

**Result:**
ลดความเสี่ยงจากการ Refresh Shared Database พร้อมกันจากหลาย Sessions

---

## 25.5 Empty Dataset

**Problem:**
Statistics และ Visualization อาจได้รับ Dataset ที่ไม่มีข้อมูล

**Solution:**
ตรวจสอบ Dataset ก่อนคำนวณและก่อนสร้าง Chart

**Result:**
ระบบแสดง Informative Message แทนการเกิด Exception

---

# 26. Wow! — สิ่งที่ทำได้ดี

## 26.1 แยก Analysis Layer ออกจาก UI

การเพิ่ม:

```text
src/analysis/statistics.py
```

ทำให้ Logic การวิเคราะห์ข้อมูลแยกออกจาก Streamlit UI อย่างชัดเจน

ส่งผลให้:

* Code อ่านง่ายขึ้น
* Test Analysis Functions ได้โดยตรง
* ลดการเขียน Logic ซ้ำใน UI
* สามารถนำผล Analysis ไปใช้กับ Visualization ได้ง่ายขึ้น

---

## 26.2 Statistics และ Visualization เชื่อมต่อกับข้อมูลจริง

Statistics Page ไม่ได้ใช้ข้อมูลตัวอย่างแบบ Hard-coded แต่รับข้อมูลจาก Game Service และ SQLite แล้วส่งต่อเข้า Analysis Layer

```text
SQLite
  ↓
Game Service
  ↓
Statistics
  ↓
Visualization
```

---

## 26.3 รองรับข้อมูลที่ไม่สมบูรณ์

ระบบไม่ได้สมมติว่าข้อมูลทุกเกมจะมีครบทุก Field

ตัวอย่าง:

```text
Rating = None
Metacritic = None
Current Players = None
```

สามารถถูกจัดการได้โดยไม่ทำให้ Statistics Page Crash

---

## 26.4 Advanced Filtering ทำงานร่วมกันหลายเงื่อนไข

ผู้ใช้สามารถใช้:

```text
Genre
+
Platform
+
Minimum Rating
+
Release Year
```

พร้อมกันได้

ทำให้สามารถสำรวจข้อมูลใน Game Library ได้ละเอียดขึ้น

---

## 26.5 Test Coverage ของ Sprint 3 ครอบคลุม Core Features

Sprint 3 มี Test Cases ครอบคลุมทั้ง:

```text
Data Processing
Analysis
Statistics
Dashboard
Filter
Sort
Comparison
Empty State
Integration
```

และ QA Result ของ Sprint 3 ระบุ:

```text
14 / 14 Test Cases Passed
```

---

# 27. Whoops! — ปัญหาและการแก้ไข

## Problem 1 — ข้อมูลจาก RAWG เป็น Nested Structure

**Problem:**
Genre และ Platform ไม่ได้อยู่ในรูปแบบ Flat Data

**Solution:**
สร้าง Functions สำหรับ Extract และ Normalize ชื่อจาก Nested RAWG Records

**Result:**
สามารถนำข้อมูลไปใช้กับ Frequency และ Group Analysis ได้

---

## Problem 2 — ข้อมูล Optional ไม่ครบทุกเกม

**Problem:**
ข้อมูลบางเกมไม่มี Rating, Metacritic หรือ Steam Player Count

**Solution:**
ไม่แทน Missing ด้วย `0` โดยอัตโนมัติ และให้ Analysis Layer ใช้เฉพาะค่าที่ valid

**Result:**
Statistics และ Visualization สามารถทำงานต่อได้แม้ข้อมูลบางส่วนหายไป

---

## Problem 3 — Steam Player Data มีการเปลี่ยนแปลง

**Problem:**
ข้อมูล Steam Player Count ไม่ใช่ข้อมูล Static

**Solution:**
จัดการ Refresh ผ่าน Game Service และเก็บ Timestamp / Snapshot ใน SQLite

**Result:**
Dashboard สามารถใช้ข้อมูล Current Players ล่าสุดที่มีในระบบ

---

## Problem 4 — การทดสอบ Dashboard ต้องตรวจสอบทั้ง UI และ Data

**Problem:**
การทดสอบ Statistics ไม่สามารถตรวจเฉพาะฟังก์ชันคำนวณได้ เพราะต้องตรวจการเชื่อมต่อกับ Streamlit UI ด้วย

**Solution:**
ใช้ทั้ง Unit Tests และ Streamlit AppTest

**Result:**
สามารถตรวจสอบทั้ง Analysis Functions และ Dashboard Integration ได้

---

# 28. Contribution Matrix — Member Performance

Contribution Score ไม่ได้ถูกกำหนดไว้ใน Source Code / Sprint Result ดังนั้นจะไม่กำหนดคะแนนย้อนหลังโดยไม่มีหลักฐาน

## 28.1 Planner — ออม (นายเดโชชิต โตวินัส)

| งานที่รับผิดชอบ      | รายละเอียด                                |      คะแนน |
| -------------------- | ----------------------------------------- | ---------: |
| Sprint Planning      | กำหนด Goal, Scope และ Sprint Direction    |     10 / 10 |
| Requirements & DoD   | กำหนด Requirements และ Definition of Done |     10 / 10 |
| Task Allocation      | แบ่งงานและติดตามความคืบหน้า               |     10 / 10 |
| Integration Tracking | ติดตามการเชื่อมต่อ Features               |     10 / 10 |
| Documentation        | จัดทำและปรับปรุง Sprint Documentation     |     10 / 10 |
| **Total**            |                                           | **50 / 50** |

---

## 28.2 Coder — คิม (นายชิษณุพงศ์ ซู)

| งานที่รับผิดชอบ               | รายละเอียด                                       |      คะแนน |
| ----------------------------- | ------------------------------------------------ | ---------: |
| Data Processing & Preparation | พัฒนา Data Normalization และเตรียมข้อมูล         |     10 / 10 |
| EDA & Statistics              | พัฒนา Analysis และ Statistics                    |     10 / 10 |
| Dashboard Statistics          | พัฒนา Summary Statistics                         |     10 / 10 |
| Visualization                 | พัฒนา Charts และเชื่อมต่อ Dashboard              |     10 / 10 |
| Advanced Features             | พัฒนา Filter / Sort / Comparison และ Integration |     10 / 10 |
| **Total**                     |                                                  | **50 / 50** |


---

## 28.3 Debugger — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

| งานที่รับผิดชอบ         | รายละเอียด                               |      คะแนน |
| ----------------------- | ---------------------------------------- | ---------: |
| Test Case Design        | ออกแบบ Test Cases สำหรับ Sprint 3        |     10 / 10 |
| Data Quality Testing    | ตรวจสอบ Data Processing และ Data Quality |     10 / 10 |
| Statistics Verification | ตรวจสอบผลการคำนวณ Statistics             |     10 / 10 |
| Integration Testing     | ตรวจสอบการทำงานร่วมกันของระบบ            |     10 / 10 |
| Bug Verification        | ตรวจสอบ Error และผลหลังแก้ไข             |     10 / 10 |
| **Total**               |                                          | **50 / 50** |


---

# 29. Contribution Summary

| สมาชิก | ชื่อเล่น | Role     | คะแนนที่ได้รับ | คะแนนเต็ม | Completion |
| --------- | --- | -------- | -------------: | --------: | ---------: |
| นายเดโชชิต โตวินัส | ออม | Planner  |              50 |        50 |          100% |
| นายชิษณุพงศ์ ซู | คิม | Coder    |              50 |        50 |          100% |
| นายภานุวัฒน์ ผองแก้ว | ฟลุ๊ค | Debugger |              50 |        50 |          100% |
| | |          |          **150** |   **150** |      **100%** |


---

# 30. Definition of Done

## Data Processing & Analysis

* [x] มี Data Processing และ Data Normalization
* [x] มีการแปลงชนิดข้อมูลสำหรับ Analysis
* [x] มีการจัดการ Missing Optional Values
* [x] มี Analysis Layer
* [x] มี Descriptive Statistics
* [x] มี Genre / Platform Frequency
* [x] มี Frequency / Proportion
* [x] มี Release Year Analysis
* [x] มี Metacritic Analysis
* [x] มี Steam Player Analysis
* [x] มี Game Comparison
* [x] มี Unit Tests สำหรับ Analysis Functions

## Dashboard & Visualization

* [x] มี Statistics Page
* [x] มี Summary Metrics
* [x] มี Genre Distribution
* [x] มี Platform Distribution
* [x] มี Rating by Genre
* [x] มี Release Year Distribution
* [x] มี Metacritic Distribution
* [x] มี Top Live Steam Players
* [x] มี Game Comparison Table
* [x] มี Empty State
* [x] Statistics และ Visualization เชื่อมต่อกับข้อมูลจริง

## Advanced Features

* [x] Advanced Filtering
* [x] Genre Filter
* [x] Platform Filter
* [x] Minimum Rating Filter
* [x] Release Year Filter
* [x] Multi-condition Filtering
* [x] Rating Sorting
* [x] Release Date Sorting
* [x] Name Sorting
* [x] Missing Value Sorting Handling
* [x] Game-to-Game Comparison

## Testing

* [x] Unit Tests สำหรับ Statistics
* [x] Data Processing Tests
* [x] Dashboard Tests
* [x] Statistics Page Integration Test
* [x] Empty Dataset Test
* [x] Missing Data Test
* [x] Filter Test
* [x] Sorting Test
* [x] Comparison Test
* [x] QA Test Cases S3-TC-01 ถึง S3-TC-14
* [x] QA Result บันทึกครบ

## Documentation

* [x] Sprint 3 Report
* [x] Project Plan อัปเดต Sprint 3
* [x] Change Log มี Sprint 3
* [x] Learning Log มี Sprint 3
* [x] README ระบุ Sprint 3 Completed

## GitHub / Source

* [x] Source Code ของ Sprint 3 อยู่ใน Repository
* [x] Tests ของ Sprint 3 อยู่ใน Repository
* [x] Documentation ของ Sprint 3 อยู่ใน Repository


---

# 31. Sprint 3 Review

## Sprint Goal

Sprint 3 บรรลุเป้าหมายหลักในการเพิ่มความสามารถด้าน Data Analysis, Statistics, Visualization และ Advanced Features ให้กับ Gaming Statistics Dashboard

จากเดิมที่ระบบเน้น:

```text
Search
View Games
API
Database
Dashboard
```

ระบบใน Sprint 3 เพิ่ม:

```text
Data Processing
      ↓
Analysis
      ↓
Statistics
      ↓
Visualization
      ↓
Game Comparison
      ↓
Advanced Filter / Sort
```

---

## Completed Features

### Data Processing

* RAWG Data Normalization
* Numeric Conversion
* Release Date Processing
* Genre / Platform Normalization
* Missing Optional Data Handling

### Analysis

* Descriptive Statistics
* Genre Frequency
* Platform Frequency
* Genre Rating Mean
* Release Year Frequency
* Metacritic Numeric Analysis
* Steam Player Ranking
* Game Comparison

### Dashboard

* Statistics Page
* Summary Metrics
* 6 Visualization Sections
* Comparison Table
* Empty State

### Advanced Features

* Multi-condition Filtering
* Advanced Sorting
* Missing Value Sorting
* Game Comparison

### Testing

* Statistics Unit Tests
* Dashboard Integration Tests
* Filter Tests
* Sort Tests
* Comparison Tests
* Empty State Tests
* 14 Sprint 3 QA Test Cases Passed

---

# 32. Partially Implemented / Scope Adjustments

บางรายการจาก Scope เริ่มต้นถูกปรับให้ตรงกับ Implementation จริง:

### Rating Distribution

ใน Scope เดิมมีแนวคิดเรื่อง Rating Distribution แต่ Implementation ปัจจุบันไม่ได้สร้าง Chart สำหรับ Distribution ของ Rating โดยตรง

สิ่งที่มีจริงคือ:

```text
Rating Summary
Rating by Genre
```

---

### Platform Rating Comparison

Scope เดิมเปิดไว้สำหรับ Rating Comparison ตาม Platform แต่ Implementation ปัจจุบันไม่ได้สร้าง Chart สำหรับ Average Rating by Platform

---

### Data Comparison

จากเดิมที่ระบุคำว่า Data Comparison ในลักษณะกว้าง ปัจจุบัน Implementation ถูกกำหนดชัดเจนเป็น:

```text
Game A vs Game B
```

โดยเปรียบเทียบ:

```text
Rating
Metacritic
Steam Players
```

---

### Statistical Testing

Sprint 3 ไม่ได้พัฒนา:

```text
t-test
ANOVA
Chi-square
Correlation Test
Regression
Machine Learning
```

เนื่องจากไม่ได้อยู่ใน Implementation ปัจจุบัน

Sprint 3 จึงเน้น **Descriptive Statistics และ Exploratory Analysis**

---

# 33. Known Limitations

ข้อจำกัดของ Implementation ปัจจุบัน:

1. Descriptive Statistics หลักเน้น Rating
2. ไม่มี Inferential Statistical Testing
3. ไม่มี Machine Learning
4. ไม่มีระบบ Authentication
5. ไม่มี CI/CD ใน Sprint 3
6. ไม่มี AI Integration ใน Sprint 3
7. Rating Distribution ยังไม่มี Chart แยกโดยตรง
8. Platform Average Rating ยังไม่มี Visualization แยก
9. Game Comparison จำกัดที่เกม 2 รายการต่อครั้ง
10. Steam Player Analysis ใช้เฉพาะข้อมูล Current Players ที่มีอยู่ในระบบ

ข้อจำกัดเหล่านี้ไม่ได้ถือเป็น Bug ของ Sprint 3 แต่เป็นขอบเขตของ Implementation ปัจจุบัน

---

# 34. Next Sprint Considerations

งานที่สามารถนำไปพัฒนาต่อใน Final Sprint ได้แก่:

* Final System Integration
* Full Regression Testing
* Performance / Reliability Testing
* Automated Testing เพิ่มเติม
* GitHub Actions / CI/CD
* AI Integration ตาม Scope ของ Final Sprint
* Final QA
* Bug Fixing
* Final Documentation
* Final Presentation

Sprint 4 จะนำผลลัพธ์จาก Sprint 3 ไปใช้เป็นฐานสำหรับ Final Project

---

# 35. Final Sprint 3 Status

## Data Processing & Analysis

**✅ Completed**

มี Data Processing, Analysis Layer, Descriptive Statistics, Frequency / Proportion และ Additional Analysis ตาม Implementation จริง

---

## Dashboard Statistics & Visualization

**✅ Completed**

มี Statistics Page พร้อม Summary Metrics และ Visualization 6 Sections

---

## Advanced Features

**✅ Completed**

มี Multi-condition Filtering, Sorting และ Game Comparison

---

## Testing & Integration

**✅ Completed**

มี Unit Tests, Dashboard Integration Tests และ QA Test Cases S3-TC-01 ถึง S3-TC-14 โดยผลการทดสอบที่บันทึกไว้เป็น Pass ทั้งหมด

---

## Documentation

**✅ Completed**

Sprint 3 Documentation ได้รับการจัดทำและปรับให้สะท้อน Implementation ของ Sprint 3

---

# 36. Sprint 3 Final Summary

Sprint 3 ได้ยกระดับ Gaming Statistics Dashboard จากระบบที่เน้นการค้นหาและแสดงข้อมูลเกม ไปสู่ระบบที่สามารถนำข้อมูลเกมมาวิเคราะห์และนำเสนอในรูปแบบ Statistics และ Visualization ได้

Architecture ของระบบได้รับการขยายด้วย Analysis Layer:

```text
RAWG / Steam
     ↓
Data Processing
     ↓
SQLite
     ↓
Game Service
     ↓
Analysis Layer
     ↓
Statistics
     ↓
Visualization
     ↓
Streamlit Dashboard
```

Feature หลักที่เสร็จสมบูรณ์:

```text
✅ Data Processing
✅ Data Analysis
✅ Descriptive Statistics
✅ Genre / Platform Analysis
✅ Release Year Analysis
✅ Metacritic Analysis
✅ Steam Player Analysis
✅ Statistics Dashboard
✅ 6 Visualization Sections
✅ Advanced Filtering
✅ Advanced Sorting
✅ Game Comparison
✅ Empty State Handling
✅ Unit Testing
✅ Dashboard Integration Testing
✅ QA 14/14 Passed
```

**Current Sprint Status: ✅ Completed**

> Sprint 3 successfully delivered the Data Analysis, Visualization and Advanced Feature layer required to extend the Gaming Statistics Dashboard toward the Final Project.

```
```
