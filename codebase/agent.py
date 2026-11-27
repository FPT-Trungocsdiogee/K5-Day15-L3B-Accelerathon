"""Luồng chính — workflow cố định đúng sơ đồ spec.md §4.

Hợp đồng: answer(text: str) -> {"output": str}. Khung tự đếm token / số lần gọi qua call_model và @tool.

Luồng (luôn cùng thứ tự, model chỉ làm MỘT việc: quyết định từng buổi dựa trên căn cứ đã tra sẵn):
    0. Đọc yêu cầu: lấy đúng MỘT ngày (+ lớp nếu có). Thiếu ngày → hỏi lại. Ngoài lát cắt → từ chối (G10).
    1. parse_timetable(ngày)                    → danh sách buổi × phòng
    2. Lọc: không phải lý thuyết tại lớp / đã ở H209-H210 / phòng ngoài toà H2 → giữ nguyên (không gọi model)
            phòng '?' (BTC chưa xếp)                                          → chưa chắc
    3. lookup_merged_room(buổi) cho mỗi buổi phòng lẻ H2xx; không có căn cứ   → chưa chắc (không gọi model)
    4. Model đối chiếu các buổi CÓ căn cứ — một lần gọi, trả JSON
    5. Chặn rủi ro: "đổi phòng" phải có phòng mới ∈ {H209, H210}, mã căn cứ thuộc đúng buổi đó và đoạn căn cứ
       có nhắc phòng mới; sai bất kỳ điều nào → ép về "chưa chắc"
    6. render_marked_timetable → bản nháp HTML (lưu drafts/), trả tóm tắt + đường dẫn cho người vận hành duyệt

Tự kiểm: python codebase/agent.py --selftest   ·   chạy một yêu cầu: python codebase/agent.py "13/11 lớp L3A"
"""
from __future__ import annotations

import json
import os
import re

from ai import call_model
from tools import (MERGED_ROOMS, ROOT, lookup_merged_room, normalize_date, parse_timetable,
                   render_marked_timetable)
from tracing import note

DRAFT_DIR = os.path.join(ROOT, "drafts")
GROUPS = ("L3A", "L3B", "L2A", "L2B")
STATUSES = ("doi_phong", "giu_nguyen", "chua_chac")

SYSTEM = """Bạn hỗ trợ NGƯỜI VẬN HÀNH LỚP đối chiếu thời khoá biểu (TKB) với thông tin gộp lớp lý thuyết về 2 phòng lớn H209 / H210.
Mỗi buổi được đưa kèm các đoạn căn cứ có mã. Với TỪNG buổi, quyết định một trong ba trạng thái:
- "doi_phong": căn cứ nói RÕ học viên ở phòng này của đúng buổi này chuyển sang H209 hoặc H210. Ghi phong_moi và mã căn cứ.
- "giu_nguyen": căn cứ nói RÕ phòng này vẫn giữ. Ghi mã căn cứ.
- "chua_chac": căn cứ không rõ, không khớp buổi/phòng, hoặc các đoạn MÂU THUẪN nhau (vd một đoạn nói H209, đoạn khác nói H210).
Tuyệt đối không đoán phòng, không dùng kiến thức ngoài căn cứ, không bịa mã căn cứ. Khi phân vân, chọn "chua_chac".
Chỉ trả về MỘT mảng JSON, không thêm chữ nào khác:
[{"ma_buoi": "...", "trang_thai": "doi_phong|giu_nguyen|chua_chac", "phong_moi": "H209|H210|", "can_cu": ["mã"], "ly_do": "một câu ngắn"}]"""

# Yêu cầu ngoài lát cắt (spec.md §4 "Không làm") — từ chối, chỉ ra việc người vận hành tự làm.
OUT_OF_SCOPE = [
    (r"\b(gửi|nhắn|email|mail|discord|zalo)\b|báo (cho )?(học viên|cả lớp|lớp)",
     "Mình không gửi thông báo cho học viên. Mình chỉ tạo bản nháp TKB đã đánh dấu; người vận hành duyệt rồi tự báo."),
    (r"(sửa|ghi đè|cập nhật|đổi)\s.{0,25}(tkb|thời kho?á biểu)\s*gốc|ghi đè",
     "Mình không sửa / ghi đè TKB gốc. Mình chỉ tạo bản nháp đánh dấu để người vận hành kiểm."),
    (r"thực hành|\blab\b",
     "Lát cắt này chỉ xử lý buổi LÝ THUYẾT; buổi thực hành (LAB) không nằm trong phạm vi."),
    (r"cả tuần|tuần (này|sau|tới)|nhiều ngày|các ngày",
     "Lát cắt này chỉ xử lý MỘT ngày mỗi lần. Hãy gửi từng ngày (vd \"13/11\")."),
    (r"(xếp|phân|tìm)\s.{0,15}phòng (mới|khác|trống)|trùng phòng",
     "Mình không tự xếp phòng mới hay xử lý trùng phòng — các buổi đó sẽ được đánh dấu \"chưa chắc\" để người quyết."),
]

