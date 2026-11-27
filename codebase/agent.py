"""Luồng chính — workflow cố định đúng sơ đồ spec.md §4 (lát cắt học viên).

Hợp đồng: answer(text: str) -> {"output": str}. Khung tự đếm token / số lần gọi qua call_model và @tool.

Luồng (luôn cùng thứ tự; model chỉ làm MỘT việc: quyết định từng buổi dựa trên căn cứ đã tra sẵn):
    0. Đọc yêu cầu: ngoài lát cắt (§4 "Không làm") → từ chối · thiếu mã học viên / ngày → hỏi lại
       · mã không có trong TKB → báo không tìm thấy. Không gọi model, không đưa mã phòng nào.
    1. parse_timetable(mã, ngày)               → các buổi của chính học viên đó trong ngày
    2. "Buổi lý thuyết ghi phòng H2xx?"         Không (thực hành / online / đã ở H209-H210 / phòng ngoài toà H2) → giữ nguyên
    3. lookup_merged_room(buổi)                → đoạn căn cứ có mã; không có → chưa chắc (không gọi model)
    4. Model đối chiếu các buổi có căn cứ — một lần gọi, trả JSON
    5. "Có căn cứ rõ?" — lớp chặn không phụ thuộc model:
         căn cứ mâu thuẫn (đoạn đã xác nhận chỉ về 2 phòng khác nhau) → chưa chắc
         căn cứ chỉ là dự kiến → chưa chắc
         "đổi phòng" phải: phòng mới ∈ {H209, H210}, trùng phòng mới của căn cứ, mã căn cứ thuộc đúng buổi
       sai bất kỳ điều nào → ép về "chưa chắc"
    6. render_marked_timetable → trang HTML (drafts/, đã gitignore) + tóm tắt chữ cho học viên tự kiểm

Tự kiểm: python codebase/agent.py --selftest   ·   một câu: python codebase/agent.py "Mình là 2A202603520, ngày 09/11 ..."
"""
from __future__ import annotations

import json
import os
import re

from ai import call_model
from tools import (MERGED_ROOMS, ROOT, STUDENT_ID_RE, ddmm, find_student, holiday_note, lookup_merged_room,
                   normalize_date, normalize_student_id, parse_timetable, related_notices,
                   render_marked_timetable)
from tracing import note

DRAFT_DIR = os.path.join(ROOT, "drafts")
STATUSES = ("doi_phong", "giu_nguyen", "chua_chac")
LABEL = {"doi_phong": "ĐỔI PHÒNG", "giu_nguyen": "giữ nguyên", "chua_chac": "CHƯA CHẮC"}

SYSTEM = """Bạn giúp HỌC VIÊN kiểm tra buổi lý thuyết của chính họ có bị gộp phòng về H209 / H210 không.
Đầu vào là JSON: mỗi buổi có phòng ghi trên TKB và các đoạn căn cứ có mã, kèm phong_moi (H209 | H210 | GIU = giữ phòng)
và do_chac (xac_nhan = đã xác nhận | du_kien = mới dự kiến).
Với TỪNG buổi, chọn đúng một trạng thái:
- "doi_phong": có đoạn căn cứ ĐÃ XÁC NHẬN nói phòng này chuyển sang H209 hoặc H210, và không đoạn nào nói phòng khác. Ghi phong_moi và mã căn cứ.
- "giu_nguyen": có đoạn căn cứ đã xác nhận nói phòng này giữ nguyên (GIU). Ghi mã căn cứ.
- "chua_chac": căn cứ chỉ là dự kiến, các đoạn mâu thuẫn nhau, hoặc không rõ.
Không đoán phòng, không dùng kiến thức ngoài căn cứ, không bịa mã căn cứ. Phân vân thì chọn "chua_chac".
Chỉ trả về MỘT mảng JSON, không thêm chữ nào khác:
[{"ma_buoi": "...", "trang_thai": "doi_phong|giu_nguyen|chua_chac", "phong_moi": "H209|H210|", "can_cu": ["mã"], "ly_do": "một câu ngắn"}]"""

