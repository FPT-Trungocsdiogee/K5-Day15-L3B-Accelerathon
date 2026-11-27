"""Công cụ của bài toán — khớp bảng công cụ ở spec.md §4.

Ba công cụ, đều KHÔNG tác động ra ngoài (chỉ đọc file trong data/, hoặc dựng bản nháp HTML):
    parse_timetable          ngày học mẫu → danh sách buổi (mỗi dòng = một buổi × một phòng)
    lookup_merged_room       một buổi → các đoạn thông tin gộp phòng H209/H210 liên quan {code, text}
    render_marked_timetable  ngày + danh sách quyết định → trang TKB HTML bản nháp "chờ duyệt"

Nguồn dữ liệu (đổi bằng biến môi trường, không cần sửa code):
    TIMETABLE_FILE     mặc định data/ai20k_schedule.json — TKB đã công bố. spec.md ghi "TKB HTML" nhưng file
                       HTML gốc không có trong data/ (xem data/DATA_CARD.md), nên đọc bản JSON cùng nội dung.
    MERGED_ROOMS_FILE  mặc định data/merged_rooms.json — thông tin gộp lớp về H209/H210 (nhóm tự điền từ
                       thông báo thật). Chưa có file → lookup trả rỗng → mọi buổi phòng lẻ thành "chưa chắc".
                       data/merged_rooms.sample.json là dữ liệu GIẢ (synthetic) chỉ để tự kiểm / demo.

Tự kiểm: python codebase/tools.py
"""
import html
import json
import os
import re

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_YEAR = 2026
MERGED_ROOMS = ("H209", "H210")


def _path(env_key, default_rel):
    p = os.environ.get(env_key) or default_rel
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def normalize_date(text: str) -> str:
    """'13/11', '13/11/2026', '2026-11-13' → '2026-11-13'. Không nhận ra → ''. (hàm phụ, không phải công cụ)"""
    text = (text or "").strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", text)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        m = re.fullmatch(r"(\d{1,2})/(\d{1,2})(?:/(\d{4}))?", text)
        if not m:
            return ""
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3) or DEFAULT_YEAR)
    if not (1 <= mo <= 12 and 1 <= d <= 31):
        return ""
    return "%04d-%02d-%02d" % (y, mo, d)


_timetable_cache = {}


def _load_timetable():
    path = _path("TIMETABLE_FILE", os.path.join("data", "ai20k_schedule.json"))
    if path not in _timetable_cache:
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)
        _timetable_cache[path] = {"meta": data.get("meta", {}), "groups": data.get("groups", {})}
    return _timetable_cache[path]


@tool
def parse_timetable(ngay: str) -> list:
    """parse_timetable — đọc TKB đã công bố của MỘT ngày học.
    Input: ngày (str, '13/11' | '13/11/2026' | '2026-11-13').
    Output: danh sách buổi, mỗi dòng = một buổi × một phòng ghi trên TKB:
        {ma_buoi, ma_buoi_goc, ngay, gio, lop, mon, loai, phong_tkb, du_phong}
        loai: LEC (lý thuyết) · ONL (lý thuyết online) · LAB (thực hành) · KG (khai giảng) · HACK
        phong_tkb: mã phòng, '' nếu không có phòng (online / khai giảng), '?' nếu BTC chưa xếp.
        Ngày nghỉ / ngoài giai đoạn / ngày không hợp lệ → [].
    Tác động ra ngoài: Không — chỉ đọc file trong data/."""
    day = normalize_date(ngay)
    if not day:
        return []
    rows = []
    for lop, group in _load_timetable()["groups"].items():
        for s in group.get("sessions", []):
            if s.get("date") != day:
                continue
            base = {
                "ma_buoi_goc": s["session_id"], "ngay": day,
                "gio": "%s-%s" % (s.get("start", ""), s.get("end", "")),
                "lop": lop, "mon": s.get("name", ""), "loai": s.get("kind", ""),
            }
            rooms = s.get("rooms") or []
            if not rooms:
                rows.append(dict(base, ma_buoi=s["session_id"], phong_tkb="", du_phong=False))
            for r in rooms:
                code = r.get("code") or "?"
                rows.append(dict(base, ma_buoi="%s/%s" % (s["session_id"], code),
                                 phong_tkb=code, du_phong=bool(r.get("backup"))))
    return rows


