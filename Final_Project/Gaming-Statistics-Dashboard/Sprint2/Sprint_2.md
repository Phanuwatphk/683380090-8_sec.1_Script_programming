# 🎮 Gaming Statistics Dashboard — Sprint 2 Report

> บันทึกประวัติตามช่วง Sprint: โครงสร้างและพฤติกรรมบางส่วนเปลี่ยนในรุ่นส่งมอบ ให้ใช้ [README](../README.md) สำหรับการติดตั้ง/ใช้งานปัจจุบัน และ [Final QA](../docs/FINAL_QA.md) สำหรับผลตรวจล่าสุด

## Final Term Project — CP352301 Script Programming

**Sprint:** Sprint 2 — Web UI, API Integration & Database  
**Period:** 20–24 September 2026 (20–24 กันยายน 2569)
**Status:** ✅ Completed

**Repository:** https://github.com/Phanuwatphk/Gaming-Statistics-Dashboard

---

# 1. Sprint Overview

Sprint 2 เป็นการพัฒนาต่อยอดจาก Sprint 1
โดยเปลี่ยนระบบจาก Command Line Interface (CLI)
ให้เป็น Web Application ที่สามารถใช้งานผ่าน Web Browser

ใน Sprint นี้ทีมได้พัฒนาและเชื่อมต่อระบบหลัก ได้แก่

- Web UI ด้วย Streamlit
- RAWG Video Games Database API
- Steam API สำหรับข้อมูลจำนวนผู้เล่นปัจจุบัน
- SQLite Database
- Data Processing
- Service Layer
- Search และ Pagination
- Game Library
- Genre Exploration
- Top Rated Games
- Live Players
- Game Detail
- Automated Testing

ระบบถูกออกแบบให้แยกส่วนการทำงานระหว่าง

```text
Web UI
   ↓
Game Service
   ↓
Data Processing
   ↓
API
   ↓
SQLite Database
   ↓
Web Dashboard
````

โดย Sprint 2 ไม่ได้เป็นเพียงการเปลี่ยนจาก CLI เป็น Web UI
แต่เป็นการพัฒนาโครงสร้าง Application ให้สามารถทำงานร่วมกับ External API
และ Database ได้จริง

---

# 2. Sprint Goal

> พัฒนา Gaming Statistics Dashboard จาก CLI Foundation
> ให้เป็น Web Application ที่สามารถใช้งานผ่าน Web Browser
> พร้อมเชื่อมต่อข้อมูลจริงจาก RAWG และ Steam API
> และจัดเก็บข้อมูลด้วย SQLite

เมื่อจบ Sprint 2 ระบบสามารถ:

* เปิดใช้งานผ่าน Web Browser
* แสดง Web Dashboard
* ดึงข้อมูลเกมจาก RAWG API
* ค้นหาเกมจาก RAWG
* จัดเก็บข้อมูลเกมลง SQLite
* อ่านข้อมูลเกมจาก SQLite
* แสดง Game Library
* Filter เกมตาม Genre
* Filter เกมตาม Platform
* Filter เกมตาม Minimum Rating
* แสดง Top Rated Games
* แสดง Game Detail
* แสดง Steam Live Players
* แสดง Steam Top 100
* แสดงจำนวนผู้เล่นปัจจุบัน
* แสดงเวลาอัปเดตข้อมูล
* จัดการ API Error
* จัดการ Database Error
* จัดการ Empty State
* มี Automated Tests สำหรับ Core Modules

---

# 3. Team Members & Roles

| สมาชิก | ชื่อเล่น | Role          | หน้าที่หลัก                                                                            |
| --------- | --- | ------------- | -------------------------------------------------------------------------------------- |
| นายภานุวัฒน์ ผองแก้ว | ฟลุ๊ค | Planner       | Sprint Planning, Scope, Requirements, Architecture, Documentation และติดตามความคืบหน้า |
| นายเดโชชิต โตวินัส | ออม | Coder         | Web Application, Streamlit UI, RAWG API, Steam API, SQLite และ Application Logic       |
| นายชิษณุพงศ์ ซู | คิม | Debugger / QA | Testing, QA, Edge Cases, Error Checking และ Bug Verification                           |

---

# 4. Sprint 2 Scope

## In Scope

สิ่งที่พัฒนาใน Sprint 2:

### Web Application

* Streamlit Web Application
* Dashboard Layout
* Sidebar Navigation
* Home Page
* Game Library
* Search Page
* Genres Page
* Top Rated Page
* Live Players Page
* Game Detail Page

### RAWG API

* RAWG API Client
* API Key Configuration
* Game Listing
* Game Search
* RAWG Pagination
* RAWG Error Handling
* API Response Validation

### Steam API

* Steam Store Search
* Steam App ID Matching
* Current Player Count
* Steam Most Played Games
* Steam App Details
* Steam Top 100
* Live Player Ranking
* Steam Error Handling

### Database

* SQLite Database
* Games Table
* Dashboard Metadata Table
* Game Insert / Update
* Game Search
* Steam Mapping
* Current Player Data
* Refresh Timestamp
* Live Ranking Snapshot

### Data Processing

* RAWG Data Normalization
* Genre Normalization
* Platform Normalization
* Missing Value Handling
* Type Conversion
* Duplicate Name Handling

### Application Features

* Search
* Filter
* Sort
* Pagination
* Game Detail
* Top Rated
* Genre Exploration
* Live Players
* Refresh / Snapshot System

### Testing

* API Tests
* Steam API Tests
* Database Tests
* Game Service Tests
* Data Processing Tests
* Time Utility Tests
* Dashboard Tests

---

## Out of Scope

สิ่งที่ยังไม่ถือเป็น Core Scope ของ Sprint 2:

* Advanced Statistical Analysis
* Correlation Analysis
* Advanced EDA
* Machine Learning
* Prediction
* Advanced Data Visualization
* Complex Statistical Dashboard
* AI Integration
* GitHub Actions / CI/CD

Features ดังกล่าวสามารถพัฒนาต่อใน Sprint ถัดไปตาม Project Plan

---

# 5. System Architecture

โครงสร้างการทำงานหลักของระบบ:

```text
                    ┌────────────────────┐
                    │    Web Browser     │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │   Streamlit UI     │
                    │   Dashboard        │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │    Game Service    │
                    └──────┬───────┬─────┘
                           │       │
                 ┌─────────┘       └─────────┐
                 ▼                           ▼
        ┌─────────────────┐         ┌─────────────────┐
        │    RAWG API     │         │    Steam API    │
        └────────┬────────┘         └────────┬────────┘
                 │                           │
                 └───────────┬───────────────┘
                             ▼
                    ┌────────────────────┐
                    │  Data Processing   │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │   SQLite Database  │
                    └────────────────────┘
