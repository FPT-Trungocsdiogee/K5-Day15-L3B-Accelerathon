# Accelerathon — Đánh dấu buổi lý thuyết đổi phòng sang H209/H210

**Thành viên, lớp, track:** xem [TEAMS.md](TEAMS.md) — Lớp L3B · Track A (EdTech). **Điền TEAMS.md đúng format**: khi chấm và đánh giá, BTC quét file này để ghép điểm cho từng người.

*Lát cắt = phần nhỏ nhất làm xong được trong hackathon: một người dùng · một việc · một quyết định AI · một kết quả.*

---

## Nhóm làm gì, khung làm gì

| Nhóm quyết định và viết | Khung làm sẵn (không cần sửa) |
|---|---|
| Người dùng, pain, bằng chứng, impact (`evidence/`, `spec.md` §1–§2) | — |
| Hình dạng giải pháp, công cụ, prompt, luồng (`spec.md` §4, `codebase/agent.py`, `tools.py`, `ai.py`) | Ghi mọi lần gọi model / công cụ vào trace, cộng token (`codebase/tracing.py`) |
| Bộ câu thử, metric, chuẩn "đạt" (`eval/benchmark.csv`, `eval/metric_spec.yaml`, `spec.md` §7) | Kiểm đủ cột, đủ câu `kho` / `tu_choi`, đủ ≥1/3 câu từ người dùng / data thật (`run.py check`) |
| Chấm cột `pass` theo metric spec | Chạy cả bộ một lệnh, có run ID, model, token từng câu (`run.py eval`) · tính % đạt (`run.py score`) |
| Persona, số người dùng thật, giá model (`cost/personas.yaml`) | Sinh ~50 phiên, chạy thật qua bản chạy thử, tính chi phí / phiên, / task thành công, / tháng 3 kịch bản (`run.py simulate`) |

**Lát cắt của nhóm:** học viên L3A/L3B nhập mã học viên + một ngày học lý thuyết → trợ lý đối chiếu từng buổi lý thuyết đang ghi phòng lẻ H2xx với thông tin gộp lớp về H209/H210 → trả TKB ngày đó của chính học viên, đánh dấu buổi đổi phòng (phòng cũ gạch → phòng mới) kèm mã căn cứ, hoặc ghi "chưa chắc" để hỏi người vận hành lớp. Không sửa TKB gốc, không gửi thông báo cho ai.

## Chạy trong 3 phút

Bộ khung cần **Python 3.10 trở lên** (Python 3.9 có sẵn trên macOS vẫn chạy được, chỉ in một dòng nhắc). **Không cần `pip install`.**

**Bước 1 — Mở cửa sổ lệnh ngay trong thư mục repo**

| Windows (PowerShell) | macOS |
|---|---|
| Mở thư mục repo bằng File Explorer → bấm vào thanh địa chỉ → gõ `powershell` → Enter | Mở **Terminal** (Cmd + Space, gõ "Terminal") → gõ `cd ` (có dấu cách) → kéo thả thư mục repo vào → Enter |

Gõ `dir` (Windows) hoặc `ls` (macOS / Linux): thấy `run.py` và `README.md` là đang đứng đúng chỗ.

**Bước 2 — Kiểm Python và chạy thử**

| Việc | Windows (PowerShell) | macOS / Linux |
|---|---|---|
| Kiểm Python | `python --version` (không được thì `py --version`) | `python3 --version` |
| Chạy bản chạy thử (chế độ giả, chưa gọi model) | `python run.py` | `python3 run.py` |
| Kiểm bộ câu thử | `python run.py check` | `python3 run.py check` |
| Tạo file `.env` để nối model | `copy .env.example .env` | `cp .env.example .env` |

- Windows: gõ `python` mà mở Microsoft Store hoặc báo không có lệnh → dùng `py`. Chưa có Python: cài từ python.org, **tick "Add python.exe to PATH"**, mở lại PowerShell.
- macOS: báo `command not found: python` là bình thường → dùng `python3`.
- `python run.py` in ra "[câu trả lời giả — chưa nối model] …" là khung chạy đúng. Nối model thật: [docs/connect-model.md](docs/connect-model.md).

Trong README này lệnh viết là `python …`; máy nhóm cần `python3` hay `py` thì gõ thay.

## Lệnh

