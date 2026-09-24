# MacroPulse AI 2.0 — Ready-to-run

Đây là phiên bản đã nối pipeline dữ liệu + 3 AI.

## 1. Cài đặt

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. API keys

Tạo:

`.streamlit/secrets.toml`

Ví dụ:

```toml
OPENAI_API_KEY = "..."
ANTHROPIC_API_KEY = "..."
GEMINI_API_KEY = "..."
FRED_API_KEY = "..."
```

Không commit file này lên Git.

FRED API cần API key cho web-service requests. Xem tài liệu FRED:
https://fred.stlouisfed.org/docs/api/fred/

## 3. Chạy

```powershell
streamlit run app.py
```

Mở địa chỉ Streamlit hiển thị, thường là:

`http://localhost:8501`

## 4. Dữ liệu hiện được kết nối

### Thị trường
- VN-Index — VNStock
- USD/VND — Yahoo Finance
- DXY
- Gold
- Brent
- US Treasury proxy
- Fed Funds / macro Mỹ — FRED

### FRED
Có adapter cho:
- DFF
- DGS10
- DGS2
- CPIAUCSL
- CPILFESL
- PCEPI
- UNRATE
- PAYEMS
- GDPC1
- M2SL

FRED API hỗ trợ lấy observations theo series và lịch sử; API key là bắt buộc cho web service. 

## 5. Ba AI

MacroPulse gửi cùng một snapshot dữ liệu cho:
- GPT
- Claude
- Gemini

Mỗi AI trả:
- direction
- confidence
- summary
- risks
- drivers

Sau đó Consensus Engine tính mức đồng thuận.

### Gemini

Code dùng REST endpoint `generateContent` và JSON response mode. Đây phù hợp với API hiện hành của Google GenAI. Nếu đổi model Gemini, chỉ cần đổi `GEMINI_MODEL`. 

## 6. Quan trọng

Đây chưa phải hệ thống dự báo định lượng hoàn chỉnh. Nó đã là một dashboard phân tích có dữ liệu thật và AI thật, nhưng lớp scoring hiện tại là baseline.

Để trở thành MacroPulse bản production, bước tiếp theo nên bổ sung:
1. SBV: M2, tín dụng, OMO, tín phiếu, lãi suất liên ngân hàng.
2. GSO: CPI, GDP, IIP, retail sales, trade, FDI.
3. PMI Việt Nam.
4. Database lịch sử SQLite/PostgreSQL.
5. Economic calendar.
6. News/event engine.
7. AI debate vòng 2.
8. Backtesting: so sánh dự báo 7 ngày với kết quả thực tế.
9. Email report tự động.
10. Deployment cloud.