```

---

# 6. Project Structure

โครงสร้าง Project ที่ใช้งานจริงใน Sprint 2:

```text
Gaming-Statistics-Dashboard/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env
├── .env.example
│
├── data/
│   └── gaming_statistics.db
│
├── docs/
│   ├── CHANGELOG.md
│   ├── LEARNINGLOG.md
│   ├── Plan.md
│   └── Project_Pitch.md
│
├── Sprint1/
│   └── Sprint_1.md
│
├── Sprint2/
│   └── Sprint_2.md
│
├── src/
│   ├── __init__.py
│   ├── app.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── rawg_api.py
│   │   └── steam_api.py
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   └── styles.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── game_service.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_processing.py
│   │   └── time_utils.py
│   │
│   └── lagacy/
│       └── main.py
│
└── tests/
    ├── test_dashboard.py
    ├── test_data_processing.py
    ├── test_database.py
    ├── test_game_service.py
    ├── test_rawg_api.py
    ├── test_steam_api.py
    └── test_time_utils.py
```

---

# 7. Tools & Technologies

| Technology    | Usage                                    |
| ------------- | ---------------------------------------- |
| Python        | Main programming language                |
| Streamlit     | Web Application และ Dashboard            |
| Requests      | HTTP Request สำหรับ API                  |
| RAWG API      | ข้อมูลเกม                                |
| Steam API     | ข้อมูลผู้เล่นปัจจุบันและ Steam Top Games |
| SQLite        | Database                                 |
| Pandas        | Data Processing / Data Management        |
| python-dotenv | จัดการ Environment Variables             |
| pytest        | Automated Testing                        |
| Git           | Version Control                          |
| GitHub        | Repository และ Collaboration             |
| VS Code       | Development Environment                  |

---

# 8. RAWG API Integration

## 8.1 RAWG API Client

สร้าง:

```text
src/api/rawg_api.py
```

รับผิดชอบการติดต่อ RAWG API โดยไม่ให้ UI ติดต่อ API โดยตรง

### Features

* Fetch Games
* Search Games
* Pagination
* Ordering
* API Key Configuration
* Timeout Handling
* Connection Error Handling
* HTTP Error Handling
* JSON Validation

---

## 8.2 RAWG API Data

ข้อมูลหลักที่ระบบนำมาใช้:

| Field         | Description         |
| ------------- | ------------------- |
| game_id       | RAWG Game ID        |
| name          | Game Name           |
| rating        | Rating              |
| released      | Release Date        |
| genres        | Game Genres         |
| platforms     | Supported Platforms |
| metacritic    | Metacritic Score    |
| ratings_count | Number of Ratings   |
| image         | Game Image          |

---

## 8.3 RAWG Error Handling

ระบบมีการจัดการกรณี:

* API Key หาย
* API Key ไม่ถูกต้อง
* HTTP Error
* Connection Error
* Timeout
* Invalid JSON
* Unexpected API Response
* Empty Result

---

# 9. Steam API Integration

ใน Sprint 2 ได้มีการเพิ่ม Steam API
เพื่อให้ระบบสามารถแสดงข้อมูลจำนวนผู้เล่นที่กำลัง Online อยู่ในเกม
และจัดอันดับเกมที่มีผู้เล่นปัจจุบันสูงได้

สร้าง:

```text
src/api/steam_api.py
```

---

## 9.1 Steam Store Search

ระบบสามารถค้นหา Steam App ID จากชื่อเกม

โดยใช้ Exact Name Matching
เพื่อป้องกันการจับคู่กับเกมที่มีชื่อใกล้เคียงแต่ไม่ใช่เกมเดียวกัน

ตัวอย่าง:

```text
Portal 2
↓
Steam Store Search
↓
Steam App ID
```

---

## 9.2 Current Player Count

ระบบสามารถเรียกจำนวนผู้เล่นปัจจุบันของ Steam App ได้

ตัวอย่าง:

```text
Game
↓
Steam App ID
↓
GetNumberOfCurrentPlayers
↓
Current Players
```

ข้อมูลถูกจัดเก็บลง SQLite พร้อมเวลาอัปเดต

---

## 9.3 Steam Most Played Games

ระบบสามารถดึงข้อมูลเกมที่กำลังมีผู้เล่นสูงจาก Steam

ข้อมูลที่นำมาใช้ เช่น:

* Steam App ID
* Game Name
* Current Players
* Live Rank
* Image
* Genre

---

## 9.4 Steam Top 100

ระบบสร้างหน้า:

```text
Live Players
```

สำหรับแสดง Steam Top 100

โดยเรียงตามจำนวนผู้เล่นปัจจุบัน

ตัวอย่าง:

```text
#1 Game A      120,000 Players
#2 Game B       95,000 Players
#3 Game C       80,000 Players
...
#100 Game X      5,000 Players
```

---

## 9.5 Steam Snapshot

ระบบไม่ได้เรียก Steam API ทุกครั้งที่ผู้ใช้เปิดหน้า

แต่ใช้ระบบ Snapshot และ Refresh Interval

ค่าเริ่มต้น:

```text
15 minutes
```

ข้อมูลที่เกี่ยวข้องถูกจัดเก็บไว้ใน SQLite

ทำให้ผู้ใช้หลายคนสามารถอ่านข้อมูลจาก Snapshot เดียวกันได้
และลดจำนวน API Requests

---

# 10. Data Processing

สร้าง:

```text
src/utils/data_processing.py
```

หน้าที่หลักคือ Normalize ข้อมูลจาก RAWG API

### Processing ที่ทำ

* Convert Game ID เป็น Integer
* Convert Rating เป็น Float
* Convert Metacritic เป็น Integer
* Convert Ratings Count เป็น Integer
* Normalize Genres
* Normalize Platforms
* Handle Missing Values
* Normalize Game Name
* Remove Duplicate Genre / Platform Values

ตัวอย่าง RAWG:

```text
genres:
[
    {"name": "Action"},
    {"name": "RPG"}
]
```

ถูกแปลงเป็น:

```text
["Action", "RPG"]
```

Platforms ถูกจัดการในลักษณะเดียวกัน

---

# 11. SQLite Database

สร้าง:

```text
src/database/database.py
```

ใช้ SQLite เป็น Local Database ของ Application

---

## 11.1 Games Table

ข้อมูลหลัก:

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
steam_app_id
steam_lookup_status
current_players
players_updated_at
catalog_updated_at
catalog_rank
is_live_top
live_rank
```

