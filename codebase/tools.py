"""Công cụ của bài toán — khớp bảng công cụ ở spec.md §4 (lát cắt học viên).

Ba công cụ, đều KHÔNG tác động ra ngoài (chỉ đọc file, hoặc dựng trang HTML cho học viên đang hỏi):
    parse_timetable          mã học viên + ngày → các buổi của CHÍNH học viên đó trong ngày
    lookup_merged_room       một buổi → các đoạn thông tin gộp phòng H209/H210 áp dụng cho buổi đó
    render_marked_timetable  quyết định từng buổi → trang TKB của học viên: ~~phòng cũ~~ → phòng mới, 3 màu, cột căn cứ

Hàm phụ (không phải công cụ, không gọi model): normalize_date, normalize_student_id, find_student,
holiday_note, related_notices.

Nguồn dữ liệu (đổi bằng biến môi trường, không cần sửa code):
    STUDENT_SCHEDULE_FILE  mặc định data/ai20k_student_schedule_long.csv — phòng của TỪNG học viên từng buổi
    TIMETABLE_FILE         mặc định data/ai20k_schedule.json — dùng để biết phòng dự phòng và ngày nghỉ lễ
    MERGED_ROOMS_FILE      mặc định eval/merged_room_fixture.csv — thông tin gộp phòng GOP-xx
                           (cột: code, lop, tu_ngay, den_ngay, do_chac, phong_cu, phong_moi, text;
                            do_chac = xac_nhan | du_kien; phong_moi = H209 | H210 | GIU)

Tự kiểm: python codebase/tools.py
"""
import csv
import html
import json
import os
import re

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_YEAR = 2026
MERGED_ROOMS = ("H209", "H210")
STUDENT_ID_RE = re.compile(r"\b2[aA]\d{9}\b")


def _path(env_key, default_rel):
    p = os.environ.get(env_key) or default_rel
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


# ------------------------------------------------------------------ hàm phụ
def normalize_date(text: str) -> str:
    """'13/11', '13/11/2026', '2026-11-13' → '2026-11-13'. Không nhận ra → ''."""
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


def ddmm(day: str) -> str:
    """'2026-11-13' → '13/11'."""
    return "%s/%s" % (day[8:10], day[5:7]) if len(day) == 10 else day


def normalize_student_id(text: str) -> str:
    """'2a202603885' → '2A202603885'. Không đúng dạng 2A + 9 chữ số → ''."""
    text = (text or "").strip()
    return text.upper() if STUDENT_ID_RE.fullmatch(text) else ""


_cache = {}


def _students():
    """student_id → {"lop", "rows": [dòng CSV]} (đọc một lần)."""
    path = _path("STUDENT_SCHEDULE_FILE", os.path.join("data", "ai20k_student_schedule_long.csv"))
    if path not in _cache:
        index = {}
        with open(path, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                s = index.setdefault(r["student_id"], {"lop": r["group"], "rows": []})
                s["rows"].append(r)
        _cache[path] = index
    return _cache[path]


def _timetable():
    """(meta, {session_id: set(phòng dự phòng)}) từ TKB nhóm."""
    path = _path("TIMETABLE_FILE", os.path.join("data", "ai20k_schedule.json"))
    if path not in _cache:
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)
        backups = {}
        for g in data.get("groups", {}).values():
            for s in g.get("sessions", []):
                backups[s["session_id"]] = {r["code"] for r in s.get("rooms") or [] if r.get("backup")}
        _cache[path] = (data.get("meta", {}), backups)
    return _cache[path]


def _notices():
    path = _path("MERGED_ROOMS_FILE", os.path.join("eval", "merged_room_fixture.csv"))
    if not os.path.exists(path):
        return []
    if path not in _cache:
        with open(path, encoding="utf-8-sig", newline="") as f:
            _cache[path] = [dict(r) for r in csv.DictReader(f)]
    return _cache[path]


def find_student(ma_hoc_vien: str) -> dict | None:
    """Mã có trong TKB → {"ma", "lop"}; không có → None. Chỉ trả lớp, không trả thông tin người khác."""
    ma = normalize_student_id(ma_hoc_vien)
    s = _students().get(ma) if ma else None
    return {"ma": ma, "lop": s["lop"]} if s else None


def holiday_note(day: str) -> str:
    """Ngày nghỉ lễ / ngoài giai đoạn 1 → câu giải thích; ngày thường → ''."""
    meta, _ = _timetable()
    for h in meta.get("holidays", []):
        if h.get("date") == day:
            return "ngày %s là ngày nghỉ lễ, không có lịch học" % ddmm(day)
    period = meta.get("period", {})
    if day and (day < period.get("start", "") or day > period.get("end", "9999")):
        return "TKB giai đoạn 1 chỉ có từ %s đến %s; ngày %s không có trong dữ liệu" % (
            ddmm(period.get("start", "")), ddmm(period.get("end", "")), ddmm(day))
    return ""