@tool
def lookup_merged_room(buoi: dict) -> list:
    """lookup_merged_room — tra thông tin gộp lớp về H209/H210 cho một buổi.
    Input: một buổi (dict từ parse_timetable; dùng ngay, lop, ma_buoi_goc, phong_tkb).
    Output: danh sách đoạn căn cứ {code, text} liên quan; [] nếu không có (hoặc chưa có file thông tin gộp).
        Một đoạn liên quan khi: cùng ngày · lớp khớp (hoặc đoạn áp cho mọi lớp) · mã buổi khớp (nếu đoạn ghi)
        · phòng của buổi nằm trong 'tu_phong' của đoạn (hoặc đoạn không giới hạn phòng).
    Tác động ra ngoài: Không — chỉ đọc file trong data/."""
    path = _path("MERGED_ROOMS_FILE", os.path.join("data", "merged_rooms.json"))
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig") as f:
        notices = json.load(f).get("notices", [])
    found = []
    for n in notices:
        days = n.get("ngay") if isinstance(n.get("ngay"), list) else [n.get("ngay")]
        if buoi.get("ngay") not in [normalize_date(d or "") for d in days]:
            continue
        if n.get("lop") and buoi.get("lop") not in n["lop"]:
            continue
        if n.get("ma_buoi") and n["ma_buoi"] != buoi.get("ma_buoi_goc"):
            continue
        if n.get("tu_phong") and buoi.get("phong_tkb") not in n["tu_phong"]:
            continue
        found.append({"code": n["code"], "text": n["text"]})
    return found


_STATUS = {
    "doi_phong": ("ĐỔI PHÒNG", "#fff1c2", "#8a6100"),
    "giu_nguyen": ("Giữ nguyên", "#e6f4ea", "#1e6b34"),
    "chua_chac": ("CHƯA CHẮC — cần người kiểm", "#fde2e1", "#a11b14"),
}


@tool
def render_marked_timetable(ngay: str, quyet_dinh: list) -> str:
    """render_marked_timetable — dựng trang TKB bản nháp đã đánh dấu, chờ người vận hành duyệt.
    Input: ngày (str) + danh sách quyết định, mỗi phần tử là một buổi (dict từ parse_timetable) kèm
        {trang_thai: doi_phong|giu_nguyen|chua_chac, phong_moi: 'H209'|'H210'|'', can_cu: [mã đoạn], ly_do: str}.
    Output: chuỗi HTML (trang đầy đủ) — 3 màu cho 3 trạng thái, cột căn cứ, nhãn "BẢN NHÁP — CHỜ DUYỆT".
    Tác động ra ngoài: Không — chỉ trả chuỗi HTML; không ghi đè TKB gốc, không gửi cho ai."""
    e = html.escape
    counts = {k: sum(1 for q in quyet_dinh if q.get("trang_thai") == k) for k in _STATUS}
    body = []
    for q in sorted(quyet_dinh, key=lambda q: (q.get("gio", ""), q.get("lop", ""), q.get("ma_buoi", ""))):
        label, bg, fg = _STATUS.get(q.get("trang_thai"), _STATUS["chua_chac"])
        room = e(q.get("phong_tkb") or "—") + (" (dự phòng)" if q.get("du_phong") else "")
        new = e(q.get("phong_moi") or "")
        body.append(
            "<tr style='background:%s'><td>%s</td><td>%s</td><td>%s</td><td>%s · %s</td><td>%s</td>"
            "<td style='color:%s;font-weight:600'>%s%s</td><td>%s</td><td>%s</td></tr>" % (
                bg, e(q.get("ma_buoi", "")), e(q.get("gio", "")), e(q.get("lop", "")),
                e(q.get("mon", "")), e(q.get("loai", "")), room, fg, e(label),
                (" → " + new) if new else "", e(", ".join(q.get("can_cu") or [])), e(q.get("ly_do", ""))))
    return """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BẢN NHÁP — TKB %(day)s đánh dấu đổi phòng</title>
<style>body{font-family:system-ui,sans-serif;margin:24px;color:#222}table{border-collapse:collapse;width:100%%}
td,th{border:1px solid #ccc;padding:6px 8px;text-align:left;font-size:14px}th{background:#f3f3f3}
.draft{display:inline-block;background:#a11b14;color:#fff;padding:4px 10px;border-radius:4px;font-weight:700}</style>
</head><body>
<p class="draft">BẢN NHÁP — CHỜ NGƯỜI VẬN HÀNH DUYỆT</p>
<h1>TKB ngày %(day)s — đánh dấu buổi lý thuyết đổi phòng sang H209/H210</h1>
<p>Đổi phòng: <b>%(d)d</b> · Giữ nguyên: <b>%(g)d</b> · Chưa chắc: <b>%(c)d</b>.
Bản nháp này không sửa TKB gốc và chưa được gửi cho học viên. Kiểm từng dòng có màu trước khi báo.</p>
<table><thead><tr><th>Mã buổi</th><th>Giờ</th><th>Lớp</th><th>Môn · loại</th><th>Phòng trên TKB</th>
<th>Trạng thái</th><th>Căn cứ</th><th>Lý do</th></tr></thead><tbody>
%(rows)s
</tbody></table></body></html>
""" % {"day": e(normalize_date(ngay) or ngay), "d": counts["doi_phong"], "g": counts["giu_nguyen"],
       "c": counts["chua_chac"], "rows": "\n".join(body)}