---

## 11.2 Dashboard Metadata

สร้าง Table:

```text
dashboard_metadata
```

ใช้เก็บข้อมูลระบบ เช่น:

* players_last_refresh
* catalog_last_refresh
* live_top_last_refresh

เพื่อควบคุม Refresh Interval

---

## 11.3 Database Functions

ระบบรองรับ:

* Create Database
* Create Table
* Insert Games
* Update Games
* Read Games
* Search Games
* Check Existing Game
* Steam App Mapping
* Update Current Players
* Save Live Top Games
* Read Live Top Games
* Save Metadata
* Read Metadata

---

# 12. Game Service

สร้าง:

```text
src/services/game_service.py
```

ทำหน้าที่เป็น Service Layer
เพื่อแยก Application Logic ออกจาก UI และ API

---

## Responsibilities

* Fetch RAWG Games
* Search RAWG
* Process RAWG Data
* Save Games
* Read Games
* Search Local Database
* Import Search Results
* Import Catalog Pages
* Refresh RAWG Catalog
* Refresh Steam Player Data
* Refresh Steam Top Games
* Manage Refresh Interval
* Provide Dashboard-ready Data

---

# 13. Streamlit Web Application

Entry Point:

```text
src/app.py
```

Run ด้วย:

```bash
streamlit run src/app.py
```

---

# 14. Web Application Pages

ระบบมี Navigation หลัก:

```text
Home
Game Library
Search
Genres
Top Rated
Live Players
```

และมี:

```text
Game Detail
```

สำหรับดูรายละเอียดของเกม

---

# 15. Home Page

หน้า Home แสดง:

* Popular Games
* Steam Top 100 Total Players
* Game Cards
* Game Rating
* Current Players
* Genre
* Pagination
* Game Details

ระบบสามารถดึง Popular Games จาก RAWG
และ Live Player Data จาก Steam Snapshot

---

# 16. Game Library

หน้า Game Library ใช้สำหรับเรียกดูเกมที่ถูกบันทึกไว้ใน SQLite

สามารถ:

* ดู Game Cards
* Filter Genre
* Filter Platform
* Filter Minimum Rating
* Pagination
* View Details

ตัวอย่าง Filter:

```text
Genre
Platform
Minimum Rating
```

---

# 17. Search

หน้า Search สามารถ:

1. ค้นหาเกมจาก SQLite ก่อน
2. หากไม่พบข้อมูล
3. เรียก RAWG API
4. บันทึกผลลัพธ์ลง SQLite
5. แสดงผลลัพธ์บน Dashboard

Flow:

```text
User Search
     ↓
SQLite Search
     ↓
พบข้อมูล?
 ┌───┴───┐
Yes      No
 ↓        ↓
Show    RAWG API
         ↓
      Save SQLite
         ↓
       Display
```

ระบบยังรองรับ Pagination สำหรับ Search Result จาก RAWG

---

# 18. Genres

หน้า Genres ใช้สำหรับจัดกลุ่มเกมตาม Genre

ตัวอย่าง:

```text
Action
  ├── Game A
  ├── Game B
  └── Game C

RPG
  ├── Game D
  ├── Game E
  └── Game F
```

เกมหนึ่งเกมสามารถอยู่ในหลาย Genre ได้

---

# 19. Top Rated

หน้า Top Rated

