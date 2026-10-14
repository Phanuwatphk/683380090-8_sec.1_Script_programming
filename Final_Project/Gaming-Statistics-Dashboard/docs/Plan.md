# Gaming Statistics Dashboard — Project Plan

**CP352301 Script Programming · สถานะการตรวจส่งมอบ 13 October 2026**

เอกสารนี้สรุปแผนเดิมและสถานะโค้ดปัจจุบัน ไม่ใช้วันตรวจโค้ดแทนวันที่สมาชิกทำงานหรือวันที่ส่งงานจริง

## เป้าหมาย

ส่งมอบ Streamlit dashboard ที่ค้นหาและสำรวจข้อมูล RAWG/Steam ได้ มี SQLite cache, filters, pagination, game details, statistics, charts และ comparison พร้อม tests และเอกสารที่ตรงกับ source

## Timeline และบทบาทตามแผน

| Sprint | ช่วงตามแผน | Planner | Coder | Debugger | งาน |
|:--|:--|:--|:--|:--|:--|
| 1 | 10–15 Sep 2026 | คิม (นายชิษณุพงศ์ ซู) | ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว) | ออม (นายเดโชชิต โตวินัส) | CLI foundation |
| 2 | 20–24 Sep 2026 | ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว) | ออม (นายเดโชชิต โตวินัส) | คิม (นายชิษณุพงศ์ ซู) | Web UI, API, SQLite |
| 3 | 25–29 Sep 2026 | ออม (นายเดโชชิต โตวินัส) | คิม (นายชิษณุพงศ์ ซู) | ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว) | Analysis, charts, filters, comparison |
| Final | 2–6 Oct 2026 | คิม (นายชิษณุพงศ์ ซู) | ฟลุ๊ค (นายภานุวัฒน์ ผองแก้ว) | ออม (นายเดโชชิต โตวินัส) | Integration, regression, documentation, delivery |

มีการตรวจและปรับ source เพิ่มเติมวันที่ 13 October 2026 รายงาน Sprint 1–3 เป็นบันทึกประวัติ ไม่ใช่คู่มือติดตั้งของรุ่นปัจจุบัน

## สถานะงานส่งมอบ

| งาน | สถานะ/หลักฐาน |
|:--|:--|
| รวม Web UI, APIs, SQLite, analysis | มี implementation และ integration tests |
| RAWG 24 ชั่วโมง / Steam 15 นาที | แยก config และ metadata; มี cache boundary tests |
| ผู้พัฒนาโหลดเฉพาะ Details | มี request/cache/failure tests |
| Bulk import | รองรับ ranges, parallel fetching, writer เดียว และ 1 request/page |
| Missing/invalid data | Normalize และแสดง N/A; ทดสอบ malformed values |
| ประสิทธิภาพ | Home ใช้ SQL LIMIT; Statistics เตรียม DataFrame ครั้งเดียว |
| พาธ/imports | ใช้ตำแหน่งไฟล์; ทดสอบจาก working directory อื่น |
| Repository/CI | สคริปต์และ CLI เก่าไม่ถูก ignore; import scripts มี tests; secret/env/cache ไม่อยู่ใน Git |
| ผล regression และ clean checkout | ดู [Final QA](FINAL_QA.md) |
| Commit/push รอบสุดท้าย | เจ้าของโปรเจกต์ดำเนินการ |
| Presentation/submission | ไม่มีหลักฐานการนำเสนอหรือส่งงานในรอบตรวจนี้ |

## Definition of Done สำหรับโค้ด

- Source, dependencies, configuration และเอกสารใช้งานสอดคล้องกัน
- เปิดแอปและนำทางหน้าหลักได้โดยไม่มี exception
- Tests ผ่านจากไฟล์ที่จะส่งมอบ โดยไม่พึ่งไฟล์ที่ ignored ไว้ในเครื่อง
- Compile, dependency consistency, SQLite integrity และ whitespace checks ผ่าน
- API failures ไม่ทำให้ข้อมูลเดิมหรือ cache สำเร็จสูญหาย
- ไม่มี API key, .env หรือ Streamlit secrets ในไฟล์ส่งมอบ
- มีรายการข้อจำกัดและผลตรวจที่ทำซ้ำได้

## สิ่งที่ต้องทำโดยเจ้าของโปรเจกต์

ตรวจ diff และ stage source/scripts/tests/docs ที่ต้องการ commit จากนั้น commit/push และทดสอบ deployment ของ branch จริง การตรวจในเครื่องไม่ได้แทนผล CI บน GitHub หรือการยืนยัน deployment หลัง push

ดูคำสั่งรันและตั้งค่าที่ [README](../README.md) และรายละเอียดส่งมอบที่ [Final Sprint](<../Final Sprint/Final_Sprint.md>)
