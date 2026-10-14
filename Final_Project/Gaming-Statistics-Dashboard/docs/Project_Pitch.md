# Gaming Statistics Dashboard — Project Pitch

**CP352301 Script Programming · ปรับให้ตรงกับรุ่นส่งมอบวันที่ 13 October 2026**

## ปัญหาและเป้าหมาย

ข้อมูลเกมและจำนวนผู้เล่นกระจายอยู่หลายแหล่ง ผู้ใช้ต้องการค้นหา สำรวจ และเปรียบเทียบเกมในหน้าจอเดียว โปรเจกต์นี้รวม RAWG metadata กับ Steam player snapshots ในเว็บแอป Python/Streamlit พร้อม SQLite cache และการวิเคราะห์ด้วย Pandas

กลุ่มเป้าหมายคือผู้เล่นเกมและผู้เรียนที่ต้องการสำรวจ rating, genres, platforms, release years และจำนวนผู้เล่น การวิเคราะห์อ้างอิงชุดข้อมูลที่บันทึกไว้ ไม่ใช่การสำรวจเกมทุกเกมทั่วโลก

## ความสามารถที่ส่งมอบ

| ส่วน | สิ่งที่ผู้ใช้ทำได้ |
|:--|:--|
| Home | ดูเกมยอดนิยมสะสมจาก RAWG และยอดผู้เล่นรวมของ Steam Top ที่ดึงสำเร็จ |
| Library/Search | ค้นหา กรองหลายเงื่อนไข เรียงลำดับ และแบ่งหน้า |
| Genres/Top Rated | สำรวจตามประเภทหรือคะแนน |
| Details | ดูข้อมูลเกมและโหลดผู้พัฒนาเมื่อยังไม่มี cache |
| Live Players | ดูอันดับ Steam พร้อมเวลา snapshot |
| Statistics | ดู summary metrics, กราฟ 6 ชุด และเปรียบเทียบ 2 เกม |
| Bulk import | เพิ่มข้อมูลทีละหน้าแบบ parallel โดยไม่เรียกผู้พัฒนาเพิ่ม |

กราฟประกอบด้วย Genre Distribution, Platform Distribution, Rating by Genre, Release Year Distribution, Metacritic Distribution และ Top Live Steam Players Summary metrics มี count, mean, median, min, max และ standard deviation

## ข้อมูลและการทำงาน

RAWG list API ใช้เกมหน้าละ 40 รายการ Home รีเฟรช 100 เกมด้วย 3 requests ทุก 24 ชั่วโมงตามอายุ cache ใช้ `-added` เป็นความนิยมสะสม ไม่ได้อ้างว่าเป็นอันดับกระแสล่าสุด

Steam snapshot ตรวจทุก 15 นาทีเมื่อแอปรันซ้ำ ผู้พัฒนาจาก RAWG ถูกดึงด้วย 1 request เมื่อเปิด Details ของเกมที่ยังไม่เคยโหลดสำเร็จ ทั้งผลที่มีชื่อและผลว่างที่สำเร็จจะถูก cache

Search อ่าน SQLite ก่อน หากไม่พบจึงขอ RAWG แล้ว normalize/store ข้อมูล เมื่อ API ไม่พร้อม ระบบแสดงข้อมูลที่มีอยู่หรือข้อความที่เหมาะสม ค่า rating ที่ยังไม่มีคะแนนเฉลี่ยแสดง N/A และไม่ถูกนำมาคิดค่าเฉลี่ย

## สถาปัตยกรรม

~~~text
Streamlit components
        ↓
GameService
   ↙          ↘
API clients   SQLite repository
        ↓
Normalization / cached records
        ↓
Pandas analysis → charts and comparison
~~~

พาธและ refresh settings อยู่ใน `src/config.py` UI ไม่เขียน SQL และ analysis ไม่เรียก API Runtime dependencies แยกจาก test dependencies เพื่อให้การ deploy และ CI ใช้งานชัดเจน

## การตรวจสอบและการพัฒนา

พัฒนาเป็น Sprint 1: CLI, Sprint 2: Web/API/SQLite, Sprint 3: Analysis/Visualization และ Final Sprint: Integration/QA รายงานประวัติยังเก็บไว้แยกจากเอกสารการใช้งานปัจจุบัน

Tests ใช้ mock APIs และ temporary SQLite รวม Streamlit AppTest ดูผลตรวจจริงที่ [Final QA](FINAL_QA.md) วิธีติดตั้ง รัน และตั้งค่าอยู่ใน [README](../README.md) แผนส่งมอบอยู่ใน [Plan](Plan.md)

## ขอบเขต

ระบบไม่มีบัญชีผู้ใช้ ระบบซื้อเกม หรือฐานข้อมูล cloud ถาวร ข้อมูล Steam/RAWG เก็บแยก ID เพื่อไม่จับคู่ผิด สถิติแสดงเฉพาะข้อมูลใน instance และ snapshot ไม่ถูกอัปโหลดกลับ GitHub อัตโนมัติ

การวางจำหน่าย การให้คะแนน และอันดับจากผู้ให้บริการอาจเปลี่ยนได้ ตัวเลขผู้เล่นใช้เวลา snapshot ประกอบเสมอ RAWG metadata/images มี [เงื่อนไขการใช้งาน](https://rawg.io/apidocs) และแสดง attribution ใน sidebar