แสดงเกมที่มี Rating สูง
โดยเรียงจาก Rating สูงไปต่ำ

ตัวอย่าง:

```text
#1 Game A    4.9
#2 Game B    4.8
#3 Game C    4.7
```

---

# 20. Live Players

หน้า Live Players แสดง Steam Top 100

ข้อมูล:

* Rank
* Game Name
* Current Players
* Game Image
* Genre
* Update Time

ข้อมูลถูกเรียงตามจำนวนผู้เล่นปัจจุบัน

---

# 21. Game Detail

หน้า Game Detail แสดงข้อมูลของเกม เช่น:

* Game Name
* Game Image
* Rating
* Steam Players Now
* Release Date
* Platforms
* Metacritic
* Genres

หากเกมไม่มีข้อมูล Steam Player Count
ระบบจะแสดง:

```text
N/A
```

แทนการทำให้ Application Crash

---

# 22. Pagination

ระบบเพิ่ม Pagination เพื่อไม่ให้ Dashboard แสดงเกมจำนวนมากในครั้งเดียว

จำนวนเกมต่อหน้า:

```text
50 Games
```

รองรับ:

```text
Previous
Page
Next
```

ทั้ง Local Data และ Remote API Results

---

# 23. Error & Empty State Handling

ระบบรองรับสถานการณ์ต่าง ๆ เช่น:

### API Error

```text
Unable to fetch data
```

### Database Error

```text
Database Error
```

### Empty Database

```text
Your library is empty
```

### Search Not Found

```text
No matching games
```

### Missing Live Data

```text
Live Steam data is unavailable
```

### Missing Image

```text
No cover image available
```

เป้าหมายคือไม่ให้ User พบ Python Traceback
จาก Error ที่สามารถจัดการได้ในระดับ Application

---

# 24. Configuration

ใช้ Environment Variable สำหรับ API Key

```text
RAWG_API_KEY
```

ตัวอย่าง:

```text
RAWG_API_KEY=your_api_key_here
```

นอกจากนี้มี Configuration:

```text
PLAYER_REFRESH_MINUTES
GAMING_DASHBOARD_DB
```

ค่าเริ่มต้น:

```text
PLAYER_REFRESH_MINUTES = 15
GAMING_DASHBOARD_DB = data/gaming_statistics.db
```

ไฟล์ `.env` ไม่ควรถูก Commit เข้า GitHub

---

# 25. Development Tasks

## Task 1 — Web Application

### Planner — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

* กำหนด Web Application Scope
* กำหนด Navigation
* ตรวจสอบ Dashboard Requirements
* ตรวจสอบ Architecture
* ติดตามความคืบหน้า

### Coder — ออม (นายเดโชชิต โตวินัส)

* สร้าง Streamlit Entry Point
* สร้าง Dashboard
* สร้าง Sidebar Navigation
* สร้าง Page Components

### Debugger — คิม (นายชิษณุพงศ์ ซู)

* ตรวจสอบ Web UI
* ตรวจสอบ Navigation
* ตรวจสอบ Empty State
* ตรวจสอบ UI Errors

---

## Task 2 — RAWG API

### Planner — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

* กำหนดข้อมูลที่ต้องใช้
* ตรวจสอบ API Scope
* ตรวจสอบ Error Cases

### Coder — ออม (นายเดโชชิต โตวินัส)

* สร้าง RAWG API Client
* Implement Game Fetch
* Implement Search
* Implement Pagination
* Implement Error Handling

### Debugger — คิม (นายชิษณุพงศ์ ซู)

* ทดสอบ API Response
* ทดสอบ Invalid API Key
* ทดสอบ Connection Error
* ทดสอบ Empty Response

---

## Task 3 — Steam API

### Planner — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

* กำหนด Live Player Feature
* กำหนด Steam Data Flow
* กำหนด Snapshot Concept

### Coder — ออม (นายเดโชชิต โตวินัส)

* Implement Steam Store Search
* Implement Steam App ID Mapping
* Implement Current Player Count
* Implement Steam Top Games
* Implement Steam App Details
* Implement Concurrent Requests
* Implement Steam Error Handling

### Debugger — คิม (นายชิษณุพงศ์ ซู)

* ทดสอบ Steam API
* ทดสอบ Current Player Count
* ทดสอบ Invalid Response
* ทดสอบ Connection Error
* ตรวจสอบ Ranking

---

## Task 4 — SQLite Database

### Planner — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

* ออกแบบ Database Concept
* กำหนดข้อมูลที่ต้องจัดเก็บ
* ตรวจสอบ Data Flow

### Coder — ออม (นายเดโชชิต โตวินัส)

* Implement SQLite Connection
* Create Games Table
* Create Metadata Table
* Insert / Update Data
* Search Data
* Live Player Snapshot
* Refresh Metadata

### Debugger — คิม (นายชิษณุพงศ์ ซู)

* ทดสอบ Database Creation
* ทดสอบ Insert
* ทดสอบ Read
* ทดสอบ Search
* ทดสอบ Duplicate Handling

---

## Task 5 — Integration

### Planner — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

* ตรวจสอบ Architecture
* ตรวจสอบ Data Flow
* ตรวจสอบ Scope

### Coder — ออม (นายเดโชชิต โตวินัส)

* Connect API
* Connect Data Processing
* Connect SQLite
* Connect Streamlit
* Implement Service Layer

### Debugger — คิม (นายชิษณุพงศ์ ซู)

* Integration Testing
* Error Flow Testing
* Empty State Testing
* Search Testing
* Pagination Testing