def related_notices(buoi: dict) -> list:
    """Các đoạn gộp phòng cùng phòng nhưng KHÔNG áp dụng cho buổi này — để giải thích vì sao 'chưa chắc':
    cùng lớp nhưng ngoài khoảng ngày, hoặc cùng ngày nhưng là của lớp khác."""
    out, seen = [], set()
    for n in _notices():
        if n["phong_cu"] != buoi.get("phong_tkb") or n["code"] in seen:
            continue
        in_range = n["tu_ngay"] <= buoi.get("ngay", "") <= n["den_ngay"]
        same_class = n["lop"] == buoi.get("lop")
        if same_class and not in_range:
            why = ("chỉ áp dụng ngày %s" % ddmm(n["tu_ngay"]) if n["tu_ngay"] == n["den_ngay"]
                   else "chỉ áp dụng %s–%s" % (ddmm(n["tu_ngay"]), ddmm(n["den_ngay"])))
        elif in_range and not same_class:
            why = "là của lớp %s, không áp dụng cho lớp %s" % (n["lop"], buoi.get("lop"))
        else:
            continue
        seen.add(n["code"])
        out.append({"code": n["code"], "ly_do": why})
    return out


# ------------------------------------------------------------------ công cụ
@tool
def parse_timetable(ma_hoc_vien: str, ngay: str) -> list:
    """parse_timetable — đọc TKB của MỘT học viên trong MỘT ngày.
    Input: mã học viên (str, không phân biệt hoa thường) + ngày (str, '13/11' | '13/11/2026' | '2026-11-13').
    Output: danh sách buổi của chính học viên đó trong ngày:
        {ma_buoi, ngay, gio, lop, mon, loai, phong_tkb, du_phong}
        loai: LEC (lý thuyết) · ONL (lý thuyết online) · LAB (thực hành) · KG (khai giảng) · HACK
        phong_tkb: phòng xếp cho học viên này, '' nếu không có phòng (online / khai giảng).
        Mã không có trong TKB / ngày không hợp lệ / ngày không có buổi → [].
    Tác động ra ngoài: Không — chỉ đọc file trong data/; không trả lịch của học viên khác."""
    ma, day = normalize_student_id(ma_hoc_vien), normalize_date(ngay)
    s = _students().get(ma) if ma else None
    if not s or not day:
        return []
    _, backups = _timetable()
    out = []
    for r in s["rows"]:
        if r["date"] != day:
            continue
        room = r["room"] or ""
        out.append({
            "ma_buoi": r["session_id"], "ngay": day, "gio": "%s-%s" % (r["start"], r["end"]),
            "lop": r["group"], "mon": r["session_name"], "loai": r["kind"],
            "phong_tkb": room, "du_phong": room in backups.get(r["session_id"], set()),
        })
    return sorted(out, key=lambda b: b["gio"])


@tool
def lookup_merged_room(buoi: dict) -> list:
    """lookup_merged_room — tra thông tin gộp lớp về H209/H210 ÁP DỤNG cho một buổi.
    Input: một buổi (dict từ parse_timetable; dùng ngay, lop, phong_tkb).
    Output: danh sách đoạn căn cứ {code, text, phong_moi, do_chac, tu_ngay, den_ngay}; [] nếu không có.
        Áp dụng khi: cùng lớp · ngày của buổi nằm trong [tu_ngay, den_ngay] · phòng của buổi = phong_cu.
        phong_moi: H209 | H210 | GIU (giữ phòng) · do_chac: xac_nhan | du_kien.
    Tác động ra ngoài: Không — chỉ đọc file."""
    out = []
    for n in _notices():
        if (n["lop"] == buoi.get("lop") and n["phong_cu"] == buoi.get("phong_tkb")
                and n["tu_ngay"] <= buoi.get("ngay", "") <= n["den_ngay"]):
            out.append({k: n[k] for k in ("code", "text", "phong_moi", "do_chac", "tu_ngay", "den_ngay")})
    return out


_STATUS = {
    "doi_phong": ("ĐỔI PHÒNG", "#fff1c2", "#8a6100"),
    "giu_nguyen": ("Giữ nguyên", "#e6f4ea", "#1e6b34"),
    "chua_chac": ("CHƯA CHẮC — hỏi người vận hành lớp", "#fde2e1", "#a11b14"),
}