DATE_RE = re.compile(r"\b(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}(?:/\d{4})?)\b")


def read_request(text: str) -> dict:
    """Bước 0: tách ngày + lớp, hoặc trả lời ngay (từ chối / hỏi lại). Không gọi model."""
    low = (text or "").lower()
    for pattern, reply in OUT_OF_SCOPE:
        if re.search(pattern, low):
            return {"reply": "Ngoài phạm vi: " + reply}
    days = sorted({normalize_date(m) for m in DATE_RE.findall(text or "")} - {""})
    if len(days) > 1:
        return {"reply": "Ngoài phạm vi: mỗi lần chỉ đối chiếu MỘT ngày (đang thấy %s). Hãy gửi từng ngày."
                % ", ".join(days)}
    if not days:
        return {"reply": "Bạn muốn đối chiếu TKB ngày nào? Gửi ngày cụ thể, vd \"13/11\" hoặc \"13/11 lớp L3A\" "
                         "(mình không đoán \"mai\" / \"hôm nay\")."}
    groups = [g for g in GROUPS if re.search(r"\b%s\b" % g.lower(), low)]
    return {"ngay": days[0], "lop": groups}


def triage(row: dict) -> dict | None:
    """Bước 2: quyết định không cần model. Trả quyết định, hoặc None nếu là buổi phòng lẻ H2xx cần đối chiếu."""
    room, kind = row["phong_tkb"], row["loai"]
    if kind != "LEC":
        why = {"ONL": "học online, không có phòng", "LAB": "thực hành — ngoài lát cắt"}.get(kind, "không phải buổi lý thuyết")
        return {"trang_thai": "giu_nguyen", "ly_do": why}
    if room in MERGED_ROOMS:
        return {"trang_thai": "giu_nguyen", "ly_do": "đã ở phòng gộp %s" % room}
    if room in ("", "?"):
        return {"trang_thai": "chua_chac", "ly_do": "BTC chưa xếp phòng trên TKB"}
    if not re.fullmatch(r"H2\d{2}", room):
        return {"trang_thai": "giu_nguyen", "ly_do": "phòng ngoài toà H2 — ngoài lát cắt"}
    return None