---

# 26. Sprint 2 Daily Task Allocation & Update

Sprint 2 ดำเนินงานระหว่างวันที่ **20–24 กันยายน 2569**

| วันที่           | Planner — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)                                       | Coder — ออม (นายเดโชชิต โตวินัส)                                                     | Debugger / QA — คิม (นายชิษณุพงศ์ ซู)                               | Daily Update                                                  |
| ---------------- | ----------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------- |
| **20 ก.ย. 2569** | ตรวจสอบ Sprint 2 Scope, Architecture และ Requirements | เริ่มปรับโครงสร้าง Project และเตรียม Web Application            | ตรวจสอบ Requirements และเตรียม Test Cases         | **เริ่ม Sprint 2 และเตรียมโครงสร้างสำหรับ Web Application**   |
| **21 ก.ย. 2569** | ตรวจสอบ Web UI Flow และ API/Data Flow                 | พัฒนา Streamlit Dashboard, Navigation และ RAWG API              | ทดสอบ Web UI และตรวจสอบ API Response              | **Web UI และ RAWG API เริ่มทำงานร่วมกัน**                     |
| **22 ก.ย. 2569** | ตรวจสอบ Database Design และ Integration               | พัฒนา SQLite, Data Processing และ Game Service                  | ทดสอบ Database, Data Processing และ Service Layer | **API → Processing → SQLite Data Flow ทำงานได้**              |
| **23 ก.ย. 2569** | ตรวจสอบ Feature Scope และติดตาม Integration           | เพิ่ม Steam API, Live Players, Pagination และปรับปรุง Dashboard | ทดสอบ Steam API, Live Player Data และ Edge Cases  | **เพิ่ม Steam Live Player Feature และปรับปรุง Web Dashboard** |
| **24 ก.ย. 2569** | ตรวจสอบ Definition of Done และจัดทำ Sprint Report     | แก้ Bugs, ปรับ UI และตรวจสอบ Final Version                      | ทดสอบ Core Modules และสรุป QA Result              | **สรุป Sprint 2 และตรวจสอบระบบก่อนส่งมอบ**                    |

---

# 27. Sprint Progress

| Area                      | Status            |
| ------------------------- | ----------------- |
| Streamlit Web Application | ✅ Completed       |
| Dashboard Navigation      | ✅ Completed       |
| RAWG API                  | ✅ Completed       |
| RAWG Search               | ✅ Completed       |
| RAWG Pagination           | ✅ Completed       |
| Data Processing           | ✅ Completed       |
| SQLite Database           | ✅ Completed       |
| Game Service              | ✅ Completed       |
| Game Library              | ✅ Completed       |
| Search                    | ✅ Completed       |
| Genre                     | ✅ Completed       |
| Top Rated                 | ✅ Completed       |
| Game Detail               | ✅ Completed       |
| Steam API                 | ✅ Completed       |
| Steam Current Players     | ✅ Completed       |
| Steam Top 100             | ✅ Completed       |
| Live Player Snapshot      | ✅ Completed       |
| Refresh Interval          | ✅ Completed       |
| Error Handling            | ✅ Completed       |
| Pagination                | ✅ Completed       |
| Automated Tests           | ✅ Implemented     |
| CI/CD                     | ⏳ Not in Sprint 2 |
| Advanced Statistics       | ⏳ Next Sprint     |

---

# 28. QA Test Cases

Sprint 2 มี Automated Tests ครอบคลุม:

| Test Area       | Coverage                                                                     |
| --------------- | ---------------------------------------------------------------------------- |
| RAWG API        | API Response, API Key, Search, Pagination, HTTP Error, Network Error         |
| Steam API       | App ID Matching, Player Count, Connection Error, Invalid Response, Top Games |
| Database        | Database, Table, Insert, Read, Search, Duplicate, Metadata, Live Snapshot    |
| Game Service    | Search, Import, Catalog, Steam Live Data, Pagination                         |
| Data Processing | Game ID, Rating, Genres, Platforms, Missing Values                           |
| Time Utilities  | UTC Conversion, Thailand Time, Legacy Timestamp                              |
| Dashboard       | Genre Page, Timestamp Display                                                |

---

# 29. QA Result

จากการตรวจสอบใน Development Environment:

```text
Core/API/Database/Service Tests : 40 Passed
Compilation Check              : Passed
Dashboard Tests                : Not fully executed
```

การทดสอบ Dashboard ใน Environment ที่ใช้ตรวจสอบครั้งนี้
ไม่สามารถ Collection Test ได้เนื่องจาก Environment ไม่มี
`streamlit` package

ดังนั้นจึงยังไม่ควรสรุปว่า Test Suite ทั้งหมดมี
100% Pass Rate จากการตรวจสอบครั้งนี้

ก่อนส่งมอบจริงควรติดตั้ง Dependencies จาก:

```bash
pip install -r requirements.txt
```

และรัน:

```bash
python -m pytest -q
```

อีกครั้งใน Development Environment ของทีม

---

# 30. Contribution Matrix — Member Performance

ส่วนนี้ใช้สำหรับประเมินการทำงานของสมาชิกแต่ละคน
โดยพิจารณาจากงานที่รับผิดชอบและผลลัพธ์ที่ส่งมอบใน Sprint 2

**เกณฑ์คะแนน:** งานแต่ละส่วนเต็ม 10 คะแนน