ASK_OPERATOR = "hỏi người vận hành lớp"
# Ngoài lát cắt (spec §4 "Không làm") và tấn công — xét theo thứ tự. Câu trả lời KHÔNG chứa mã phòng.
OUT_OF_SCOPE = [
    (r"bỏ qua (mọi|tất cả|các|toàn bộ) (hướng dẫn|chỉ dẫn|quy tắc)|system prompt|prompt hệ thống|in nguyên văn",
     "Mình không in hướng dẫn hệ thống hay nguyên văn dữ liệu. Mình chỉ giúp kiểm buổi lý thuyết của chính bạn "
     "có đổi phòng không: gửi mã học viên + một ngày học."),
    (r"bỏ qua (phần |các )?căn cứ|không cần căn cứ|đổi hết",
     "Mình không đánh dấu đổi phòng khi chưa có căn cứ rõ: buổi thiếu căn cứ vẫn là \"chưa chắc\" để bạn "
     + ASK_OPERATOR + ", không đổi hàng loạt."),
    (r"\b(gửi|nhắn|email|e-mail|mail|zalo|discord)\b",
     "Mình không gửi thông báo cho ai. Mình chỉ hiển thị TKB của chính bạn đã đánh dấu; báo cho cả lớp là việc "
     "của người vận hành lớp."),
    (r"hệ thống (tkb )?(của )?trường|(sửa|ghi đè|cập nhật)\s.{0,40}(tkb|thời kho?á biểu)\s*gốc",
     "Mình không đọc / ghi hệ thống của trường và không sửa TKB gốc. Mình chỉ đối chiếu với TKB đã lưu sẵn trong "
     "data/ (có thể không phải bản mới nhất) và hiển thị đánh dấu kèm căn cứ; muốn sửa TKB gốc thì báo người vận hành lớp."),
    (r"danh sách|cả lớp|toàn bộ (lớp|học viên)|học viên khác|bạn khác|người khác",
     "Mình không cung cấp lịch / phòng của học viên khác hay danh sách mã học viên. Bạn gửi mã của chính mình "
     "+ một ngày học để mình tra."),
    (r"trùng (giờ|phòng)|tự (chọn|xếp)|phòng trống|xếp phòng",
     "Mình không tự xếp phòng hay xử lý trùng phòng. Buổi không đủ căn cứ sẽ được đánh dấu \"chưa chắc\" để "
     "người vận hành lớp quyết định."),
    (r"thực hành|\blab\b|cả tuần|tuần (này|sau|tới)|nhiều ngày|các ngày",
     "Mình chỉ đối chiếu buổi LÝ THUYẾT của MỘT ngày (không xử lý buổi thực hành hay nhiều ngày). "
     "Gửi mã học viên + một ngày học lý thuyết, vd \"ngày 13/11\"."),
]
DATE_RE = re.compile(r"\b(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}(?:/\d{4})?)\b")


def read_request(text: str) -> dict:
    """Bước 0: tách mã + ngày, hoặc trả lời ngay. Không gọi model, không đưa mã phòng."""
    low = (text or "").lower()
    for pattern, reply in OUT_OF_SCOPE:
        if re.search(pattern, low):
            return {"reply": "Ngoài phạm vi: " + reply}
    ids = sorted({normalize_student_id(m) for m in STUDENT_ID_RE.findall(text or "")})
    days = sorted({normalize_date(m) for m in DATE_RE.findall(text or "")} - {""})
    if len(ids) > 1:
        return {"reply": "Ngoài phạm vi: mình chỉ tra lịch của chính bạn — gửi một mã học viên thôi."}
    if not ids:
        return {"reply": "Bạn gửi giúp mã học viên của mình (dạng 2A + 9 chữ số)%s nhé. Mình tra theo mã học viên, "
                         "không tra theo tên vì tên viết tắt có thể trùng nhiều người."
                         % ("" if days else " và một ngày học cụ thể, vd 13/11")}
    student = find_student(ids[0])
    if not student:
        return {"reply": "Không tìm thấy mã học viên bạn gửi trong TKB. Bạn kiểm tra lại mã, hoặc hỏi người vận hành "
                         "lớp / BTC."}
    if len(days) > 1:
        return {"reply": "Ngoài phạm vi: mỗi lần mình chỉ đối chiếu MỘT ngày. Bạn gửi từng ngày nhé."}
    if not days:
        return {"reply": "Bạn muốn kiểm ngày nào? Gửi ngày cụ thể (vd 13/11) — mình không đoán \"mai\" / \"hôm nay\"."}
    return {"ma": student["ma"], "lop": student["lop"], "ngay": days[0]}