def parse_model_json(text: str) -> list:
    """Lấy mảng JSON trong câu trả lời của model; hỏng → []."""
    m = re.search(r"\[.*\]", text or "", re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
    except ValueError:
        return []
    return [d for d in data if isinstance(d, dict)] if isinstance(data, list) else []


def guard(row: dict, evidence: list, d: dict | None) -> dict:
    """Bước 5 — chặn rủi ro (spec §4 "Có căn cứ rõ?"). Quyết định không đủ căn cứ → 'chua_chac'."""
    if not d:
        return {"trang_thai": "chua_chac", "phong_moi": "", "can_cu": [],
                "ly_do": "model không trả quyết định hợp lệ cho buổi này"}
    status = d.get("trang_thai") if d.get("trang_thai") in STATUSES else "chua_chac"
    texts = {p["code"]: p["text"] for p in evidence}
    cited = [c for c in (d.get("can_cu") or []) if isinstance(c, str)]
    new_room = str(d.get("phong_moi") or "").strip().upper()
    why = str(d.get("ly_do") or "")[:200]

    def blocked(reason):
        note("chặn %s: %s" % (row["ma_buoi"], reason))
        return {"trang_thai": "chua_chac", "phong_moi": "", "can_cu": [c for c in cited if c in texts],
                "ly_do": "bị chặn — %s (model: %s)" % (reason, why or "không ghi lý do")}

    if status in ("doi_phong", "giu_nguyen"):
        if not cited:
            return blocked("không có mã căn cứ")
        if any(c not in texts for c in cited):
            return blocked("mã căn cứ không thuộc buổi này: %s" % ", ".join(c for c in cited if c not in texts))
    if status == "doi_phong":
        if new_room not in MERGED_ROOMS:
            return blocked("phòng mới '%s' không phải H209/H210" % new_room)
        if not any(new_room in texts[c] for c in cited):
            return blocked("đoạn căn cứ không nhắc %s" % new_room)
        other = MERGED_ROOMS[1 - MERGED_ROOMS.index(new_room)]
        clash = [c for c, t in texts.items() if other in t and new_room not in t]
        if clash:
            return blocked("căn cứ mâu thuẫn: %s nói %s" % (", ".join(clash), other))
        return {"trang_thai": "doi_phong", "phong_moi": new_room, "can_cu": cited, "ly_do": why}
    if status == "giu_nguyen":
        return {"trang_thai": "giu_nguyen", "phong_moi": "", "can_cu": cited, "ly_do": why}
    return {"trang_thai": "chua_chac", "phong_moi": "", "can_cu": [c for c in cited if c in texts],
            "ly_do": why or "căn cứ không rõ"}


def decide_with_model(items: list) -> dict:
    """Bước 4: một lần gọi model cho mọi buổi có căn cứ. → {ma_buoi: quyết định thô của model}."""
    blocks = []
    for row, evidence in items:
        blocks.append("Buổi %s · lớp %s · %s (%s) · %s · %s · phòng trên TKB: %s%s\nCăn cứ:\n%s" % (
            row["ma_buoi"], row["lop"], row["mon"], row["loai"], row["ngay"], row["gio"], row["phong_tkb"],
            " (dự phòng)" if row["du_phong"] else "",
            "\n".join("  [%s] %s" % (p["code"], p["text"]) for p in evidence)))
    reply = call_model(SYSTEM, "Đối chiếu %d buổi sau:\n\n%s" % (len(items), "\n\n".join(blocks)))
    decisions = parse_model_json(reply["text"])
    if not decisions:
        note("model không trả JSON hợp lệ → mọi buổi có căn cứ thành 'chưa chắc'")
    return {str(d.get("ma_buoi")): d for d in decisions}


def save_draft(day: str, groups: list, page: str) -> str:
    """Lưu bản nháp vào drafts/ (thư mục nháp của repo, không phải TKB gốc). → đường dẫn tương đối."""
    os.makedirs(DRAFT_DIR, exist_ok=True)
    name = "tkb-%s%s.html" % (day, ("-" + "-".join(groups)) if groups else "")
    with open(os.path.join(DRAFT_DIR, name), "w", encoding="utf-8") as f:
        f.write(page)
    return "drafts/" + name


def summarize(day: str, groups: list, decisions: list, draft_path: str) -> str:
    counts = {k: sum(1 for q in decisions if q["trang_thai"] == k) for k in STATUSES}
    lines = ["BẢN NHÁP — CHỜ DUYỆT · TKB ngày %s%s" % (day, (" · lớp " + ", ".join(groups)) if groups else ""),
             "Đổi phòng: %d · Giữ nguyên: %d · Chưa chắc: %d" % (counts["doi_phong"], counts["giu_nguyen"],
                                                                 counts["chua_chac"])]
    marked = [q for q in decisions if q["trang_thai"] != "giu_nguyen"]
    if marked:
        lines.append("")
        lines.append("Các dòng cần kiểm:")
    for q in sorted(marked, key=lambda q: (q["gio"], q["ma_buoi"])):
        if q["trang_thai"] == "doi_phong":
            lines.append("- %s · %s %s · %s: ĐỔI PHÒNG %s → %s [căn cứ: %s]" % (
                q["ma_buoi"], q["lop"], q["mon"], q["gio"], q["phong_tkb"], q["phong_moi"], ", ".join(q["can_cu"])))
        else:
            lines.append("- %s · %s %s · %s: CHƯA CHẮC — %s%s" % (
                q["ma_buoi"], q["lop"], q["mon"], q["gio"], q["ly_do"],
                (" [đoạn liên quan: %s]" % ", ".join(q["can_cu"])) if q["can_cu"] else ""))
    lines += ["", "Bản nháp HTML: %s" % draft_path,
              "Chưa sửa TKB gốc, chưa gửi cho học viên. Người vận hành kiểm từng dòng rồi tự báo."]
    return "\n".join(lines)


def answer(text: str) -> dict:
    req = read_request(text)
    if "reply" in req:
        note("không chạy luồng: %s" % req["reply"][:80])
        return {"output": req["reply"]}
    day, groups = req["ngay"], req["lop"]

    rows = [r for r in parse_timetable(day) if not groups or r["lop"] in groups]
    if not rows:
        return {"output": "TKB không có buổi học nào ngày %s%s (ngày nghỉ, hoặc ngoài giai đoạn 1 05/11–28/11). "
                          "Không có gì để đánh dấu." % (day, (" cho lớp " + ", ".join(groups)) if groups else "")}

    decisions, to_model = [], []
    for row in rows:
        d = triage(row)
        if d is None:
            evidence = lookup_merged_room(row)
            if evidence:
                to_model.append((row, evidence))
                continue
            d = {"trang_thai": "chua_chac", "ly_do": "không có căn cứ gộp phòng cho buổi này"}
        decisions.append(dict(row, phong_moi="", can_cu=[], **d))

    if to_model:
        raw = decide_with_model(to_model)
        for row, evidence in to_model:
            decisions.append(dict(row, **guard(row, evidence, raw.get(row["ma_buoi"]))))
    note("dừng: %d buổi, %d qua model" % (len(decisions), len(to_model)))

    page = render_marked_timetable(day, decisions)
    return {"output": summarize(day, groups, decisions, save_draft(day, groups, page))}


if __name__ == "__main__":
    import sys

    import tracing

    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    def run(text):
        tracing.begin("cli")
        out = answer(text)["output"]
        summary, _ = tracing.end()
        print(">>> %s\n%s\n[trace] model=%d · tool=%d · token in/out=%d/%d\n" % (
            text, out, summary["model_calls"], summary["tool_calls"], summary["tokens_in"], summary["tokens_out"]))
        return out

    if len(sys.argv) > 1 and sys.argv[1] != "--selftest":
        run(" ".join(sys.argv[1:]))
        sys.exit(0)

    # --selftest: dùng thông tin gộp GIẢ + model giả có kịch bản, để kiểm luồng và lớp chặn mà không tốn token.
    os.environ.setdefault("MERGED_ROOMS_FILE", os.path.join("data", "merged_rooms.sample.json"))
    scripted = json.dumps([
        {"ma_buoi": "L3A-12/H203", "trang_thai": "doi_phong", "phong_moi": "H209", "can_cu": ["GP-01"], "ly_do": "GP-01"},
        {"ma_buoi": "L3A-12/H207", "trang_thai": "doi_phong", "phong_moi": "H209", "can_cu": ["GP-02"],
         "ly_do": "cố ý sai: GP-02 nói H210"},
        {"ma_buoi": "L3B-12/H203", "trang_thai": "doi_phong", "phong_moi": "H209", "can_cu": ["GP-99"],
         "ly_do": "cố ý bịa mã"},
    ])
    _real_call_model = call_model
    call_model = tracing.model_call(lambda system, user: {  # noqa: F811 — chỉ thay trong tự kiểm
        "text": scripted, "model": "selftest-stub", "tokens_in": 0, "tokens_out": 0})

    out = run("Đánh dấu TKB ngày 13/11")
    assert "L3A-12/H203" in out and "ĐỔI PHÒNG H203 → H209 [căn cứ: GP-01]" in out
    assert "L3A-12/H207 · L3A LEC 6 · 09:00-13:00: CHƯA CHẮC — bị chặn — đoạn căn cứ không nhắc H209" in out
    assert "L3B-12/H203" in out and "mã căn cứ không thuộc buổi này: GP-99" in out
    assert "L3B-12/H207" in out and "không có căn cứ gộp phòng" in out

    # Model bỏ qua đoạn mâu thuẫn GP-04 (nói H210), chỉ trích GP-03 (nói H209) → phải bị chặn.
    scripted = json.dumps([{"ma_buoi": "L3B-12/H203", "trang_thai": "doi_phong", "phong_moi": "H209",
                            "can_cu": ["GP-03"], "ly_do": "bỏ qua GP-04"}])
    out = run("13/11 L3B")
    assert "căn cứ mâu thuẫn: GP-04 nói H210" in out and "Đổi phòng: 0" in out
    print("[ok] luồng chính + lớp chặn (đúng / sai phòng / bịa mã / mâu thuẫn / không căn cứ)")

    assert "Ngoài phạm vi" in run("Gửi thông báo đổi phòng ngày 13/11 cho học viên")
    assert "Ngoài phạm vi" in run("Đánh dấu cả tuần 9/11 đến 14/11")
    assert "Ngoài phạm vi" in run("Buổi thực hành 13/11 đổi phòng không?")
    assert "ngày nào" in run("Mai lớp mình học phòng nào?")
    assert "không có buổi học nào" in run("23/11")
    print("[ok] từ chối ngoài phạm vi · hỏi lại khi thiếu ngày · ngày nghỉ")

    call_model = _real_call_model
    out = run("13/11 lớp L3A")
    print("[ok] chạy với model thật/giả theo .env (MODEL_PROVIDER) — model giả → các buổi có căn cứ thành 'chưa chắc'")
    print("Tất cả kiểm tra của agent.py đều qua.")