* 10 = ทำครบตามหน้าที่และส่งมอบงานเรียบร้อย
* 8–9 = ทำได้เกือบครบ มีการแก้ไขหรือปรับปรุงเล็กน้อย
* 6–7 = ทำได้บางส่วน แต่ยังต้องมีการช่วยเหลือหรือแก้ไขเพิ่มเติม
* 1–5 = ทำงานไม่ครบตามหน้าที่
* 0 = ไม่ได้ดำเนินงานในส่วนดังกล่าว

> คะแนนด้านล่างเป็น Contribution Assessment ของ Sprint 2
> และสามารถปรับตามการประเมินจริงของสมาชิกในทีมได้

---

## 30.1 Planner — ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว)

| งานที่รับผิดชอบ     | รายละเอียด                                  |     คะแนน |
| ------------------- | ------------------------------------------- | --------: |
| Sprint Planning     | กำหนด Goal, Scope และ Sprint Direction      | **10/10** |
| System Architecture | วางโครงสร้าง Web, API, Service และ Database | **10/10** |
| Requirements        | กำหนด Features และ Definition of Done       | **10/10** |
| Task Allocation     | แบ่งงานและติดตามการดำเนินงาน                | **10/10** |
| Documentation       | จัดทำและปรับปรุง Sprint Documentation       | **10/10** |
| **Total**           |                                             | **50/50** |

### Planner Contribution

รับผิดชอบด้านการวางแผนและควบคุม Scope
รวมถึงตรวจสอบให้ Implementation สอดคล้องกับเป้าหมายของ Sprint 2

---

## 30.2 Coder — ออม (นายเดโชชิต โตวินัส)

| งานที่รับผิดชอบ           | รายละเอียด                                   |     คะแนน |
| ------------------------- | -------------------------------------------- | --------: |
| Streamlit Web Application | พัฒนา Web Application และ Dashboard          | **10/10** |
| RAWG API                  | พัฒนา API Client, Search และ Pagination      | **10/10** |
| Steam API                 | พัฒนา Live Player และ Steam Top Games        | **10/10** |
| SQLite & Service          | พัฒนา Database และ Application Service Layer | **10/10** |
| Integration & Bug Fixing  | เชื่อมระบบและแก้ไขปัญหาจากการพัฒนา           | **10/10** |
| **Total**                 |                                              | **50/50** |

### Coder Contribution

รับผิดชอบ Source Code หลักของ Sprint 2
ตั้งแต่ Web Application, External APIs, Data Processing,
Database ไปจนถึง Integration ของระบบ

---

## 30.3 Debugger / QA — คิม (นายชิษณุพงศ์ ซู)

| งานที่รับผิดชอบ     | รายละเอียด                        |     คะแนน |
| ------------------- | --------------------------------- | --------: |
| Test Case Design    | ออกแบบ Test Cases สำหรับ Sprint 2 | **10/10** |
| API Testing         | ทดสอบ RAWG และ Steam API          | **10/10** |
| Database Testing    | ตรวจสอบ SQLite Operations         | **10/10** |
| Integration Testing | ตรวจสอบการทำงานร่วมกันของระบบ     | **10/10** |
| Bug Verification    | ตรวจสอบ Error และผลหลังแก้ไข      | **10/10** |
| **Total**           |                                   | **50/50** |

### Debugger Contribution

รับผิดชอบการตรวจสอบระบบในระดับ API,
Database, Service และ Web Application
รวมถึง Edge Cases และ Error Handling

---

# 31. Contribution Summary

| สมาชิก | ชื่อเล่น | Role          | คะแนนที่ได้รับ | คะแนนเต็ม | Completion |
| --------- | --- | ------------- | -------------: | --------: | ---------: |
| นายภานุวัฒน์ ผองแก้ว | ฟลุ๊ค | Planner       |             50 |        50 |   **100%** |
| นายเดโชชิต โตวินัส | ออม | Coder         |             50 |        50 |   **100%** |
| นายชิษณุพงศ์ ซู | คิม | Debugger / QA |             50 |        50 |   **100%** |

### Team Contribution

```text
Planner       : 50/50
Coder         : 50/50
Debugger / QA : 50/50

Total Team Score = 150/150
Team Completion  = 100%
```

---

# 32. Definition of Done

Sprint 2 ถือว่าเสร็จเมื่อ:

### Web Application

* [x] Web Application สามารถเปิดผ่าน Browser ได้
* [x] Streamlit Dashboard ทำงานได้
* [x] Sidebar Navigation ทำงานได้
* [x] Home Page ทำงานได้
* [x] Game Library ทำงานได้
* [x] Search Page ทำงานได้
* [x] Genres Page ทำงานได้
* [x] Top Rated Page ทำงานได้
* [x] Live Players Page ทำงานได้
* [x] Game Detail Page ทำงานได้

### RAWG API

* [x] RAWG API Client
* [x] API Key Configuration
* [x] Game Fetch
* [x] Game Search
* [x] Pagination
* [x] HTTP Error Handling
* [x] Network Error Handling
* [x] Response Validation

### Steam API

* [x] Steam Store Search
* [x] Steam App ID Matching
* [x] Current Player Count
* [x] Steam Top Games
* [x] Steam App Details
* [x] Live Player Ranking
* [x] Steam Error Handling

### Database

* [x] SQLite Database
* [x] Games Table
* [x] Dashboard Metadata Table
* [x] Insert Game
* [x] Update Game
* [x] Read Game
* [x] Search Game
* [x] Steam Mapping
* [x] Current Player Storage
* [x] Live Player Snapshot
* [x] Refresh Metadata

### Data Processing

