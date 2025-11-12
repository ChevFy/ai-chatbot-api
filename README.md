## คุณสมบัติหลัก
- เปิด HTTP API ด้วย FastAPI
- Endpoint สำหรับทดสอบ (`/test`) และ endpoint สำหรับส่งข้อความไปให้ chatbot (`/chat`)
- เก็บประวัติการสนทนาแบบเรียบง่ายในหน่วยความจำ (sessions per client IP)

## ข้อกำหนด (Prerequisites)
- Python 
- คีย์ API ของ Cohere (หรือผู้ให้บริการที่ใช้) ต้องมีและตั้งเป็นตัวแปรแวดล้อม `COHERE_API_KEY`

ไฟล์สำคัญในโปรเจค:
- `main.py` — แอป FastAPI และ endpoint `POST /chat` ที่เรียก `co.chat(...)`
- `run.py` — ตัวรัน (uvicorn) สำหรับ development
- `start.sh` — สคริปต์สร้าง virtualenv และรันโปรเจค (สะดวกสำหรับการพัฒนา)
- `requirements.txt` — ไลบรารีที่ต้องติดตั้ง

## ตัวอย่างการตั้งค่า
1. สร้างไฟล์ `.env` ไว้ที่โฟลเดอร์โปรเจค แล้วใส่:

```
COHERE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

2. ใช้ `start.sh` เพื่อสร้าง virtualenv ติดตั้ง dependency และรันเซิร์ฟเวอร์:

```bash
chmod +x start.sh
./start.sh
```

หรือ รันด้วยคำสั่ง Python โดยตรง (ภายใน virtualenv):

```bash
source .venv/bin/activate
python3 run.py
```

เมื่อรันแล้ว เซิร์ฟเวอร์จะฟังที่ `http://0.0.0.0:8000` (ค่าเริ่มต้นจาก `run.py`)

## API Endpoints

- GET /test
	- คำอธิบาย: เพื่อตรวจสอบว่า API ทำงานหรือไม่
	- ตัวอย่างผลลัพธ์: `{ "message": "Test API" }`

- POST /chat
	- คำอธิบาย: ส่งข้อความให้ chatbot แล้วรับการตอบกลับ
	- รูปแบบของ JSON body (ใช้ Pydantic model `chatRequest`):

```json
{
	"message": "สวัสดี",
	"history": []
}
```

	- คำตอบ: JSON containing `reply` เช่น `{ "reply": "สวัสดี! ผมช่วยอะไรได้บ้าง" }`
	- หมายเหตุ: โปรเจคนี้เก็บ history ในตัวแปร `sessions` แบบ in-memory โดยใช้ client IP เป็น key — ไม่เหมาะสำหรับการใช้งาน production หรือ multi-instance

ตัวอย่าง curl:

```bash
curl -X POST http://localhost:8000/chat \
	-H "Content-Type: application/json" \
	-d '{"message":"สวัสดี","history":[]}'
```

## ข้อควรระวัง / ข้อจำกัด
- โปรเจคนี้เป็นตัวอย่างสำหรับเรียกใช้ Chatbot API เท่านั้น ไม่ได้ออกแบบมาสำหรับงาน production
- ไม่มีระบบ Authentication/Authorization
- เก็บ session ในหน่วยความจำ (จะหายเมื่อโปรเซสหยุด)
- หากต้องการใช้งาน production ควรเพิ่ม: auth, persistent session store (เช่น Redis/DB), rate-limiting, logging ที่เหมาะสม และการจัดการข้อผิดพลาด/timeout

## Dependencies
ดู `requirements.txt` สำหรับไลบรารีที่จำเป็น (เช่น fastapi, uvicorn, pydantic, cohere)

## สรุป
โปรเจคนี้มีจุดประสงค์เพื่อเป็นตัวอย่างการเชื่อมต่อและใช้งาน Chatbot API เท่านั้น — ใช้เป็น reference ในการพัฒนา หรือนำไปปรับแต่งต่อเพื่อตอบโจทย์การใช้งานจริง

---

