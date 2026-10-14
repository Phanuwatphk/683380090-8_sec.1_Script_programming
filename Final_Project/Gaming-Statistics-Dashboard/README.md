# Gaming Statistics Dashboard

**Final Term Project — CP352301 Script Programming**

เว็บแอป Streamlit สำหรับค้นหา สำรวจ และวิเคราะห์ข้อมูลเกมจาก RAWG พร้อมอันดับผู้เล่นปัจจุบันจาก Steam ข้อมูลที่โหลดสำเร็จเก็บใน SQLite เพื่อใช้เป็น cache และเป็นข้อมูลตั้งต้นหลังแอปเริ่มใหม่

## 🚀 เริ่มใช้งาน

ต้องใช้ Python 3.11 ขึ้นไป; CI ตรวจบน Python 3.12

Runtime ใช้ Streamlit 1.52 ขึ้นไปตาม API ที่ใช้สำหรับ navigation และ scroll reset โดยกำหนดไว้ใน requirements แล้ว

~~~bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
cp .env.example .env
~~~

แก้ `RAWG_API_KEY` ใน `.env` เป็น key ของคุณ แล้วรัน:

~~~bash
python -m streamlit run src/app.py
~~~

บน Windows ใช้ `.venv\Scripts\Activate.ps1` แทนคำสั่ง activate และคัดลอก `.env.example` เป็น `.env` ด้วยคำสั่งของระบบ

`requirements.txt` ใช้สำหรับรันแอป ส่วน `requirements-dev.txt` เพิ่ม pytest สำหรับพัฒนาและทดสอบ ห้ามนำ `.env` หรือ `.streamlit/secrets.toml` เข้า Git

## 🎮 หน้าและข้อมูลที่แสดง

| หน้า | การทำงาน |
|:--|:--|
| Home | แสดงเกมจาก RAWG เรียงตาม `-added` และยอดผู้เล่นรวมของรายการ Steam Top 100 ที่ดึงสำเร็จ |
| Game Library | เกมใน SQLite; กรอง Genre, Platform, Minimum Rating และ Release Year; เรียงชื่อ คะแนน หรือวันวางจำหน่าย |
| Search | ค้นใน SQLite ก่อน ถ้าไม่พบจึงค้น RAWG และบันทึกผล |
| Genres | จัดกลุ่มเกมตาม genre; กดชื่อ genre บนการ์ดเพื่อเปิดกลุ่มนั้นได้ |
| Top Rated | เรียงเกมที่บันทึกไว้ตามคะแนน RAWG |
| Live Players | อันดับ Steam พร้อมจำนวนผู้เล่นและเวลาอัปเดต snapshot |
| Details | รูป คะแนน วันวางจำหน่าย Metacritic, platforms, genres และผู้พัฒนา |
| Statistics | จำนวนเกม ค่าเฉลี่ย มัธยฐาน สูงสุด ต่ำสุด ส่วนเบี่ยงเบนมาตรฐาน กราฟ 6 ชุด และการเปรียบเทียบ 2 เกม |

ปุ่ม Back to Games ใน Details กลับไปหน้าที่เปิดเกมมา โดยคงหน้ารายการเดิมและตัวกรอง/การเรียงลำดับของ Game Library ไว้ใน session เดิม

การ์ดแบ่งหน้าละ 50 เกม Home และผล Search จาก API โหลดหน้าถัดไปเมื่อกดนำทาง ส่วน Library, Genres, Top Rated และ Live Players แบ่งหน้าข้อมูลที่บันทึกไว้

`-added` เรียงตามจำนวนผู้ใช้ RAWG ที่เพิ่มเกมเข้ารายการจากมากไปน้อย เป็นความนิยมสะสม ไม่ใช่อันดับกระแสรายสัปดาห์ และไม่ใช่จำนวนผู้เล่นออนไลน์

เกมจาก RAWG ใช้ `game_id` เป็นค่าบวก เกมจาก Steam Top ใช้ค่าติดลบของ Steam App ID เพื่อไม่ให้ชนกัน ชื่อเดียวกันจึงอาจมีทั้งรายการ RAWG และ Steam ใน Library ระบบไม่จับคู่สองแหล่งด้วย ID โดยตรง