def triage(b: dict) -> dict | None:
    """Bước 2: quyết định không cần model. None = buổi lý thuyết ở phòng lẻ H2xx, cần tra căn cứ."""
    room, kind = b["phong_tkb"], b["loai"]
    if kind != "LEC":
        why = {"ONL": "học online, không có phòng", "LAB": "thực hành — ngoài lát cắt, không đánh dấu"}.get(
            kind, "không phải buổi lý thuyết")
        return {"trang_thai": "giu_nguyen", "ly_do": why}
    if not room:
        return {"trang_thai": "chua_chac", "ly_do": "TKB chưa ghi phòng — " + ASK_OPERATOR}
    if room in MERGED_ROOMS:
        return {"trang_thai": "giu_nguyen", "ly_do": "đã ở phòng gộp %s" % room}
    if not re.fullmatch(r"H2\d{2}", room):
        return {"trang_thai": "giu_nguyen", "ly_do": "%s không phải phòng lẻ H2xx — không đổi" % room}
    return None


def no_evidence_reason(b: dict) -> str:
    """Giải thích 'chưa chắc' khi không có căn cứ áp dụng: kể các đoạn gần đúng nhưng không áp dụng."""
    parts = ["không có căn cứ gộp phòng cho %s ngày %s" % (b["phong_tkb"], ddmm(b["ngay"]))]
    parts += ["%s %s" % (r["code"], r["ly_do"]) for r in related_notices(b)]
    if b.get("du_phong"):
        parts.append("%s là phòng dự phòng của buổi này" % b["phong_tkb"])
    return "; ".join(parts) + " — " + ASK_OPERATOR