| Lệnh | Làm gì |
|---|---|
| `python run.py` | Chạy bản chạy thử (gõ đầu vào, nhận kết quả, kèm số lần gọi model / token) |
| `python run.py check` | Kiểm `eval/benchmark.csv` (6 cột, số câu, `kho` / `tu_choi`, mã `source`, ô trống, dòng mẫu) `eval/metric_spec.yaml` (≥3 metric điền đủ) và `TEAMS.md` (đúng format để BTC quét). Chỉ cảnh báo, không sửa file |
| `python run.py eval --try` | **Thử nối model:** chạy 3 câu đầu (`--try 5` = 5 câu) → `eval/run-try.csv`. Thấy "Nối model được" là xong. Không tính là một lượt |
| `python run.py eval` | Chạy cả bộ qua `codebase/agent.py` → `eval/run-1.csv` (lần sau `run-2.csv`…) + `traces/run-1.jsonl`. Mỗi dòng có run ID, model, số lần gọi model / công cụ, token. Model còn giả → chỉ ghi `run-mock.csv`; mọi câu lỗi → `run-error.csv`; Ctrl+C → `run-stopped.csv` — đều **không** được đánh số |
| `python run.py eval --fake` | Thử riêng bộ chạy, không gọi agent → `eval/run-fake.csv` |
| `python run.py score eval/run-1.csv` | Sau khi điền cột `pass` (1 / 0): in % đạt tổng và theo `type`. Còn ô trống → "CHƯA CHẤM XONG", không in % |
| `python run.py simulate --try` | Thử mô phỏng chi phí 10 phiên → `cost/simulate-try.csv` |
| `python run.py simulate` | Mô phỏng chi phí khi dùng thật theo `cost/personas.yaml` (≥50 phiên) → `cost/simulate-N.csv` + `cost/simulate-N-summary.md` |
| `python run.py simulate --rate-from eval/run-2.csv` | Như trên, lấy tỉ lệ đạt từ đúng lượt chỉ định. Không ghi thì khung lấy lượt `run-N` mới nhất đã chấm, cùng model, và ghi rõ đã lấy lượt nào trong bản tóm tắt |

Gói miễn phí báo hết lượt: thêm `--wait 4` sau `eval` hoặc `simulate` (nghỉ 4 giây giữa hai lượt gọi). Sửa CSV bằng Excel: *File → Save As → CSV UTF-8*; Google Sheets: *Tệp → Tải xuống → CSV*.

**Lượt có lỗi kỹ thuật** (cột `error` có chữ): không sửa tay file đó, chạy lại thành lượt mới và ghi vào bảng các lượt ở `eval/README.md`. Không xoá file lượt nào.

Nhóm dùng stack khác (Node, Streamlit, notebook…): sửa hàm `run_app()` trong `run.py` để `python run.py` vẫn chạy được bản chạy thử, và giữ `answer()` trong `codebase/agent.py` để `eval`, `simulate` chạy được.

## Bản chạy thử — viết ở đâu

| File | Viết gì | Bước guide |
|---|---|---|
| `codebase/agent.py` | `answer(text)` — luồng cố định: từ chối ngoài phạm vi → hỏi lại khi thiếu mã / ngày → tra căn cứ → model quyết định cho buổi có căn cứ → lớp `guard()` kiểm trước khi hiện | 3.2 |
| `codebase/tools.py` | Ba công cụ có `@tool`: `parse_timetable`, `lookup_merged_room`, `render_marked_timetable` | 2.2, 3.2 |
| `codebase/ai.py` | `call_model(system, user)` — chỗ duy nhất gọi model (Gemini REST, đọc token từ `usageMetadata`). Thiếu `.env` thì chạy **chế độ giả** | 3.3 |

- **Hiện trạng:** đã nối model thật (Gemini, đặt qua `MODEL_NAME` trong `.env`; `.env` không commit). Hai lượt eval đã chạy: xem bảng ở [eval/report.md](eval/report.md).
- Bộ chạy gửi **nguyên ô `input`** của câu thử vào `answer(text)`. Dữ liệu nền (TKB đã lưu, căn cứ gộp phòng) để trong `data/` và `eval/merged_room_fixture.csv`, đọc qua công cụ.

## Phần nào thật, phần nào giả

| Thành phần | Thật / Giả | Ghi chú |
|---|---|---|
| Lời gọi AI ở quyết định trung tâm | **Thật** | Model: `gemini-3.1-flash-lite` (lượt 1), `gemini-3.5-flash-lite` (lượt 2). Chỉ quyết định đổi / giữ / chưa chắc cho buổi có căn cứ; 18/32 câu thử không qua model |
| TKB học viên đọc | **Thật** (đã công bố) | Chuẩn hoá từ TKB BTC cấp, lưu trong `data/`. Chứa mã học viên thật, xem [data/DATA_CARD.md](data/DATA_CARD.md) |
| Căn cứ gộp phòng H209/H210 | **Giả — nhóm tự viết** | `eval/merged_room_fixture.csv` (GOP-01…GOP-05, nguồn `tu_viet`). Không phải thông báo chính thức của BTC; không dùng để đi học thật |
| Chấm cột `pass` | **Thật — chấm tay** | Theo `pass_criterion`, không dùng LLM chấm |
| Đọc / ghi hệ thống của trường | **Không có** | Không đọc TKB trực tiếp, không sửa TKB gốc, không gửi thông báo (thiết kế, xem `spec.md` §4) |