## การโหลดข้อมูลและ cache

| ข้อมูล | ช่วงเวลาเริ่มต้น | การเรียก RAWG |
|:--|:--|:--|
| RAWG Home | 24 ชั่วโมง | 100 เกมใช้ 3 requests; snapshot ยังใหม่ใช้ 0 requests |
| Steam Top / Live Players | 15 นาที | ใช้ Steam API แยกจาก RAWG |
| ผู้พัฒนา | เมื่อเปิด Details ของเกมที่ยังไม่มี cache | เพิ่ม 1 request เฉพาะเกมนั้น |
| Bulk import | เมื่อรันสคริปต์ | 1 request ต่อหน้า สูงสุด 40 เกม ไม่มี request ผู้พัฒนาเพิ่ม |

ระบบตรวจอายุ snapshot เมื่อแอปรันซ้ำ ไม่ใช่ background scheduler ขณะไม่มีคนใช้ เมื่อข้อมูลเก่าจะอัปเดต API ก่อนแสดงหน้า หาก API ล้มเหลวจะใช้ข้อมูลเดิมพร้อมคำเตือน

Home, Library, Genres, Search และสคริปต์ไม่ดึงผู้พัฒนาเพิ่ม หน้า Details จะบันทึกทั้งผลที่มีชื่อและผลว่างที่ RAWG ตอบสำเร็จ เพื่อไม่เรียกซ้ำ หากคำขอล้มเหลวจะยังไม่ทำเครื่องหมายว่าสำเร็จ และลองใหม่เมื่อเปิด Details ครั้งถัดไป เกมที่มีเฉพาะ Steam ID จะไม่ส่ง ID ติดลบไปหา RAWG

คะแนน RAWG ที่เป็น 0 หมายถึงยังไม่มีคะแนนเฉลี่ยที่เผยแพร่ ระบบใช้ `N/A` และไม่นำมาคำนวณคะแนนเฉลี่ย Steam players ที่ไม่มีข้อมูลก็แสดง `N/A` เช่นกัน วันวางจำหน่ายเก็บตามแหล่งข้อมูล จึงอาจมีปีในอนาคต

## ตั้งค่า

| ตัวแปร | ค่าเริ่มต้น | ความหมาย |
|:--|:--|:--|
| `RAWG_API_KEY` | ไม่มี | Key สำหรับ RAWG |
| `GAMING_DASHBOARD_DB` | `data/gaming_statistics.db` | ตำแหน่ง SQLite |
| `PLAYER_REFRESH_MINUTES` | `15` | อายุ snapshot ของ Steam |
| `CATALOG_REFRESH_HOURS` | `24` | อายุ snapshot ของ RAWG Home |
| `GAMING_DASHBOARD_SKIP_REFRESH` | ไม่ตั้ง | ตั้งเป็น `1` เพื่อข้ามการรีเฟรช snapshot ในการทดสอบ; Details ที่ขาดผู้พัฒนายังสามารถเรียก API ได้ |

พาธฐานข้อมูลแบบ relative อ้างอิงโฟลเดอร์โปรเจกต์ ไม่อ้างอิงตำแหน่ง terminal ค่า interval เป็นจำนวนเต็ม; ค่าไม่ถูกต้องใช้ค่าเริ่มต้น ค่าติดลบใช้ 0 และค่า 0 หมายถึงตรวจแล้วรีเฟรชทุก rerun

## เพิ่มเกมลงฐานข้อมูล

สคริปต์ใน `src/script/` รวมใน source ของโปรเจกต์และมี tests ตรวจทั้งแบบ sequential และ parallel

แก้ช่วงใน `src/script/import_games.py`:

~~~python
PAGE_RANGES = [
    [101, 250],
    [251, 500],
    [501, 750],
    [751, 1000],
]
~~~

