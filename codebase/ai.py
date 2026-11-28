"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0. Lượt `run.py eval` / `simulate` chạy bằng model giả KHÔNG được tính.

Nhà cung cấp hỗ trợ (MODEL_PROVIDER trong .env) — theo docs/connect-model.md:
    gemini     Google Gemini API (REST generateContent)          — nhóm dùng (khớp bảng giá cost/personas.yaml)
    openai     OpenAI Chat Completions (hoặc API kiểu OpenAI: đặt MODEL_BASE_URL)
    anthropic  Claude Messages API
    ollama     model chạy trên máy (không cần key)
Chỉ dùng thư viện chuẩn (urllib). Không dán API key vào file này.
"""
import json
import os
import time
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
MODEL_BASE_URL = (os.environ.get("MODEL_BASE_URL") or "").strip()   # tuỳ chọn: API kiểu OpenAI (DeepSeek, Groq…)

SHOW_RAW = False     # đổi thành True để in nguyên phản hồi của API khi cần tìm tên trường
MAX_TOKENS = 2048    # đủ cho mảng JSON quyết định của cả một ngày học (agent.py gọi 1 lần / ngày)
RETRIES = 2          # thử lại khi 429 / 5xx (hết lượt tạm thời); hết số lần thì để lỗi bay ra


def post_json(url, headers, body, timeout=60):
    """Gửi POST JSON, trả về JSON phản hồi. Chỉ dùng thư viện chuẩn (urllib)."""
    payload = json.dumps(body).encode("utf-8")
    for attempt in range(RETRIES + 1):
        req = urllib.request.Request(
            url, data=payload, method="POST",
            headers=dict({"Content-Type": "application/json"}, **headers))
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:300]
            if (e.code == 429 or e.code >= 500) and attempt < RETRIES:
                time.sleep(4 * (attempt + 1))
                continue
            raise RuntimeError("HTTP %d: %s" % (e.code, msg))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":              # nhánh fake của khung — giữ nguyên
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}
    if not MODEL_NAME:
        raise RuntimeError("Thiếu MODEL_NAME trong .env (mã gọi API của model) — xem docs/connect-model.md")
    if MODEL_PROVIDER != "ollama" and not API_KEY:
        raise RuntimeError("Thiếu API_KEY trong .env cho MODEL_PROVIDER=%s" % MODEL_PROVIDER)

    if MODEL_PROVIDER == "gemini":
        r = call_gemini(system, user)
    elif MODEL_PROVIDER == "openai":
        r = call_openai(system, user)
    elif MODEL_PROVIDER in ("anthropic", "claude"):
        r = call_claude(system, user)
    elif MODEL_PROVIDER == "ollama":
        r = call_ollama(system, user)
    else:
        raise RuntimeError("MODEL_PROVIDER=%s chưa hỗ trợ — dùng gemini / openai / anthropic / ollama" % MODEL_PROVIDER)
    return {"text": r["text"], "model": MODEL_NAME,
            "tokens_in": int(r["tokens_in"] or 0), "tokens_out": int(r["tokens_out"] or 0)}


# ---------------------------------------------------------------- Gemini (nhà cung cấp khác — mục 2.4)
URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent"


def call_gemini(system, user):
    """Gọi đúng MỘT lần Gemini. Trả về {"text", "tokens_in", "tokens_out"}."""
    body = {"contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"maxOutputTokens": MAX_TOKENS, "temperature": 0}}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    data = post_json(URL_GEMINI % MODEL_NAME, {"x-goog-api-key": API_KEY}, body)
    cands = data.get("candidates") or []
    if not cands:  # bị chặn bởi bộ lọc an toàn hoặc lỗi khác — báo rõ thay vì KeyError
        raise RuntimeError("Gemini không trả candidates: %s" % json.dumps(data.get("promptFeedback", data))[:300])
    parts = (cands[0].get("content") or {}).get("parts") or []
    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    u = data.get("usageMetadata") or {}
    # Token suy nghĩ (thoughtsTokenCount) tính tiền như token ra nhưng KHÔNG nằm trong candidatesTokenCount → cộng vào.
    return {"text": text, "tokens_in": u.get("promptTokenCount", 0),
            "tokens_out": u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0)}


# ---------------------------------------------------------------- OpenAI (mục 2.1)
URL_OPENAI = (MODEL_BASE_URL.rstrip("/") + "/chat/completions") if MODEL_BASE_URL \
    else "https://api.openai.com/v1/chat/completions"


def call_openai(system, user):
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(URL_OPENAI, {"Authorization": "Bearer " + API_KEY},
                     {"model": MODEL_NAME, "messages": messages})
    u = data["usage"]   # completion_tokens đã gồm reasoning tokens
    return {"text": data["choices"][0]["message"]["content"] or "",
            "tokens_in": u["prompt_tokens"], "tokens_out": u["completion_tokens"]}


# ---------------------------------------------------------------- Claude (mục 2.2)
URL_CLAUDE = "https://api.anthropic.com/v1/messages"


def call_claude(system, user):
    data = post_json(URL_CLAUDE,
                     {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
                     {"model": MODEL_NAME, "max_tokens": MAX_TOKENS, "system": system or "",
                      "messages": [{"role": "user", "content": user}]})
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    u = data["usage"]
    return {"text": text, "tokens_in": u["input_tokens"], "tokens_out": u["output_tokens"]}


# ---------------------------------------------------------------- Ollama (mục 2.3)
URL_OLLAMA = "http://localhost:11434/api/chat"


def call_ollama(system, user):
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(URL_OLLAMA, {}, {"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=300)
    return {"text": data["message"]["content"],
            "tokens_in": data.get("prompt_eval_count", 0), "tokens_out": data.get("eval_count", 0)}


if __name__ == "__main__":
    # Thử nhanh: python codebase/ai.py  → gọi 1 câu, in câu trả lời + token.
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    out = call_model("Trả lời ngắn gọn bằng tiếng Việt.", "Phòng H209 và H210 dùng để làm gì trong khoá AI20K? (trả lời 1 câu)")
    print("provider=%s · model=%s · token vào %d / ra %d\n%s"
          % (MODEL_PROVIDER, out["model"], out["tokens_in"], out["tokens_out"], out["text"]))
