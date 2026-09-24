"""
Đăng ký toàn bộ chỉ số của MacroPulse AI.

Đây là NƠI DUY NHẤT cần sửa khi thêm, xoá hay đổi một chỉ số.
Không cần sửa data/collector.py, app.py hay bất kỳ file dashboard/* nào.

Cách thêm 1 chỉ số mới:
    1. Thêm 1 dòng Indicator(...) vào danh sách INDICATORS bên dưới.
    2. Khai báo nó xuất hiện ở đâu qua `show_in`:
         - "market_pulse" -> ô chỉ số ở tab Dashboard
         - "macro_table"  -> bảng ở tab Macro
         - "history"      -> danh sách chọn biểu đồ ở tab Markets
    3. Nếu chỉ số cần FRED API key, set requires="fred_key".
    4. Nếu chưa có nguồn dữ liệu thật, để source="manual" — app sẽ tự
       hiển thị "chưa có nguồn dữ liệu" thay vì báo lỗi.

Không có chỗ nào khác trong code hard-code id chỉ số nữa; mọi tab đọc
danh sách từ registry này.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Indicator:
    id: str                     # khoá duy nhất, dùng xuyên suốt app
    name: str                   # tên hiển thị
    region: str                 # "Vietnam" | "US" | "China" | "Global"
    category: str                # "Market" | "FX" | "Rates" | "Inflation" | "Labor" | "Growth" | "Liquidity" | "Commodity"
    source: str                  # "yahoo" | "fred" | "vnstock" | "manual"
    symbol: str = ""             # mã ticker (yahoo) hoặc series id (fred)
    unit: str = ""               # "%" | "" (định dạng số)
    show_in: tuple = field(default_factory=tuple)
    requires: str = ""           # "" | "fred_key"


INDICATORS = [
    # --- Market / FX / Commodity -------------------------------------------------
    Indicator(id="VNINDEX", name="VN-Index", region="Vietnam", category="Market",
              source="vnstock", show_in=("market_pulse", "history")),
    Indicator(id="USDVND", name="USD/VND", region="Vietnam", category="FX",
              source="yahoo", symbol="VND=X", show_in=("market_pulse", "history")),
    Indicator(id="DXY", name="DXY", region="Global", category="FX",
              source="yahoo", symbol="DX-Y.NYB", show_in=("market_pulse", "history")),
    Indicator(id="GOLD", name="Gold", region="Global", category="Commodity",
              source="yahoo", symbol="GC=F", show_in=("market_pulse", "history")),
    Indicator(id="BRENT", name="Brent", region="Global", category="Commodity",
              source="yahoo", symbol="BZ=F", show_in=("market_pulse", "history")),
    Indicator(id="US10Y", name="US 10Y", region="US", category="Rates",
              source="yahoo", symbol="^TNX", show_in=("market_pulse", "history")),
    Indicator(id="US2Y", name="US 2Y (proxy)", region="US", category="Rates",
              source="yahoo", symbol="^IRX", show_in=("history",)),

    # --- FRED (cần FRED API key) --------------------------------------------------
    Indicator(id="FEDFUNDS", name="Fed Funds Effective", region="US", category="Rates",
              source="fred", symbol="DFF", unit="%",
              show_in=("market_pulse", "macro_table", "history"), requires="fred_key"),
    Indicator(id="US10Y_FRED", name="US Treasury 10Y", region="US", category="Rates",
              source="fred", symbol="DGS10", unit="%", show_in=("history",), requires="fred_key"),
    Indicator(id="US2Y_FRED", name="US Treasury 2Y", region="US", category="Rates",
              source="fred", symbol="DGS2", unit="%", show_in=("history",), requires="fred_key"),
    Indicator(id="USCPI", name="US CPI", region="US", category="Inflation",
              source="fred", symbol="CPIAUCSL", show_in=("market_pulse", "macro_table", "history"),
              requires="fred_key"),
    Indicator(id="CORECPI", name="US Core CPI", region="US", category="Inflation",
              source="fred", symbol="CPILFESL", show_in=("macro_table",), requires="fred_key"),
    Indicator(id="PCE", name="US PCE Price Index", region="US", category="Inflation",
              source="fred", symbol="PCEPI", show_in=("macro_table",), requires="fred_key"),
    Indicator(id="UNRATE", name="US Unemployment", region="US", category="Labor",
              source="fred", symbol="UNRATE", unit="%", show_in=("macro_table",), requires="fred_key"),
    Indicator(id="PAYEMS", name="US Nonfarm Payrolls", region="US", category="Labor",
              source="fred", symbol="PAYEMS", show_in=("macro_table",), requires="fred_key"),
    Indicator(id="USGDP", name="US Real GDP", region="US", category="Growth",
              source="fred", symbol="GDPC1", show_in=("macro_table",), requires="fred_key"),
    Indicator(id="USM2", name="US M2", region="US", category="Liquidity",
              source="fred", symbol="M2SL", show_in=("macro_table",), requires="fred_key"),

    # --- Chưa có nguồn dữ liệu (khai báo trước, chờ nối nguồn) --------------------
    Indicator(id="PMI", name="Vietnam PMI", region="Vietnam", category="Growth",
              source="manual", show_in=("macro_table",)),
    Indicator(id="CREDIT", name="Vietnam Credit Growth", region="Vietnam", category="Liquidity",
              source="manual", show_in=("macro_table",)),
]

_BY_ID = {i.id: i for i in INDICATORS}


def get(indicator_id):
    return _BY_ID.get(indicator_id)


def by_group(group):
    """Trả về danh sách Indicator xuất hiện trong 1 khu vực hiển thị (show_in)."""
    return [i for i in INDICATORS if group in i.show_in]


MARKET_PULSE = [i.id for i in by_group("market_pulse")]
MACRO_TABLE = [i.id for i in by_group("macro_table")]
HISTORY_OPTIONS = [i.id for i in by_group("history")]