รวมหน้าเริ่มต้นและสิ้นสุดในแต่ละช่วง ไม่อนุญาตให้ช่วงซ้อนกัน จำนวน workers เท่ากับจำนวนช่วง ตัวอย่างปัจจุบันดึงหน้า 101–1000 ด้วย 4 workers:

~~~bash
python -m src.script.import_games
~~~

workers ดึงรายชื่อเกมพร้อมกันโดยใช้ HTTP session แยกกัน ข้อมูลผ่านคิวที่จำกัดขนาดและบันทึก SQLite ผ่าน writer เดียว หาก ID เดิมมีอยู่จะอัปเดตแทนเพิ่มซ้ำ และเก็บผู้พัฒนา/Steam snapshot ที่มีอยู่เดิม

ทดสอบช่วงเล็กหรือเลือกฐานข้อมูลอื่น:

~~~bash
python -m src.script.import_games --start-page 1 --pages 1 --database /tmp/gaming-test.db
~~~

อาร์กิวเมนต์ `--start-page`/`--pages` ใช้ช่วงเดียวแบบ sequential แทน `PAGE_RANGES` ถ้าระบุแค่หน้าเริ่มต้นจะดึง 5 หน้า ถ้าระบุแค่จำนวนหน้าจะเริ่มหน้า 1 เมื่อคำขอล้มเหลว สคริปต์หยุดพร้อม exit code 1 แต่หน้าที่บันทึกสำเร็จแล้วจะยังอยู่

รันไฟล์โดยตรงจากโฟลเดอร์อื่นได้ด้วยพาธเต็ม ดูตัวเลือกทั้งหมดด้วย `--help` จำนวน API requests เพิ่มตามจำนวนหน้า การเพิ่ม threads ไม่ได้ลดโควตาคำขอ

## 🧪 ทดสอบและตรวจคุณภาพ

~~~bash
python -m pip check
python -m compileall -q src tests
python -m pytest -q
git diff --check
~~~

Tests ใช้ temporary databases และ mock APIs ไม่ต้องใช้ key จริงหรืออินเทอร์เน็ต ครอบคลุม API errors, normalization, migrations, transactions, pagination, cache, request counts, config, imports และ Streamlit AppTest

ผลการตรวจส่งมอบอยู่ใน [Final QA](docs/FINAL_QA.md) และ [Final Sprint report](<Final Sprint/Final_Sprint.md>) CI ใช้คำสั่ง compile/pytest เดียวกันเมื่อ push ไป `main`, `sprint-1`, `sprint-2`, `sprint-3` หรือ `final-sprint` และเมื่อเปิด PR ไป `main`

## ☁️ Deploy บน Streamlit Community Cloud

เลือก repository/branch ที่ต้องการและ entry point `src/app.py` ระบบติดตั้ง runtime dependencies จาก `requirements.txt` ตั้ง `RAWG_API_KEY` เป็น environment variable ของ process; หากใช้ Streamlit Secrets ให้ใช้ส่วน root TOML แทน section แบบซ้อน ตัวแปร interval และ database override ตั้งได้แบบเดียวกัน

ตัวอย่างใน Settings → Secrets:

~~~toml
RAWG_API_KEY = "your-key"
PLAYER_REFRESH_MINUTES = 15
CATALOG_REFRESH_HOURS = 24
~~~