@tool
def render_marked_timetable(ma_hoc_vien: str, ngay: str, quyet_dinh: list) -> str:
    """render_marked_timetable — dựng trang TKB ngày đó của học viên đã đánh dấu.
    Input: mã học viên + ngày + danh sách quyết định, mỗi phần tử là một buổi (dict từ parse_timetable) kèm
        {trang_thai: doi_phong|giu_nguyen|chua_chac, phong_cu, phong_moi, can_cu: [mã đoạn], ly_do}.
    Output: chuỗi HTML — buổi đổi phòng hiện <s>phòng cũ</s> → phòng mới (mong muốn R22), 3 màu, cột căn cứ.
    Tác động ra ngoài: Không — chỉ trả chuỗi HTML cho học viên đang hỏi; không ghi đè TKB gốc, không gửi."""
    e = html.escape
    body = []
    for q in sorted(quyet_dinh, key=lambda q: q.get("gio", "")):
        label, bg, fg = _STATUS.get(q.get("trang_thai"), _STATUS["chua_chac"])
        old = e(q.get("phong_cu") or "—") + (" (dự phòng)" if q.get("du_phong") else "")
        if q.get("trang_thai") == "doi_phong" and q.get("phong_moi"):
            room = "<s>%s</s> → <b style='font-size:1.3em'>%s</b>" % (old, e(q["phong_moi"]))
        else:
            room = "<b style='font-size:1.3em'>%s</b>" % old
        body.append(
            "<tr style='background:%s'><td>%s</td><td>%s · %s</td><td>%s</td>"
            "<td style='color:%s;font-weight:600'>%s</td><td>%s</td><td>%s</td></tr>" % (
                bg, e(q.get("gio", "")), e(q.get("mon", "")), e(q.get("loai", "")), room,
                fg, e(label), e(", ".join(q.get("can_cu") or [])), e(q.get("ly_do", ""))))
    return """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TKB %(day)s — %(ma)s</title>
<style>body{font-family:system-ui,sans-serif;margin:24px;color:#222}table{border-collapse:collapse;width:100%%}
td,th{border:1px solid #ccc;padding:8px;text-align:left;font-size:15px}th{background:#f3f3f3}</style>
</head><body>
<h1>TKB ngày %(day)s của %(ma)s</h1>
<p>Đã đối chiếu các buổi lý thuyết với thông tin gộp phòng H209/H210. Mở mã căn cứ để tự kiểm trước khi đi học;
buổi "chưa chắc" hãy hỏi người vận hành lớp. Trang này không sửa TKB gốc và không gửi cho ai.</p>
<table><thead><tr><th>Giờ</th><th>Buổi · loại</th><th>Phòng</th><th>Trạng thái</th><th>Căn cứ</th><th>Lý do</th></tr></thead><tbody>
%(rows)s
</tbody></table></body></html>
""" % {"day": e(ddmm(normalize_date(ngay)) or ngay), "ma": e(normalize_student_id(ma_hoc_vien) or ma_hoc_vien),
       "rows": "\n".join(body)}


if __name__ == "__main__":
    import sys
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    assert normalize_date("09/11") == "2026-11-09" and normalize_date("mai") == ""
    assert normalize_student_id("2a202603885") == "2A202603885" and normalize_student_id("2A2026") == ""
    print("[ok] normalize_date · normalize_student_id")

    assert find_student("2a202603520") == {"ma": "2A202603520", "lop": "L3A"}
    assert find_student("2A209999999") is None
    print("[ok] find_student (có mã · mã không tồn tại)")

    day = parse_timetable("2A202603520", "09/11")
    print("[ok] parse_timetable('2A202603520', '09/11'):")
    for b in day:
        print("     %-7s %-6s %-4s %-12s %s" % (b["ma_buoi"], b["mon"], b["loai"], b["gio"], b["phong_tkb"]))
    assert [(b["mon"], b["phong_tkb"]) for b in day] == [("LAB 2", "E305"), ("LEC 3", "H203")]
    assert parse_timetable("2A202603355", "23/11") == [] and parse_timetable("2A209999999", "09/11") == []
    assert parse_timetable("2A202603520", "05/11")[-1]["du_phong"] is True   # H203* phòng dự phòng ngày 05/11
    assert holiday_note("2026-11-23") and holiday_note("2026-11-30") and not holiday_note("2026-11-09")
    print("[ok] ngày nghỉ / mã sai → [] · phòng dự phòng · holiday_note")

    def lec(ma, d):
        return next(b for b in parse_timetable(ma, d) if b["loai"] == "LEC")
    cases = [("2A202603520", "09/11", ["GOP-01"]),          # L3A H203 trong khoảng
             ("2A202603698", "18/11", []),                  # L3A ngoài khoảng GOP-01
             ("2A202604107", "16/11", ["GOP-02", "GOP-04"]),  # L3B H204: hai đoạn mâu thuẫn
             ("2A202603682", "17/11", ["GOP-05"]),          # dự kiến
             ("2A202603936", "27/11", [])]                  # L3B H201 không có căn cứ
    for ma, d, want in cases:
        got = sorted({n["code"] for n in lookup_merged_room(lec(ma, d))})
        assert got == want, (ma, d, got)
        print("     %s %s %s → %s" % (ma, d, lec(ma, d)["phong_tkb"], got or "không có căn cứ"))
    rel = {r["code"]: r["ly_do"] for r in related_notices(lec("2A202603698", "18/11"))}
    assert "GOP-01" in rel and "GOP-02" in rel, rel
    print("[ok] lookup_merged_room · related_notices:", rel)

    page = render_marked_timetable("2A202603520", "09/11", [dict(lec("2A202603520", "09/11"), trang_thai="doi_phong",
                                   phong_cu="H203", phong_moi="H209", can_cu=["GOP-01"], ly_do="<x>")])
    assert "<s>H203</s> → <b" in page and "&lt;x&gt;" in page
    print("[ok] render_marked_timetable: gạch phòng cũ → phòng mới, đã escape")
    print("Tất cả kiểm tra của tools.py đều qua.")