if __name__ == "__main__":
    import sys
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    # 1. normalize_date
    assert normalize_date("13/11") == "2026-11-13"
    assert normalize_date("2026-11-13") == "2026-11-13"
    assert normalize_date("13/11/2026") == "2026-11-13"
    assert normalize_date("mai") == "" and normalize_date("40/11") == ""
    print("[ok] normalize_date")

    # 2. parse_timetable
    rows = parse_timetable("13/11")
    assert rows, "13/11 phải có buổi học"
    assert {"ma_buoi", "gio", "lop", "mon", "loai", "phong_tkb"} <= set(rows[0])
    lec = [r for r in rows if r["loai"] == "LEC"]
    print("[ok] parse_timetable('13/11'): %d dòng, %d dòng lý thuyết" % (len(rows), len(lec)))
    for r in lec:
        print("     %-14s %-12s %-4s %-6s %s%s" % (r["ma_buoi"], r["gio"], r["lop"], r["mon"], r["phong_tkb"],
                                                 " (dự phòng)" if r["du_phong"] else ""))
    assert parse_timetable("23/11") == [], "23/11 là ngày nghỉ lễ"
    assert parse_timetable("không phải ngày") == []
    print("[ok] parse_timetable: ngày nghỉ / input sai → []")

    # 3. lookup_merged_room — dùng file mẫu GIẢ để kiểm logic khớp
    os.environ["MERGED_ROOMS_FILE"] = os.path.join("data", "merged_rooms.sample.json")
    for r in lec:
        hits = lookup_merged_room(r)
        print("     %-14s → %s" % (r["ma_buoi"], [h["code"] for h in hits] or "không có căn cứ"))
    lab = next(r for r in rows if r["loai"] == "LAB")
    assert lookup_merged_room(lab) == [], "buổi thực hành không được khớp đoạn gộp phòng lý thuyết"
    os.environ["MERGED_ROOMS_FILE"] = os.path.join("data", "khong-ton-tai.json")
    assert lookup_merged_room(lec[0]) == []
    print("[ok] lookup_merged_room (file mẫu + file thiếu → [])")

    # 4. render_marked_timetable
    demo = [dict(lec[0], trang_thai="doi_phong", phong_moi="H209", can_cu=["GP-01"], ly_do="test"),
            dict(lec[-1], trang_thai="chua_chac", phong_moi="", can_cu=[], ly_do="<b>escape?</b>")]
    page = render_marked_timetable("13/11", demo)
    assert "BẢN NHÁP" in page and "&lt;b&gt;escape?" in page and "→ H209" in page
    print("[ok] render_marked_timetable: %d ký tự HTML, có nhãn bản nháp, đã escape" % len(page))
    print("Tất cả kiểm tra của tools.py đều qua.")