ดู [Streamlit Secrets management](https://docs.streamlit.io/develop/concepts/connections/secrets-management) และ [Community Cloud file organization](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization)

`data/gaming_statistics.db` เป็น snapshot ตั้งต้นที่ติดตามใน Git การแก้ข้อมูลบน instance ไม่ถูกส่งกลับ GitHub อัตโนมัติ เมื่อ environment ถูกสร้างใหม่ ข้อมูลที่เพิ่มหลัง snapshot อาจต้องโหลดใหม่ หากต้องการเก็บข้อมูลใหม่ถาวรต้องใช้ storage ภายนอกหรืออัปเดต snapshot แยกจากการรันแอป

## 📁 โครงสร้าง

~~~text
src/
  app.py                   Streamlit entry point และ refresh workflow
  config.py                พาธและช่วงรีเฟรช
  api/                     RAWG และ Steam HTTP clients
  database/                SQLite queries, migrations และ transactions
  services/                นำเข้าเกม, snapshots และ developer cache
  utils/                   Normalization และเวลา Asia/Bangkok
  analysis/                Pandas statistics
  components/              UI, styles และกราฟ
  script/import_games.py   Bulk import แบบ sequential/parallel
data/gaming_statistics.db   Snapshot ตั้งต้น
tests/                     Unit/integration/AppTest
docs/                      เอกสารปัจจุบันและบันทึกการพัฒนา
~~~

CLI ของ Sprint 1 อยู่ใน `src/lagacy/` เพื่อเก็บประวัติการพัฒนา ไม่ใช่ entry point ของเว็บแอป ส่วนสคริปต์ import ใน `src/script/` เป็นเครื่องมือที่ดูแลอยู่ ทั้งสองโฟลเดอร์ไม่ถูก ignore

## 👥 ทีมและ Sprint

| สมาชิก | ชื่อเล่น | Sprint 1 | Sprint 2 | Sprint 3 | Final Sprint |
|:--|:--|:--|:--|:--|:--|
| นายชิษณุพงศ์ ซู | คิม | Planner | Debugger | Coder | Planner |
| นายภานุวัฒน์ ผองแก้ว | ฟลุ๊ค | Coder | Planner | Debugger | Coder |
| นายเดโชชิต โตวินัส | ออม | Debugger | Coder | Planner | Debugger |

| Sprint | ช่วงตามแผน | งานหลัก |
|:--|:--|:--|
| [Sprint 1](Sprint1/Sprint_1.md) | 10–15 Sep 2026 | CLI foundation |
| [Sprint 2](Sprint2/Sprint_2.md) | 20–24 Sep 2026 | Streamlit, API และ SQLite |
| [Sprint 3](Sprint3/Sprint_3.md) | 25–29 Sep 2026 | Analysis, visualization, filters และ comparison |
| [Final Sprint](<Final Sprint/Final_Sprint.md>) | 2–6 Oct 2026; final review 13 Oct | Integration, fixes, performance และ QA |

โค้ดและเอกสารเตรียมสำหรับ final commit; การ commit/push และส่งงานเป็นขั้นตอนของเจ้าของโปรเจกต์ รายงาน Sprint 1–3 เก็บรายละเอียดตามช่วงที่พัฒนา ให้ใช้ README นี้สำหรับพฤติกรรมรุ่นปัจจุบัน

## 📚 เอกสารและแหล่งข้อมูล

- [Project pitch](docs/Project_Pitch.md)
- [Project plan](docs/Plan.md)
- [Changelog](docs/CHANGELOG.md)
- [Learning log](docs/LEARNINGLOG.md)
- [Final QA](docs/FINAL_QA.md)
- Game data/images: [RAWG](https://rawg.io), [API documentation and terms](https://rawg.io/apidocs)
- Live player data: [Steam](https://store.steampowered.com/charts/mostplayed)

## ⚠️ ขอบเขตและข้อจำกัด

Statistics วิเคราะห์เฉพาะเกมใน SQLite ไม่ใช่ทั้งฐาน RAWG Genre/platform เป็นหลายค่าต่อเกม สัดส่วนจึงหารด้วยจำนวน assignments ไม่ใช่จำนวนเกม Steam Top อาจไม่ครบ 100 เกมหากบางรายการไม่มีข้อมูล คะแนนจาก RAWG และ Metacritic เป็นคนละแหล่ง

Home อ่านเพียงหน้าที่แสดง แต่ Library, Genres และ Statistics ยังใช้ชุดข้อมูลที่บันทึกไว้ทั้งหมด ขนาดใหญ่ขึ้นอาจเพิ่มเวลาและ RAM API มีโควตา/ข้อจำกัดของผู้ให้บริการ และข้อมูลวันวางจำหน่ายหรือคะแนนอาจเปลี่ยนภายหลัง
