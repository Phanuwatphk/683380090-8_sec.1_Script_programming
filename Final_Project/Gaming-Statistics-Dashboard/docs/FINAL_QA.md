# Final QA — Gaming Statistics Dashboard

**วันที่ตรวจ:** 13 October 2026 (Asia/Bangkok)
**สถานะโค้ด:** ผ่านรายการตรวจด้านล่าง พร้อมให้เจ้าของโปรเจกต์ตรวจ diff และ commit

## Environment

ตรวจบน Linux, Python 3.12.3 ใน environment เดิมของโปรเจกต์:

| Dependency | รุ่นที่ใช้ตรวจ |
|:--|:--|
| Streamlit | 1.65.0 |
| requests | 2.34.2 |
| pandas | 2.3.3 |
| Altair | 6.3.0 |
| python-dotenv | 1.2.4 |
| pytest | 8.4.2 |

Runtime requirements กำหนด Streamlit >=1.52 เพราะ navigation ใช้ `st.html(..., unsafe_allow_javascript=True)` ที่มีตั้งแต่ [Streamlit 1.52](https://docs.streamlit.io/develop/quick-reference/release-notes/2025) ไม่ได้อ้างว่าทดสอบทุก version ที่อยู่ในช่วง dependencies

## ผลการตรวจ

| รายการ | ผล | หลักฐาน |
|:--|:--|:--|
| Dependency consistency | ผ่าน | `python -m pip check`: No broken requirements found; installed versions อยู่ในช่วง requirements |
| Compile source/tests | ผ่าน | `python -m compileall -q src tests` |
| Workspace test suite | ผ่าน | 128 passed in 27.25s |
| Clean delivery-copy test suite | ผ่าน | 128 passed in 26.85s |
| UI workflows บน snapshot จริง | ผ่าน | AppTest 9 workflows, 40,153 records, ไม่มี exception |
| Streamlit server startup | ผ่าน | เปิดจากสำเนาส่งมอบบน localhost และปิดหลังตรวจ |
| HTTP health endpoint | ผ่าน | `/_stcore/health` ตอบ `ok` |
| SQLite integrity | ผ่าน | `PRAGMA integrity_check` ตอบ `ok`; foreign_key_check ไม่มีรายการ |
| Database snapshot | ตรวจแล้ว | 40,153 records, 11,284,480 bytes ณ เวลาตรวจ |
| Paths/imports | ผ่าน | Tests จาก working directory อื่น; package imports และ direct script launch |
| TOML/JSON config | ผ่าน | Theme และ devcontainer parse ได้; required Streamlit API มีอยู่ |
| Local documentation links | ผ่าน | ไม่พบ link ที่ชี้ไฟล์ในโปรเจกต์แล้วหาไม่เจอ |
| Markdown code fences | ผ่าน | ไม่พบ fence ที่เปิดค้างในเอกสาร |
| Known local secret scan | ผ่าน | ไม่พบค่าคีย์/secret ที่อ่านจาก .env ในชุดไฟล์ส่งมอบ |
| Git exclusions | ผ่าน | .env, secrets.toml และ virtualenv ถูก ignore; src/script/ และ src/lagacy/ ไม่ถูก ignore ตามคำสั่งล่าสุด |
| Diff whitespace | ผ่าน | `git diff --check` และ `git diff --cached --check` |

เวลา tests เป็นผลของเครื่องและข้อมูลขณะตรวจ ไม่ใช่ performance guarantee

## วิธีตรวจ clean delivery copy

สร้างสำเนาจากไฟล์ที่ Git ติดตามร่วมกับไฟล์ใหม่ที่ไม่ถูก ignore ตาม working tree ปัจจุบัน แล้วรัน compile/pytest โดยไม่มี .env หรือ virtualenv ของ workspace ในสำเนา (สำเนารอบ QA เดิมไม่มี CLI เก่า; ต่อมาปรับให้ src/lagacy/ ไม่ถูก ignore ตามคำสั่งล่าสุด) SQLite ใช้ backup API เพื่อให้สำเนาสอดคล้องกัน

การตรวจนี้ใช้ Python environment เดิมจากภายนอกสำเนา จึงยืนยันความครบของ source/config/test files แต่ไม่ได้อ้างว่าได้สร้าง virtualenv ใหม่หรือทำ Git clone จาก final commit ที่ยังไม่มี

Test suite ส่งมอบมี 128 tests ต่างจากรอบก่อนที่มี 129 เพราะนำ test ของ CLI เก่าออกจาก suite ของเว็บแอป การทดสอบ feature ของแอปและ import scripts ยังอยู่ครบ

## UI workflows ที่ตรวจ

AppTest รันจาก working directory อื่นบนฐานข้อมูลสำเนาจริง:

- Home
- Game Library
- Genres
- Top Rated
- Live Players
- Statistics รวมกราฟและ standard deviation
- Search
- ค้นหา Portal 2 จากข้อมูลใน SQLite
- Details ของเกมที่มี developer cache

การตรวจ snapshot ปิด automatic API refresh เพื่อไม่เปลี่ยนข้อมูลระหว่างทดสอบ ส่วน API errors, missing developer fetch, retry, cache, pagination และ request counts ตรวจด้วย mock APIs ใน test suite

## พฤติกรรมที่ยืนยันด้วย tests

- RAWG Home ใช้ 3 requests เพื่อโหลด 100 เกม และไม่ดึงผู้พัฒนาเพิ่ม
- Snapshot ของ RAWG ยังใหม่ใน 24 ชั่วโมงไม่เรียกซ้ำ; Steam ใช้ 15 นาทีแยกกัน
- เปิด Details ที่ขาดผู้พัฒนาใช้ 1 request; cached result รวมผลว่างไม่ถูกเรียกซ้ำ
- คำขอผู้พัฒนาที่ล้มเหลวไม่ทำให้รายละเอียดเกมหาย และลองใหม่ได้
- Bulk import ทั้ง sequential/parallel ใช้ 1 HTTP request ต่อหน้า
- ช่วง import ต้องเป็นจำนวนเต็มบวก เรียงถูกต้อง และไม่ซ้อนกัน
- Parallel fetch ใช้ sessions แยกกัน และเขียน SQLite ผ่าน writer เดียว
- Rating=0 จาก RAWG แสดง N/A รวม snapshot เก่า
- Normalization รองรับ malformed entries, missing fields และ non-finite numbers
- Failed/empty next page ไม่ล้างการ์ดเดิม
- SQLite rollback ไม่ทิ้ง records จาก batch ที่ล้มเหลว และ connections ปิดหลังจบงาน
- Home จำกัด records ก่อน decode; selected player refresh ไม่อ่านทั้ง Library
- Prepared DataFrame ให้สถิติเหมือน input แบบ list และไม่ถูกแก้โดย analysis functions

## คำสั่งทำซ้ำ

รันจาก root ของโปรเจกต์หลังติดตั้ง `requirements-dev.txt`:

~~~bash
python -m pip check
python -m compileall -q src tests
python -m pytest -q
git diff --check
git diff --cached --check
~~~

ตรวจ SQLite ด้วย Python sqlite3 หรือ SQLite CLI โดยใช้ฐานข้อมูลที่ไม่มีการเขียนพร้อมกัน หรือทำ backup ก่อน

## ขอบเขตที่ไม่ได้อ้างว่าผ่านแล้ว

- GitHub Actions ของ final commit และ remote deployment ต้องตรวจหลังเจ้าของโปรเจกต์ commit/push
- Presentation/submission ไม่ได้ดำเนินการในรอบนี้
- ไม่ได้เรียก live RAWG/Steam ซ้ำในการตรวจรอบสุดท้าย; API tests ใช้ mocks เพื่อประหยัด requests
- AppTest ตรวจ backend/UI elements แต่ไม่ได้ยืนยัน browser rendering, viewport scrolling หรือ responsive layout ทุกขนาด เครื่องมือ browser ไม่พร้อมใช้งานในรอบตรวจ
- ไม่ได้ทดสอบบน Windows/macOS, ทุก dependency version หรือระดับโหลดผู้ใช้จำนวนมาก

ดูวิธีใช้งานที่ [README](../README.md) และรายละเอียดปรับปรุงที่ [Final Sprint](<../Final Sprint/Final_Sprint.md>)

## การตั้งค่า Git/CI ล่าสุด

`src/script/` และ `src/lagacy/` ไม่อยู่ใน .gitignore; tests ของ import script ทำงานตามปกติ ไม่ถูก skip. CI push รองรับ main, sprint-1, sprint-2, sprint-3 และ final-sprint; pull requests ยังคงตรวจเมื่อเข้า main.