## Kết quả đến hiện tại

- Bộ câu thử: **32 câu** (14 thường · 11 kho · 7 từ chối); 23/32 lấy từ TKB thật, 9 câu dựa trên căn cứ nhóm tự viết.
- Lượt 1 (`gemini-3.1-flash-lite`, `run-1@20261128-081816`): **32/32 (100%)**.
- Lượt 2 (`gemini-3.5-flash-lite`, `run-2@20261128-120915`): **32/32 (100%)**. Đổi model, không đổi code và bộ câu nên chưa chứng minh model mới tốt hơn.
- Chi tiết, lỗi và điểm rủi ro: [eval/report.md](eval/report.md) · [eval/README.md](eval/README.md). Chi phí khi dùng thật: [cost/cost-estimate.md](cost/cost-estimate.md) — **chưa kết luận đáng làm** vì chưa có số impact / người / tháng đủ nguồn.

## Dùng AI vào việc gì

Bản chạy thử gọi Gemini để quyết định đổi / giữ / chưa chắc cho các buổi có căn cứ; code kiểm mã căn cứ và phòng mới trước khi hiện. Trong quá trình làm, coding agent (Claude Code, theo [AGENTS.md](AGENTS.md)) hỗ trợ viết `codebase/ai.py`, và AI soạn nháp một số mục spec — người phụ trách mục đó đọc lại và sửa. Chi tiết: [docs/ai-usage.md](docs/ai-usage.md).

## File mẫu — điền ở bước nào

| File | Điền ở bước guide | Mốc |
|---|---|---|
| `TEAMS.md` | 1.0 | CP1 · **đúng format**, BTC quét khi chấm |
| `canvas.md` | 1.4 | CP1, cập nhật CP2 |
| `evidence/hypothesis.md` | 1.1 | trước khi tìm bằng chứng |
| `evidence/data-mining.md` · `evidence/interviews/TEMPLATE.md` → `P1.md`… · `evidence/survey/TEMPLATE.md` | 1.2 | bắt đầu sau Zoom, xong CP3 |
| `evidence/summary.md` | 1.2 | CP3 |
| `spec.md` | §0–§2: 1.1–1.3 · §3–§5: 2.1–2.3 · §7: 2.4 · §8: 4.2 · §10: suốt | §7 chốt CP2 · §0–§7 CP3 · đủ CP4 |
| `data/DATA_CARD.md` | 2.4 | bản đầu CP2 |
| `eval/benchmark.csv` · `eval/metric_spec.yaml` | 2.4 | ≥10 câu + metric chốt CP2 · 20–30 câu CP3 |
| `codebase/` | 3.2, 3.3 | khung CP2 · AI thật CP3 |
| `eval/report.md` · `eval/README.md` | 4.1 (README mục 1–4 từ 2.4) | CP4 |
| `cost/personas.yaml` · `cost/cost-estimate.md` | 4.2 | thử 10 phiên CP3 · đủ CP4 |
| `validation/log.md` *(bonus)* | 4.3 | CP4 |
| `slides/outline.md` → `demo-slides.pdf` | 5.1 | CP4 |
| `reflection/TEMPLATE.md` → `reflection/<ten>.md` | 5.3 | 23:59 Thứ Bảy 28/11 |
| `AGENTS.md` · `docs/ai-usage.md` | khi dùng coding agent / AI | suốt |

## Bảy hạng mục bắt buộc — nằm ở file nào

| # | Hạng mục | File |
|---|---|---|
| 1 | Bằng chứng pain | `evidence/` (tổng hợp ở `evidence/summary.md`) |
| 2 | Impact có số | `spec.md` §2 |
| 3 | Thiết kế giải pháp | `spec.md` §4 |
| 4 | Bản chạy thử làm trọn lát cắt | `codebase/` · lệnh ở mục "Lệnh" |
| 5 | Định nghĩa "tốt" + bộ câu thử | `data/DATA_CARD.md` · `eval/` |
| 6 | Mô phỏng chi phí khi dùng thật | `cost/` |
| 7 | Slide + demo + video dự phòng | Slide: `Accelerathon - demo_slides.pdf` ở thư mục gốc · link video(CLI Demo): https://drive.google.com/file/d/1yy8aq3rMnwCeSQ9bEu2bBADNxzQbHaU4/view?usp=sharing · Web demo: https://accelerathon-aithucchien.ai.studio|