def parse_model_json(text: str) -> list:
    m = re.search(r"\[.*\]", text or "", re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
    except ValueError:
        return []
    return [d for d in data if isinstance(d, dict)] if isinstance(data, list) else []


def decide_with_model(items: list) -> dict:
    """Bước 4: một lần gọi model cho mọi buổi có căn cứ. → {ma_buoi: quyết định thô}."""
    payload = [{"ma_buoi": b["ma_buoi"], "lop": b["lop"], "mon": b["mon"], "ngay": b["ngay"], "gio": b["gio"],
                "phong_tkb": b["phong_tkb"], "phong_du_phong": b["du_phong"], "can_cu": ev} for b, ev in items]
    reply = call_model(SYSTEM, "Đối chiếu %d buổi sau (JSON):\n%s" % (len(items), json.dumps(payload, ensure_ascii=False)))
    decisions = parse_model_json(reply["text"])
    if not decisions:
        note("model không trả JSON hợp lệ → các buổi có căn cứ thành 'chưa chắc'")
    return {str(d.get("ma_buoi")): d for d in decisions}


def guard(b: dict, evidence: list, d: dict | None) -> dict:
    """Bước 5 — "Có căn cứ rõ?". Không đủ căn cứ → 'chua_chac', bất kể model nói gì."""
    by_code = {}
    for e in evidence:
        by_code.setdefault(e["code"], e)
    confirmed = {e["phong_moi"] for e in evidence if e["do_chac"] == "xac_nhan"}
    model_why = str((d or {}).get("ly_do") or "")[:200]

    def unsure(reason, cited=()):
        note("chưa chắc %s: %s" % (b["ma_buoi"], reason))
        return {"trang_thai": "chua_chac", "phong_moi": "", "can_cu": list(cited), "ly_do": reason + " — " + ASK_OPERATOR}

    if len(confirmed) > 1:
        return unsure("căn cứ mâu thuẫn: " + ", ".join(
            "%s → %s" % (c, e["phong_moi"]) for c, e in sorted(by_code.items()) if e["do_chac"] == "xac_nhan"),
            sorted(by_code))
    if not confirmed:
        return unsure(", ".join(sorted(by_code)) + " chỉ là dự kiến, chờ BTC xác nhận", sorted(by_code))
    target = next(iter(confirmed))
    if not d or d.get("trang_thai") not in STATUSES:
        return unsure("model không trả quyết định hợp lệ cho buổi này")
    status = d["trang_thai"]
    if status == "chua_chac":
        return unsure(model_why or "model chọn chưa chắc")
    cited = [c for c in (d.get("can_cu") or []) if isinstance(c, str)]
    if not cited:
        return unsure("bị chặn — model không ghi mã căn cứ")
    bad = [c for c in cited if c not in by_code]
    if bad:
        return unsure("bị chặn — mã căn cứ không thuộc buổi này: " + ", ".join(bad))
    if status == "doi_phong":
        new_room = str(d.get("phong_moi") or "").strip().upper()
        if new_room not in MERGED_ROOMS or new_room != target:
            return unsure("bị chặn — model chọn '%s' nhưng căn cứ ghi %s" % (new_room, target), cited)
        return {"trang_thai": "doi_phong", "phong_moi": new_room, "can_cu": cited, "ly_do": model_why}
    if target != "GIU":
        return unsure("bị chặn — model chọn giữ nguyên nhưng căn cứ ghi chuyển sang %s" % target, cited)
    return {"trang_thai": "giu_nguyen", "phong_moi": "", "can_cu": cited, "ly_do": model_why}


def save_page(ma: str, day: str, page: str) -> str:
    os.makedirs(DRAFT_DIR, exist_ok=True)
    name = "tkb-%s-%s.html" % (day, ma)
    with open(os.path.join(DRAFT_DIR, name), "w", encoding="utf-8") as f:
        f.write(page)
    return "drafts/" + name


def summarize(req: dict, decisions: list, page_path: str) -> str:
    lines = ["TKB ngày %s của %s (lớp %s) — đã đối chiếu thông tin gộp phòng H209/H210:"
             % (ddmm(req["ngay"]), req["ma"], req["lop"])]
    for q in sorted(decisions, key=lambda q: q["gio"]):
        head = "- %s · %s (%s)" % (q["gio"], q["mon"], q["loai"])
        tag = "%s (%s)" % (LABEL[q["trang_thai"]], q["trang_thai"])
        if q["trang_thai"] == "doi_phong":
            lines.append("%s: %s ~~%s~~ → %s [căn cứ: %s]%s" % (
                head, tag, q["phong_cu"], q["phong_moi"], ", ".join(q["can_cu"]),
                (" — " + q["ly_do"]) if q["ly_do"] else ""))
        else:
            room = (" · phòng %s" % q["phong_cu"]) if q["phong_cu"] else ""
            ev = (" [đoạn liên quan: %s]" % ", ".join(q["can_cu"])) if q["can_cu"] else ""
            lines.append("%s%s: %s — %s%s" % (head, room, tag, q["ly_do"], ev))
    lines += ["Mở mã căn cứ để tự kiểm trước khi đi học; buổi \"chưa chắc\" hãy %s." % ASK_OPERATOR,
              "Trang TKB đánh dấu: %s (không sửa TKB gốc, không gửi cho ai)." % page_path]
    return "\n".join(lines)


def answer(text: str) -> dict:
    req = read_request(text)
    if "reply" in req:
        note("không chạy luồng: %s" % req["reply"][:80])
        return {"output": req["reply"]}

    sessions = parse_timetable(req["ma"], req["ngay"])
    if not sessions:
        why = holiday_note(req["ngay"]) or "bạn không có buổi học nào ngày %s" % ddmm(req["ngay"])
        return {"output": "TKB không có buổi nào ngày %s: %s. Không có gì để đánh dấu." % (ddmm(req["ngay"]), why)}

    decisions, to_model = [], []
    for b in sessions:
        d = triage(b)
        if d is None:
            evidence = lookup_merged_room(b)
            if evidence:
                to_model.append((b, evidence))
                continue
            d = {"trang_thai": "chua_chac", "ly_do": no_evidence_reason(b)}
        decisions.append(dict(b, phong_cu=b["phong_tkb"], phong_moi="", can_cu=[], **d))

    if to_model:
        raw = decide_with_model(to_model)
        for b, evidence in to_model:
            decisions.append(dict(b, phong_cu=b["phong_tkb"], **guard(b, evidence, raw.get(b["ma_buoi"]))))
    note("dừng: %d buổi, %d qua model" % (len(decisions), len(to_model)))

    page = render_marked_timetable(req["ma"], req["ngay"], decisions)
    return {"output": summarize(req, decisions, save_page(req["ma"], req["ngay"], page))}


if __name__ == "__main__":
    import csv
    import sys

    import tracing

    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    def run(text, show=True):
        tracing.begin("cli")
        out = answer(text)["output"]
        s, _ = tracing.end()
        if show:
            print(">>> %s\n%s\n[trace] model=%d · tool=%d · token in/out=%d/%d\n" % (
                text, out, s["model_calls"], s["tool_calls"], s["tokens_in"], s["tokens_out"]))
        return out

    if len(sys.argv) > 1 and sys.argv[1] != "--selftest":
        run(" ".join(sys.argv[1:]))
        sys.exit(0)

    # ---- --selftest: thay model bằng stub (KHÔNG phải model thật), không tốn token.
    def _items(user):
        return json.loads(user.split("\n", 1)[1])

    def rule_stub(system, user):
        """Stub làm đúng luật trong SYSTEM — để kiểm phần không phải model (đọc TKB, tra căn cứ, chặn, hiển thị)."""
        out = []
        for it in _items(user):
            ok = [e for e in it["can_cu"] if e["do_chac"] == "xac_nhan"]
            targets = {e["phong_moi"] for e in ok}
            if len(targets) == 1 and targets <= set(MERGED_ROOMS):
                out.append({"ma_buoi": it["ma_buoi"], "trang_thai": "doi_phong", "phong_moi": targets.pop(),
                            "can_cu": sorted({e["code"] for e in ok}), "ly_do": "theo căn cứ đã xác nhận"})
            else:
                out.append({"ma_buoi": it["ma_buoi"], "trang_thai": "chua_chac", "phong_moi": "", "can_cu": [],
                            "ly_do": "căn cứ không rõ"})
        return {"text": json.dumps(out, ensure_ascii=False), "model": "selftest-stub", "tokens_in": 0, "tokens_out": 0}

    def bad_stub(system, user):
        """Stub cố tình sai — lớp chặn phải ép về 'chưa chắc'."""
        out = []
        for it in _items(user):
            codes = sorted({e["code"] for e in it["can_cu"]})
            wrong = "H210" if any(e["phong_moi"] == "H209" for e in it["can_cu"]) else "H209"
            out.append({"ma_buoi": it["ma_buoi"], "trang_thai": "doi_phong", "phong_moi": wrong,
                        "can_cu": codes[:1], "ly_do": "cố ý sai"})
        return {"text": json.dumps(out), "model": "selftest-stub", "tokens_in": 0, "tokens_out": 0}

    # 1) Cả bộ câu thử với stub đúng luật: kiểm trạng thái mong đợi + câu hỏi lại / từ chối không đưa mã phòng
    call_model = tracing.model_call(rule_stub)  # noqa: F811
    rows = list(csv.DictReader(open(os.path.join(ROOT, "eval", "benchmark.csv"), encoding="utf-8-sig")))
    room_re = re.compile(r"(?<![0-9A-Za-z])[A-Z]\d{3}(?!\d)")
    fails = []
    for r in rows:
        out = run(r["input"], show=False)
        want = re.search(r"trang_thai=(\w+)", r["expected"])
        if want:
            first = re.search(r"\((doi_phong|giu_nguyen|chua_chac)\)", out.split("\n", 2)[1] if out.count("\n") else "")
            lec = [l for l in out.splitlines() if "(LEC)" in l or "(ONL)" in l]
            got = re.search(r"\((doi_phong|giu_nguyen|chua_chac)\)", lec[0]).group(1) if lec else None
            if got != want.group(1):
                fails.append("%s: muốn %s, ra %s" % (r["id"], want.group(1), got or out[:60]))
            m = re.search(r"phong_moi=(H2\d\d)", r["expected"])
            if m and "→ %s" % m.group(1) not in out:
                fails.append("%s: thiếu phòng mới %s" % (r["id"], m.group(1)))
        elif r["type"] == "tu_choi" and not out.startswith("Ngoài phạm vi"):
            fails.append("%s: không từ chối — %s" % (r["id"], out[:60]))
        elif not want and room_re.search(out):
            fails.append("%s: câu hỏi lại / báo lỗi có mã phòng — %s" % (r["id"], out[:60]))
        print("%s %-7s %s" % (r["id"], r["type"], (out.splitlines()[1] if out.count("\n") else out)[:110]))
    if fails:
        print("\n".join(["[FAIL]"] + fails))
        sys.exit(1)
    print("[ok] %d câu thử: trạng thái / phòng mới đúng với expected; từ chối & hỏi lại không đưa mã phòng" % len(rows))

    # 2) Lớp chặn: model cố tình sai phòng → mọi buổi có căn cứ thành 'chưa chắc'
    call_model = tracing.model_call(bad_stub)  # noqa: F811
    out = run("Mình là 2A202603520, ngày 09/11 mình có buổi lý thuyết nào đổi phòng không?", show=False)
    assert "(doi_phong)" not in out and "bị chặn — model chọn 'H210' nhưng căn cứ ghi H209" in out, out
    out = run("Mình là 2A202604107, ngày 16/11 có buổi lý thuyết nào đổi phòng không?", show=False)
    assert "căn cứ mâu thuẫn: GOP-02 → H209, GOP-04 → H210" in out, out
    out = run("Mình là 2A202603682, ngày 17/11 có buổi lý thuyết nào đổi phòng không?", show=False)
    assert "GOP-05 chỉ là dự kiến" in out and "(doi_phong)" not in out, out
    print("[ok] lớp chặn: sai phòng · mâu thuẫn · dự kiến → chưa chắc dù model nói đổi phòng")
    print("Tất cả kiểm tra của agent.py đều qua. (Stub chỉ kiểm phần quanh model — model thật cần chạy run.py eval.)")