* [x] Normalize RAWG Data
* [x] Normalize Genres
* [x] Normalize Platforms
* [x] Missing Value Handling
* [x] Type Conversion

### Application Features

* [x] Search
* [x] Genre
* [x] Platform Filter
* [x] Rating Filter
* [x] Top Rated
* [x] Pagination
* [x] Game Detail
* [x] Live Players
* [x] Refresh Interval
* [x] Empty State
* [x] Error Handling

### Testing

* [x] RAWG API Tests
* [x] Steam API Tests
* [x] Database Tests
* [x] Game Service Tests
* [x] Data Processing Tests
* [x] Time Utility Tests
* [x] Dashboard Tests Implemented
* [ ] Full Test Suite Verified in Final Development Environment

### Documentation

* [x] Sprint 2 Report
* [x] Project Documentation
* [x] Change Log
* [x] Learning Log
* [x] Project Plan
* [x] README

### GitHub

* [x] Sprint 2 Branch
* [x] Sprint 2 Implementation
* [x] Merge to Main
* [x] Git History / Commits
* [x] Pull Request Workflow

---

# 33. Wow! — สิ่งที่ทำได้ดี

### 1. Web Application Architecture

จาก Sprint 1 ที่เป็น CLI
ทีมสามารถพัฒนาเป็น Web Application ด้วย Streamlit ได้

### 2. Separation of Responsibilities

ระบบแยกส่วนการทำงานเป็น:

```text
API
Database
Service
Data Processing
Components
Application
```

ทำให้แต่ละส่วนสามารถพัฒนาและทดสอบแยกกันได้

### 3. RAWG API Integration

ระบบสามารถดึงข้อมูลเกมจริงจาก RAWG
และสามารถ Search รวมถึง Pagination ได้

### 4. Steam Live Player Feature

ทีมเพิ่ม Steam API เข้ามาเพื่อแสดงข้อมูล
จำนวนผู้เล่นปัจจุบันและ Steam Top 100

ทำให้ Dashboard มีข้อมูลที่เปลี่ยนแปลงตามสถานการณ์จริง
มากกว่าการใช้ข้อมูล Static Dataset เพียงอย่างเดียว

### 5. SQLite Snapshot

ระบบเก็บข้อมูล API ลง SQLite
และใช้ Refresh Interval เพื่อช่วยลดการเรียก API ซ้ำ

### 6. Error Handling

มีการจัดการ Error จาก External API
และ Database ในระดับ Application

### 7. Automated Testing

Sprint 2 มี Automated Tests ครอบคลุมหลาย Layer
ทั้ง API, Database, Service และ Data Processing

---

# 34. Whoops! — ปัญหาและการแก้ไข

## Problem 1 — API Data มีโครงสร้าง Nested

ข้อมูล Genre และ Platform จาก RAWG
ไม่ได้อยู่ในรูปแบบ List ของ String โดยตรง

## Solution

สร้าง Data Processing Layer
เพื่อ Normalize ข้อมูลก่อนบันทึกลง Database

---

## Problem 2 — RAWG Pagination

RAWG มีข้อจำกัดเกี่ยวกับจำนวนข้อมูลต่อ Request

## Solution

สร้าง Logic สำหรับแบ่ง API Request
และประกอบข้อมูลกลับมาเป็น Page ที่ Dashboard ต้องการ

---

## Problem 3 — Steam App ID ไม่ตรงกับ RAWG Game ID

RAWG และ Steam ใช้ ID คนละระบบ

## Solution

สร้าง `steam_app_id`
และ `steam_lookup_status`
ใน Database เพื่อแยกข้อมูลของแต่ละระบบ

---

## Problem 4 — Steam API มีหลาย Request

การดึงข้อมูล Steam Top Games
จำเป็นต้องเรียกข้อมูลหลาย Endpoint

## Solution

ใช้ concurrent requests ผ่าน `ThreadPoolExecutor`
เพื่อลดเวลารอจากการเรียกข้อมูลแต่ละเกม

---

## Problem 5 — API ถูกเรียกซ้ำมากเกินไป

หากเรียก API ทุกครั้งที่ User เปิดหน้า
อาจทำให้เกิด Request ที่ไม่จำเป็น

## Solution

เพิ่ม Snapshot และ Refresh Interval
โดยค่าเริ่มต้นใช้:

```text
15 minutes
```

และเก็บข้อมูลล่าสุดไว้ใน SQLite

---

## Problem 6 — Dashboard แสดงข้อมูลจำนวนมาก

การแสดงเกมจำนวนมากในหน้าเดียว
ทำให้ Dashboard มีข้อมูลหนาแน่นและใช้งานยากขึ้น

## Solution

เพิ่ม Pagination

```text
50 Games / Page
```

---

# 35. Code Quality Review

จากการตรวจสอบ Source Code ของ Sprint 2
โครงสร้างโดยรวมอยู่ในระดับที่เหมาะสมสำหรับการส่ง Sprint 2

### จุดที่ดี

* มี Separation of Concerns
* API ไม่ถูกเขียนปนกับ UI
* Database Logic แยกออกจาก Service
* มี Data Processing Layer
* มี Error Classes
* มี Type Hints ในส่วนสำคัญ
* มี Docstrings
* ใช้ Environment Variable สำหรับ API Key
* มี Automated Tests
* ใช้ Mock ในการทดสอบ API
* มี SQLite Persistence
* มี Snapshot / Refresh Logic
* มี Pagination
* มี Empty / Error State
* มีการจัดการ API Failure

Architecture:

```text
Streamlit
    ↓
GameService
    ↓
┌───────────────┐
│ RAWG          │
│ Steam         │
│ Data Process  │
│ SQLite        │
└───────────────┘
```

ถือว่าเหมาะสมกับขนาดของ Project และสามารถนำไปต่อยอด Sprint 3 ได้

---

# 36. Code Review — สิ่งที่ควรปรับปรุง

แม้ Core ของ Sprint 2 จะทำได้ค่อนข้างครบ
แต่มีบางจุดที่ควรปรับก่อน Final Project

## 36.1 Full Test Suite ต้อง Verify อีกครั้ง

ใน Development Environment ที่ใช้ตรวจสอบ
Dashboard Test ต้องใช้ Streamlit

ดังนั้นควรติดตั้ง:

```bash
pip install -r requirements.txt
```

แล้วรัน:

```bash
python -m pytest -q
```

เพื่อยืนยันว่า Test Suite ทั้งหมดผ่านจริง

---

## 36.2 Steam Player Data ยังไม่ได้ผูกกับ RAWG Games ทุกเกม

ระบบมี Function สำหรับ:

```text
refresh_current_players()
```

และมีระบบ Steam App Mapping แล้ว

แต่ Flow ปัจจุบันของ `app.py`
เน้น Refresh:

```text
RAWG Catalog
+
Steam Top 100
```

ดังนั้นเกมใน RAWG Game Library ที่ไม่ได้อยู่ใน Steam Top 100
อาจยังไม่มี `current_players`

ทำให้หน้า Game Detail ของบางเกมแสดง:

```text
Steam players now
N/A
```

นี่ไม่ใช่ Bug ที่ทำให้ระบบ Sprint 2 ใช้งานไม่ได้
แต่ถ้าเป้าหมายของ Project คือ
"ค้นหาเกมใดก็ได้แล้วดูจำนวนผู้เล่นปัจจุบันของเกมนั้น"
ควรนำ `refresh_current_players()` มาเชื่อมกับ Flow ของ Search / Detail ใน Sprint ถัดไป

---

## 36.3 `lagacy/` ควรเปลี่ยนชื่อ

ปัจจุบันมี:

```text
src/lagacy/
```

ควรเปลี่ยนเป็น:

```text
src/legacy/
```

หรือย้ายไฟล์เก่าที่ไม่ใช้แล้วออกจาก Source Structure
เพื่อไม่ให้เกิดความสับสน

---

## 36.4 Dashboard มี Logic ค่อนข้างมาก

`dashboard.py` รับผิดชอบหลาย Page
และมีหลาย Rendering Functions

สำหรับ Sprint 2 ยังถือว่าใช้งานได้
แต่ถ้า Sprint 3 เพิ่ม:

* Statistics
* Charts
* Filter
* Sort
* Analytics

ไฟล์นี้อาจใหญ่ขึ้นมาก

ใน Sprint 3 อาจแยกเป็น:

```text
components/
├── home.py
├── game_library.py
├── search.py
├── genres.py
├── top_rated.py
├── live_players.py
└── game_detail.py
```

---

# 37. Sprint 2 Review

### Sprint Goal

เปลี่ยน Gaming Statistics Dashboard
จาก CLI Foundation ให้เป็น Web Application
และเชื่อมต่อ External API + SQLite

### Result

Sprint 2 สามารถทำตามเป้าหมายหลักได้:

```text
CLI
 ↓
Streamlit Web Application
 ↓
RAWG API
 ↓
Data Processing
 ↓
SQLite
 ↓
Dashboard
```

และมีการเพิ่ม:

```text
Steam API
 ↓
Current Players
 ↓
Steam Top 100
 ↓
Live Players Dashboard
```

ดังนั้น Sprint 2 ได้สร้าง Foundation
ที่สามารถนำไปพัฒนาต่อด้าน Data Analysis
และ Visualization ใน Sprint ถัดไปได้

---

# 38. Sprint 2 Final Status

```text
╔══════════════════════════════════════════╗
║        SPRINT 2 — COMPLETED              ║
╚══════════════════════════════════════════╝
```

### Web Application

* ✅ Streamlit Web Application
* ✅ Dashboard
* ✅ Navigation
* ✅ Game Library
* ✅ Search
* ✅ Genres
* ✅ Top Rated
* ✅ Game Detail
* ✅ Live Players

### API

* ✅ RAWG API
* ✅ RAWG Search
* ✅ RAWG Pagination
* ✅ Steam API
* ✅ Steam App ID Mapping
* ✅ Current Player Count
* ✅ Steam Top 100

### Database

* ✅ SQLite
* ✅ Games Table
* ✅ Dashboard Metadata
* ✅ Game Persistence
* ✅ Search
* ✅ Live Player Snapshot
* ✅ Refresh Timestamp

### Engineering

* ✅ Service Layer
* ✅ Data Processing
* ✅ Error Handling
* ✅ Pagination
* ✅ Snapshot / Cache Logic
* ✅ Environment Configuration

### Testing

* ✅ Automated Tests Implemented
* ✅ Core Tests Passed in Review Environment
* ⚠️ Full Test Suite ต้อง Verify อีกครั้งใน Environment ที่ติดตั้ง Streamlit ครบ

### Documentation

* ✅ Sprint 2 Report
* ✅ Project Documentation
* ✅ Change Log
* ✅ Learning Log

---

## Current Sprint Status

**Sprint 1: ✅ Completed**

**Sprint 2: ✅ Completed**

**Next Step: Sprint 3 — Data Processing, Statistics & Visualization**

```
```
